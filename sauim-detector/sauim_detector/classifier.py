import numpy as np
from tqdm import tqdm

def classify_signal(y, sr, model, clf):
    """
    Classificador com checagem de sobreposição:
    se a nova janela começa dentro da última, apenas estende.
    """
    segmentation = np.zeros(len(y))
    detections = []
    prev_state = 0  # estado anterior (0=sem sinal, 1=com sinal)

    for i in tqdm(range(0, len(y) - 5*sr, sr)):
        frame = y[i:i+5*sr]
        model_outputs = model.infer_tf(frame[np.newaxis, :])
        decision_score = clf.decision_function(model_outputs['embedding'])
        current_state = 1 if decision_score >= 0.0 else 0

        if current_state == 1:
            start = i / sr
            end = (i + 5*sr) / sr
            segmentation[i:i+5*sr] = 1

            if prev_state == 0:
                if detections and start <= detections[-1][1]:
                    # Início dentro da última → só estende
                    detections[-1][1] = end
                else:
                    # Abre uma nova detecção
                    detections.append([start, end, "sauim"])
            else:
                # Atualiza o tempo final da última detecção
                detections[-1][1] = end
                
        prev_state = current_state

    return [tuple(d) for d in detections]
