import warnings
import asyncio
import aiohttp
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

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

    return True

async def fetch_data_from_url(session, url, timeout=20):
    """
    Asynchronously fetches HTML content from the given URL and validates it.

    Parameters:
        session (aiohttp.ClientSession): The aiohttp session for requests.
        url (str): The URL to fetch HTML content from.
        timeout (int): The request timeout in seconds.

    Returns:
        dict: A dictionary with 'url' and 'html' if HTML is valid.
        None: If HTML is invalid or request fails.
    """
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        async with session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            html = await response.text()
            if not is_valid_html(html):
                return None
            return {'url': str(response.url), 'html': html}
    except Exception:
        return None

async def fetch_website_data(session, url, **kwargs):
    """
    Asynchronously fetches HTML content from the main URL and internal subpages.

    Parameters:
        session (aiohttp.ClientSession): The aiohttp session to use for making the request.
        url (str): The URL from which to fetch the HTML content.
        **kwargs: Additional keyword arguments, including:
            - timeout (int): The number of seconds to wait. Default is 20 seconds.
            - subpage_limit (int): The maximum number of internal subpages to fetch. Default is 3.

    Returns:
        list: A list of dictionaries, each containing 'url' and 'html' of the main and subpages.
        None: If the request fails or the URL is not accessible.
    """
    timeout = kwargs.get('timeout', 20)
    subpage_limit = kwargs.get('subpage_limit', 3)

    try:
        main_result = await fetch_data_from_url(session, url, timeout)
        if not main_result:
            return None

        results = [main_result]
        seen_urls = set()
        seen_urls.add(main_result['url'])

        # Parse main page for internal links
        soup = BeautifulSoup(main_result['html'], 'html.parser')
        domain = urlparse(main_result['url']).netloc
        
        internal_links = [
            urljoin(main_result['url'], a['href']) 
            for a in soup.find_all('a', href=True) 
            if (a['href'].startswith('/') or urlparse(a['href']).netloc == domain)
        ]

        for link in internal_links:
            if len(results) >= subpage_limit + 1:
                break
            if link not in seen_urls:
                sub_result = await fetch_data_from_url(session, link, timeout)
                if sub_result:
                    results.append(sub_result)
                    seen_urls.add(link)

        return results
    except Exception:
        return None

async def collect_data(url_list, batch_size=1000, size=-1, 
                       filename='url_html_data.parquet', **kwargs):
    """
    Asynchronously fetches HTML content from a list of URLs and writes the data to a Parquet file in batches.

    Parameters:
        url_list (list): List of URLs to fetch.
        batch_size (int): Number of URLs to process in each batch before writing to the Parquet file.
        size (int): Maximum number of webpages to retrieve. Default is -1 (fetch all).
        filename (str): Name of the Parquet file to write data to.
        **kwargs: Additional keyword arguments for `fetch_website_data`.

    Returns:
        None
    """
    pqwriter = None
    total_processed = 0  # Total URLs processed
    total_fetched = 0    # Total accessible URLs
    total_webpages = 0   # Total number of pages including subpages

    connector = aiohttp.TCPConnector(limit=0)
    async with aiohttp.ClientSession(connector=connector) as session:
        for batch_start in range(0, len(url_list), batch_size):
            if 0 < size <= total_webpages:
                break

            current_batch = url_list[batch_start:batch_start + batch_size]
            tasks = [fetch_website_data(session, url, **kwargs) for url in current_batch]
            results = await asyncio.gather(*tasks)
            successful_results = [r for r in results if r]
            flattened_results = [page for website_data in successful_results for page in website_data]
            total_fetched += len(successful_results)
            total_webpages += len(flattened_results)
            total_processed += len(current_batch)

            if flattened_results:
                df = pd.DataFrame(flattened_results)
                table = pa.Table.from_pandas(df)
                if not pqwriter:
                    pqwriter = pq.ParquetWriter(filename, table.schema, compression='ZSTD')
                pqwriter.write_table(table)

            batch_number = (batch_start // batch_size) + 1
            print(f'Processed batch {batch_number}: Total processed URLs: {total_processed}, '
                  f'Accessible URLs: {total_fetched}, Total webpages: {total_webpages}')

    if pqwriter:
        pqwriter.close()

    print(f'Build completed. Total URLs processed: {total_processed}, '
          f'Accessible URLs: {total_fetched}, Total webpages: {total_webpages}')
