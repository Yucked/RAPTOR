# RAPTOR

**Retinal Aggregate Profiling, Tracking, and Object Recognition**

RAPTOR is a Python-based bioimage analysis pipeline for detecting, segmenting, and quantifying protein aggregates in retinal confocal microscopy images. Designed for human and *Nothobranchius furzeri* (African turquoise killifish) retinal samples, RAPTOR extracts reproducible measurements of aggregate abundance, size, fluorescence intensity, and distribution across retinal layers to support studies of aging and neurodegeneration.

## Features

- **Microscopy image loading:** Supports Zeiss `.czi` z-stacks and `.tif`/`.tiff` images, with pixel calibration extracted from CZI metadata.
- **Metadata parsing:** Extracts sample age, condition, genotype, retinal region, magnification, channels, protein markers, and replicate information from standardized filenames.
- **Image preprocessing:** Maximum-intensity projection, rolling-ball background correction, and tissue masking.
- **Aggregate segmentation:** Protein-specific intensity thresholds, physical size filters, and local-contrast filtering.
- **Retinal layer analysis:** Supports externally prepared TIFF masks and experimental automatic layer-mask generation for layer-resolved measurements.
- **Quality control:** Threshold comparison and visual inspection of tissue and aggregate masks.
- **Optional 3D analysis:** Can compare projection-based measurements with volumetric metrics when enabled.

## Quantitative Measurements

| Metric | Description |
| --- | --- |
| `puncta_count` | Number of detected aggregates (connected objects) |
| `puncta_density_per_um2` | Aggregates per square micrometer of tissue |
| `area_fraction_pct` | Percentage of tissue area occupied by aggregate signal |
| `integrated_density` | Sum of background-corrected fluorescence intensity within detected aggregates |
| `integrated_density_per_um2` | Integrated fluorescence normalized to tissue area |
| `mean_puncta_size_um2` | Mean aggregate area in square micrometers |

When a layer mask is available, RAPTOR also reports metrics by retinal layer, including PR, ONL, OPL, INL, IPL, and GCL. The default measurements use a 2D maximum-intensity projection rather than full 3D object tracking.

## Technologies

Python · JupyterLab · NumPy · pandas · SciPy · scikit-image · Matplotlib · Seaborn · BioIO · bioio-czi · tifffile

## Installation

Install [Anaconda or Miniconda](https://www.anaconda.com/download), then create an environment:

```bash
conda create -y -n raptor python=3.12
conda activate raptor
conda install -y -c conda-forge scikit-image scipy numpy pandas matplotlib seaborn tifffile jupyter
pip install --no-binary bioio bioio-czi
```

The commands follow the setup specified in the analysis notebook. Dependency versions are not pinned, and this is not yet a tested reproducible environment lockfile.

## Getting Started

1. Place `book_v7_fixed.ipynb` and `metadata_parser.py` in the same working directory.
2. Put your microscopy images in an accessible data directory.
3. Start JupyterLab with `jupyter lab` and open `book_v7_fixed.ipynb`.
4. In the configuration cell, update `BASE_PATH` and `FILE_NAME` to point to your sample. Check `protein_channel_index` and `area_channel_index` against the actual image channel order.
5. Optionally specify `layer_mask_path` to use a labeled TIFF retinal-layer mask.
6. Run the notebook from top to bottom, inspect the threshold and segmentation previews, and review the computed measurements.
7. If needed, tune the relevant entry in `PROTEIN_CONFIGS` and rerun the dependent cells.

**Important:** The example paths and channel assignments in the notebook are sample-specific. Protein-specific thresholds and size ranges are starting points and must be validated for each imaging dataset.

## Supported Markers and Metadata

The filename parser recognizes APP, tau, phosphorylated tau (p-tau), and α-synuclein (asyn), together with structural markers HuC/D and ZPR3. Its recognized genotypes include `wt` and `appko`. The filename naming convention is required for automatic detection of sample metadata and selection of protein parameters.

Example filename:

```text
36wo_1630_488_magenta_zpr3_647_green_app_wt_inner.czi
```

## Workflow

```text
Confocal Image (.czi / .tif / .tiff)
    -> Load image and parse sample metadata
    -> Extract protein and tissue channels
    -> Background correction and tissue masking
    -> Protein-specific thresholding
    -> Size and local-contrast filtering
    -> Aggregate segmentation
    -> Optional retinal layer assignment
    -> Quantitative metrics and quality-control visualizations
```

## Project Status

RAPTOR is currently a research-oriented Jupyter notebook workflow. The provided code supports interactive analysis and visualization; it is not yet packaged as a command-line application or validated turnkey batch-processing system. The name **Tracking** refers to aggregate profiling across image samples and conditions, not implemented temporal object tracking.

## Research Applications

RAPTOR is designed to support comparisons of protein aggregate burden across retinal regions, layers, ages, genotypes, and experimental conditions. Segmentation outputs should be quality-checked against the source microscopy images before biological interpretation.
