import matplotlib.image as mpimg
import cv2
import pytesseract
import numpy as np

def load_image(image_path):
  
    return mpimg.imread(image_path)
def prepare_image_for_cv(img_array):
    """
    Prepares a NumPy image array for OpenCV/Tesseract processing.
    Ensures image is uint8 (0-255) and removes alpha channel if present.

    Args:
        img_array (np.array): Input image as a NumPy array.

    Returns:
        np.array: Prepared image array in uint8 format (0-255), without alpha channel.
                  Returns None if input is invalid or an error occurs during preparation.
    """
    if not isinstance(img_array, np.ndarray):
        print(f"Erro: Entrada inválida para prepare_image_for_cv. Esperado np.ndarray, recebido {type(img_array)}")
        return None

    img_prepared = img_array.copy() # Trabalhe em uma cópia para não modificar o original

    # 1. Converter para uint8 (0-255) se não for já.
    if img_prepared.dtype != np.uint8:
        if np.max(img_prepared) <= 1.0 and np.min(img_prepared) >= 0.0: # Se os valores estão normalizados para 0-1
             img_prepared = (img_prepared * 255).astype(np.uint8)
        else: # Se os valores já estão entre 0-255 (mas em outro dtype, como float), apenas converte
            img_prepared = img_prepared.astype(np.uint8)

    # 2. Remover o canal alfa se presente (se a imagem tiver 4 canais)
    if img_prepared.ndim == 3 and img_prepared.shape[2] == 4:
        img_prepared = img_prepared[:, :, :3] # Remove o canal alfa

    return img_prepared



def find_word_bounding_boxes(image):
    
    img_to_process = None
    
    if isinstance(image, str):
        img_to_process = cv2.imread(image)
    
        if img_to_process is None:
            print("Invalid image path or image data.")
            return []
    
    elif isinstance(image, np.ndarray):
        img_to_process = image
   
    else: #tratar caso seja rgba / tirar um canal
       print("Unsupported image format. Please provide a valid image path or a NumPy array.")
       return []
            
     # Salvar a resolução original da imagem antes de qualquer redimensionamento para OCR
    original_height, original_width = img_to_process.shape[0], img_to_process.shape[1]
    
    img_prepared= prepare_image_for_cv(img_to_process)
    if img_prepared is None:
        print("Erro ao preparar a imagem para processamento.")
        return []
    
    # --- NOVO: Redimensionar a imagem para o Tesseract (para performance do OCR) ---
    # As bounding boxes retornadas pelo Tesseract serão em relação a esta imagem REDIMENSIONADA.
    scale_percent_for_ocr = 50 # Reduz para 50% do tamanho original. Ajuste este valor (e.g., 25, 75).
    width_for_ocr = int(img_prepared.shape[1] * scale_percent_for_ocr / 100)
    height_for_ocr = int(img_prepared.shape[0] * scale_percent_for_ocr / 100)
    dim_for_ocr = (width_for_ocr, height_for_ocr)
    
    img_for_ocr = cv2.resize(img_prepared, dim_for_ocr, interpolation = cv2.INTER_AREA)
    
    #Converter para escala de cinza p/ melhorar o OCR
   
    if img_for_ocr.ndim == 3 and img_for_ocr.shape[2] == 3:
   
        gray = cv2.cvtColor(img_for_ocr, cv2.COLOR_BGR2GRAY)
    else:
        gray = img_for_ocr # Já é escala de cinza ou 2D
        
    #Usar o tesseract para obter os boxes
    # config='--psm 6' é um Page Segmentation Mode comum para uma única linha uniforme de texto.
    # Outros PSMs podem ser explorados dependendo da sua imagem (e.g., --psm 3 para página padrão)
    print("INFO: Iniciando processamento OCR com Tesseract...")
    
    try:
        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, config='--psm 6')
    except pytesseract.TesseractError as e:
        print(f"Error during OCR processing: {e}")
        return []
    
    word_bboxes = []
    n_boxes = len(data['level']) #numero de itens detectados 
    
    for i in range(n_boxes):
         # Level 5 geralmente corresponde a palavras.
        # data['text'][i].strip() garante que o texto não é vazio após remover espaços em branco.
        # data['conf'][i] > 0 garante que a confiança de detecção é positiva (não -1 para linhas vazias)
        if data['level'][i] == 5 and  data['text'][i].strip() and float(data['conf'][i]) > 0:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            word_text = data['text'][i].strip()
            confidence = float(data['conf'][i])

            word_bboxes.append({
                'text': word_text,
                'bbox': (x, y, w, h), # (x_min, y_min, width, height)
                'confidence': confidence # Pode ser útil para depuração ou filtragem futura
            })
    return word_bboxes