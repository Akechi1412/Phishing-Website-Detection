import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(data_size=50000):
    """
    Loads phishing and legitimate data, assigns labels, splits into train, val, and test sets, 
    and shuffles them.

    Parameters:
    data_size (int): Number of samples to load for each class. Default is 50,000.

    Returns:
    data_train (list): Shuffled training data combining phishing and legitimate samples.
    data_val (list): Shuffled validation data combining both classes.
    data_test (list): Shuffled test data combining both classes.

    Steps:
    1. Load phishing and legitimate data from Parquet files, assign label 1 for phishing, 0 for legitimate.
    2. Split each dataset into train (80%), val (10%), and test (10%).
    3. Combine and shuffle phishing and legitimate data for each split.
    """
    # Load phishing data
    df = pd.read_parquet('data/phishing_data.parquet')
    phishing_data = df.head(data_size).to_dict(orient='records')
    for item in phishing_data:
        item['label'] = 1
 
    # Load legitimate data
    df = pd.read_parquet('data/legitimate_data.parquet')
    legitimate_data = df.head(data_size).to_dict(orient='records')
    for item in legitimate_data:
        item['label'] = 0

    train_size = 0.8
    val_size = 0.1
    test_size = 0.1
    # Split phishing data
    phishing_train, phishing_temp = train_test_split(phishing_data, 
                                                     train_size=train_size, 
                                                     random_state=42)
    phishing_val, phishing_test = train_test_split(phishing_temp, 
                                                   train_size=val_size/(val_size + test_size), 
                                                   random_state=42)
    # Split legitimate data
    legitimate_train, legitimate_temp = train_test_split(legitimate_data, 
                                                     train_size=train_size, 
                                                     random_state=42)
    legitimate_val, legitimate_test = train_test_split(legitimate_temp, 
                                                   train_size=val_size/(val_size + test_size), 
                                                   random_state=42)

    # Mix and Shuffle
    data_train = phishing_train + legitimate_train
    np.random.shuffle(data_train)
    data_val = phishing_val + legitimate_val
    np.random.shuffle(data_val)
    data_test = phishing_test + legitimate_test
    np.random.shuffle(data_test)

    return data_train, data_val, data_test
