import numpy as np

def merge_detections(detections):
    """
    Merge consecutive or overlapping sauim detections.

    Args:
        detections : List of detection dicts.

    Returns:
        List of merged detection dicts.
    """
    if not detections:
        return []

    # The OCSVM only detects the target class (sauim), so merging is based on
    # time only. Use a sorted copy to avoid mutating the caller's list.
    detections = sorted(detections, key=lambda d: d["start_time"])

    merged = []
    current = dict(detections[0])
    current["_conf_sum"]     = current["confidence"]
    current["_conf_count"]   = 1

    for det in detections[1:]:
        overlapping  = det["start_time"] <= current["end_time"]

        if overlapping:
            # Extend current segment and accumulate confidence
            current["end_time"]     = max(current["end_time"], det["end_time"])
            current["_conf_sum"]   += det["confidence"]
            current["_conf_count"] += 1
        else:
            # Finalise current segment and start a new one
            current["confidence"] = round(current["_conf_sum"] / current["_conf_count"], 4)
            del current["_conf_sum"], current["_conf_count"]
            merged.append(current)
            current = dict(det)
            current["_conf_sum"]   = det["confidence"]
            current["_conf_count"] = 1

    # Finalise last segment
    current["confidence"] = round(current["_conf_sum"] / current["_conf_count"], 4)
    del current["_conf_sum"], current["_conf_count"]
    merged.append(current)

    return merged

def classify_signal(y, sr, model, clf):
    """
    Classify an audio signal into presence/absence of target events
    (e.g., tamarin vocalizations) using embeddings + OCSVM, 
    and merge overlapping windows into continuous detections.

    Steps:
    1. Slide a 5-second window across the signal with a hop of 1 second.
    2. Extract embeddings from the pre-trained model.
    3. Apply the OCSVM classifier to get a decision score.
    4. If score >= 0, mark as detection.
    5. Merge overlapping or consecutive detections:
       - If the new window starts inside the previous one, extend it.
       - Otherwise, open a new detection segment.

    Args:
        y (np.ndarray): input waveform
        sr (int): sampling rate
        model: embedding model with an `infer_tf` method
        clf: OCSVM classifier with `decision_function`

    Returns:
        list of detection dicts
    """

    detections = []

    for i in range(0, len(y) - 5*sr + 1, sr):
        frame = y[i:i+5*sr]

        # Feature extraction and classification
        model_outputs = model.infer_tf(frame[np.newaxis, :])
        decision_score = float(clf.decision_function(model_outputs['embedding'])[0])

        if decision_score >= 0.0:
            start = i / sr
            end = (i + 5*sr) / sr
            detections.append({
                "species":    "Pied tamarin",
                "scientific": "Saguinus bicolor",
                "confidence": round(decision_score, 6),
                "start_time": float(start),
                "end_time":   float(end)
            })

    # Merge consecutive/overlapping sauim detections
    detections = merge_detections(detections)

    return detections
