"""
File: utils.py
Description: This script includes utility functions for computation or data loading.
Author: Phong Nguyen
Date: October 8, 2024
"""

import requests as rq
import pandas as pd
import multiprocessing as mp

def fetch_url_data(url):
    """
    Fetches HTML content from the given URL.

    This function sends an HTTP GET request to the provided URL and retrieves the HTML content 
    if the request is successful (status code 200). If the request fails or if any exception 
    occurs during the request, it returns None.

    Args:
        url (str): The URL from which to fetch the HTML content.

    Returns:
        dict: A dictionary containing the URL and its corresponding HTML content if the request is successful.
        None: If the request fails or the URL is not accessible.
    """
    try:
        response = rq.get(url, timeout=5)
        if response.status_code == 200:
            return {'url': url, 'html': response.text}
        else:
            return None
    except Exception as e:
        return None


def update_progress(result, progress, accessible_data):
    """
    Updates the progress of URL processing and stores accessible URL data.

    This function increments the total number of processed URLs and updates the list of accessible URLs 
    if the result is valid (not None). It also prints the progress every 100 URLs processed.

    Args:
        result (dict or None): The result of the URL processing. Contains 'url' and 'html' if successful, otherwise None.
        progress (list): A shared list to track progress. Index 0 tracks total processed URLs, 
                         and index 1 tracks accessible URLs.
        accessible_data (list): A shared list to store the accessible URL data (results).
    """
    progress[0] += 1
    if result:
        accessible_data.append(result)
        progress[1] += 1
    if progress[0] % 100 == 0:
        print(f'URL {progress[0]}, Accessible URL {progress[1]}')


def get_data_parallel(urls, num_processes=4, len=-1):
    """
    Fetches HTML content from URLs in parallel using multiprocessing.

    This function processes a list of URLs in parallel, fetching HTML content for each URL using multiple processes.
    It updates the progress as URLs are processed, and optionally stops after a specified number of URLs (len).
    The function uses a manager to share data between processes, and it stores the results (accessible URLs) 
    in a list.

    Args:
        urls (list): A list of URLs to process.
        num_processes (int, optional): The number of processes to run in parallel. Defaults to 4.
        len (int, optional): The number of URLs to process. If len is -1, all URLs are processed. Defaults to -1.

    Returns:
        list: A list of dictionaries containing accessible URLs and their HTML content.
    """
    with mp.Manager() as manager:
        accessible_data = manager.list()
        progress = manager.list([0, 0])

        with mp.Pool(processes=num_processes) as pool:
            for result in pool.imap_unordered(fetch_url_data, urls):
                update_progress(result, progress, accessible_data)
                if len > 0 and progress[0] == len:
                    break

        return list(accessible_data)
