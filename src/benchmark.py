import pandas as pd
import numpy as np
from annotation import *
from mask_functions import *
from metrics import *
from benchmark import *

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
    column_labels = ["Spatial Index", "Algorithm"]
    column_labels.extend([metric.__name__.replace("_", " ").upper() for metric in metrics])
    test_data = []
    for (spatial_key, annotations) in annotation_collection.spatial_index.items():
        (accurate_list, comparison_dict) = group_annotations(annotations, accurate_query, comparison_queries)
        for (comparison_query, comparison_list) in comparison_dict.items():
            accurate_mask = combine_masks(accurate_list)
            comparison_mask = combine_masks(comparison_list)
            results = []
            results.extend([spatial_key, str(comparison_query)])
            for metric in metrics:
                if metric is relative_error:
                    output = metric(accurate_list, comparison_list)
                    results.append(output)
                else:
                    output = metric(accurate_mask, comparison_mask)
                    results.append(output)
            test_data.append(results)
    df = pd.DataFrame(test_data, columns=column_labels)
    df.to_csv("outputdata/benchmark_metrics.csv")
    return df

def average_dataframe(df):
    averaged_df = df.groupby("Algorithm").mean(numeric_only=True)
    averaged_df.to_csv("outputdata/averaged_metrics.csv")
    return averaged_df


        

        
        

