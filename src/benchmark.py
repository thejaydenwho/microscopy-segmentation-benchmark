# The purpose of this file is to streamline benchmarking across multiple datasets
# represented by a single AnnotationObject. This data can be generalized to see patterns.

import pandas as pd
import numpy as np
from annotation import *
from mask_functions import *
from metrics import *
from benchmark import *

# Within a single spatial location of the full Annotation dataset,
# collect all the ground truth Annotations as well as
# each set of comparison Annotations to be compared

def group_annotations(annotations, ground_truth_query, comparison_queries):
    ground_truth_list = []
    comparison_dict = {}

    for comparison_query in comparison_queries:
        comparison_dict[comparison_query] = []

    for annotation in annotations:

        if ground_truth_query.matches(annotation):
            ground_truth_list.append(annotation)
            
        else:

            for comparison_query in comparison_queries:

                if comparison_query.matches(annotation):
                    comparison_dict[comparison_query].append(annotation)
                    break

    return (ground_truth_list, comparison_dict)

# Benchmark the given metrics across each of the spatial locations
# within the AnnotationCollection based on the Queries

def run_benchmark(annotation_collection, ground_truth_query, comparison_queries, metrics):
    column_labels = ["Spatial Index", "Algorithm"]
    column_labels.extend([metric.__name__.replace("_", " ").upper() for metric in metrics])
    test_data = []

    for (spatial_key, annotations) in annotation_collection.spatial_index.items():
        (ground_truth_list, comparison_dict) = group_annotations(annotations, ground_truth_query, comparison_queries)

        for (comparison_query, comparison_list) in comparison_dict.items():
            ground_truth_mask = combine_masks(ground_truth_list)
            comparison_mask = combine_masks(comparison_list)
            results = []
            results.extend([spatial_key, str(comparison_query)])

            for metric in metrics:

                if metric is relative_error:
                    output = metric(ground_truth_list, comparison_list)
                    results.append(output)

                else:
                    output = metric(ground_truth_mask, comparison_mask)
                    results.append(output)

            test_data.append(results)
    df = pd.DataFrame(test_data, columns=column_labels)
    df.to_csv("outputdata/benchmark_metrics.csv")
    return df

# For each model being tested, average the benchmarking data
# gathered across all the spatial locations

def average_dataframe(df):
    averaged_df = df.groupby("Algorithm").mean(numeric_only=True)
    averaged_df.to_csv("outputdata/averaged_metrics.csv")
    return averaged_df


        

        
        

