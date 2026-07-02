import pandas as pd
import matplotlib.pyplot as plt
from annotation import *
from mask_functions import *
from metrics import *
from benchmark import *

def visualize_benchmark(accurate_tag, comparison_tags, annotations_dict, image_width, image_height):
    df = run_group_benchmark(accurate_tag, comparison_tags, annotations_dict, image_width, image_height)
    df.plot(kind = "bar", rot = 0)
    plt.show()

    