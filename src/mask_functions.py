# The purpose of this file is to create masks that can be 
# interpreted into numerical or visual data

import cv2
import numpy as np
import matplotlib.pyplot as plt
from annotation import *

# Example: combine_mask(AnnotationCollection([a1, a2, a3]))
# Given a list of Annotation objects, it combines the binary masks to create one unified mask

def combine_masks(annotation_collection):
    combined_mask = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=bool)

    for annotation in annotation_collection:
        combined_mask |= annotation.generate_mask()
        
    return combined_mask

# Example: create_overlay_mask(manual_mask, stardist_mask)
# Given the manual binary mask and auto-segmented binary mask,
# a visual RGB overlay mask is created

def create_overlay_mask(ground_truth_mask, comparison_mask):
    # True Positives: Both masks determined this to be part of an object
    tp = (ground_truth_mask & comparison_mask)
    # False Positives: Only the comparison mask determined this to be part of an object
    fp = (comparison_mask & ~ground_truth_mask)
    # False Negatives: Only the ground truth mask determined this to be part of an object
    fn = (ground_truth_mask & ~comparison_mask)
    base_mask = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3),dtype=np.uint8)
    base_mask[tp] = [255, 255, 0] # Yellow
    base_mask[fp] = [255, 0, 0] # Red
    base_mask[fn] = [0, 255, 0] # Green
    return base_mask

