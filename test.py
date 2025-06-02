import sys
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import re
import cv2

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from eyediom.reader import read_file_to_string
from eyediom.image import load_image, find_word_bounding_boxes
from eyediom.eyedata import parse_eyetracking_data
from eyediom.utils import scale_eye_data
from eyediom.visualization import plot_image_with_trajectory
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Caminhos
# image_path = '/data/tela1.png'
# data_path = '/data/coleta_de_dadoscoleta_de_dados_eyetracking_com_tela1_calibrado.txt'

image_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'tela1.png')
data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'coleta_de_dados_eyetracking_com_tela1_calibrado.txt')
# Carregamento
img = load_image(image_path)
data_str = read_file_to_string(data_path)

# Processamento
left_eye, right_eye = parse_eyetracking_data(data_str)

# Normalização
left_eye = scale_eye_data(left_eye, img.shape, offset_x=40, offset_y=40, scale_y_factor = 1.1)
right_eye = scale_eye_data(right_eye, img.shape, offset_x=40, offset_y=40, scale_y_factor=1.1) #offset para descer as trajetórias/ scale para esticar

# Visualização
plot_image_with_trajectory(img, left_eye, right_eye)

# --- 5. Detecção de Palavras e Bounding Boxes ---
# Chamando a nova função find_word_bounding_boxes


detected_words = find_word_bounding_boxes(img) # Passamos o caminho da imagem diretamente para a função.

print("\n--- Palavras Detectadas ---")
if detected_words:
    for word_info in detected_words:
        print(f"Texto: '{word_info['text']}', BBox: {word_info['bbox']}, Confiança: {word_info['confidence']:.2f}")
else:
    print("Nenhuma palavra detectada ou ocorreu um erro na detecção.")


# --- 6. Visualização Aprimorada ---
# Agora, vamos modificar a visualização para incluir as bounding boxes das palavras.

fig, ax = plt.subplots(figsize=(12, 8)) # Ajuste o tamanho da figura para melhor visualização
ax.imshow(img_display) # Use img_display para plotar a imagem

# Desenhar as bounding boxes das palavras
if detected_words:
    for word_info in detected_words:
        x, y, w, h = word_info['bbox']
        # Desenhar o retângulo: (x, y) é o canto superior esquerdo, (x+w, y+h) é o canto inferior direito
        rect = plt.Rectangle((x, y), w, h, linewidth=1, edgecolor='g', facecolor='none', linestyle='--')
        ax.add_patch(rect)
        # Opcional: Adicionar o texto da palavra perto da bounding box
        # ax.text(x, y - 5, word_info['text'], color='g', fontsize=8) # Ajuste a posição do texto se sobrepor

# Plotar as trajetórias dos olhos
ax.plot(left_eye_pixels[:, 0], left_eye_pixels[:, 1], 'b', label='Left Eye', alpha=0.7) # alpha para transparência
ax.plot(right_eye_pixels[:, 0], right_eye_pixels[:, 1], 'r', label='Right Eye', alpha=0.7)

ax.axis('off') # Remover os eixos
ax.legend() # Mostrar a legenda dos olhos

plt.title("Trajetórias do Olhar e Palavras Detectadas")
plt.show()