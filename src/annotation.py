import cv2
import numpy as np
from config import *

class Annotation:
    def __init__(self, object_id, dataset_id, source_file, tags, shape, xy, z, time, channel, coordinates):
        self.object_id = object_id
        self.dataset_id = dataset_id
        self.source_file = source_file
        self.tags = tags
        self.shape = shape
        self.xy = xy
        self.z = z
        self.time = time
        self.channel = channel
        self.coordinates = coordinates
        self.mask = None
        
    def __str__(self):
        return(f'''\n
               Object ID: {self.object_id}\n
               Dataset ID: {self.dataset_id}\n
               Source File: {self.source_file}\n
               Tags: {self.tags}\n
               Shape: {self.shape}\n
               XY: {self.xy}\n
               Z: {self.z}\n
               Time: {self.time}\n
               Channel: {self.channel}''')

    def generate_mask(self):
        if self.mask is None:
            mask = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=np.uint8)
            points = np.round(self.coordinates).astype(np.int32)
            cv2.fillPoly(mask,[points],color=1)
            self.mask = mask.astype(bool)
        return self.mask

class Query:
    def __init__(self, label, object_id = None, dataset_id = None, tags = None, shape = None, xy = None, z = None, time = None, channel = None):
        self.label = label
        self.object_id = object_id
        self.dataset_id = dataset_id
        self.tags = tags
        self.shape = shape
        self.xy = xy
        self.z = z
        self.time = time
        self.channel = channel

    def __str__(self):
        return self.label
    
    def __eq__(self,other):
        if isinstance(other,Query):
            attributes = ["label", "object_id", "dataset_id", "tags", "shape", "xy", "z", "time", "channel"]
            for attribute in attributes:
                self_attr = getattr(self, attribute)
                other_attr = getattr(other, attribute)
                if (self_attr != other_attr):
                    return False
            return True
        else:
            return False
        
    def __hash__(self):
    # Only tags needs conversion because it is a mutable list
        tags_hashable = frozenset(self.tags) if self.tags is not None else None
        return hash((
            self.label,
            self.object_id,
            self.dataset_id,
            tags_hashable,
            self.shape,
            self.xy,
            self.z,
            self.time,
            self.channel
        ))

    def matches(self, annotation):
        attributes = [
            "object_id",
            "dataset_id",
            "shape",
            "xy",
            "z",
            "time",
            "channel"
        ]
        # check ordinary attributes
        for attr in attributes:
            query_value = getattr(self, attr)
            if query_value is None:
                continue
            annotation_value = getattr(annotation, attr)
            if annotation_value != query_value:
                return False
        # check tags separately
        if self.tags is not None:
            if not set(self.tags).issubset(set(annotation.tags)):
                return False
        return True
    
class AnnotationCollection:
    def __init__(self, annotations=None):
        self.annotations = []
        self.spatial_index = {}
        if annotations is not None:
            self.add_annotations(annotations)
                
    def __iter__(self):
        return iter(self.annotations)
    
    def __len__(self):
        return len(self.annotations)
    
    def add_annotations(self, annotations):
        self.annotations.extend(annotations)
        for annotation in annotations:
            key = (annotation.source_file, annotation.dataset_id, annotation.xy, 
                annotation.z, annotation.time, annotation.channel)
            if key not in self.spatial_index:
                self.spatial_index[key] = [annotation]
            else:
                self.spatial_index[key].append(annotation)

    def filter_by(self, query):
        filtered = []
        for annotation in self.annotations:
            if query.matches(annotation):
                filtered.append(annotation)
        return filtered
        
    

                        
    

                    



        
    
    
        