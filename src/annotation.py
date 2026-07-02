import cv2
import numpy as np

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

    def generate_mask(self, image_width, image_height):
        mask = np.zeros((image_height, image_width), dtype=np.uint8)
        points = np.round(self.coordinates).astype(np.int32)
        cv2.fillPoly(mask,[points],color=1)
        self.mask = mask
        np.savetxt("mask_output.txt", mask, fmt="%d")
        return mask
    
    
        