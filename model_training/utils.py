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
    words = [word.lower() for word in words if word.strip()]
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
    most_common_words = [word for word, count in word_counts.most_common(vocab_size - 1)]
    dictionary = {word: idx + 1 for idx, word in enumerate(most_common_words)}
    
    # If filename is provided, save the dictionary to a file
    if filename:
        with open(filename, 'wb') as file:
            pickle.dump(dictionary, file)
        print(f"Dictionary saved to {filename}")

    return dictionary

def transform_url(url, dictionary, max_word=50):
    """
    Transforms the given URL into a sequence of indices based on a pre-built dictionary.

    Parameters:
        url (str): The input URL to be transformed.
        dictionary (dict): A dictionary mapping words to indices.
        max_word (int, optional): The maximum length of the output sequence. Defaults to 50.

    Returns:
        numpy array: A array of indices representing the words in the URL, padded or truncated to 'max_word'.
    
    Notes:
        - Each word in the URL is replaced by its corresponding index from the dictionary.
        - Words not found in the dictionary are replaced by 0.
        - The output sequence is truncated or padded with zeros to be exactly 'max_word' in length.
    """
    words = split_url(url)
    sequence = [dictionary[word] if word in dictionary else 0 for word in words]
    return np.array((sequence[:max_word] + [0] * max_word)[:max_word])

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
    This function converts a DOM tree into a graph using level-order traversal
    and generates an adjacency matrix and feature matrix.
    
    Parameters:
        dom_tree: A DOM tree represented as a root node, where each node has a list of children.
    
    Returns:
        DiGraph: A NetworkX di-graph representing the DOM structure with integrated features.
    """
    if dom_tree is None:
        return nx.DiGraph()

    graph = nx.DiGraph()
    queue = deque([dom_tree])

    # Define a mapping from tag names to integers
    tag_to_idx = {
    'html': 1, 'head': 2, 'title': 3, 'body': 4,
    'article': 5, 'section': 6, 'nav': 7, 'aside': 8, 'header': 9, 
    'footer': 10, 'h1': 11, 'h2': 12, 'h3': 13, 'h4': 14, 
    'h5': 15, 'h6': 16, 'p': 17, 'blockquote': 18, 'ol': 19, 
    'ul': 20, 'li': 21, 'figure': 22, 'figcaption': 23, 'main': 24,
    'div': 25, 'span': 26, 'a': 27, 'img': 28, 'button': 29, 
    'form': 30, 'input': 31, 'textarea': 32, 'select': 33, 
    'option': 34, 'table': 35, 'tr': 36, 'th': 37, 'td': 38,
    'video': 39, 'audio': 40, 'source': 41, 'canvas': 42,
    'svg': 43, 'iframe': 44, 'script': 45, 'link': 46, 'meta': 47,
    'style': 48, 'noscript': 49, 'object': 50, 'embed': 51,
    'base': 52, 'fieldset': 53, 'legend': 54, 'label': 55,
    'strong': 56, 'em': 57, 'b': 58, 'i': 59, 'address': 60
}

    while queue:
        node = queue.popleft()
        if not isinstance(node, Tag):
            continue

        node_name = node.name
        node_id = id(node)
        tag_idx = tag_to_idx.get(node_name, 0)
        features = [
            tag_idx / len(tag_to_idx) ,
            1 if 'href' in node.attrs else 0,
            1 if 'src' in node.attrs else 0
        ]
        
        graph.add_node(node_id, name=node_name, features=features)

        children = [child for child in node.children if isinstance(child, Tag)]
        for child in children:
            if isinstance(child, Tag):
                graph.add_edge(node_id, id(child))
                queue.append(child)

    return graph

def create_graph_adjacency(graph, max_node=100):
    """
    Create the adjacency matrix from the graph and limit its size.
    
    Parameters:
        graph: A NetworkX di-graph.
        max_node: The maximum number of nodes in the adjacency matrix.
    
    Returns:
        An adjacency matrix (numpy array).
    """
    if graph.number_of_nodes() == 0:
        return np.zeros((max_node, max_node))

    adjacency_matrix = nx.to_numpy_array(graph)
    current_size = adjacency_matrix.shape[0]

    if current_size < max_node:
        padding = np.zeros((max_node - current_size, max_node - current_size))
        adjacency_matrix = np.block([[adjacency_matrix, np.zeros((current_size, max_node - current_size))],
                                      [np.zeros((max_node - current_size, current_size)), padding]])
    elif current_size > max_node:
        adjacency_matrix = adjacency_matrix[:max_node:, :max_node:]
        
    return adjacency_matrix

def create_graph_feature(graph, max_node):
    """
    Create the feature matrix from the graph and limit its size.
    
    Parameters:
        graph: A NetworkX di-graph.
        max_node: The maximum number of nodes in the feature matrix.
    
    Returns:
        A feature matrix (numpy array).
    """
    if graph.number_of_nodes() == 0:
        return np.zeros((max_node, 3))

    features_list = [data['features'] for _, data in graph.nodes(data=True)]
    feature_matrix = np.array(features_list, dtype='float64')

    if feature_matrix.shape[0] < max_node:
        padding = np.zeros((max_node - feature_matrix.shape[0], feature_matrix.shape[1]))
        feature_matrix = np.vstack((feature_matrix, padding))
        
    return feature_matrix[:max_node, :]

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

# For testing functions
if __name__ == '__main__':
    # print(split_url('http://example.com/login.php?id=123'))
    html = '''
    
    
'''
    dom_tree = parse_html(html)
    graph = create_graph(dom_tree)
    adjacency_matrix = create_graph_adjacency(graph, max_node=10)
    feature_matrix = create_graph_feature(graph, max_node=10)
    print(graph)
    print(adjacency_matrix)
    print(feature_matrix)
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    labels = nx.get_node_attributes(graph, 'name')
    nx.draw(graph, pos, labels=labels, with_labels=True, max_node=300, node_color='lightblue', font_size=10, edge_color='gray')
    plt.title("DOM Tree Graph")
    plt.show()
