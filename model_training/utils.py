import asyncio
import aiohttp
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

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
            if len(accessible_data) > 0:
                pqwriter.write_table(table)
            accessible_data = []

            batch_number = (batch_start // batch_size) + 1
            print(f"Processed batch {batch_number}: Total processed: {total_processed}, Accessible URLs: {total_fetched}")

    if pqwriter:
        pqwriter.close()

    print(f"Build completed. Total URLs processed: {total_processed}, Accessible URLs: {total_fetched}")