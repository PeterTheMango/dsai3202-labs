from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def train_models(X_train, y_train):
    """
    Trains multiple machine learning models on the given training dataset.

    This function initializes and trains four different classifiers: 
    - Random Forest
    - Support Vector Classifier (SVC)
    - Logistic Regression
    - Multi-Layer Perceptron (MLP)

    Each model is trained on the provided training features (X_train) and labels (y_train).

    Parameters:
    -----------
    X_train : pandas.DataFrame or numpy.ndarray
        Feature matrix for training.
    
    y_train : pandas.Series or numpy.ndarray
        Target labels for training.

    Returns:
    --------
    dict
        A dictionary containing trained models, where keys are model names and values are the trained model instances.
    """

    models = {
        "RandomForest": RandomForestClassifier(),
        "SVC": SVC(),
        "LogisticRegression": LogisticRegression(),
        "MultiLayerPerceptron": MLPClassifier(max_iter=500)
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
        print(f"{name} has been trained.")

    return models
    
def test_models(model_name, model, X_test, y_test):
    """
    Evaluates a trained machine learning model on the test dataset, prints performance metrics, 
    and writes the results to a file.

    This function makes predictions using the given model and compares them to the true labels 
    (y_test). It calculates and prints key performance metrics:
    - Accuracy
    - Recall
    - F1 Score
    - Classification Report

    The results are also saved to a file named `<model_name>_performance.txt`.

    Parameters:
    -----------
    model_name : str
        The name of the trained model being tested.
    
    model : sklearn.base.ClassifierMixin
        The trained model to be evaluated.
    
    X_test : pandas.DataFrame or numpy.ndarray
        Feature matrix for testing.
    
    y_test : pandas.Series or numpy.ndarray
        True labels for testing.

    Returns:
    --------
    None
        The function prints evaluation metrics and writes them to a file but does not return any value.
    """

    pred = model.predict(X_test)  # Fixed variable name

    accuracy = accuracy_score(y_test, pred)
    recall = recall_score(y_test, pred, average='binary')
    f1 = f1_score(y_test, pred, average='binary')
    report = classification_report(y_test, pred)

    output = (
        f"========== {model_name} Model Performance ==========\n"
        f"Accuracy: {accuracy:.4f}\n"
        f"Recall: {recall:.4f}\n"
        f"F1 Score: {f1:.4f}\n"
        f"\nClassification Report:\n{report}\n"
    )

    file_name = f"{model_name}_performance.txt"
    with open(file_name, "w") as f:
        f.write(output)

    print(f"Performance metrics saved to {file_name}")

