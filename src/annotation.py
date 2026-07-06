import cv2
import numpy as np
from config import *

class Annotation:
    def __init__(self, object_id, dataset_id, tags, shape, location, channel, coordinates):
        self.object_id = object_id
        self.dataset_id = dataset_id
        self.tags = tags
        self.shape = shape
        self.location = location
        self.channel = channel
        self.coordinates = coordinates
        self.mask = None
        
    def __str__(self):
        return(f'''Object ID: {self.object_id}\n
               Dataset ID: {self.dataset_id}\n
               Tags: {self.tags}\n
               Shape: {self.shape}\n
               Location: {self.location}\n
               Channel: {self.channel}''')

    def generate_mask(self):
        if self.mask is None:
            mask = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=np.uint8)
            points = np.round(self.coordinates).astype(np.int32)
            cv2.fillPoly(mask,[points],color=1)
            self.mask = mask.astype(bool)
        return self.mask
        
# Filters 
def filter_annotations(annotations_dict, tag, location, channel):
    annotations = annotations_dict[tag]
    return [
        a for a in annotations  
        if a.location == location 
        and a.channel == channel 
    ]
        
    
    
        