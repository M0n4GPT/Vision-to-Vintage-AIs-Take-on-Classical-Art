import os
import time
import argparse
import csv
from pathlib import Path # Added for cleaner path manipulation

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler
from torchvision import transforms, models
from PIL import Image
import glob
import random

try:
    from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
    from torch.distributed.fsdp import CPUOffload, ShardingStrategy
except ImportError:
    FSDP = None

# ---------- Dataset ----------
class StyleTransferDataset(Dataset):
    def __init__(self, content_dir, style_root, transform):
        # content images
        self.content_paths = glob.glob(os.path.join(content_dir, '*'))
        # style images per class subfolder (0, 1, 2...)
        self.style_paths = []  # list of (path, label)
        if os.path.exists(style_root):
            style_label_dirs = sorted(os.listdir(style_root))
            for label_str in style_label_dirs:
                cls_dir = os.path.join(style_root, label_str)
                if os.path.isdir(cls_dir):
                    try:
                        label = int(label_str)
                        paths = glob.glob(os.path.join(cls_dir, '*'))
                        for p in paths:
                            self.style_paths.append((p, label))
                    except ValueError:
                        print(f"Warning: Style directory '{label_str}' is not a valid integer label. Skipping.")
        if not self.style_paths:
            print(f"Warning: No valid style images found in {style_root} with integer subdirectories.")
        self.transform = transform

    def __len__(self):
        return len(self.content_paths)

    def __getitem__(self, idx):
        c_img = Image.open(self.content_paths[idx]).convert('RGB')
        # randomly choose style sample if available, otherwise use a placeholder (though training would likely fail)
        if not self.style_paths:
            # This is a fallback, ideally training should not proceed without styles.
            # Create a dummy black image for style and a dummy label 0.
            s_img = Image.new('RGB', (256, 256), color = 'black') 
            label = 0 
        else:
            s_path, label = random.choice(self.style_paths)
            s_img = Image.open(s_path).convert('RGB')
        return self.transform(c_img), self.transform(s_img), label

# ---------- AdaIN ----------
def adain(content_feat, style_feat, eps: float = 1e-5):
    c_mean = content_feat.mean(dim=[2,3], keepdim=True)
    c_std = content_feat.std(dim=[2,3], keepdim=True)
    s_mean = style_feat.mean(dim=[2,3], keepdim=True)
    s_std = style_feat.std(dim=[2,3], keepdim=True)
    norm = (content_feat - c_mean) / (c_std + eps)
    return norm * s_std + s_mean

# ---------- Model ----------
class StyleTransferModel(nn.Module):
    def __init__(self):
        super().__init__()
        vgg = models.vgg19(pretrained=True).features
        self.enc = nn.Sequential(*list(vgg.children())) # This goes up to conv5_4, outputting ~H/32 x W/32 features
        # For a 256x256 input, enc output is 512x8x8
        for p in self.enc.parameters(): p.requires_grad = False
        
        # Decoder should take 512x8x8 and output 3x256x256
        self.dec = nn.Sequential(
            nn.Conv2d(512, 256, 3, padding=1), nn.ReLU(True),
            nn.Upsample(scale_factor=2, mode='nearest'), # 8x8 -> 16x16 (256 channels)
            nn.Conv2d(256, 256, 3, padding=1), nn.ReLU(True), # Added conv layer
            
            nn.Conv2d(256, 128, 3, padding=1), nn.ReLU(True),
            nn.Upsample(scale_factor=2, mode='nearest'), # 16x16 -> 32x32 (128 channels)
            nn.Conv2d(128, 128, 3, padding=1), nn.ReLU(True), # Added conv layer
            
            nn.Conv2d(128, 64, 3, padding=1), nn.ReLU(True),
            nn.Upsample(scale_factor=2, mode='nearest'), # 32x32 -> 64x64 (64 channels)
            nn.Conv2d(64, 64, 3, padding=1), nn.ReLU(True), # Added conv layer
            
            # New Upsampling Stage 1
            nn.Upsample(scale_factor=2, mode='nearest'), # 64x64 -> 128x128 (64 channels)
            nn.Conv2d(64, 32, 3, padding=1), nn.ReLU(True),

            # New Upsampling Stage 2
            nn.Upsample(scale_factor=2, mode='nearest'), # 128x128 -> 256x256 (32 channels)
            nn.Conv2d(32, 3, 3, padding=1), # Output 3 channels for RGB
            nn.Sigmoid() # Output values between 0 and 1
        )

    def forward(self, content, style):
        c_feat = self.enc(content)
        s_feat = self.enc(style)
        t = adain(c_feat, s_feat)
        out = self.dec(t)
        return out, t, s_feat

# ---------- Inference Wrapper ----------
class Stylizer(nn.Module):
    def __init__(self, style_transfer_base_model, style_dir, transform, device):
        super().__init__()
        self.model = style_transfer_base_model # This is the StyleTransferModel instance
        self.style_dir = style_dir
        self.transform = transform
        self.device = device
        self.style_feats = {}
        self.style_labels_to_ids = {}
        self.style_ids_to_labels = {}
        self._load_styles()

    def _load_styles(self):
        # print(f"Stylizer attempting to load styles from: {self.style_dir}")
        idx_counter = 0
        for artist_name in os.listdir(self.style_dir):
            artist_path = os.path.join(self.style_dir, artist_name)
            if os.path.isdir(artist_path):
                for style_image_name in os.listdir(artist_path):
                    if style_image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        style_id = os.path.splitext(style_image_name)[0].lower().replace(' ', '_')
                        # print(f"  Loading style: ID='{style_id}', Artist='{artist_name}', File='{style_image_name}'")
                        try:
                            image_path = os.path.join(artist_path, style_image_name)
                            style_img = self.transform(Image.open(image_path).convert('RGB')).unsqueeze(0).to(self.device)
                            with torch.no_grad():
                                style_feat = self.model.enc(style_img)
                            self.style_feats[style_id] = style_feat
                            self.style_labels_to_ids[idx_counter] = style_id
                            self.style_ids_to_labels[style_id] = idx_counter
                            idx_counter += 1
                        except Exception as e:
                            # print(f"    Error loading style image {image_path}: {e}")
                            pass # Continue if one style image fails
        # print(f"Stylizer loaded {len(self.style_feats)} style features.")

    def adain(self, content_feat, style_feat):
        # print(f"AdaIN: content_feat shape: {content_feat.shape}, style_feat shape: {style_feat.shape}")
        assert content_feat.size()[:2] == style_feat.size()[:2]
        b, c = content_feat.size()[:2]
        # Reshape style_feat to handle cases where it might be [1, C, H_style, W_style] for multiple content images
        style_m = style_feat.view(b, c, -1).mean(dim=2).view(b,c,1,1)
        style_s = style_feat.view(b, c, -1).std(dim=2).view(b,c,1,1) + 1e-5 # Add epsilon for numerical stability
        content_m = content_feat.view(b,c,-1).mean(dim=2).view(b,c,1,1)
        content_s = content_feat.view(b,c,-1).std(dim=2).view(b,c,1,1) + 1e-5 # Add epsilon

        # print(f"AdaIN: style_m shape: {style_m.shape}, style_s shape: {style_s.shape}")
        # print(f"AdaIN: content_m shape: {content_m.shape}, content_s shape: {content_s.shape}")

        normalized_feat = (content_feat - content_m) / content_s
        return normalized_feat * style_s + style_m

    def forward(self, content, style_label: torch.Tensor): # style_label is a 1D tensor e.g. tensor([0])
        # content: tensor Bx3xHxW
        content_feat = self.model.enc(content) # [B, C_feat, H_feat, W_feat]
        # print(f"Stylizer.forward: content_feat min: {content_feat.min().item():.4f}, max: {content_feat.max().item():.4f}, mean: {content_feat.mean().item():.4f}, shape: {content_feat.shape}")

        batch_size = content.size(0)

        # This check causes JIT error if self.style_feats is empty, even if not taken.
        # JIT tries to compile all branches.
        # if not self.style_feats: 
        #      raise RuntimeError("Stylizer has no style features loaded. Cannot perform inference.")

        if style_label.numel() != batch_size:
            # This error message with f-string might also be problematic for JIT
            # Consider a simpler error or ensuring this condition is never met during scripting
            raise ValueError("style_label must have batch_size elements")
            # raise ValueError(f"style_label must have {batch_size} elements, one for each content image. Got {style_label.numel()}")

        style_batch_feats_list = []
        for i in range(batch_size): # JIT unrolls loops, this is usually fine
            label_val = style_label[i].item() # .item() can be problematic for JIT scripting.
                                            # It's better if style_label is already an int or if this logic
                                            # can be expressed without .item() for scripting, if possible.
                                            # However, for now, let's see if removing prints is enough.
            style_id = self.style_labels_to_ids.get(label_val)
            
            # These f-strings in error messages are also risky for JIT
            if style_id is None:
                raise ValueError("Invalid style label provided.")
                # raise ValueError(f"Invalid style label {label_val} provided for item {i} in batch. Available labels map to IDs: {self.style_labels_to_ids}")
            
            selected_style_feat = self.style_feats.get(style_id)
            if selected_style_feat is None: # Should not happen if _load_styles and get worked
                raise RuntimeError("Internal error: Style ID not found in loaded style_feats.")
                # raise RuntimeError(f"Internal error: Style ID '{style_id}' (from label {label_val}) not found in loaded style_feats.")
            style_batch_feats_list.append(selected_style_feat)
        
        # Stack the selected style features to match the batch size of content_feat
        # Each style_feat is [1, C, H_style, W_style], so cat them along dim 0
        style_batch_feat = torch.cat(style_batch_feats_list, dim=0)
        # print(f"Stylizer.forward: style_batch_feat min: {style_batch_feat.min().item():.4f}, max: {style_batch_feat.max().item():.4f}, mean: {style_batch_feat.mean().item():.4f}, shape: {style_batch_feat.shape}")

        transformed_feat = self.adain(content_feat, style_batch_feat)
        # print(f"Stylizer.forward: transformed_feat (after AdaIN) min: {transformed_feat.min().item():.4f}, max: {transformed_feat.max().item():.4f}, mean: {transformed_feat.mean().item():.4f}, shape: {transformed_feat.shape}")
        
        output_image = self.model.dec(transformed_feat)
        # print(f"Stylizer.forward: output_image (decoder output) min: {output_image.min().item():.4f}, max: {output_image.max().item():.4f}, mean: {output_image.mean().item():.4f}, shape: {output_image.shape}")
        
        return torch.clamp(output_image, 0., 1.)

# ---------- Training & Export ----------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', required=True, help="Root for training data (content/ and style/ subdirs with 0,1.. sub-subdirs for style)")
    parser.add_argument('--style_dir_for_stylizer', required=True, help="Directory for Stylizer style images (e.g., data/styles/Artist/Painting.jpg)")
    parser.add_argument('--global_batch_size', type=int, default=4) # Reduced for faster local testing if needed
    parser.add_argument('--micro_batch_size', type=int, default=2)  # Reduced
    parser.add_argument('--epochs', type=int, default=1) # Reduced for faster local testing
    parser.add_argument('--precision', choices=['fp32','amp'], default='fp32')
    parser.add_argument('--strategy', choices=['none','ddp','fsdp'], default='none')
    parser.add_argument('--style_w', type=float, default=10.0)
    parser.add_argument('--tv_w', type=float, default=1e-6)
    parser.add_argument('--lr', type=float, default=1e-4)
    parser.add_argument('--export_path', type=str, required=True)
    args = parser.parse_args()

    # --- This part is for the actual training loop, which we might not run every time for serving --- 
    # --- We primarily care about the Stylizer export using the new style loading logic --- 
    run_training_loop = True # Set to True if you want to actually retrain the StyleTransferModel's decoder

    distributed = args.strategy in ['ddp','fsdp']
    if distributed:
        # Basic setup, for full DDP/FSDP, more robust env var checks are needed
        if 'LOCAL_RANK' in os.environ:
            torch.cuda.set_device(int(os.environ['LOCAL_RANK']))
        torch.distributed.init_process_group('nccl')
        rank = torch.distributed.get_rank()
        world = torch.distributed.get_world_size()
    else:
        rank, world = 0, 1
    
    # This transform is for Stylizer's internal style feature generation AND for training data loading
    transform = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(256), transforms.ToTensor()])
    
    # Moved device and style_transfer_base_model instantiation outside the run_training_loop block
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device} for model operations.")
    style_transfer_base_model = StyleTransferModel().to(device)

    if run_training_loop:
        if not os.path.exists(os.path.join(args.data_root, 'content')) or \
           not os.path.exists(os.path.join(args.data_root, 'style')):
            print(f"Error: For training loop, --data_root ('{args.data_root}') must contain 'content' and 'style' subdirectories.")
            print("The 'style' subdirectory should contain further subdirectories named '0', '1', '2', etc., each with style images.")
            print("Skipping training loop as data structure is not met.")
            run_training_loop = False # Force skip if data not present
        else:
            assert args.global_batch_size % (args.micro_batch_size*world)==0
            accum = args.global_batch_size // (args.micro_batch_size*world)

            ds = StyleTransferDataset(os.path.join(args.data_root,'content'), os.path.join(args.data_root,'style'), transform)
            if not ds.style_paths and rank == 0: # Check if dataset actually found styles for training
                print("Critical Error: StyleTransferDataset found no style images for training. Aborting training loop.")
                run_training_loop = False 
            else:
                sampler = DistributedSampler(ds, rank=rank, num_replicas=world, shuffle=True) if distributed else None
                loader = DataLoader(ds, batch_size=args.micro_batch_size, sampler=sampler, shuffle=not distributed and sampler is None, num_workers=4, pin_memory=True)
                opt = optim.Adam(style_transfer_base_model.dec.parameters(), lr=args.lr)
                scaler = torch.cuda.amp.GradScaler() if args.precision=='amp' else None

                if args.strategy=='ddp': style_transfer_base_model = nn.parallel.DistributedDataParallel(style_transfer_base_model, device_ids=[torch.cuda.current_device()])
                if args.strategy=='fsdp': style_transfer_base_model = FSDP(style_transfer_base_model, cpu_offload=CPUOffload(False), sharding_strategy=ShardingStrategy.FULL_SHARD)

                log = []
                print("Starting training loop...")
                for e in range(args.epochs):
                    if sampler: sampler.set_epoch(e)
                    start_t_epoch=time.time()
                    opt.zero_grad()
                    for i,(c,s,_) in enumerate(loader):
                        c,s=c.to(device),s.to(device)
                        with torch.cuda.amp.autocast(args.precision=='amp'):
                            out,t,sf=style_transfer_base_model(c,s)
                            of=style_transfer_base_model.enc(out)
                        l_c=F.mse_loss(of,t)
                        l_s=F.mse_loss(of.mean([2,3]), sf.mean([2,3]))+F.mse_loss(of.std([2,3]), sf.std([2,3]))
                        l_tv = torch.sum(torch.abs(out[:,:,1:]-out[:,:,:-1]))+torch.sum(torch.abs(out[:,:,:,1:]-out[:,:,:,:-1]))
                        loss=(l_c+args.style_w*l_s+args.tv_w*l_tv)/accum
                        if scaler: scaler.scale(loss).backward()
                        else: loss.backward()
                        if (i+1)%accum==0:
                            if scaler: scaler.step(opt); scaler.update()
                            else: opt.step()
                            opt.zero_grad()
                        # Log details (moved outside inner if for clarity, happens after opt step or zero_grad)
                        if (i+1)%accum==0 or (i+1) == len(loader):
                            t_e_epoch=time.time()-start_t_epoch
                            max_mem_gb = torch.cuda.max_memory_allocated(device=device)/1e9 if torch.cuda.is_available() else 0
                            if rank==0: 
                                log_entry = (args.strategy,world,e,i+1,len(loader),t_e_epoch,max_mem_gb,loss.item())
                                log.append(log_entry)
                                print(f"Epoch{e} [{i+1}/{len(loader)}] {t_e_epoch:.1f}s mem{max_mem_gb:.2f}GB Loss {loss.item():.4f}")
                print("Training loop finished.")
    else:
        if rank == 0:
            print("Skipping training loop as run_training_loop is False.")

    # Export stylizer - this is the primary goal for fixing the serving model
    if rank==0:
        # Ensure the base model passed to Stylizer is the unwrapped model if DDP/FSDP was used
        unwrapped_model = style_transfer_base_model.module if hasattr(style_transfer_base_model, 'module') else style_transfer_base_model
        
        print(f"Initializing Stylizer with style directory: {args.style_dir_for_stylizer}")
        stylizer = Stylizer(unwrapped_model, args.style_dir_for_stylizer, transform, device)
        
        if not stylizer.style_feats: # Check if stylizer loaded any styles
            print("Critical Error: Stylizer failed to load style features. Cannot export model OR run direct test.")
        else:
            # --- BEGIN DIRECT STYLIZER TEST ---
            print("\n--- Starting Direct Stylizer Test ---")
            content_image_path = "data/examples/test_content_image.jpg" # Assuming user places it here
            output_save_path = "direct_stylizer_output.png" # Will save in the script's directory

            try:
                print(f"Loading content image from: {content_image_path}")
                if not os.path.exists(content_image_path):
                    print(f"ERROR: Content image not found at {content_image_path}. Please place it there.")
                else:
                    content_pil_image = Image.open(content_image_path).convert('RGB')
                    content_tensor = transform(content_pil_image).unsqueeze(0).to(device)
                    print("Content image loaded and transformed.")

                    # Try a specific style_id, e.g., "le_reve", or fallback to the first loaded style
                    style_to_test_id = "le_reve" # Change if "le_reve" is not a valid style from your STYLES_DIR
                    if style_to_test_id in stylizer.style_ids_to_labels:
                        chosen_style_label_int = stylizer.style_ids_to_labels[style_to_test_id]
                        print(f"Testing with style ID: '{style_to_test_id}' (Label: {chosen_style_label_int})")
                    elif stylizer.style_labels_to_ids: # Fallback to the first style if "le_reve" not found
                        chosen_style_label_int = 0
                        chosen_style_id = stylizer.style_labels_to_ids.get(0, "Unknown_Style_0")
                        print(f"WARNING: Style ID '{style_to_test_id}' not found. Falling back to first loaded style: '{chosen_style_id}' (Label: 0)")
                    else:
                        print("ERROR: No styles available in Stylizer to test with.")
                        chosen_style_label_int = -1

                    if chosen_style_label_int != -1:
                        style_label_tensor = torch.tensor([chosen_style_label_int], device=device, dtype=torch.long)

                        print("Performing stylizer.forward()...")
                        with torch.no_grad():
                            output_tensor = stylizer(content_tensor, style_label_tensor)
                        print("Stylizer forward pass completed.")

                        # Post-process
                        print("Post-processing output tensor...")
                        output_tensor_squeezed = output_tensor.squeeze(0).cpu().clamp(0, 1)
                        output_pil_image = transforms.ToPILImage()(output_tensor_squeezed)
                        print("Output tensor post-processed to PIL Image.")

                        output_pil_image.save(output_save_path)
                        print(f"--- Direct stylizer test output saved to: {os.path.abspath(output_save_path)} ---")
                        print("--- Please check this image to see if the style transfer worked correctly. ---")

            except Exception as e_test:
                print(f"ERROR during direct Stylizer test: {e_test}")
                import traceback
                traceback.print_exc()
            
            print("--- End Direct Stylizer Test ---\n")
            
            # --- Original JIT Scripting and Saving ---
            # Now, proceed to JIT script and save the stylizer if the direct test was satisfactory
            # (or if run_training_loop was True and direct test was skipped)
            
            # Ensure the stylizer is on the correct device before scripting, especially if loaded from a state_dict
            stylizer.to(device) 
            stylizer.eval() # Ensure it's in eval mode

            print(f"JIT scripting and saving Stylizer to: {args.export_path}")
            try:
                scripted_stylizer = torch.jit.script(stylizer)
                scripted_stylizer.save(args.export_path)
                print(f"Stylizer successfully JIT scripted and saved to {args.export_path}")
            except Exception as e:
                print(f"Error during JIT scripting or saving: {e}")
                print("Proceeding without saving the JIT model due to the error above.")

    else: # rank != 0
        print("Skipping JIT scripting and saving as rank != 0.")

if __name__=='__main__':
    main()
