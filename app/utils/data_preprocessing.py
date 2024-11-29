import numpy as np
import re
from collections import Counter
import pickle
from bs4 import BeautifulSoup, Tag
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

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

def vectorize_url(url, dictionary, max_words=50):
    """
    Transforms the given URL into a sequence of indices based on a pre-built dictionary.

    Parameters:
        url (str): The input URL to be transformed.
        dictionary (dict): A dictionary mapping words to indices.
        max_words (int, optional): The maximum length of the output sequence. Defaults to 50.

    Returns:
        numpy array: A array of indices representing the words in the URL, padded or truncated to 'max_words'.
    
    Notes:
        - Each word in the URL is replaced by its corresponding index from the dictionary.
        - Words not found in the dictionary are replaced by 0.
        - The output sequence is truncated or padded with zeros to be exactly 'max_words' in length.
    """
    words = split_url(url)
    sequence = [dictionary[word] if word in dictionary else 0 for word in words]
    return np.array((sequence[:max_words] + [0] * max_words)[:max_words])

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
            tag_idx / len(tag_to_idx),                   # Normalized tag index
            1 if 'href' in node.attrs else 0,            # Contains link
            1 if 'src' in node.attrs else 0,             # Contains source
        ]
        
        graph.add_node(node_id, name=node_name, features=features)

        children = [child for child in node.children if isinstance(child, Tag)]
        for child in children:
            if isinstance(child, Tag):
                graph.add_edge(node_id, id(child))
                queue.append(child)

    return graph

def create_graph_adjacency(graph, max_nodes):
    """
    Create the adjacency matrix from the graph and limit its size.
    
    Parameters:
        graph: A NetworkX di-graph.
        max_nodes: The maximum number of nodes in the adjacency matrix.
    
    Returns:
        An adjacency matrix (numpy array).
    """
    if graph.number_of_nodes() == 0:
        return np.zeros((max_nodes, max_nodes))
    
    selected_nodes = list(graph.nodes())[:max_nodes]
    subgraph = graph.subgraph(selected_nodes)
    adjacency_matrix = nx.to_numpy_array(subgraph, nodelist=selected_nodes)

    current_size = adjacency_matrix.shape[0]
    if current_size < max_nodes:
        padding = np.zeros((max_nodes - current_size, max_nodes - current_size))
        adjacency_matrix = np.block([[adjacency_matrix, np.zeros((current_size, max_nodes - current_size))],
                                     [np.zeros((max_nodes - current_size, current_size)), padding]])
        
    return adjacency_matrix

def create_graph_feature(graph, max_nodes):
    """
    Create the feature matrix from the graph and limit its size.
    
    Parameters:
        graph: A NetworkX di-graph.
        max_nodes: The maximum number of nodes in the feature matrix.
    
    Returns:
        A feature matrix (numpy array).
    """
    feature_dim = 3
    if graph.number_of_nodes() == 0:
        return np.zeros((max_nodes, feature_dim))

    selected_nodes = list(graph.nodes())[:max_nodes]
    features_list = [graph.nodes[node]['features'] for node in selected_nodes]
    feature_matrix = np.array(features_list)

    if feature_matrix.shape[0] < max_nodes:
        padding = np.zeros((max_nodes - feature_matrix.shape[0], feature_dim))
        feature_matrix = np.vstack((feature_matrix, padding))
        
    return feature_matrix

# For testing functions
if __name__ == '__main__':
    # print(split_url('http://example.com/login.php?id=123'))
    html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Sample Web Page</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />  
        </head>
        <body>
            <h1>Sample Title</h1>
            <p>Sample Paragraph</p>
        </body>
        </html>
        '''
    dom_tree = parse_html(html)
    graph = create_graph(dom_tree)
    adjacency_matrix = create_graph_adjacency(graph, max_nodes=12)
    feature_matrix = create_graph_feature(graph, max_nodes=12)
    print(graph)
    print(adjacency_matrix)
    print(feature_matrix)
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph, k=1)
    labels = nx.get_node_attributes(graph, 'name')
    nx.draw(graph, pos, labels=labels, with_labels=True, node_color='lightblue', 
            font_size=10, edge_color='gray', node_size=1200)
    plt.title("DOM Tree Graph")
    plt.show()