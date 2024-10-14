import numpy as np
import asyncio
import aiohttp
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import re
from collections import Counter
import pickle
from bs4 import BeautifulSoup, Tag
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import random
from sklearn.model_selection import train_test_split

async def fetch_url_data(session, url):
    """
    Asynchronously fetches HTML content from the given URL using aiohttp.

    Parameters:
        session (aiohttp.ClientSession): The aiohttp session to use for making the request.
        url (str): The URL from which to fetch the HTML content.

    Returns:
        dict: A dictionary containing the URL and its corresponding HTML content if the request is successful.
        None: If the request fails or the URL is not accessible.
    """
    try:
        url = url.strip()
        if not url.startswith('http'):
            url = 'http://' + url
        async with session.get(url, timeout=20) as response:
            if response.status == 200:
                html = await response.text()
                return {'url': str(response.url), 'html': html}
    except Exception as e:
        return None

async def build_dataset(url_list, batch_size=1000, size=-1, filename='url_html_data.parquet'):
    """
    Asynchronously fetches HTML content from a list of URLs and writes the data to a Parquet file in batches.

    Parameters:
        url_list (list): A list of URLs to fetch.
        batch_size (int): Number of URLs to process in each batch before writing to the Parquet file. Default is 1000.
        size (int): Maximum number of accessible URLs to retrieve. Default is -1 (fetch all).
        filename (str): The name of the Parquet file to write the data to. Default is 'url_html_data.parquet'.

    Returns:
        None
    """
    pqwriter = None
    accessible_data = []
    total_processed = 0
    total_fetched = 0

    connector = aiohttp.TCPConnector(limit=0)
    async with aiohttp.ClientSession(connector=connector) as session:
        for batch_start in range(0, len(url_list), batch_size):
            if 0 < size <= total_fetched:
                break

            current_batch = url_list[batch_start:batch_start + batch_size]
            tasks = [fetch_url_data(session, url) for url in current_batch]
            results = await asyncio.gather(*tasks)
            successful_results = [r for r in results if r]
            accessible_data.extend(successful_results)
            total_fetched += len(successful_results)
            total_processed += len(current_batch)

            df = pd.DataFrame(accessible_data)
            table = pa.Table.from_pandas(df)
            if not pqwriter and len(accessible_data) > 0:
                pqwriter = pq.ParquetWriter(filename, table.schema, compression='ZSTD')
            if pqwriter and len(accessible_data) > 0:
                pqwriter.write_table(table)
            accessible_data = []

            batch_number = (batch_start // batch_size) + 1
            print(f"Processed batch {batch_number}: Total processed: {total_processed}, Accessible URLs: {total_fetched}")

    if pqwriter:
        pqwriter.close()

    print(f"Build completed. Total URLs processed: {total_processed}, Accessible URLs: {total_fetched}")

def split_url(url):
    """
    Splits the given URL into individual components including words and special characters.

    Parameters:
        url (str): The input URL to be tokenized.

    Returns:
        list: A list of words and special characters present in the URL.
    
    Notes:
        - Special characters are defined by the 'special_chars' variable.
        - The function uses regular expressions to identify words and special characters.
        - Words that are purely whitespace are filtered out.
    """
    special_chars = '!@#%∧&*() +-=[]{}\\—‘’“,./<>?$:;_~|`'
    words = re.findall(r'\w+|[' + re.escape(special_chars) + ']', url)
    words = [word for word in words if word.strip()]
    return words

def build_dictionary(words, vocab_size=10000, filename=''):
    """
    Builds a dictionary of the most common words from a list, mapping each word to a unique index.

    Parameters:
        words (list): A list of words from which the dictionary will be built.
        vocab_size (int, optional): The maximum number of most frequent words to include in the dictionary. Defaults to 10,000.
        filename (str, optional): The name of the file to save the dictionary if specified. Defaults to an empty string ('').

    Returns:
        dict: A dictionary where keys are words and values are unique integer indices starting from 1.
    
    Notes:
        - Words are counted and sorted by frequency.
        - The top 'vocab_size' most common words are kept in the dictionary.
        - The indices in the dictionary start from 1.
        - If 'filename' is not an empty string, the dictionary will be saved to a .pkl file.
    """
    word_counts = Counter(words)
    most_common_words = [word for word, count in word_counts.most_common(vocab_size)]
    dictionary = {word: idx + 1 for idx, word in enumerate(most_common_words)}
    
    # If filename is provided, save the dictionary to a file
    if filename:
        with open(filename, 'wb') as file:
            pickle.dump(dictionary, file)
        print(f"Dictionary saved to {filename}")

    return dictionary

def transform_url(url, dictionary, word_size=50):
    """
    Transforms the given URL into a sequence of indices based on a pre-built dictionary.

    Parameters:
        url (str): The input URL to be transformed.
        dictionary (dict): A dictionary mapping words to indices.
        word_size (int, optional): The maximum length of the output sequence. Defaults to 50.

    Returns:
        list: A list of indices representing the words in the URL, padded or truncated to 'word_size'.
    
    Notes:
        - Each word in the URL is replaced by its corresponding index from the dictionary.
        - Words not found in the dictionary are replaced by 0.
        - The output sequence is truncated or padded with zeros to be exactly 'word_size' in length.
    """
    words = split_url(url)
    sequence = [dictionary[word] if word in dictionary else 0 for word in words]
    return (sequence[:word_size] + [0] * word_size)[:word_size]

def parse_html(html_document):
    """
    Parses an HTML document and converts it into a DOM tree.

    Parameters:
        html_document (str): A string representing the HTML document.

    Returns:
        BeautifulSoup: A BeautifulSoup object representing the DOM tree.

    Notes:
        - This function uses the BeautifulSoup library to parse the HTML.
        - The returned object can be used to navigate the DOM structure.
    """
    # Parse the HTML document into a DOM Tree
    dom_tree = BeautifulSoup(html_document, 'html.parser')
    return dom_tree


def create_graph(dom_tree):
    """
    This function converts a DOM tree into a graph using level-order traversal.
    
    Args:
    dom_tree: A DOM tree represented as a root node, where each node has a list of children.
    
    Returns:
    A NetworkX di-graph representing the structure of the DOM tree.
    If the tree is empty, it returns an empty di-graph.
    """
    if dom_tree is None:
        return nx.DiGraph()

    graph = nx.DiGraph()
    queue = deque([dom_tree])

    while queue:
        node = queue.popleft()
        if not isinstance(node, Tag):
            continue
        node_name = node.name
        node_features = {
            'has_href': 'href' in node.attrs,
            'has_src': 'src' in node.attrs
        }
        graph.add_node(node_name, **node_features)

        for child in node.children:
            if isinstance(child, Tag):
                graph.add_edge(node_name, child.name)
                queue.append(child)

    return graph

def load_data(data_size=50000):
    """
    Loads phishing and legitimate data, assigns labels, splits into train, val, and test sets, 
    and shuffles them.

    Parameters:
    data_size (int): Number of samples to load for each class. Default is 50,000.

    Returns:
    train_data (list): Shuffled training data combining phishing and legitimate samples.
    val_data (list): Shuffled validation data combining both classes.
    test_data (list): Shuffled test data combining both classes.

    Steps:
    1. Load phishing and legitimate data from Parquet files, assign label 1 for phishing, 0 for legitimate.
    2. Split each dataset into train (70%), val (20%), and test (10%).
    3. Combine and shuffle phishing and legitimate data for each split.
    """
    # Load phishing data
    df = pd.read_parquet('data/phishing_data.parquet')
    phishing_data = df.head(data_size).to_dict(orient='records')
    for item in phishing_data:
        item['label'] = 1
 
    # Load legitimate data
    df = pd.read_parquet('data/phishing_data.parquet')
    legitimate_data = df.head(data_size).to_dict(orient='records')
    for item in legitimate_data:
        item['label'] = 0

    train_size = 0.7
    val_size = 0.2
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
    train_data = phishing_train + legitimate_train
    random.shuffle(train_data)
    val_data = phishing_val + legitimate_val
    random.shuffle(val_data)
    test_data = phishing_test + legitimate_test
    random.shuffle(test_data)

    return train_data, val_data, test_data

# For testing functions
if __name__ == '__main__':
    # print(split_url('http://example.com/login.php?id=123'))
    html = '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Simple HTML Document</title>
        </head>
        <body>
            <h1>Title</h1>
            <p>Paragraph</p>
        </body>
    </html>
    '''
    dom_tree = parse_html(html)
    graph = create_graph(dom_tree)
    print(graph)
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=300, node_color='lightblue', font_size=10, edge_color='gray')
    plt.title("DOM Tree Graph")
    plt.show()
