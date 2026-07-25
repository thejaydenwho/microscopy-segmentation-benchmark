# The purpose of this file is to use the benchmarking dataframes collected 
# and visualize the data in different graphs

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from annotation import *
from mask_functions import *
from metrics import *
from benchmark import *

# Uses an averaged dataframe to compare overall metrics betwene different models

def create_bar_chart(df, metrics, image_name, title = ""):
    column_labels = [metric.__name__.replace("_", " ").upper() for metric in metrics]
    summary_df = df.groupby("Algorithm")[column_labels].mean()
    transposed_df = summary_df.T
    ax = transposed_df.plot(kind="bar", rot=0)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.xlabel("Metric")
    plt.ylabel("Score")
    plt.title(title)
    plt.savefig(f"outputdata/{image_name}", dpi=300, bbox_inches="tight")
    plt.close()

# The four visualizing functions below 
# use the raw benchmark dataframe to analyze distribution 

def create_box_plot(df, metrics, image_name, title=""):
    column_labels = [
        metric.__name__.replace("_", " ").upper()
        for metric in metrics
    ]

    fig, axes = plt.subplots(
        1,
        len(column_labels),
        figsize=(6 * len(column_labels), 5)
    )

    if len(column_labels) == 1:
        axes = [axes]

    for ax, label in zip(axes, column_labels):
        df.boxplot(column=label, by="Algorithm", ax=ax)

        ax.set_title(label)
        ax.set_xlabel("")
        ax.set_ylabel("Metric Score")

        # Rotate algorithm names for readability
        ax.tick_params(axis="x", rotation=45)

        # Align rotated labels to the right
        for tick in ax.get_xticklabels():
            tick.set_horizontalalignment("right")

    plt.suptitle(title)
    plt.tight_layout()

    plt.savefig(
        f"outputdata/{image_name}",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def create_vertical_histogram(df, metrics, image_name, title = ""):
    column_labels = [metric.__name__.replace("_", " ").upper() for metric in metrics]
    algorithms = df["Algorithm"].unique()
    fig, axes = plt.subplots(
        len(algorithms),
        len(column_labels),
        figsize=(5 * len(column_labels), 4 * len(algorithms)))
    if len(algorithms) == 1:
        axes = np.array([axes])
    if len(column_labels) == 1:
        axes = axes.reshape(-1, 1)
    for row, algorithm in enumerate(algorithms):
        for col, label in enumerate(column_labels):
            ax = axes[row][col]
            scores = df[df["Algorithm"] == algorithm][label]
            ax.hist(scores,bins=15)
            ax.set_title(f"{algorithm} - {label}")
            ax.set_xlabel("Score")
            ax.set_ylabel("Frequency")
            ax.set_xlim(0, 1)
    plt.tight_layout()
    plt.savefig(f"outputdata/{image_name}", dpi=300, bbox_inches="tight")
    plt.close()

def create_horizontal_histogram(df, metrics, image_name, title = ""):
    column_labels = [
        metric.__name__.replace("_", " ").upper()
        for metric in metrics
    ]
    algorithms = df["Algorithm"].unique()
    fig, axes = plt.subplots(
        len(column_labels),
        len(algorithms),
        figsize=(5 * len(algorithms), 4 * len(column_labels)))
    if len(column_labels) == 1:
        axes = np.array([axes])
    if len(algorithms) == 1:
        axes = axes.reshape(-1, 1)
    for row, label in enumerate(column_labels):
        for col, algorithm in enumerate(algorithms):
            ax = axes[row][col]
            scores = df[df["Algorithm"] == algorithm][label]
            ax.hist(scores, bins=15)
            ax.set_title(f"{algorithm} - {label}")
            ax.set_xlabel("Score")
            ax.set_ylabel("Frequency")
            ax.set_xlim(0, 1)
    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(f"outputdata/{image_name}", dpi=300, bbox_inches="tight")
    plt.close()

def create_density(df, metrics, image_name, title = ""):
    column_labels = [metric.__name__.replace("_", " ").upper() for metric in metrics]
    algorithms = df["Algorithm"].unique()
    fig, axes = plt.subplots(
        len(algorithms),
        len(column_labels),
        figsize=(5 * len(column_labels), 4 * len(algorithms)),
        sharex=True
    )
    if len(algorithms) == 1:
        axes = np.array([axes])
    if len(column_labels) == 1:
        axes = axes.reshape(-1, 1)
    colors = sns.color_palette("tab10", len(algorithms))
    for row, algorithm in enumerate(algorithms):
        for col, label in enumerate(column_labels):
            ax = axes[row][col]
            scores = df[df["Algorithm"] == algorithm][label]
            sns.kdeplot(
                data=scores,
                ax=ax,
                fill=True,
                color=colors[row],
                alpha=0.5,
                linewidth=2
            )
            ax.set_title(f"{algorithm} - {label}")
            ax.set_xlabel("Score")
            ax.set_ylabel("Density")
            ax.set_xlim(0, 1)
    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(f"outputdata/{image_name}", dpi=300, bbox_inches="tight")
    plt.close()

# Create a binary image for a certain instance of object segmentation

def visualize_binary_image(annotation_collection, query, image_name):
    filtered_list = annotation_collection.filter_by(query)
    mask = combine_masks(filtered_list)
    binary_image = (mask * 255).astype(np.uint8)
    cv2.imwrite((f"outputdata/{image_name}"), binary_image)
    return True

# Create an RGB image visualizing the overlay 
# between a set of ground truth annotations and comparison annotations

def visualize_overlay(annotation_collection, ground_truth_query, comparison_query, image_name):
    ground_truth_annotations = annotation_collection.filter_by(ground_truth_query)
    comparison_annotations = annotation_collection.filter_by(comparison_query)
    ground_truth_mask = combine_masks(ground_truth_annotations)
    comparison_mask = combine_masks(comparison_annotations)
    overlay_mask = create_overlay_mask(ground_truth_mask, comparison_mask)
    plt.imshow(overlay_mask)
    yellow_patch = mpatches.Patch(color='yellow', label='True Positive (TP)')
    red_patch = mpatches.Patch(color='red', label='False Positive (FP)')
    green_patch = mpatches.Patch(color='green', label='False Negative (FN)')
    plt.legend(handles=[yellow_patch, red_patch, green_patch], bbox_to_anchor=(1.05, 1), 
    loc='upper left', borderaxespad=0.)
    plt.axis("off")
    plt.title(f"{str(comparison_query)} vs {str(ground_truth_query)}")
    plt.tight_layout()
    plt.savefig(f"outputdata/{image_name}", dpi=300, bbox_inches="tight")
    plt.close()
    return True


    