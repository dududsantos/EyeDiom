# Em utils.py

import numpy as np

def scale_eye_data(eye_data, image_width_pixels, image_height_pixels,
                   offset_x=0, offset_y=0, scale_x_factor=1.0, scale_y_factor=1.0):
    """
    Escala as coordenadas normalizadas do eyetracker (0-1) para pixels da imagem.

    Args:
        eye_data (np.array): Array NumPy das coordenadas do olho (N, 2), onde N é o número de amostras.
                             As coordenadas são normalizadas (0.0 a 1.0).
        image_width_pixels (int): Largura da imagem em pixels.
        image_height_pixels (int): Altura da imagem em pixels.
        offset_x (float): Deslocamento em pixels na direção X após a escala.
        offset_y (float): Deslocamento em pixels na direção Y após a escala.
        scale_x_factor (float): Fator multiplicador para a escala X (além da largura da imagem).
                                 Útil se a área 0-1 não mapear para 100% da largura da tela.
        scale_y_factor (float): Fator multiplicador para a escala Y (além da altura da imagem).
                                 Útil se a área 0-1 não mapear para 100% da altura da tela.

    Returns:
        np.array: As coordenadas do olho escaladas em pixels.
    """
    scaled_data = np.copy(eye_data) # Cria uma cópia para não modificar o array original

    # Escala com base nas dimensões da imagem e fatores adicionais
    scaled_data[:, 0] = scaled_data[:, 0] * image_width_pixels * scale_x_factor
    scaled_data[:, 1] = scaled_data[:, 1] * image_height_pixels * scale_y_factor

    # Aplica os offsets
    scaled_data[:, 0] += offset_x
    scaled_data[:, 1] += offset_y

    return scaled_data