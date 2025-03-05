import time
from tqdm import tqdm
from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt

def process_images(images):
    processed_images = []
    for image in tqdm(images):
        filtered_images = {
            'Original': image,
            'Entropy': entropy(image, disk(2)),
            'Gaussian': nd.gaussian_filter(image, sigma=1),
            'Sobel': sobel(image),
            'Gabor': gabor(image, frequency=0.9)[1],
            'Hessian': hessian(image, sigmas=range(1, 100, 1)),
            'Prewitt': prewitt(image)
        }
        processed_images.append(filtered_images)
    return processed_images

def run_sequential(yes_images, no_images):
    """
    Processes two sets of images sequentially using various image filtering techniques and measures execution time.

    This function applies multiple image processing filters (entropy, Gaussian, Sobel, Gabor, Hessian, and Prewitt) 
    to each image in the `yes_images` and `no_images` lists using the `process_images` function. The processing 
    is done sequentially, and the total execution time is recorded.

    Parameters:
    -----------
    yes_images : list of ndarray
        A list of images (NumPy arrays) that belong to the "yes" category.
    
    no_images : list of ndarray
        A list of images (NumPy arrays) that belong to the "no" category.

    Returns:
    --------
    float
        The total execution time (in seconds) taken to process both image sets.
    """
    
    start_time = time.time()
    yes_inputs = process_images(yes_images)
    no_inputs = process_images(no_images)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time