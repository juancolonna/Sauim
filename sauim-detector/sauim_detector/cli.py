import argparse
import os
from .loader import load_audio
from .classifier import classify_signal
from joblib import load
import soundfile as sf
import tensorflow as tf
import tensorflow_hub as hub
import json

tf.experimental.numpy.experimental_enable_numpy_behavior()

# Load the pre-trained embedding model
model = hub.load('https://www.kaggle.com/models/google/bird-vocalization-classifier/TensorFlow2/bird-vocalization-classifier/8')

# Load the OCSVM classifier from package data
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "ocsvm_sauim.joblib")
clf = load(MODEL_PATH)

def main():
    """
    Command-line interface for bioacoustic processing and
    Pied tamarin (Saguinus bicolor) vocalization detection.
    - Loads an audio file
    - Runs feature extraction + classification (OCSVM)
    - Saves detection labels in Audacity format
    - Optionally saves filtered audio as .wav
    """
    parser = argparse.ArgumentParser(description="Bioacoustic audio processing and Pied tamarin classification.")
    parser.add_argument("filepath", help="Path to input .wav file")
    parser.add_argument("--save-audio", action="store_true",
                        help="If set, saves the filtered audio as a .wav file.")
    parser.add_argument("--save-detections", action="store_true",
                        help="If set, saves the detection labels in Audacity format.")
    args = parser.parse_args()

    sr = 32000  # Target sampling rate
    y, sr = load_audio(args.filepath, sr=sr)
    detections = classify_signal(y, sr, model, clf)
    print(f"Total detections: {len(detections)}")
    base, _ = os.path.splitext(args.filepath)

    # Save detection labels to a text file (Audacity label format)
    if args.save_detections:
        output_file = base + "_detections.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            for det in detections:
                f.write(
                    f"{det['start_time']:.2f}\t"
                    f"{det['end_time']:.2f}\t"
                    f"{det['species']}\n"
                )
        print(f"✅ Labels saved as: {output_file}")
    else:
        # Output predictions as JSON to stdout (read by the VAMP plugin via popen)
        print(json.dumps(detections), flush=True)

    # Save filtered audio if the flag is set
    if args.save_audio:
        filtered_file = base + "_filtered.wav"
        sf.write(filtered_file, y, sr)
        print(f"✅ Filtered signal saved as: {filtered_file}")


if __name__ == "__main__":
    main()
