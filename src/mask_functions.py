import cv2
import numpy as np
import matplotlib.pyplot as plt
from annotation import *


# given a list of Annotation objects, it combines the binary masks to create one unified mask
def combine_masks(annotation_collection):
    combined_mask = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=bool)
    for annotation in annotation_collection:
        combined_mask |= annotation.generate_mask()
    return combined_mask

# true positives are yellow, false positives are red, false negatives are green
def create_overlay_mask(accurate_mask, comparison_mask):
    tp = (accurate_mask & comparison_mask)
    fp = (comparison_mask & ~accurate_mask)
    fn = (accurate_mask & ~comparison_mask)
    base_mask = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3),dtype=np.uint8)
    base_mask[tp] = [255, 255, 0] # yellow
    base_mask[fp] = [255, 0, 0] # red
    base_mask[fn] = [0, 255, 0] # green
    return base_mask

def convert_to_binary_image(mask):
    binary_image = (mask * 255).astype(np.uint8)
    cv2.imwrite("outputdata/binary_image.png", binary_image)
    return True

def convert_to_rgb_image(mask):
    plt.imshow(mask)
    plt.axis("off")
    plt.show()
