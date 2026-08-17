# Bioacoustic records of Saguinus bicolor

Dataset of field audio recordings used for training, testing and evaluation of automatic detection of Saguinus bicolor (sauim) calls.

## Contents

- Training / reference recordings:
	- `Sauim.wav` — Records from Bosque da Ciência (training/testing).
	- `Sauim_filtered.wav` — Same training records, band-pass filtered.

- Mindu (Parque do Mindú) recordings used for event detection:
	- `Mindu_Saguinus_bicolor_02.02.19-000.wav` — Full field recording (section 6 of article).
	- `Mindu_Saguinus_bicolor_02.02.19-000_filtered.wav` — Band-pass filtered version.
	- `Mindu_Saguinus_bicolor_02.02.19-000_detections.txt` — Manual temporal annotations (boundaries / detections).

- Mindu sections / collections:
	- `Parque_do_Mindu.zip` — Mindu records with sauim calls (section 7).
	- `Parque_do_Mindu_without_Sauim.zip` — Mindu records without sauim calls.

- Negative-class recordings (ambient / non-sauim):
	- `Anthrophony.wav`
	- `Anurans.wav`
	- `Background.wav`
	- `Birds.wav`
	- `Geophony.wav`

- Filtered negative-class recordings:
	- `Anthrophony_filtered.wav`
	- `Anurans_filtered.wav`
	- `Background_filtered.wav`
	- `Birds_filtered.wav`
	- `Geophony_filtered.wav`

## Usage

- For training use `Sauim.wav` (or `Sauim_filtered.wav` to use pre-filtered data).
- For evaluation of event detection, use the Mindu recording and `*_detections.txt` as reference annotations.