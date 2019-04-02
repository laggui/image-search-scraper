import os
import requests
import concurrent.futures

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from requests.exceptions import HTTPError, ConnectionError

from webscraper import SupportedSearchClients

def download_image(dest_dir: str, image_dict: dict):
    '''
    Scrape images from website url and save them to destination directory
    '''
    filename = image_dict['file']
    url = image_dict['url']
    
    headers = {'User-Agent': 'Mozilla/5.0'} # add header info for sites trying to block scraping

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except ConnectionError as e:
        # ignore failed connection
        print(f'[WARNING] ConnectionError: "{e}".\nFailed to retrieve image from: {url}')
        return '', 'ConnectionError'
    except HTTPError:
        # ignore failed connection
        print(f'[WARNING] HTTPError {r.status_code}. Failed to retrieve image from: {url}')
        return '', 'HTTPError'
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    img = os.path.join(dest_dir, filename)
    if not os.path.exists(img):
        local_file = open(img, 'wb')
        local_file.write(r.content)
        local_file.close()
    #f.close()
    return img, 'Success'

def download_all_images(query: str, download_dir: str, links: list, query_id: int = 0, progress_object: object = None):
    completed = 0
    total = len(links)
    download_dir += '/' + query
    # By default, the executor sets number of workers to 5 times the number of
    # CPUs.
    with ThreadPoolExecutor() as executor:
        # Iterate through links and schedule image download instead of mapping
        # in order to track progress
        future_to_url = {executor.submit(download_image, download_dir, link): link['url'] for link in links}
        for future in concurrent.futures.as_completed(future_to_url):
            completed += 1
            url = future_to_url[future]
            _, status = future.result()
            if progress_object:
                progress_object.updateProgress.emit(query_id, (completed / total) * 100)
    print('Download done')