# Em EyeDiom/utils.py (VERSÃO SIMPLIFICADA)

import numpy as np

def scale_eye_data(eye_data, image_shape, offset_y=0, scale_y_factor=1.0):
    """
    Escala as coordenadas normalizadas do eyetracker (0-1) para pixels da imagem,
    com ajuste de offset e fator de escala apenas para o eixo Y.

    Args:
        eye_data (np.array): Array NumPy das coordenadas do olho (N, 2), onde N é o número de amostras.
                             As coordenadas são normalizadas (0.0 a 1.0).
        image_shape (tuple): Tupla (altura, largura) da imagem em pixels.
        offset_y (float): Deslocamento em pixels na direção Y após a escala.
        scale_y_factor (float): Fator multiplicador para a escala Y.
                                 Ajuste para esticar/encolher verticalmente.

    Returns:
        np.array: As coordenadas do olho escaladas em pixels.
    """
    scaled_data = np.copy(eye_data) # Cria uma cópia para não modificar o array original

    # Escala a coordenada X apenas com a largura da imagem (sem fator de escala X)
    # image_shape[1] é a largura da imagem
    scaled_data[:, 0] = scaled_data[:, 0] * image_shape[1]

    # Escala a coordenada Y com a altura da imagem E o fator de escala Y
    # image_shape[0] é a altura da imagem
    scaled_data[:, 1] = scaled_data[:, 1] * image_shape[0] * scale_y_factor

    # Aplica os offsets
    # offset_x foi removido, aplica apenas offset_y
    scaled_data[:, 1] += offset_y

    return scaled_data