## Style Transfer Base Model

This notebook sets up the **base infrastructure** for our style transfer project.

As part of the Model Training's responsibility, this base model serves as the foundational starting point for further experimentation and development. It includes:

-  A minimal working version of the style transfer pipeline  
-  Pretrained VGG19 feature extraction (content and style layers)  
-  Gram matrix computation and style/content loss setup   
-  Only a few training steps are performed

###  [1.1.0] – 2025‑04‑16

#### Added
- Image upload endpoint, allowing users to submit their own content and style images.
- Support for 10 predefined style options; each run randomly selects one style for transfer.
- Inference timing: logs and prints the actual execution time taken by the TensorFlow Hub style‑transfer model.




<!--
 **Colab Notebook**  
Click below to open and run the notebook directly in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/M0n4GPT/Vision-to-Vintage-AIs-Take-on-Classical-Art/blob/main/ModelTraining/base_model/style_transfer_base_model.ipynb)
-->
