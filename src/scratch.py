# This file is used to run and test code.

import json
from config import *
from nimbus_parser import * 
from annotation import *
from mask_functions import *
from metrics import *
from visualization import *

annotation_col = AnnotationCollection(annotations_from_json("inputdata/PC3_Model_Full_Dataset.json"))

gt_query = Query(label = "Ground Truth", tags=["testing"])
base_model = Query(label = "0", tags=["cyto_3"])
e10_model = Query(label = "10", tags=["10E"])
e20_model = Query(label = "20", tags=["20E"])
e30_model = Query(label = "30", tags=["30E"])
e40_model = Query(label = "40", tags=["40E"])
e50_model = Query(label = "50", tags=["50E"])
e60_model = Query(label = "60", tags=["60E"])

epoch_improvements = run_benchmark(annotation_col, gt_query, [base_model, e10_model, e20_model, e30_model, e40_model, e50_model, e60_model], [iou, dice_coefficient, precision, recall,relative_error], "epoch_testing_results.csv")
avg_epoch_improvements = average_dataframe(epoch_improvements, "epoch_metrics.csv")

cyto3_model = Query(label = "Cyto3 Cellpose", tags=["cyto_3"])
trained_model = Query(label = "Fine-tuned Cellpose", tags=["60E"])
stardist = Query(label = "Stardist", tags=["stardist"])
cellpose_sam = Query(label = "CellposeSAM", tags=["cellpose_sam"])

model_comparisons = run_benchmark(annotation_col, gt_query, [cyto3_model, trained_model, stardist, cellpose_sam], [iou, dice_coefficient, precision, recall,relative_error], "model_testing_results.csv")
avg_model_comparisons = average_dataframe(model_comparisons, "model_metrics.csv")
create_bar_chart(avg_model_comparisons, [iou, dice_coefficient, precision, recall], "model_barchart.png", "Comparing Segmentation Performance")
create_box_plot(model_comparisons, [dice_coefficient], "model_consistency.png", "Segmentation Performance Consistency Across Models")

