from sklearn.model_selection import train_test_split

def split_data(data):
    """
    Splits a dataset into training and testing sets for machine learning.

    This function separates the input features (X) and the target variable (y), where the target 
    column is assumed to be named "Tumor". It then splits the data into training and testing sets 
    using a 75-25% split.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing the dataset, where the "Tumor" column represents the target variable.

    Returns:
    --------
    tuple
        A tuple containing four elements:
        - X_train (pandas.DataFrame): Training set features.
        - X_test (pandas.DataFrame): Testing set features.
        - y_train (pandas.Series): Training set labels.
        - y_test (pandas.Series): Testing set labels.
    """

    X = data.drop(columns=["Tumor"])
    y = data["Tumor"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    return X_train, X_test, y_train, y_test