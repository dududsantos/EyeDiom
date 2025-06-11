# Em EyeDiom/utils.py (VERSÃO FINAL SIMPLIFICADA)

import numpy as np

def scale_eye_data(eye_data, image_shape, offset_x=0,offset_y=0, scale_y_factor=1.0):
   
    scaled_data = np.copy(eye_data) # Cria uma cópia para não modificar o array original

    # Escala a coordenada X apenas com a largura da imagem (assumindo que já está OK)
    # image_shape[1] é a largura da imagem
    scaled_data[:, 0] = scaled_data[:, 0] * image_shape[1]

    # Escala a coordenada Y com a altura da imagem E o fator de escala Y
    # image_shape[0] é a altura da imagem
    scaled_data[:, 1] = scaled_data[:, 1] * image_shape[0] * scale_y_factor

    # Aplica o offset 
    scaled_data[:, 0] += offset_x
    scaled_data[:, 1] += offset_y

    return scaled_data

def map_eye_to_word (gaze_x_pixel, gaze_y_pixel, word_bboxes):
   
   for word_bbox in word_bboxes:
        bbox = word_bbox['bbox']
        word_text = word_bbox['text']
        x_min, y_min, width, height = bbox
        
        x_max = x_min + width
        y_max = y_min + height
        
        # Verifica se o ponto de gaze está dentro do bounding box da palavra
        if x_min <= gaze_x_pixel <= x_max and y_min <= gaze_y_pixel <= y_max:
            # Calcula a posição relativa dentro da palavra (de 0.0 a 1.0)
            if width>0:
                relative_x = (gaze_x_pixel - x_min) / width
            else:
                relative_x = 0.0
                
            return word_text, relative_x
        
        return None, None