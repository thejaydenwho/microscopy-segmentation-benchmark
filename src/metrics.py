# The purpose of this file is to store the different metrics 
# to be calculated during benchmarking and visualized

import numpy as np

# Given a binary mask, compute the area in pixels

def area(mask):
    ones_count = np.count_nonzero(mask)
    return ones_count

# Given two binary masks, compute the area of their overlap

def intersection(mask1, mask2):
    ones_count = area(np.bitwise_and(mask1, mask2))
    return ones_count

# Given two binary masks, compute the area of their combined mask

def union(mask1, mask2):
    ones_count = area(np.bitwise_or(mask1, mask2))
    return ones_count

# Both IOU and Dice Coefficient are used to analyze image segmentation models.

# Computes the IOU score 

def iou(mask1, mask2):
    return intersection(mask1, mask2)/ float(union(mask1, mask2))

# Computes the Dice Coefficient

def dice_coefficient(mask1, mask2):
    return (2 * intersection(mask1, mask2))/ float(area(mask1) + area(mask2))

# Precision determines how conservative a model is at segmentation
# (Higher -> More conservative)

def precision(ground_truth_mask, comparison_mask):
    true_positives = intersection(ground_truth_mask, comparison_mask)
    false_positives = area(comparison_mask) - true_positives
    return (true_positives/float(true_positives + false_positives))

# Recall determines how thorough a model is at segmentation 
# (Higher -> More thorough)

def recall(ground_truth_mask, comparison_mask):
    true_positives = intersection(ground_truth_mask, comparison_mask)
    false_negatives = area(ground_truth_mask) - true_positives
    return (true_positives/float(true_positives + false_negatives))

# Relative error focuses on the amount of objects that were segemented
# between the two annotation groups (Lower -> More accurate)

def relative_error(ground_truth_annotations, comparison_annotations):
    ground_truth_count = len(ground_truth_annotations)
    comparison_count = len(comparison_annotations)
    return ((comparison_count - ground_truth_count)/ ground_truth_count)





