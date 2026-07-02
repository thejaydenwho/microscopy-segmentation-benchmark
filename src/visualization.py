import pandas as pd
import matplotlib.pyplot as plt
from annotation import *
from mask_functions import *
from metrics import *


# import a list of tags (being the different annotation groups compared in the benchmark)
def group_benchmark(accurate_tag, comparison_tags, annotations_dict, image_width, image_height):
    functions = [iou, dice_coefficient, precision, recall]
    accurate_annotations = annotations_dict[accurate_tag]
    accurate_mask = combine_masks(accurate_annotations, image_width, image_height)
    x_labels = [func.__name__.replace("_", " ").upper() for func in functions]
    x_labels.append("RELATIVE ERROR")
    series_data = []
    for comparison_tag in comparison_tags:
        comparison_annotations = annotations_dict[comparison_tag]
        comparison_mask = combine_masks(comparison_annotations, image_width, image_height)
        trial_data = []
        output = None
        for func in functions:
            output = func(accurate_mask, comparison_mask)
            trial_data.append(output)
        output = relative_error(accurate_tag, comparison_tag, annotations_dict)
        trial_data.append(output)
        series_data.append(trial_data)
    return (series_data, x_labels)

def visualize_benchmark(accurate_tag, comparison_tags, annotations_dict, image_width, image_height):
    (series_data, x_labels) = group_benchmark(accurate_tag, comparison_tags, annotations_dict, image_width, image_height)
    series_data = np.array(series_data).T
    df = pd.DataFrame(series_data, index = x_labels, columns = comparison_tags)
    df.plot(kind = "bar", rot = 0)
    plt.show()

    