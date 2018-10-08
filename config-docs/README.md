## JSON configuration file documentation

The configuration file used to automate the process of building your dataset follows the JSON standard file format. The data found in the file is similar to what you would need to pass for a single query through the command line arguments, with the advantage of easily allowing multiple queries and different APIs.

To do so, the data is primarily grouped by API type (_google_ or _bing_). Then, for each API type, you can specify numerous API keys if you have multiple APIs through which you want to send your queries.

### JSON Values

Below is a list of the different keys found in a configuration file.


| **Key**    | **Value** | **Description**                                                                      |
|:-----------|:---------:|:-------------------------------------------------------------------------------------|
| save_dir   | string    | Path to the parent directory where scraped images will be saved.                     |
| api        | array     | List of available API objects (of type _google_ or _bing_).                          |
| google     | array     | List of Google API objects.                                                          |
| bing       | array     | List of Bing API objects.                                                            |
| key        | string    | A valid API key for the selected API object.                                         |
| cse        | array     | *[For Google only]* List of Custom Search Engine objects.                            |
| id         | string    | *[For Google only]* A valid Google Custom Search Engine ID for the selected API key. |
| queries    | array     | List of query objects for the selected API key (or selected CSE ID for _google_).    |
| query      | string    | Search query term.                                                                   |
| start      | number    | Index of the first result to return for the selected query.                          |
| num        | number    | Number of images to retrieve for the selected query.                                 |


### Configuration file example

Below is a JSON configuration file example. This example makes use of multiple APIs (i.e., _google_ and _bing_, the only ones supported at the moment), as well as multiple queries with different parameters. The comments were added for descriptive purposes, but are not supported in JSON file format. The valid example file without comments can be found [here](conf_example.json).

```json
{
	"save_dir": "C:/path/to/save/directory", // replace with your save directory to hold all downloaded images
	"api": [
		{
			"google": [
				{
					"key": "YOuRg00GLe-aPiK3yhER3", // replace with your Google Custom Search JSON API key
					"cse": [
						{
							"id": "600613:customsearchengineidh3r3", // replace with your Google Custom Search Engine ID
							"queries": [
								{
									"query": "huawei p20",
									"start": 1,
									"num": 19
								},
								{
									"query": "iphone se",
									"start": 5,
									"num": 5
								},
								{
									"query": "google pixel XL",
									"start": 10,
									"num": 9
								}
							]
						}
					]
				}
			]
		},
		{
			"bing": [
				{
					"key": "bing1m4g3s34rchapik3yh3r3", // replace with your Bing Search API key
					"queries": [
						{
							"query": "huawei p20",
							"start": 1,
							"num": 24
						},
						{
							"query": "iphone se",
							"start": 9,
							"num": 9
						},
						{
							"query": "google pixel XL",
							"start": 13,
							"num": 10
						}
					]
				}
			]
		}
	]
}
```