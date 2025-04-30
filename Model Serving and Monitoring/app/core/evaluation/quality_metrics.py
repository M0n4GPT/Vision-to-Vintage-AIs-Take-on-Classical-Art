import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import tensorflow as tf
import logging

logger = logging.getLogger(__name__)

class QualityMetrics:
    @staticmethod
    def calculate_psnr(original: np.ndarray, transformed: np.ndarray) -> float:
        """Calculate Peak Signal-to-Noise Ratio (PSNR)"""
        return psnr(original, transformed)
    
    @staticmethod
    def calculate_ssim(original: np.ndarray, transformed: np.ndarray) -> float:
        """Calculate Structural Similarity Index (SSIM)"""
        return ssim(original, transformed, multichannel=True)
    
    @staticmethod
    def calculate_style_loss(original: np.ndarray, transformed: np.ndarray) -> float:
        """Calculate style loss using Gram matrix"""
        def gram_matrix(x):
            x = tf.transpose(x, (2, 0, 1))
            features = tf.reshape(x, (tf.shape(x)[0], -1))
            gram = tf.matmul(features, tf.transpose(features))
            return gram
            
        original_gram = gram_matrix(original)
        transformed_gram = gram_matrix(transformed)
        return tf.reduce_mean(tf.square(original_gram - transformed_gram))
    
    @staticmethod
    def calculate_content_loss(original: np.ndarray, transformed: np.ndarray) -> float:
        """Calculate content loss using mean squared error"""
        return tf.reduce_mean(tf.square(original - transformed))
    
    @staticmethod
    def evaluate_quality(original: np.ndarray, transformed: np.ndarray) -> dict:
        """Evaluate all quality metrics"""
        try:
            metrics = {
                "psnr": QualityMetrics.calculate_psnr(original, transformed),
                "ssim": QualityMetrics.calculate_ssim(original, transformed),
                "style_loss": QualityMetrics.calculate_style_loss(original, transformed).numpy(),
                "content_loss": QualityMetrics.calculate_content_loss(original, transformed).numpy()
            }
            logger.info(f"Quality metrics calculated: {metrics}")
            return metrics
        except Exception as e:
            logger.error(f"Error calculating quality metrics: {str(e)}")
            raise 