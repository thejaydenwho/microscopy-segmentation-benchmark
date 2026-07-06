import pandas as pd
from annotation import *
from mask_functions import *
from metrics import *
from benchmark import *

# import a list of tags (being the different annotation groups compared in the benchmark)
def run_group_benchmark(accurate_tag, comparison_tags, annotations_dict):
    functions = [iou, dice_coefficient, precision, recall]
    accurate_annotations = annotations_dict[accurate_tag]
    accurate_mask = combine_masks(accurate_annotations)
    x_labels = [func.__name__.replace("_", " ").upper() for func in functions]
    x_labels.append("RELATIVE ERROR")
    series_data = []
    for comparison_tag in comparison_tags:
        comparison_annotations = annotations_dict[comparison_tag]
        comparison_mask = combine_masks(comparison_annotations)
        trial_data = []
        output = None
        for func in functions:
            output = func(accurate_mask, comparison_mask)
            trial_data.append(output)
        output = relative_error(accurate_tag, comparison_tag, annotations_dict)
        trial_data.append(output)
        series_data.append(trial_data)
    series_data = np.array(series_data).T
    df = pd.DataFrame(series_data, index = x_labels, columns = comparison_tags)
    df.to_csv("benchmark_output.csv")
    return df
