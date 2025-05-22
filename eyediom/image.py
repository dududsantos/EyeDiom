import matplotlib.image as mpimg

def load_image(image_path):
    """
    Load an image from a given path as a NumPy array.
       
    """
    return mpimg.imread(image_path)