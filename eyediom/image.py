import matplotlib.image as mpimg
import cv2
import pytesseract

def load_image(image_path):
    """
    Load an image from a given path as a NumPy array.
       
    """
    return mpimg.imread(image_path)

#Detecta a palavra na imagem e retorna seu bounding box e txto
def find_word_bounding_boxes(image_path):
    
    if isinstance(image_path, str):
        img = cv2.imread(image_path)
    
    if img is None:
        print("Invalid image path or image data.")
        return []
    
    else: #tratar caso seja rgba / tirar um canal
        if image_path.ndim ==3 and image_path.shape[2] == 4:
            img = image_path[:, :, :3]  # Remove alpha channel if present
        else:
            img = image_path
            
            
    #Converter para escala de cinza p/ melhorar o OCR
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
        
    #Usar o tesseract para obter os boxes
     # output_type=Output.DICT retorna um dicionário com info detalhada (texto, bbox, conf, etc.)
    # config='--psm 6' é um Page Segmentation Mode comum para uma única linha uniforme de texto.
    # Outros PSMs podem ser explorados dependendo da sua imagem (e.g., --psm 3 para página padrão)
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