# microscopy-segmentation-benchmark

This project was developed during my time in the After School Matters STEM Laboratory Research Internship at the University of Chicago, where I worked in the Fei Lab. The goal of the project was to create a reproducible benchmarking framework in Python to compare different microscopy segmentation models using data exported from the NimbusImage platform.

To demonstrate the capabilities of the framework, I fine-tuned a pre-trained segmentation model (Cellpose) using manual annotations of the DAPI region of PC3 cells and compared its performance with other segmentation models. The presentation included in this repository provides more detail about the work and results.

## Presentation

[View the final project presentation](presentation/final-presentation.pdf)

## Project Structure

* `src/` — Source code for parsing annotations, generating binary masks, calculating metrics, and visualizing results
* `inputdata/` — Input annotation data used by the framework
* `outputdata/` — Generated benchmarking results and visualizations
* `presentation/` — Final project presentation
