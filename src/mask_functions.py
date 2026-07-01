import cv2
import numpy as np

# given a list of Annotation objects, it combines the binary masks to create one unified mask
def combine_masks(annotations,image_width, image_height):
    mask_list = []
    for annotation in annotations:
        mask = annotation.generate_mask(image_width,image_height)
        mask_list.append(annotation.generate_mask(image_height, image_width))
    combined_mask = np.bitwise_or.reduce(mask_list)
    return combined_mask

def convert_to_image(mask):
    binary_image = (mask * 255).astype(np.uint8)
    cv2.imwrite("binary_image.png", binary_image)
