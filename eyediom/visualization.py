import matplotlib.pyplot as plt

def plot_image_with_trajectory(img, left_eye, right_eye):
    """Plota a imagem com as trajetórias dos olhos sobrepostas."""
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, img.shape[1], img.shape[0], 0])

    
    ax.plot(left_eye[:,0], left_eye[:,1], 'b', label='Left Eye')
    ax.plot(right_eye[:,0], right_eye[:,1], 'r', label='Right Eye')
    
    ax.axis('off')
    plt.legend()
    plt.show()
