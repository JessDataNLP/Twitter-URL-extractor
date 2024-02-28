
import requests
import concurrent.futures
from tqdm import tqdm

def expand_url(short_url):
    """
    Attempt to expand a short URL to its full form.
    
    :param short_url: A shortened URL.
    :return: The expanded URL if successful, otherwise None.
    """
    try:
        response = requests.get(short_url, allow_redirects=True)
        return response.url
    except (requests.RequestException, UnicodeDecodeError):
        return None

def process_urls(urls, chunksize=100):
    """
    Process a list of URLs to expand them and optionally classify.
    
    :param urls: A list of URLs to be expanded.
    :param chunksize: The number of URLs to process in each thread.
    :return: A list of expanded URLs.
    """
    # Prepare a list to hold the expanded URLs
    expanded_urls = [None] * len(urls)

    def process_chunk(start_idx):
        for i in range(start_idx, min(start_idx + chunksize, len(urls))):
            expanded_urls[i] = expand_url(urls[i])

    # Using ThreadPoolExecutor for parallel processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks for each chunk
        futures = [executor.submit(process_chunk, start_idx) for start_idx in range(0, len(urls), chunksize)]

        # Track progress with tqdm
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Expanding URLs"):
            pass

    return expanded_urls
