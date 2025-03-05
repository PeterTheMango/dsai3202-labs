# DSAI3202 - Lab 4, Part 2
## Objectives
- Load the MRI images using OpenCV.
- Implement parallel processing to efficiently handle image processing and model training.
- Train a machine learning model for brain tumor classification.
- Evaluate the performance of your model on a test set.

### Tasks:
- **Parallel execution:**
        1. Create a separate function for each filter and write to be executed in parallel using either multiprocessing or multithreading.
        ![filters](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxwxlviIb3cMrX6sYKmFaeqh0cNWP8pG9VdBvlj)
        2. Use a multiprocessing or multithreading (*whatever you wish, from what you have learned in this course*) to manage parallel execution of the filter functions on the images and or the concurrent application on multiple images at the same time.
        ![multiprocessing approach](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxw98EJ9hMdDvhl5AEZpe0Wkox3KJ4YHOrIwG2f)
        3. Implement synchronization mechanisms to ensure safe access to shared resources.
	 - Using apply_async().get() so that it wont move on until the image are done. Also using as_completed() to ensure that the process is done handling the image before moving onto the next.
        ![Sync](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxwrIPr6LBiwnCOvcAKsW9MaXTu4dhYxQlqobNj)
5. Measure the execution time of the parallel processing to compare it with the sequential execution.
        ![execution_time](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxwsoHHXG8EOclQUXAvGw7KiYZCfrpL0oSW36n9)
### Questions:
- Explain you parallelization?
	- Using multiprocessing Pools for running the parallel execution of the process_images_parallel in order for one process is running for the YES images and one for the NO images.
	- Using ThreadPoolExecutors and futures, we are able to separate each filter into their own thread and the filter will wait for the first filter to finish before moving on with the same image but can run on a new image.
- Analyze the speedup and efficiency of the parallel execution. Discuss the results and any trade-offs encountered.
	-	Speedup: 5.51x
	-	Efficiency: 0.92
	-	Trade-Offs: The more resources we use in terms of threading and multiprocessing, the more overhead we get. So I had to balnce between the use of multithreading and multiprocessing in terms of number of processes and threads made.

### Machine Learning Results

        ========== LogisticRegression Model Performance ==========
    Accuracy: 0.6977
    Recall: 0.7500
    F1 Score: 0.6977
    
    Classification Report:
                  precision    recall  f1-score   support
    
               0       0.75      0.65      0.70        23
               1       0.65      0.75      0.70        20
    
        accuracy                           0.70        43
       macro avg       0.70      0.70      0.70        43
    weighted avg       0.70      0.70      0.70        43

    ========== MultiLayerPerceptron Model Performance ==========
    Accuracy: 0.5581
    Recall: 0.3000
    F1 Score: 0.3871
    
    Classification Report:
                  precision    recall  f1-score   support
    
               0       0.56      0.78      0.65        23
               1       0.55      0.30      0.39        20
    
        accuracy                           0.56        43
       macro avg       0.55      0.54      0.52        43
    weighted avg       0.55      0.56      0.53        43

    ========== RandomForest Model Performance ==========
    Accuracy: 0.7209
    Recall: 0.6500
    F1 Score: 0.6842
    
    Classification Report:
                  precision    recall  f1-score   support
    
               0       0.72      0.78      0.75        23
               1       0.72      0.65      0.68        20
    
        accuracy                           0.72        43
       macro avg       0.72      0.72      0.72        43
    weighted avg       0.72      0.72      0.72        43

    ========== SVC Model Performance ==========
    Accuracy: 0.6744
    Recall: 0.8500
    F1 Score: 0.7083
    
    Classification Report:
                  precision    recall  f1-score   support
    
               0       0.80      0.52      0.63        23
               1       0.61      0.85      0.71        20
    
        accuracy                           0.67        43
       macro avg       0.70      0.69      0.67        43
    weighted avg       0.71      0.67      0.67        43


### Acknowledgements

> ChatGPT 4o (AI) helped me in creating the docstrings for each of the functions and other ways to improve the multiprocessing.


