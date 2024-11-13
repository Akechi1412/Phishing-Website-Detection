import warnings
import asyncio
import aiohttp
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from bs4 import BeautifulSoup

def is_valid_html(html_document):
    """
    Checks if the HTML content is valid by parsing it with BeautifulSoup and checking for warnings.

    Parameters:
        html_document (str): The HTML document to parse.

    Returns:
        bool: True if the HTML is valid, False otherwise.
    """
    if not html_document.strip():
        return False
    if len(html_document) < 20 and ('<' not in html_document and '>' not in html_document):
        return False
    if html_document.strip().startswith('<?xml'):
        return False

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        BeautifulSoup(html_document, 'html.parser')
        if len(w) > 0:
            return False

    return True

async def fetch_data_from_url(session, url, timeout=20):
    """
    Asynchronously fetches HTML content from the given URL.

    Parameters:
        session (aiohttp.ClientSession): The aiohttp session for requests.
        url (str): The URL to fetch HTML content from.
        timeout (int): The request timeout in seconds.

    Returns:
        dict: A dictionary with 'url' and 'html'.
        None: If request fails.
    """
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        async with session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            html = await response.text()
            return {'url': str(response.url), 'html': html}
    except Exception:
        return None

async def collect_data(url_list, batch_size=1000, size=-1, filename='url_html_data.parquet'):
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
            tasks = [fetch_data_from_url(session, url) for url in current_batch]
            results = await asyncio.gather(*tasks)
            successful_results = [r for r in results if r]
            accessible_data.extend(successful_results)
            total_fetched += len(successful_results)
            total_processed += len(current_batch)

            if successful_results:
                df = pd.DataFrame(successful_results)
                table = pa.Table.from_pandas(df)
                if not pqwriter:
                    pqwriter = pq.ParquetWriter(filename, table.schema, compression='ZSTD')
                pqwriter.write_table(table)

            accessible_data = []
            batch_number = (batch_start // batch_size) + 1
            print(f"Processed batch {batch_number}: Total processed: {total_processed}, Accessible URLs: {total_fetched}")

    if pqwriter:
        pqwriter.close()
