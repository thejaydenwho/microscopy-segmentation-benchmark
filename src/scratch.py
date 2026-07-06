import json
from config import *
from nimbus_parser import * 
from annotation import *
from mask_functions import *
from metrics import *
from visualization import *
import cProfile
import time 

path2 = "data/sample_DAPI.json"
data2 = parse_annotations(path2)
path = "data/multi_image.json"
data = parse_annotations(path)

def main():
    visualize_benchmark("manual_DAPI_annotation",['cellpose_sam_DAPI_annotation', 'stardist_DAPI_annotation'],data)

start_time = time.perf_counter()
main()
end_time = time.perf_counter()
print(end_time-start_time)

print(data2.keys())


visualize_overlay("manual_DAPI_annotation" , "cellpose_sam_DAPI_annotation", {"XY":0,"Z":0,"Time":0}, 0, data)

print(filter_annotations(data, "manual_DAPI_annotation", {"XY":0,"Z":0,"Time":0}, 0))

