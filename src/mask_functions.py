import cv2
import numpy as np
from annotation import *

# given a list of Annotation objects, it combines the binary masks to create one unified mask
def combine_masks(annotations,image_width, image_height):
    combined_mask = np.zeros((image_height, image_width), dtype=np.uint8)
    for annotation in annotations:
        mask = annotation.generate_mask(image_width,image_height)
        cv2.bitwise_or(combined_mask, mask, dst=combined_mask)
    return combined_mask

def convert_to_image(mask):
    binary_image = (mask * 255).astype(np.uint8)
    cv2.imwrite("binary_image.png", binary_image)
    return True
