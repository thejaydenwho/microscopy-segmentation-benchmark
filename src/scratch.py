import json
from nimbus_parser import * 
from annotation import *
from mask_functions import *
from metrics import *
from visualization import *

path = "data/sample_DAPI.json"
path2 = "data/sample_mlo.json"
data = parse_annotations(path)
data2 = parse_annotation_property_values(path)
print(list(data.keys()))

print(visualize_benchmark("manual_DAPI_annotation",['cellpose_sam_DAPI_annotation', 'stardist_DAPI_annotation'],data,2048,1024))
