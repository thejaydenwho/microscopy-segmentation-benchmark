import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from annotation import *
from mask_functions import *
from metrics import *
from benchmark import *

def visualize_benchmark(annotation_collection, accurate_query, comparison_queries):
    df = run_group_benchmark(annotation_collection, accurate_query, comparison_queries)
    df.plot(kind = "bar", rot = 0)
    plt.show()


def visualize_overlay(annotation_collection, accurate_query, comparison_query):
    accurate_annotations = annotation_collection.filter_by(accurate_query)
    comparison_annotations = annotation_collection.filter_by(comparison_query)
    accurate_mask = combine_masks(accurate_annotations)
    comparison_mask = combine_masks(comparison_annotations)
    overlay_mask = create_overlay_mask(accurate_mask, comparison_mask)
    plt.imshow(overlay_mask)
    yellow_patch = mpatches.Patch(color='yellow', label='True Positive (TP)')
    red_patch = mpatches.Patch(color='red', label='False Positive (FP)')
    green_patch = mpatches.Patch(color='green', label='False Negative (FN)')
    plt.legend(handles=[yellow_patch, red_patch, green_patch], bbox_to_anchor=(1.05, 1), 
    loc='upper left', borderaxespad=0.)
    plt.axis("off")
    plt.title(str(comparison_query))
    plt.tight_layout()
    plt.show()
    return overlay_mask


    