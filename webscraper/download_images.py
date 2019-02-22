import os
import requests
from requests.exceptions import HTTPError, ConnectionError

def download_image(url, dest_dir, filename=None):
    '''
    Scrape images from website url and save them to destination directory
    '''
    if filename is None:
        filename = url.split('/')[-1]
    
    headers = {'User-Agent': 'Mozilla/5.0'} # add header info for sites trying to block scraping

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except ConnectionError as e:
        # ignore failed connection
        print("(Warning) ConnectionError: \"{0}\".\nFailed to retrieve image from: {1}".format(e, url))
        return "", "ConnectionError"
    except HTTPError:
        # ignore failed connection
        print("(Warning) HTTPError {0}. Failed to retrieve image from: {1}".format(r.status_code, url))
        return "", "HTTPError"
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    img = os.path.join(dest_dir, filename)
    if not os.path.exists(img):
        local_file = open(img, 'wb')
        local_file.write(r.content)
        local_file.close()
    #f.close()
    return img, "success"