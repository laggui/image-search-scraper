import re
import json
from search_clients import GoogleCustomSearchClient, BingSearchClient
from download_images import download_image
from parsers import parse_arguments, parse_conf

def split_request_into_n_queries(num_images, max_results_per_query):
    '''
    Return the number of queries necessary to retrieve num_images based on the maximum
    results per query, along with a list containing the number of images for each query
    '''
    # retrieve the number of queries necessary to get num_images
    n_queries = num_images // max_results_per_query
    n_rest = num_images % max_results_per_query

    num_img_list = []
    [num_img_list.append(max_results_per_query) for n in range(n_queries)]
    if n_rest: 
        num_img_list.append(n_rest)
        n_queries += 1
    return (n_queries, num_img_list)

def generate_filename_from_fquery(fquery, search_item, idx):
    '''
    Generate a filename from the specified formatted query with the file extension and idx
    '''
    ext = search_item['type'].split('/')[-1]
    if not ext:
        ext = 'jpeg'
    return"{0}_{1}.{2}".format(fquery, str(idx).zfill(4), ext)

def get_google_images(cse_id, api_key, save_dir, query, start_idx, num_images):
    '''
    Get images for the specified query through the Google Custom Search Engine
    '''
    MAX_RESULTS = 100 # maximum results per searched phrased for cse api
    MAX_RESULTS_PER_Q = 10 # maximum results per query for cse api

    # check for invalid result requests
    if num_images + start_idx > MAX_RESULTS + 1:
        if start_idx == 1:
            msg = ("(Warning) {0} results requested. Google CSE only returns the first {1} results."
                   "Truncated request to {1} results.")
            print(msg.format(num_images, MAX_RESULTS))
            num_images = MAX_RESULTS
        else:
            diff = (num_images + start_idx - 1) - MAX_RESULTS
            if start_idx - diff < 1:
                diff = start_idx - 1
            msg = ("(Warning) Results [{0}-{1}] requested. Google CSE only returns the first {2} results."
                   "Truncated request to results [{3}-{2}].")
            print(msg.format(start_idx, num_images + start_idx - 1, MAX_RESULTS, start_idx - diff))
            start_idx -= diff
            if num_images > MAX_RESULTS: num_images = MAX_RESULTS

    fquery = re.sub(r'\W+', '-', query) # remove special characters from query

    client = GoogleCustomSearchClient(cse_id, api_key) # initialize cse client

    # calculate the number of queries necessary to get num_images
    n_queries, num_img_list = split_request_into_n_queries(num_images, MAX_RESULTS_PER_Q)

    # split queries in result batches
    for q in range(n_queries):
        idx_offs = q * MAX_RESULTS_PER_Q
        search = client.search(query, start=start_idx + idx_offs, num=num_img_list[q])

        for i, item in enumerate(search):
            filename = generate_filename_from_fquery(fquery, item, i + idx_offs)
            download_image(item['url'], "{0}/{1}".format(save_dir, fquery), filename)

def get_bing_images(api_key, save_dir, query, offset, num_images):
    '''
    Get images for the specified query through Bing's image search API
    '''
    MAX_RESULTS_PER_Q = 150 # maximum results per query for bing api

    fquery = re.sub(r'\W+', '-', query) # remove special characters from query

    client = BingSearchClient(api_key) # initialize bing image search client

    # get the number of results to request for the first query
    if num_images > MAX_RESULTS_PER_Q:
        n_results = MAX_RESULTS_PER_Q
    else:
        n_results = num_images
    
    # retrieve search results until num_images have been retrieved or bing api has no more
    # unique images to return
    img_cnt = 0
    while(n_results > 0):
        search, next_offs, _ = client.search(query, offset=offset, count=n_results)

        for i, item in enumerate(search):
            filename = generate_filename_from_fquery(fquery, item, img_cnt + i)
            download_image(item['url'], "{0}/{1}".format(save_dir, fquery), filename)
        
        if i + 1 < n_results:
            msg = ("(Warning) {0}/{1} results requested for current query. Bing's image search API only"
                " returned {2} results. Subsequent queries might return duplicates.")
            print(msg.format(n_results, num_images, i + 1))
        offset = next_offs
        img_cnt += i
        # update number of results left to request for subsequent query
        n_results = num_images - n_results

def build_dataset(command, **kwargs):
    '''
    Build dataset from specified command line query or from configuration file (allows use of
    multiple APIs and queries)
    '''
    GOOGLE_SUBDIR = "/google-api"
    BING_SUBDIR = "/bing-api"

    if kwargs is not None:
        if command == 'google':
            # get images with specified command line arguments
            kwargs.update(save_dir=kwargs['save_dir']+GOOGLE_SUBDIR)
            get_google_images(**kwargs)
        elif command == 'bing':
            # get images with specified command line arguments
            kwargs.update(save_dir=kwargs['save_dir']+BING_SUBDIR, offset=kwargs['start_idx'] - 1)
            kwargs.pop('start_idx', None)
            get_bing_images(**kwargs)
        elif command == 'conf':
            # parse the JSON conf file to build the dataset
            data = parse_conf(kwargs.get('file'))
            args = {}
            google_dir = data['save_dir'] + GOOGLE_SUBDIR
            bing_dir = data['save_dir'] + BING_SUBDIR
            # iterate through every specified API
            for api in data['api']:
                # iterate through every google API
                if 'google' in api:
                    for google_api in api['google']:
                        args.update(api_key=google_api['key'], save_dir=google_dir)
                        # iterate through every CSE ID for specified API
                        for cse in google_api['cse']:
                            args.update(cse_id=cse['id'])
                            # get images for every single query for each specified api_key/cse_id combo
                            for q in cse['queries']:
                                args.update({'query':q['query'], 'start_idx':q['start'], 'num_images':q['num']})
                                get_google_images(**args)
                # iterate through every bing API
                elif 'bing' in api:
                    for bing_api in api['bing']:                    
                        args.update(api_key=bing_api['key'], save_dir=bing_dir)
                        # get images for every single query
                        for q in bing_api['queries']:
                            args.update({'query':q['query'], 'offset':q['start'] - 1, 'num_images':q['num']})
                            get_bing_images(**args)

if __name__ == '__main__':
    args = parse_arguments()
    build_dataset(**args)