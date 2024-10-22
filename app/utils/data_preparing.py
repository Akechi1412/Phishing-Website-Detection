import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from utils.data_preprocessing import parse_html
import warnings
from concurrent.futures import ProcessPoolExecutor

def is_valid_html(html_document):
    """
    Checks if the HTML content is valid by parsing it and checking for warnings.
    
    Parameters:
    html_document (str): The HTML document to parse.
    
    Returns:
    bool: True if the HTML is valid (no warnings), False otherwise.
    """
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        parse_html(html_document)
        if len(w) > 0:
            return False
    return True

def validate_and_label(item, label):
    """
    Validates and labels a single HTML data record.

    Parameters:
    item (dict): The data record to validate.
    label (int): The label to assign if the record is valid.

    Returns:
    dict or None: The labeled record if valid, or None if invalid.
    """
    if is_valid_html(item['html']):
        item['label'] = label
        return item
    return None

def filter_valid_data(data, label, data_size):
    """
    Filters and labels valid data using multiprocessing for speed.

    Parameters:
    data (list): The dataset to filter.
    label (int): The label to assign to each valid record.
    data_size (int): The number of valid records to retrieve.

    Returns:
    list: A list of valid, labeled records up to the data_size limit.
    """
    valid_data = []

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(validate_and_label, data, [label] * len(data)))

    valid_data = [item for item in results if item is not None][:data_size]
    
    return valid_data

def load_data(data_size, train_size=0.8, val_size=0.1, test_size=0.1):
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
    if train_size + val_size + test_size != 1:
        raise ValueError("The sum of train_size, val_size, and test_size must equal 1.")

    # Load and filter phishing data
    df = pd.read_parquet('data/phishing_data.parquet')
    phishing_data = df.to_dict(orient='records')
    phishing_valid_data = filter_valid_data(phishing_data, label=1, data_size=data_size)
    
    # Load and filter legitimate data
    df = pd.read_parquet('data/legitimate_data.parquet')
    legitimate_data = df.to_dict(orient='records')
    legitimate_valid_data = filter_valid_data(legitimate_data, label=0, data_size=data_size)

    # Ensure both datasets are large enough
    if len(phishing_valid_data) < data_size or len(legitimate_valid_data) < data_size:
        raise ValueError("Not enough valid data found.")

    # Split phishing data
    phishing_train, phishing_temp = train_test_split(phishing_valid_data, 
                                                     train_size=train_size, 
                                                     random_state=42)
    phishing_val, phishing_test = train_test_split(phishing_temp, 
                                                   train_size=val_size/(val_size+test_size),  
                                                   random_state=42)
    # Split legitimate data
    legitimate_train, legitimate_temp = train_test_split(legitimate_valid_data, 
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
