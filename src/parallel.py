import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt

# Individual filter functions
def apply_entropy(image):
    """
    Apply entropy filter to the input image.
    
    Parameters:
        image (numpy.ndarray): Input grayscale image.
    
    Returns:
        numpy.ndarray: Image after applying entropy filter.
    """
    return entropy(image, disk(2))

def apply_gaussian(image):
    """
    Apply Gaussian filter to the input image.
    
    Parameters:
        image (numpy.ndarray): Input grayscale image.
    
    Returns:
        numpy.ndarray: Image after applying Gaussian filter.
    """
    return nd.gaussian_filter(image, sigma=1)

def apply_sobel(image):
    """
    Apply Sobel filter to detect edges in the image.
    
    Parameters:
        image (numpy.ndarray): Input grayscale image.
    
    Returns:
        numpy.ndarray: Image after applying Sobel filter.
    """
    return sobel(image)

def apply_gabor(image):
    """
    Apply Gabor filter to the input image.
    
    Parameters:
        image (numpy.ndarray): Input grayscale image.
    
    Returns:
        numpy.ndarray: Image after applying Gabor filter.
    """
    return gabor(image, frequency=0.9)[1]

def apply_hessian(image):
    """
    Apply Hessian filter to detect blob-like structures in the image.
    
    Parameters:
        image (numpy.ndarray): Input grayscale image.
    
    Returns:
        numpy.ndarray: Image after applying Hessian filter.
    """
    return hessian(image, sigmas=range(1, 100, 1))

def apply_prewitt(image):
    """
    Apply Prewitt filter to detect edges in the image.
    
    Parameters:
        image (numpy.ndarray): Input grayscale image.
    
    Returns:
        numpy.ndarray: Image after applying Prewitt filter.
    """
    return prewitt(image)

def process_image(image):
    """
    Apply multiple image filters concurrently using threading.
    
    Parameters:
        image (numpy.ndarray): Input grayscale image.
    
    Returns:
        dict: Dictionary containing the filtered images with filter names as keys.
    """
    filters = [
        ("Entropy", apply_entropy),
        ("Gaussian", apply_gaussian),
        ("Sobel", apply_sobel),
        ("Gabor", apply_gabor),
        ("Hessian", apply_hessian),
        ("Prewitt", apply_prewitt)
    ]
    
    results = {}
    with ThreadPoolExecutor(max_workers=len(filters)) as executor:
        future_to_filter = {executor.submit(func, image): name for name, func in filters}
        for future in as_completed(future_to_filter):
            filter_name = future_to_filter[future]
            try:
                results[filter_name] = future.result()
            except Exception as exc:
                results[filter_name] = None
    results["Original"] = image
    return results

def process_images_parallel(images, pos=0):
    """
    Process a list of images concurrently using threading with progress tracking.
    
    Parameters:
        images (list): List of images to be processed.
        pos (int, optional): Position of the tqdm progress bar.
    
    Returns:
        list: List of dictionaries containing filtered images.
    """
    with ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
        processed_images = list(tqdm(
            executor.map(process_image, images),
            total=len(images),
            position=pos,
            leave=True,
            ncols=80,
            desc=f"Type {pos} Images"
        ))
    return processed_images

def run_parallel(yes_images, no_images, batch_size=10):
    """
    Process images in parallel using multiprocessing.
    
    Parameters:
        yes_images (list): List of images containing tumors.
        no_images (list): List of images without tumors.
        batch_size (int, optional): Size of image batches to process (default is 10).
    
    Returns:
        tuple: A tuple containing execution time, processed images with tumors, and processed images without tumors.
    """
    start_time = time.time()
    
    with mp.Pool(processes=2) as pool:
        async_yes = pool.apply_async(process_images_parallel, args=(yes_images, 0))
        async_no = pool.apply_async(process_images_parallel, args=(no_images, 1))
        
        yes_inputs = async_yes.get()
        no_inputs = async_no.get()
    
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time, yes_inputs, no_inputs
