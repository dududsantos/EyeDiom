import os
from .image import load_image, find_word_bounding_boxes

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

        phrases_in_expression = []
        
        for filename in sorted(os.listdir(expression_path)):
            if filename.endswith(".png"):
                sentence_text = os.path.splitext(filename)[0]
                image_path = os.path.join(expression_path, filename)
                
                word_bboxes = find_word_bounding_boxes(image_path)

                phrases_in_expression.append({
                "sentences": sentence_text,
                "image_paths": image_path,
                "word_bboxes": word_bboxes
            })

        if phrases_in_expression:
            expression_data[expression] = phrases_in_expression
    
    return expression_data
