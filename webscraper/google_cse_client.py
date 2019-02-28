from webscraper.search_api_client import SearchAPIClient
from webscraper.download_images import download_image

import re

class GoogleCustomSearchEngineClient(SearchAPIClient):
    """
    Google Custom Search Engine Client
    """
    def __init__(self, cse_id: str, api_key: str):
        if not api_key:
            raise ValueError("Expected an API Key")
        if not cse_id:
            raise ValueError("Expected a Custom Search Engine ID")
        super().__init__("https://www.googleapis.com/customsearch/v1", 100, 10, 1,
                         {}, {'key':api_key, 'cx':cse_id, 'searchType':'image'})

    def get_links(self, query: str, num_images: int, start_idx: int = 0):
        return self._get_all_items(query, num_images, start_idx)

    def _check_value(self, **kwargs):
        start = kwargs.pop('start', 1)
        num = kwargs.pop('num', None)
        if kwargs:
            raise TypeError("%r are invalid keyword arguments." % (kwargs.keys()))
        if num is None:
            raise ValueError("Missing number of results to return.")
        if start < self.min_index:
            raise ValueError("Invalid start index value. Valid values start at {}.".format(
                self.min_index))
        if num > self.max_results_per_q or num < self.min_index:
            raise ValueError(("Invalid num value. Number of search results to return must"
                              " be between {} and {}, inclusive.".format(
                                  self.min_index, self.max_results_per_q)))

    def _parse_response(self, query):
        items = []
        for i,item in enumerate(self.response['items']):
            items.append({
                'type': item['mime'],
                'width': item['image']['width'],
                'height': item['image']['height'],
                'size': item['image']['byteSize'],
                'url': item['link'],
                'hostPage': item['image']['contextLink'],
                'file': self.generate_filename_from_query(query, i, None if not item['mime'] else item['mime'])
            })
        return items

    def _split_request_into_n_queries(self, num_images: int):
        """
        Return the number of queries necessary to retrieve num_images based on the maximum
        results per query, along with a list containing the number of images for each query
        """
        # retrieve the number of queries necessary to get num_images
        n_queries = num_images // self.max_results_per_query
        n_rest = num_images % self.max_results_per_query

        num_img_list = [self.max_results_per_query] * n_queries
        if n_rest:
            num_img_list.append(n_rest)
            n_queries += 1
        return (n_queries, num_img_list)

    def _get_all_items(self, query: str, num_images: int, start_idx: int = 0):
        items = []
        # Check for invalid result requests
        if num_images + start_idx > self.max_results + 1:
            if start_idx == 1:
                msg = ("(Warning) {0} results requested. Google CSE only returns the first {1} results."
                    "Truncated request to {1} results.")
                print(msg.format(num_images, self.max_results))
                num_images = self.max_results
            else:
                diff = (num_images + start_idx - 1) - self.max_results
                if start_idx - diff < 1:
                    diff = start_idx - 1
                msg = ("(Warning) Results [{0}-{1}] requested. Google CSE only returns the first {2}"
                    " results. Truncated request to results [{3}-{2}].")
                print(msg.format(start_idx, num_images + start_idx - 1, self.max_results, start_idx - diff))
                start_idx -= diff
                if num_images > self.max_results: num_images = self.max_results

        # Calculate the number of queries necessary to get num_images
        n_queries, num_img_list = self._split_request_into_n_queries(num_images, self.max_results_per_query)

        # Split queries in result batches
        for q in range(n_queries):
            idx_offs = q * self.max_results_per_query
            search = self.search(query, start=start_idx + idx_offs, num=num_img_list[q])
            items.append(search)
        return items