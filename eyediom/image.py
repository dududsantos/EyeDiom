import matplotlib.image as mpimg
import cv2
import pytesseract
import numpy as np

def load_image(image_path):
    """
    Load an image from a given path as a NumPy array.
       
    """
    return mpimg.imread(image_path)

#Detecta a palavra na imagem e retorna seu bounding box e txto
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
            
            
    if img_to_process.dtype != np.uint8:
        # Primeiro, garantir que está na escala de 0-1 antes de multiplicar por 255
        # Alguns dtypes float já podem vir de 0-255, mas a maioria virá de 0-1.
        # Para ser seguro, reescalamos antes da conversão para uint8
        if np.max(img_to_process) <= 1.0: # Se os valores estão normalizados para 0-1
             img_to_process = (img_to_process * 255).astype(np.uint8)
        else: # Se os valores já estão entre 0-255 (mas não são uint8)
            img_to_process = img_to_process.astype(np.uint8)
            
    #Converter para escala de cinza p/ melhorar o OCR
   
    if img_to_process.ndim ==3 and img_to_process.shape[2] == 4:
        img_to_process = img_to_process[:, :, :3]  # Remove alpha channel if present
    
    if img_to_process.ndim == 3 and img_to_process.shape[2] == 3: # Verifica se é uma imagem colorida (3 
        gray = cv2.cvtColor(img_to_process, cv2.COLOR_BGR2GRAY) 
    else:
        gray = img_to_process
        
    #Usar o tesseract para obter os boxes
     # output_type=Output.DICT retorna um dicionário com info detalhada (texto, bbox, conf, etc.)
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