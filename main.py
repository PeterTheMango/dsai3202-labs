import glob
import multiprocessing
from src.functions import read_images
from src.sequential import run_sequential
from src.parallel import run_parallel
from src.features import extract_feature
from src.splitting import split_data
from src.train_test import train_models, test_models
# Define the path to the dataset
dataset_path = 'data/brain_tumor_dataset/'

# List all image files in the 'yes' and 'no' directories
yes_images = glob.glob(dataset_path + 'yes/*.jpg')
no_images = glob.glob(dataset_path + 'no/*.jpg')

yes_images = read_images(yes_images)
no_images = read_images(no_images)

print(f"Number of 'yes' images: {len(yes_images)}")
print(f"Number of 'no' images: {len(no_images)}")

# Sequential Running
#seq_time = run_sequential(yes_images, no_images)
seq_time = 8253.132199048996
print(f"Sequential Running: {seq_time}s")

# Parallel 
par_time, yes_inputs, no_inputs = run_parallel(yes_images, no_images)
print(f"Parallel Running: {par_time}")

num_cpu = multiprocessing.cpu_count() 
speedup = seq_time / par_time
efficiency = speedup / num_cpu

print(f"Speedup: {speedup:.2f}x")
print(f"Efficiency: {efficiency:.2f}")

data, running_time = extract_feature(yes_inputs, no_inputs)
X_train, X_test, y_train, y_test = split_data(data)

models = train_models(X_train, y_train)

for name, model in models.items():
    test_models(name, model, X_test, y_test)

