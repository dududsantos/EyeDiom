# Em EyeDiom/utils.py (VERSÃO FINAL SIMPLIFICADA)

import numpy as np

def scale_eye_data(eye_data, image_shape, offset_y=0, scale_y_factor=1.0):
   
    scaled_data = np.copy(eye_data) # Cria uma cópia para não modificar o array original

    # Escala a coordenada X apenas com a largura da imagem (assumindo que já está OK)
    # image_shape[1] é a largura da imagem
    scaled_data[:, 0] = scaled_data[:, 0] * image_shape[1]

    # Escala a coordenada Y com a altura da imagem E o fator de escala Y
    # image_shape[0] é a altura da imagem
    scaled_data[:, 1] = scaled_data[:, 1] * image_shape[0] * scale_y_factor

    # Aplica o offset Y
    scaled_data[:, 1] += offset_y

    return scaled_data