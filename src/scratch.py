import json
from config import *
from nimbus_parser import * 
from annotation import *
from mask_functions import *
from metrics import *
from visualization import *
import cProfile
import time 

json_path = "data/multi_image.json"
multi_image_annotations = annotations_from_json(json_path)
multi_image_annotations = AnnotationCollection(multi_image_annotations)

folder_path = "data"
full_annotations = annotations_from_folder(folder_path)

json_path2 = "data/largescale_mlo.json"
mlo_annotations = annotations_from_json(json_path2)
mlo_annotations = AnnotationCollection(mlo_annotations)

#visualize_benchmark(mlo_annotations, Query(label="manual annotations", tags=["manual_rRNA_annotation"]), [Query(label="CellposeSAM", tags=["cellpose_sam_rRNA_annotation"]), Query(label="Stardist", tags=["stardist_rRNA_annotation"]), Query(label="CondensateNet", tags=["condensate_net_rRNA_annotation"])])

#visualize_overlay(mlo_annotations, Query(label="manual annotations", tags=["manual_rRNA_annotation"]), Query(label="CellposeSAM", tags=["cellpose_sam_rRNA_annotation"]))

manual_query = Query(label="manual annotations", tags=["manual_DAPI_annotation"])
cellpose_query = Query(label="CellposeSAM", tags=["cellpose_sam_DAPI_annotation"])
stardist_query = Query(label="Stardist", tags=["stardist_DAPI_annotation"])
condensate_query = Query(label="CondensateNet", tags=["condensate_net_DAPI_annotation"])


df = run_benchmark(multi_image_annotations, manual_query,[cellpose_query,stardist_query,condensate_query], [iou, dice_coefficient, precision, recall, relative_error])

print(mlo_annotations.annotations[1])