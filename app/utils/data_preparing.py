import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from concurrent.futures import ProcessPoolExecutor

def load_data(limit=-1, offset=0, **kwargs):
    """
    Loads phishing and legitimate data from Parquet files, assigns labels, splits into train, validation, 
    and test sets, and shuffles them, with options to limit the data size and set an offset.

    Parameters:
    limit (int): Maximum number of samples to load per class. If -1, loads all samples. Default is -1.
    offset (int): Starting index for data to load per class. Default is 0.
    train_size (float): Proportion of data used for training. Default is 0.8.
    val_size (float): Proportion of data used for validation. Default is 0.1.
    test_size (float): Proportion of data used for testing. Default is 0.1.

    Returns:
    data_train (list): Shuffled training data combining phishing and legitimate samples.
    data_val (list): Shuffled validation data combining both classes.
    data_test (list): Shuffled test data combining both classes.

    Steps:
    1. Load phishing and legitimate data from Parquet files, assign label 1 for phishing, 0 for legitimate.
    2. Apply the limit and offset on the loaded data to control the number of samples per class.
    3. Split each dataset into train (80%), val (10%), and test (10%).
    4. Combine and shuffle phishing and legitimate data for each split.
    """
    # Split sizes
    train_size = kwargs.get('train_size', 0.8)
    val_size = kwargs.get('val_size', 0.1)
    test_size = kwargs.get('test_size', 0.1)
    if train_size + val_size + test_size != 1:
        raise ValueError("The sum of train_size, val_size, and test_size must equal 1.")

    # Load and label phishing data
    df_phishing = pd.read_parquet('data/phishing_data.parquet')
    df_phishing['label'] = 1
    phishing_data = df_phishing.iloc[offset: offset + limit if limit > 0 else None].to_dict(orient='records')

    # Load label legitimate data
    df_legitimate = pd.read_parquet('data/legitimate_data.parquet')
    df_legitimate['label'] = 0
    legitimate_data = df_legitimate.iloc[offset: offset + limit if limit > 0 else None].to_dict(orient='records')

    # Split phishing data
    phishing_train, phishing_temp = train_test_split(phishing_data, 
                                                     train_size=train_size, 
                                                     random_state=42)
    phishing_val, phishing_test = train_test_split(phishing_temp, 
                                                   train_size=val_size/(val_size+test_size),  
                                                   random_state=42)
    # Split legitimate data
    legitimate_train, legitimate_temp = train_test_split(legitimate_data, 
                                                         train_size=train_size, 
                                                         random_state=42)
    legitimate_val, legitimate_test = train_test_split(legitimate_temp, 
                                                       train_size=val_size/(val_size+test_size), 
                                                       random_state=42)

    # Combine and shuffle
    data_train = phishing_train + legitimate_train
    np.random.shuffle(data_train)
    data_val = phishing_val + legitimate_val
    np.random.shuffle(data_val)
    data_test = phishing_test + legitimate_test
    np.random.shuffle(data_test)

    return data_train, data_val, data_test
