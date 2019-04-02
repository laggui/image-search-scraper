from webscraper.search_api_client import SearchAPIClient
from webscraper.download_images import download_image

import re

class BingImageSearchClient(SearchAPIClient):
    """
    Bing Image Search Client
    """
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError('Expected an API Key')
        super().__init__('https://api.cognitive.microsoft.com/bing/v7.0/images/search', 25000, 150, 1,
                         {'Ocp-Apim-Subscription-Key':api_key}, {})

    def get_links(self, query: str, count: int, offset: int = 0):
        return self._get_all_items(query, count, offset)

    def _check_value(self, **kwargs):
        offset = kwargs.pop('offset', 0)
        count = kwargs.pop('count', None)
        if kwargs:
            raise TypeError(f'{kwargs.keys()} are invalid keyword arguments.')
        if count is None:
            raise ValueError('Missing number of results to return.')
        if offset < self.min_index - 1:
            raise ValueError(f'Invalid start index value. Valid values start at {self.min_index - 1}.')
        if count > self.max_results_per_q or count < self.min_index:
            raise ValueError(('Invalid num value. Number of search results to return must '
                              f'be between {self.min_index} and {self.max_results_per_q}, inclusively.'))

    def _parse_response(self):
        items = []
        for item in self.response['value']:
            items.append({
                'type': item['encodingFormat'],
                'width': item['width'],
                'height': item['height'],
                'size': item['contentSize'],
                'url': item['contentUrl'],
                'hostPage': item['hostPageDisplayUrl']
            })
        return (items, self.response['nextOffset'], self.response['totalEstimatedMatches'])

    def _get_all_items(self, query: str, count: int, start_idx: int = 1):
        """
        Get images for the specified query through Bing's image search API
        """
        offset = start_idx - 1
        items = []
        # Get the number of results to request for the first query
        if num_images > self.max_results_per_q:
            n_results = self.max_results_per_q
        else:
            n_results = num_images

        # Retrieve search results until num_images have been retrieved or bing api has no more
        # unique images to return
        img_cnt = 0
        while n_results > 0:
            search, next_offs, _ = self.search(query, offset=offset, count=n_results)
            search = self.add_filename_to_search_dict(search, query, offset=img_cnt)
            items.extend(search)

            if len(search) < n_results:
                msg = ('[WARNING] {0}/{1} results requested for current query. Bing image search API'
                       ' only returned {2} results. Subsequent queries might return duplicates.')
                print(msg.format(n_results, num_images, len(search)))
            offset = next_offs
            img_cnt += len(search)
            # Update number of results left to request for subsequent query
            n_results = num_images - n_results
        return items