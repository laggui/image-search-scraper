import requests
import json

class GoogleCustomSearchClient():
    '''
    Google Custom Search Engine Client
    '''
    def __init__ (self, cse_id, api_key):
        if not cse_id:
            raise ValueError("Expected a Custom Search Engine ID")
        if not api_key:
            raise ValueError("Expected an API Key")
        
        self.cse_id = cse_id
        self.api_key = api_key
        self.endpoint = "https://www.googleapis.com"
    
    def search(self, query, start=1, num=1):
        MAX_RESULTS_PER_Q = 10 # maximum results per query for cse api
        MIN_INDEX = 1
        
        if not query:
            raise ValueError("Expected a query")
        if start < MIN_INDEX:
            raise ValueError("Invalid start index value. Valid values start at 1.")
        if num > MAX_RESULTS_PER_Q or num < MIN_INDEX:
            raise ValueError("Invalid num value. Number of search results to return must be between 1 and 10, inclusive.")

        __url = "{0}/customsearch/v1?q={1}&start={2}&num={3}&key={4}&cx={5}&searchType=image".format(self.endpoint,
                                                                         query, start, num, self.api_key, self.cse_id)
        response = requests.get(__url).json()['items']

        items = []
        for item in response:
            items.append({
                'type': item['mime'],
                'width': item['image']['width'],
                'height': item['image']['height'],
                'size': item['image']['byteSize'],
                'url': item['link'],
                'hostPage': item['image']['contextLink']
            })
        return items

class BingSearchClient():
    '''
    Bing Image Search Client
    '''
    def __init__ (self, api_key):
        if not api_key:
            raise ValueError("Expected an API Key")
        
        self.headers = {'Ocp-Apim-Subscription-Key':api_key}
        self.params = {}#{'license':'public', 'imageType':'photo'}
        self.endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    
    def get_estimated_matches(self, query):
        if not query:
            raise ValueError("Expected a query")
        
        self.params.update(q=query)
        r = requests.get(self.endpoint, headers=self.headers, params=self.params).json()
        return r['totalEstimatedMatches']

    def search(self, query, offset=0, count=1):
        MAX_RESULTS_PER_Q = 150

        if not query:
            raise ValueError("Expected a query")
        if offset < 0:
            raise ValueError("Invalid offset value. Valid values start at 0.")
        if count > MAX_RESULTS_PER_Q or count < 1:
            raise ValueError("Invalid num value. Number of search results to return must be between 1 and 150, inclusive.")

        self.params.update(q=query, offset=offset, count=count)
        response = requests.get(self.endpoint, headers=self.headers, params=self.params).json()

        items = []
        for item in response['value']:
            items.append({
                'type': item['encodingFormat'],
                'width': item['width'],
                'height': item['height'],
                'size': item['contentSize'],
                'url': item['contentUrl'],
                'hostPage': item['hostPageDisplayUrl']
            })
        return (items, response['nextOffset'], response['totalEstimatedMatches'])