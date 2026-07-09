import pandas as pd
import numpy as np
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

def group_annotations(annotations, accurate_query, comparison_queries):
    accurate_list = []
    comparison_dict = {}
    for comparison_query in comparison_queries:
        comparison_dict[comparison_query] = []
    for annotation in annotations:
        if accurate_query.matches(annotation):
            accurate_list.append(annotation)
        else:
            for comparison_query in comparison_queries:
                if comparison_query.matches(annotation):
                    comparison_dict[comparison_query].append(annotation)
                    break
    return (accurate_list, comparison_dict)

def run_benchmark(annotation_collection, accurate_query, comparison_queries, metrics):
    column_labels = [metric.__name__.replace("_", " ").upper() for metric in metrics]
    index_labels = []
    test_data = []
    for (spatial_key, annotations) in annotation_collection.spatial_index.items():
        (accurate_list, comparison_dict) = group_annotations(annotations, accurate_query, comparison_queries)
        for (comparison_query, comparison_list) in comparison_dict.items():
            accurate_mask = combine_masks(accurate_list)
            comparison_mask = combine_masks(comparison_list)
            results = []
            for metric in metrics:
                if metric is relative_error:
                    output = metric(accurate_list, comparison_list)
                    results.append(output)
                else:
                    output = metric(accurate_mask, comparison_mask)
                    results.append(output)
            index_labels.append(str(comparison_query))
            test_data.append(results)
    df = pd.DataFrame(test_data, columns=column_labels, index=index_labels)
    df.to_csv("benchmark2_output.csv")
    return df


        

        
        

