import json
from annotation import Annotation
from mask_functions import *

# Given the path of the json file as a string, return a dictionary containing the data
def load_json(path):
    with open(path,'r') as file:
        data = json.load(file)
    return data

def get_annotations(data):
    return data["annotations"]

def parse_annotation(ann):
    object_id = ann["_id"]
    dataset_id = ann["datasetId"]
    tags = ann["tags"]
    shape = ann["shape"]
    location = ann["location"]
    channel = ann["channel"]
    coordinates = ann["coordinates"]
    formatted_coordinates = []
    for point in coordinates:
        x_coordinate = point["x"]
        y_coordinate = point["y"]
        formatted_coordinates.append([x_coordinate,y_coordinate])
    annotation_object = Annotation(object_id, dataset_id, tags, shape, location, channel, formatted_coordinates)
    return annotation_object

def parse_annotations(path):
    data = load_json(path)
    annotations = get_annotations(data)
    annotation_list = []
    for ann in annotations:
        annotation_list.append(parse_annotation(ann))
    return annotation_list


def get_annotation_property_values(data):
    return data["annotationPropertyValues"]

def parse_annotation_property_value(apv):
    new_apv = apv.copy()
    apv_list = []
    for obj_id in new_apv.keys():
        apv_dict = {}
        apv_dict["object_id"] = obj_id
        measurement_id, *_ = apv[obj_id]
        apv_dict["measurement_id"] = measurement_id
        measurement_dict = (new_apv[obj_id])[measurement_id]
        for (metric, value) in measurement_dict.items():
            if metric == "Centroid":
                apv_dict[metric] = [value["x"], value["y"]]
            else:
                apv_dict[metric] = value
        apv_list.append(apv_dict)
    return apv_list  

def parse_annotation_property_values(path):
    data = load_json(path)
    apv = get_annotation_property_values(data)
    apv_list = parse_annotation_property_value(apv)
    return apv_list

path = "data/sample_mlo_advanced.json"
path2 = "data/sample_mlo.json"
data = parse_annotations(path)
data2 = parse_annotation_property_values(path)
combined_mask = combine_masks(data,2048,2048)
print(convert_to_image(combined_mask))
