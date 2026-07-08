import json
import os
from pathlib import Path
from annotation import *

def load_json(json_file):
    with open(json_file,'r') as file:
        data_dict = json.load(file)
    return data_dict

def annotation_from_entry(entry, source_file):
    object_id = entry["_id"]
    dataset_id = entry["datasetId"]
    tags = entry["tags"]
    shape = entry["shape"]
    xy = entry["location"]["XY"]
    z = entry["location"]["Z"]
    time = entry["location"]["Time"]
    channel = entry["channel"]
    coordinates = entry["coordinates"]
    formatted_coordinates = []
    for point in coordinates:
        x_coordinate = point["x"]
        y_coordinate = point["y"]
        formatted_coordinates.append([x_coordinate,y_coordinate])
    annotation = Annotation(object_id, dataset_id, source_file, tags, shape, xy, z, time, channel, formatted_coordinates)
    return annotation

def annotations_from_json(json_file):
    data_dict = load_json(json_file)
    entries = data_dict["annotations"]
    annotation_list = []
    source_file = os.path.basename(json_file)
    for entry in entries:
        annotation = annotation_from_entry(entry, source_file)
        annotation_list.append(annotation)
    return annotation_list

def annotations_from_folder(folder_path):
    all_annotations = []
    folder = Path(folder_path)
    for json_file in folder.glob("*.json"):
        annotations = annotations_from_json(json_file)
        all_annotations.extend(annotations)
    return AnnotationCollection(all_annotations)


'''
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
'''