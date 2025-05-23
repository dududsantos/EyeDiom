def scale_eye_data(eye_data, image_shape, offset_y=0):
    """Escala as coordenadas normalizadas para dimensões reais da imagem."""
    eye_data[:, 0] *= image_shape[1]  # Largura
    eye_data[:, 1] *= image_shape[0]  # Altura

    #aplicando offset
    
    eye_data[:, 1] += offset_y

    return eye_data
