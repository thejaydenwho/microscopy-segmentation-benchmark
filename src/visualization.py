import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from annotation import *
from mask_functions import *
from metrics import *
from benchmark import *

def create_bar_chart(df, title):
    transposed_df = df.T
    transposed_df.plot(kind = "bar", rot = 0)
    plt.xlabel("Metric")
    plt.ylabel("Score")
    plt.title(title)
    plt.show()

def create_box_plot(df, metrics):
    column_labels = [
        metric.__name__.replace("_", " ").upper()
        for metric in metrics
    ]

    fig, axes = plt.subplots(
        1,
        len(column_labels),
        figsize=(4 * len(column_labels), 4)
    )

    if len(column_labels) == 1:
        axes = [axes]

    for ax, label in zip(axes, column_labels):
        df.boxplot(
            column=label,
            by="Algorithm",
            ax=ax
        )
        ax.set_title(label)
        ax.set_xlabel("")
        ax.set_ylabel("Score")

    plt.suptitle("")
    plt.tight_layout()
    plt.show()

def create_vertical_histogram(df, metrics):
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
    plt.show()

def create_horizontal_histogram(df, metrics):
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
    plt.tight_layout()
    plt.show()

def create_density(df, metrics):
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
    plt.tight_layout()
    plt.show()

def visualize_overlay(annotation_collection, accurate_query, comparison_query):
    accurate_annotations = annotation_collection.filter_by(accurate_query)
    comparison_annotations = annotation_collection.filter_by(comparison_query)
    accurate_mask = combine_masks(accurate_annotations)
    comparison_mask = combine_masks(comparison_annotations)
    overlay_mask = create_overlay_mask(accurate_mask, comparison_mask)
    plt.imshow(overlay_mask)
    yellow_patch = mpatches.Patch(color='yellow', label='True Positive (TP)')
    red_patch = mpatches.Patch(color='red', label='False Positive (FP)')
    green_patch = mpatches.Patch(color='green', label='False Negative (FN)')
    plt.legend(handles=[yellow_patch, red_patch, green_patch], bbox_to_anchor=(1.05, 1), 
    loc='upper left', borderaxespad=0.)
    plt.axis("off")
    plt.title(str(comparison_query))
    plt.tight_layout()
    plt.show()
    return overlay_mask


    