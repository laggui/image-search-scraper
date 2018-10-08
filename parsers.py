import json
import argparse

def parse_arguments():
    '''
    Get command line arguments and return them
    '''
    parser = argparse.ArgumentParser(description='Dataset builder from web image scraping')
    subparsers = parser.add_subparsers(title='Subcommands', description='Valid subcommands', help='additional help', dest='command')

    conf_parser = subparsers.add_parser('conf', description='Image Scraper from JSON configuration file')
    conf_parser.add_argument('file', type=str, help='JSON configuration file defining APIs to use for every query')

    google_parser = subparsers.add_parser('google', description='Google Custom Search Engine Image Scraper')
    google_parser.add_argument('--cse-id', type=str, help='Custom Search Engine ID', required=True)
    google_parser.add_argument('--api-key', type=str, help='Google Custom Search API key', required=True)
    google_parser.add_argument('--save-dir', type=str, help='Path to parent directory where images will be downloaded', required=True)
    google_parser.add_argument('--query', type=str, help='Query to be searched', required=True)
    google_parser.add_argument('--start-idx', type=int, default=1, help='Index of the first result to return')
    google_parser.add_argument('--num-images', type=int, default=10, help='Number of images to retrieve')

    bing_parser = subparsers.add_parser('bing', description='Bing Images Search API Image Scraper')
    bing_parser.add_argument('--api-key', type=str, help='Bing API key', required=True)
    bing_parser.add_argument('--save-dir', type=str, help='Path to parent directory where images will be downloaded', required=True)
    bing_parser.add_argument('--query', type=str, help='Query to be searched', required=True)
    bing_parser.add_argument('--start-idx', type=int, default=1, help='Index of the first result to return')
    bing_parser.add_argument('--num-images', type=int, default=10, help='Number of images to retrieve')

    args = parser.parse_args()
    return vars(args)

def parse_conf(filename):
    '''
    Read JSON configuration file for dataset builder
    '''
    with open(filename, "r") as read_file:
        data = json.load(read_file)
        return data