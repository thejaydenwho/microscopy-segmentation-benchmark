import numpy as np

def area(mask):
    ones_count = np.count_nonzero(mask)
    return ones_count

def intersection(mask1, mask2):
    ones_count = np.count_nonzero(np.bitwise_and(mask1, mask2))
    return ones_count

def union(mask1, mask2):
    ones_count = np.count_nonzero(np.bitwise_or(mask1, mask2))
    return ones_count

def iou(mask1, mask2):
    return intersection(mask1, mask2)/ float(union(mask1, mask2))

def dice_coefficient(mask1, mask2):
    return (2 * intersection(mask1, mask2))/ float(area(mask1) + area(mask2))

def precision(accurate_mask, comparison_mask):
    true_positives = intersection(accurate_mask, comparison_mask)
    false_positives = area(comparison_mask) - true_positives
    return (true_positives/float(true_positives + false_positives))

def recall(accurate_mask, comparison_mask):
    true_positives = intersection(accurate_mask, comparison_mask)
    false_negatives = area(accurate_mask) - true_positives
    return (true_positives/float(true_positives + false_negatives))

def relative_error(accurate_annotations, comparison_annotations):
    accurate_count = len(accurate_annotations)
    comparison_count = len(comparison_annotations)
    return ((comparison_count - accurate_count)/ accurate_count)





