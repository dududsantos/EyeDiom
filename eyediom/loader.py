import os

def load_expressions_and_sentences(base_path):
    """
    Carrega as expressões idiomáticas com suas frases e caminhos das imagens.

    Args:
        base_path (str): Caminho base para a pasta 'sentences/', que contém subpastas por expressão.

    Returns:
        Dict[str, Dict[str, List[str]]]: Dicionário com:
            - 'sentences': lista com os textos das frases (derivado do nome do arquivo)
            - 'image_paths': lista com os caminhos absolutos das imagens
    """
    expression_data = {}

    for expression in sorted(os.listdir(base_path)):
        expression_path = os.path.join(base_path, expression)
        if not os.path.isdir(expression_path):
            continue

        sentences = []
        image_paths = []

        for filename in sorted(os.listdir(expression_path)):
            if filename.endswith(".png"):
                sentence_text = os.path.splitext(filename)[0]
                image_path = os.path.join(expression_path, filename)

                sentences.append(sentence_text)
                image_paths.append(image_path)

        if sentences:
            expression_data[expression] = {
                "sentences": sentences,
                "image_paths": image_paths
            }

    return expression_data
