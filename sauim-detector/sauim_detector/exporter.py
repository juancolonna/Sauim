def save_audacity_labels(labels, filename="labels.txt"):
    """
    Salva um arquivo de labels no formato compatível com o Audacity.

    Args:
        labels (list of tuples): lista [(start, end, text), ...]
            - start (float): tempo inicial em segundos
            - end (float): tempo final em segundos (igual ao start se for ponto)
            - text (str): rótulo associado
        filename (str): caminho do arquivo de saída (.txt)
    """
    with open(filename, "w", encoding="utf-8") as f:
        for start, end, text in labels:
            f.write(f"{start:.6f}\t{end:.6f}\t{text}\n")