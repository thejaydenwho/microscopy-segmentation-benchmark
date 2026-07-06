import json
from nimbus_parser import * 
from annotation import *
from mask_functions import *
from metrics import *
from visualization import *
import cProfile
import time 
path2 = "data/sample_mlo.json"
data2 = parse_annotation_property_values(path2)

def main():
    path = "data/multi_image.json"
    data = parse_annotations(path)
    visualize_benchmark("manual_DAPI_annotation",['cellpose_sam_DAPI_annotation', 'stardist_DAPI_annotation'],data,2048,1024)

start_time = time.perf_counter()
main()
end_time = time.perf_counter()
print(end_time-start_time)