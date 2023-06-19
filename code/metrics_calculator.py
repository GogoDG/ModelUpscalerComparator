import cv2
import numpy as np
from skimage.color import rgba2rgb, gray2rgb
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def preprocess_image(image):
    # Convert RGBA image to RGB or grayscale
    if image.shape[2] == 4:
        image = rgba2rgb(image)
    elif len(image.shape) == 2:
        image = gray2rgb(image)

    return image


def calculate_metrics(image1, image2):
    # Preprocess images
    image1 = preprocess_image(image1)
    image2 = preprocess_image(image2)

    # Resize images to a common size if needed
    if image1.shape != image2.shape:
        image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]), interpolation=cv2.INTER_AREA)

    # Convert background to grayscale
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute the image metrics
    ssim_score, _ = structural_similarity(image1_gray, image2_gray, full=True)
    mse = np.mean((image1_gray - image2_gray) ** 2)
    psnr = peak_signal_noise_ratio(image1_gray, image2_gray)

    return ssim_score, mse, psnr