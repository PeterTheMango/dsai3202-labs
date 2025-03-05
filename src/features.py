import numpy as np
import pandas as pd
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from skimage import feature

def compute_glcm_features(image, filter_name):
    """
    Compute Gray-Level Co-occurrence Matrix (GLCM) features for a given image.
    
    Parameters:
        image (numpy.ndarray): The input grayscale image.
        filter_name (str): The name of the filter applied to the image.
    
    Returns:
        dict: A dictionary containing GLCM feature values with keys formatted as '{filter_name}_{feature}_{index}'.
    """
    image = (image * 255).astype(np.uint8)
    graycom = feature.graycomatrix(image, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
    
    features = {}
    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
        values = feature.graycoprops(graycom, prop).flatten()
        for i, value in enumerate(values):
            features[f'{filter_name}_{prop}_{i+1}'] = value
    return features

def process_single_image(filtered_images, tumor_presence):
    """
    Process a single image by computing GLCM features for each filtered version of the image.
    
    Parameters:
        filtered_images (dict): A dictionary of filtered images where keys are filter names and values are images.
        tumor_presence (int): Label indicating tumor presence (1 for tumor, 0 for no tumor).
    
    Returns:
        dict: A dictionary containing GLCM features along with the tumor presence label.
    """
    glcm_features = {}
    for key, image in filtered_images.items():
        glcm_features.update(compute_glcm_features(image, key))
    glcm_features['Tumor'] = tumor_presence
    return glcm_features

def process_images_parallel(images_list, tumor_presence):
    """
    Process multiple images in parallel using multiprocessing to compute GLCM features.
    
    Parameters:
        images_list (list): A list of dictionaries where each dictionary contains filtered images.
        tumor_presence (int): Label indicating tumor presence (1 for tumor, 0 for no tumor).
    
    Returns:
        list: A list of dictionaries containing GLCM features for each processed image.
    """
    num_cores = multiprocessing.cpu_count()
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        results = list(executor.map(process_single_image, images_list, [tumor_presence] * len(images_list)))
    return results

def extract_feature(yes_inputs, no_inputs):
    """
    Extract GLCM features from both tumor-present and tumor-absent image datasets.
    
    Parameters:
        yes_inputs (list): A list of dictionaries containing filtered images with tumors.
        no_inputs (list): A list of dictionaries containing filtered images without tumors.
    
    Returns:
        tuple: A tuple containing a shuffled pandas DataFrame with extracted features and the execution time.
    """
    start_time = time.time()

    yes_glcm_features = process_images_parallel(yes_inputs, 1)
    no_glcm_features = process_images_parallel(no_inputs, 0)
    
    all_glcm_features = yes_glcm_features + no_glcm_features
    
    dataframe = pd.DataFrame(all_glcm_features)
    
    shuffled_dataframe = dataframe.sample(frac=1).reset_index(drop=True)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return (shuffled_dataframe, execution_time)
