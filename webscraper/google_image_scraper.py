# Adapted from https://github.com/hardikvasa/google-images-download
import os
import sys
import time
import json
import requests

from webscraper.download_images import download_image

__driverpath__ = os.path.dirname(os.path.realpath(__file__)) + '/driver/chromedriver.exe'

class GoogleImageScraper():
    """
    Google Image Scraper class to download images from html content of a web image search
    """
    def __init__(self):
        pass

    #building main search URL
    def build_search_url(self, query: str, safe_search: bool = False):
        """
        Build search url from query
        """
        #check safe_search
        safe_search_string = '&safe=active' if safe_search else ''
        url = 'https://www.google.com/search?q=' + query + '&source=lnms&tbm=isch' + safe_search_string
        return url

    def download_page(self, url: str):
        """
        Download entire web document (Raw Page Content)
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            r = requests.get(url, headers=headers)
            r.raise_for_status()
        except ConnectionError as e:
            # ignore failed connection
            print("(Warning) ConnectionError: \"{0}\".\nFailed to retrieve image from: {1}".format(e, url))
            return
        except HTTPError:
            # ignore failed connection
            print("(Warning) HTTPError {0}. Failed to retrieve image from: {1}".format(r.status_code, url))
            return
        
        return str(r.content)

    def download_extended_page(self, url, chromedriver):
        """
        Download page for more than 100 images
        """
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")

        try:
            browser = webdriver.Chrome(chromedriver, options=options)
        except Exception as e:
            print("Looks like we cannot locate the path the 'chromedriver' (use the '--chromedriver' "
                  "argument to specify the path to the executable.) or google chrome browser is not "
                  "installed on your machine (exception: %s)" % e)
            sys.exit()
        browser.set_window_size(1024, 768)

        # Open the link
        browser.get(url)
        time.sleep(1)
        print("Getting you a lot of images. This may take a few moments...")

        element = browser.find_element_by_tag_name("body")
        # Scroll down
        for i in range(30):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

        try:
            browser.find_element_by_id("smb").click()
            for i in range(50):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)  # bot id protection
        except:
            for i in range(10):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)  # bot id protection

        print("Reached end of Page.")
        time.sleep(0.5)

        source = browser.page_source #page source
        #close the browser
        browser.close()

        return source

    def download(self, save_dir: str, query: str, num_images: int, start_idx: int = 0):
        """
        Download specified number of images from query into destination save directory
        """
        # TO-DO: argument for image size to narrow search results?
        print("Evaluating...")

        url = self.build_search_url(query)

        if num_images < 101:
            raw_html = self.download_page(url)
        else:
            raw_html = self.download_extended_page(url, __driverpath__)

        items, errorCount = self._get_all_items(query, raw_html, save_dir, num_images, start_idx)

        print("\nErrors: " + str(errorCount) + "\n")

    def format_object(self,object):
        """
        Format the object in readable format
        """
        formatted_object = {}
        formatted_object['image_format'] = object['ity']
        formatted_object['image_height'] = object['oh']
        formatted_object['image_width'] = object['ow']
        formatted_object['image_link'] = object['ou']
        formatted_object['image_description'] = object['pt']
        formatted_object['image_host'] = object['rh']
        formatted_object['image_source'] = object['ru']
        formatted_object['image_thumbnail_url'] = object['tu']
        return formatted_object

    def generate_filename_from_query(self, query: str, idx: int, ext: str = None):
        """
        Generate a filename from the specified formatted query with the file extension and idx
        """
        if not ext:
            ext = 'jpeg'
        return f'{query}_{str(idx).zfill(5)}.{ext}'

    def _get_next_item(self, s: str):
        """
        Finding 'Next Image' from the given raw page
        """
        start_line = s.find('rg_meta notranslate')
        if start_line == -1:  # If no links are found then give an error!
            end_quote = 0
            link = "no_links"
            return link, end_quote
        else:
            start_line = s.find('class="rg_meta notranslate">')
            start_object = s.find('{', start_line + 1)
            end_object = s.find('</div>', start_object + 1)
            object_raw = str(s[start_object:end_object])
            #remove escape characters
            try:
                object_decode = bytes(object_raw, "utf-8").decode("unicode_escape")
                final_object = json.loads(object_decode)
            except:
                final_object = ""
            return final_object, end_object

    def _get_all_items(self, query: str, page: str, save_dir: str, num_images: int, start_idx: int = 0):
        """
        Retrieve specified number of links from the web page
        """
        items = []
        offset = start_idx + 1
        errorCount = 0
        i = 0
        count = 1
        while count <= num_images:
            obj, end_content = self._get_next_item(page)
            if obj == "no_links":
                break
            elif obj == "":
                page = page[end_content:]
            elif offset and count < int(offset):
                    count += 1
                    page = page[end_content:]
            else:
                #format the item for readability
                obj = self.format_object(obj)

                #download the images
                filename = self.generate_filename_from_query(query, i, obj['image_format'])
                return_image_name, download_status = download_image(obj['image_link'], save_dir, filename)
                if download_status == "success":
                    count += 1
                    obj['image_filename'] = return_image_name
                    items.append(obj)  # Append all the links in the list named 'Links'
                else:
                    errorCount += 1

                page = page[end_content:]
            i += 1
        if count < num_images:
            print("\n\nUnfortunately all " + str(
                num_images) + " could not be downloaded because some images were not downloadable. " + str(
                count-1) + " is all we got for this search filter!")
        return items, errorCount