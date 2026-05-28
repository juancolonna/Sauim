# 🐒 Sauim Detector

`sauim-detector` is a Python command-line tool for bioacoustic processing and automatic detection of Pied tamarin (*Saguinus bicolor*) vocalizations. It uses a pre-trained bird vocalization embedding model and a custom One-Class SVM classifier trained to detect the target species.

Quick tutorial: [Watch on YouTube](https://www.youtube.com/watch?v=avhEqXSRP7U)

## Installation

Create and activate a Python 3.12 environment. This step is recommended to keep dependencies isolated; the environment name can be anything:

```bash
conda create -n sauim python=3.12 pip
conda activate sauim
python -m pip install --upgrade pip
```

Install the released package from PyPI:

```bash
python -m pip install sauim-detector
```

For local development, clone the repository and install the package in editable mode:

```bash
git clone https://github.com/juancolonna/Sauim.git
cd Sauim
python -m pip install -e ./sauim-detector
```

The package requires Python `>=3.12,<3.13`. TensorFlow and TensorFlow Hub compatibility is sensitive to Python and `setuptools` versions, so the project pins `setuptools<82`.

## Usage

Run the detector from the repository root:

```bash
sauim-detector records/Mindu_Saguinus_bicolor_02.02.19-000.wav
```

By default, detections are printed to the terminal in JSON format.

Save detections as an Audacity label file:

```bash
sauim-detector records/Mindu_Saguinus_bicolor_02.02.19-000.wav --save-detections
```

Save the processed audio used by the detector:

```bash
sauim-detector records/Mindu_Saguinus_bicolor_02.02.19-000.wav --save-audio
```

Use both options together:

```bash
sauim-detector records/Mindu_Saguinus_bicolor_02.02.19-000.wav --save-detections --save-audio
```

## Outputs

With `--save-detections`, the CLI writes an Audacity-compatible label file next to the input audio:

```text
start_time    end_time    label
0.00          7.20        Pied tamarin
10.00         15.50       Pied tamarin
20.00         30.80       Pied tamarin
```

These labels can be imported into Audacity with **File > Import > Labels...**.

Without `--save-detections`, the CLI prints JSON detections to stdout. Each detection includes:

- `species`: common name
- `scientific`: scientific name
- `confidence`: One-Class SVM decision score, not a calibrated probability
- `start_time`: detection start time in seconds
- `end_time`: detection end time in seconds

Example:

```json
[
  {
    "species": "Pied tamarin",
    "scientific": "Saguinus bicolor",
    "confidence": 0.003421,
    "start_time": 12.0,
    "end_time": 17.0
  }
]
```

## Notes

- Input files must be `.wav` files.
- Audio is loaded at 32 kHz.
- The classifier only detects the target species, Pied tamarin (*Saguinus bicolor*).
- The `confidence` field is the raw OCSVM decision score. Positive scores are detections; negative scores are rejected before output.
- Labels should be manually validated in Audacity.
