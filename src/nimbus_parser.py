# The purpose of this file is to convert JSON files exported from your NimbusImage dataset 
# into useable Annotation data

import json
import os
from pathlib import Path
from annotation import *

# Example: load_json("sample_mlo.json") 
# Returns a dictionary of all the attributes of the JSON file

def load_json(json_file):

    with open(json_file,'r') as file:
        data_dict = json.load(file)
        
    return data_dict


# This is a helper function for annotations_from_json()
# Returns an Annotation object of the dictionary entry

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

    annotation = Annotation(object_id, dataset_id, source_file,
                             tags, shape, xy,
                               z, time, channel, formatted_coordinates)
    return annotation

# Example: annotations_from_json("sample_mlo.json") 
# Returns a list of Annotation objects for the JSON file

def annotations_from_json(json_file):
    data_dict = load_json(json_file)
    entries = data_dict["annotations"]
    annotation_list = []
    source_file = os.path.basename(json_file)
    for entry in entries:
        annotation = annotation_from_entry(entry, source_file)
        annotation_list.append(annotation)
    return annotation_list

# Example: annotations_from_folder("inputdata")
# Returns an AnnotationCollection object containing all the Annotations
# from each JSON file within the folder

def annotations_from_folder(folder_path):
    all_annotations = []
    folder = Path(folder_path)

    for json_file in folder.glob("*.json"):
        annotations = annotations_from_json(json_file)
        all_annotations.extend(annotations)
        
    return AnnotationCollection(all_annotations)