import pandas as pd
from annotation import *
from mask_functions import *
from metrics import *
from benchmark import *

def run_group_benchmark(annotation_collection, accurate_query, comparison_queries):
    functions = [iou, dice_coefficient, precision, recall]
    accurate_annotations = annotation_collection.filter_by(accurate_query)
    accurate_mask = combine_masks(accurate_annotations)
    x_labels = [func.__name__.replace("_", " ").upper() for func in functions]
    x_labels.append("RELATIVE ERROR")
    query_labels = [str(query) for query in comparison_queries]
    series_data = []
    for comparison_query in comparison_queries:
        comparison_annotations = annotation_collection.filter_by(comparison_query)
        comparison_mask = combine_masks(comparison_annotations)
        trial_data = []
        output = None
        for func in functions:
            output = func(accurate_mask, comparison_mask)
            trial_data.append(output)
        output = relative_error(accurate_annotations, comparison_annotations)
        trial_data.append(output)
        series_data.append(trial_data)
    series_data = np.array(series_data).T
    df = pd.DataFrame(series_data, index = x_labels, columns = query_labels)
    df.to_csv("benchmark_output.csv")
    return df