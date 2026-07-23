# This file is used to run and test code.

import json
from config import *
from nimbus_parser import * 
from annotation import *
from mask_functions import *
from metrics import *
from visualization import *
import cProfile
import time 
'''
json_path = "inputdata/multi_image.json"
multi_image_annotations = annotations_from_json(json_path)
multi_image_annotations = AnnotationCollection(multi_image_annotations)

folder_path = "inputdata"
full_annotations = annotations_from_folder(folder_path)

json_path2 = "inputdata/largescale_mlo.json"
mlo_annotations = annotations_from_json(json_path2)
mlo_annotations = AnnotationCollection(mlo_annotations)

manual_query = Query(label="manual annotations", tags=["manual_DAPI"])
cellpose_query = Query(label="CellposeSAM", tags=["cellpose_sam_DAPI"])
stardist_query = Query(label="Stardist", tags=["stardist_dapi"])

json_path3 = "inputdata/massive_test.json"

mlo_annotations = AnnotationCollection(annotations_from_json(json_path3))

df = run_benchmark(mlo_annotations, manual_query, [cellpose_query,stardist_query],[iou,dice_coefficient,precision])
create_bar_chart(average_dataframe(df),metrics=[iou,dice_coefficient],image_name="bc.png")
create_density(df,[iou,dice_coefficient,precision],"density2.png")

gt_query = Query(label="Manual", tags=["manual_DAPI_annotation"], xy=0, z=0, time=0, channel=0)
comparison_query = Query(label="CellposeSAM", tags=["cellpose_sam_DAPI_annotation"], xy=0, z=0, time=0, channel=0)

visualize_binary_image(multi_image_annotations, comparison_query, "BinaryImage.png")
visualize_overlay(multi_image_annotations, gt_query, comparison_query, "ExampleOverlay.png")


rRNA_annotations = AnnotationCollection(annotations_from_json("inputdata/rRNAcellposetrain1.json"))
example_query = Query(label="Manual", tags=["manual"], xy=0, z=4, time=1, channel=3)
example_query2 = Query(label="CellposeSAM", tags=["cellpose_sam"], xy=0, z=4, time=1, channel=3)
visualize_binary_image(rRNA_annotations, example_query, "BinaryImage2.png")
visualize_overlay(rRNA_annotations, example_query, example_query2, "OverlayImage2.png")
gt_query2 = Query(label="Manual", tags=["manual"])
example_query2 = Query(label="CellposeSAM", tags=["cellpose_sam"])
example_query3 = Query(label="Stardist", tags=["stardist"])
example_query4 = Query(label="CellposeTrained", tags=["cellpose"])

df = run_benchmark(rRNA_annotations, gt_query2, [example_query2, example_query3, example_query4],[dice_coefficient,precision,iou,recall,relative_error])
avg_df = average_dataframe(df)
create_bar_chart(avg_df, [iou, dice_coefficient], image_name="barchart.png")
create_density(df, [dice_coefficient, precision, iou], image_name="density.png")
create_vertical_histogram(df, [dice_coefficient, precision, iou], image_name="histogram.png")
'''
'''
annotation_collection = AnnotationCollection(annotations_from_json("inputdata/quickcheck.json"))
has_negative = False

for annotation in annotation_collection:
    print(annotation)
    for x, y in annotation.coordinates:
        if x < 0 or y < 0:
            print(annotation.object_id, x, y)
            has_negative = True

print("Negative coordinates found:", has_negative)

print(len(annotation_collection))

visualize_binary_image(annotation_collection, query=Query("hello"), image_name="testing.png")
'''

annotation_col = AnnotationCollection(annotations_from_json("inputdata/scientificfigures.json"))
print(len(annotation_col))


gt_query = Query(label = "Ground Truth", tags=["testing"])
base_model = Query(label = "Cyto3 Base Model", tags=["cyto_3"])
e10_model = Query(label = "Trained Model", tags=["10E"])
stardist = Query(label = "Stardist", tags=["stardist"])
cellpose_sam = Query(label = "CellposeSAM", tags=["cellpose_sam"])

'''
e20_model = Query(label = "20 Epoch", tags=["20E"])
e30_model = Query(label = "30 Epoch", tags=["30E"])
e40_model = Query(label = "40 Epoch", tags=["40E"])
e50_model = Query(label = "50 Epoch", tags=["50E"])
e60_model = Query(label = "60 Epoch", tags=["60E"])
'''
visualize_overlay(annotation_col, gt_query, base_model, "base.png")
results = run_benchmark(annotation_col, gt_query, [cellpose_sam, stardist, base_model,e10_model], [dice_coefficient,precision,iou,recall,relative_error])
avg_results = average_dataframe(results)

create_bar_chart(avg_results, [iou, dice_coefficient, precision, recall], "scientific_figure.png", "Trained Cellpose Model vs. Alternate Segmentation Models")
create_bar_chart(avg_results, [relative_error], "scientific_figure2.png", "Trained Cellpose Model vs. Alternate Segmentation Models")

