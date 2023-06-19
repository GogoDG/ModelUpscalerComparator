import cv2
import numpy as np
from cv2 import dnn_superres

MODEL_PATHS = {
    ("edsr", 2): './models/EDSR_x2.pb',
    ("edsr", 4): './models/EDSR_x4.pb',
    ("espcn", 2): './models/ESPCN_x2.pb',
    ("espcn", 4): './models/ESPCN_x4.pb',
    ("fsrcnn", 2): './models/FSRCNN_x2.pb',
    ("fsrcnn", 4): './models/FSRCNN_x4.pb',
    ("lapsrn", 2): './models/LapSRN_x2.pb',
    ("lapsrn", 4): './models/LapSRN_x4.pb',
    ("lapsrn", 8): './models/LapSRN_x8.pb'
}


def upscale_image_rgb(image_path, model_path, model, scale):
    # Create an SR object
    sr = dnn_superres.DnnSuperResImpl_create()

    # Read image
    image = cv2.imread(image_path)

    rgb_image = image[:, :, :3]

    # Read the desired model
    sr.readModel(model_path)

    # Set the desired model and scale
    sr.setModel(model, scale)

    # Upscale the RGB channels
    result = sr.upsample(rgb_image)

    return result


def upscale_image_with_transparency(image_path, model_path, model, scale):
    # Read image with alpha channel support
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Separate the image into RGB channels and alpha channel
    alpha_channel = image[:, :, 3]

    # Upscale the RGB channels with upscale_image_rgb function
    upscaled_rgb = upscale_image_rgb(image_path, model_path, model, scale)

    # Upscale the alpha channel
    upscaled_alpha = cv2.resize(alpha_channel, (upscaled_rgb.shape[1], upscaled_rgb.shape[0]),
                                interpolation=cv2.INTER_NEAREST)

    # Merge the upscaled RGB channels and the upscaled alpha channel
    result = np.dstack((upscaled_rgb, upscaled_alpha))

    return result
