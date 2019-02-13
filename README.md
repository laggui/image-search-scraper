## Dataset builder tool from web image scraping

### Overview

This user-friendly application allows you to easily construct your very own dataset for your personal application or research needs by scraping the web for images that match your queries (classes, labels, etc.). Its friendly interface allows for single or multiple queries to automate the process of building your dataset through the use of multiple image search APIs, each allowing numerous queries.

----

### On this page

1. [Supported APIs](#supported-apis)
1. [Usage](#usage)
1. [Limitations](#limitations)
   1. [Google Custom Search JSON API](#google-custom-search-json-api)
   1. [Bing Image Search API v7](#bing-image-search-api-v7)
1. [Prerequisites](#prerequisites)
   1. [Set up Google Custom Search Engine](#set-up-google-custom-search-engine)
   1. [Set up Bing Image Search API v7](#set-up-bing-image-search-api-v7)

----
### Supported APIs

We currently support image scraping with Google's [Custom Search JSON API][google-api-overview] and Microsoft's [Bing Image Search API v7][bing-image-search]. For more information on how to get the necessary credentials in order to use this tool, refer to the [prerequisites](#prerequisites) section.

### Usage

*In progress*

### Limitations

As with all APIs, Google and Microsoft's Image Search APIs have certain limitations. The main limitations of each can be found below.

#### Google Custom Search JSON API

- The maximum search results to be returned per API call is 10. If the number of results requested is greater than 10, the tool will split the search into multiple calls (i.e., 2 calls will be made in order to get 17 results).
- For the same searched phrase, the API will return a maximum of 100 results (even if split into 10 queries of 10 results per day). This is extremely restrictive if you need to build a dataset with more than 100 samples per query (class, label, etc.).
- [For free users only] The API provides 100 search queries per day. To circumvent this restriction, multiple search engines could be created and their different IDs could be associated to a different set of queries through the JSON configuration file.
- [For paying users only] The API allows for a maximum of 10k requests per day per API.

For more information, please visit [Google Custom Search JSON API][google-api-overview].

#### Bing Image Search API v7

- The maximum search results to return per query is 150. However, if a number greater than 150 is specified, the tool will split the search into multiple calls.
- The total number of results for the same searched phrase is only limited to the number of relevant results the API will find (usually much greater than 100).
   - For example, an image search for _"huawei p20"_ has a total estimated match of over 940 results (may vary). The total estimated matches, as the name indicates, is only an estimate. Thus, the image scraper will retrieve the results returned by the Bing Image Search API until the specified number of images has been retrieved or until the API has no more unique images relevant to the search to return.
- As opposed to Google's Custom Search Engine and their API, which returns a finite number of images at every query (the number specified by the user), Bing Image Search API doesn't guarantee that the number of results delivered will be equal to the number of results requested (may be less). Bing estimates the number of matches for each query, but this number will change from one query to another.
   - Thus, some search terms may result in duplicate images if the number of results requested is greater than what Bing's Images Search API ultimately found relevant for the query. Don't worry, the tool will output a warning if that is the case.

For more information, please visit Microsoft's [Cognitive Services pricing for Bing Image Search API][bing-pricing] or [Bing Image Search API v7 reference][bing-v7-ref].

*Note: for future improvement, the suggested related searches by the API could be used to get more results from Bing if needed.*
   
### Prerequisites

In order to call Google or Microsoft's API, you need an API key. The instructions below will guide you through getting your key for the selected API.

#### Set up Google Custom Search Engine

To search for images you need to sign up for Google Custom Search Engine.
Here are the steps you need to follow:

##### 1. Create a Google Custom Search Engine

Before using the JSON Custom Search API you will first need to create and configure your Custom Search Engine. If you have not already created a Custom Search Engine, go to the [Custom Search Engine control panel][cse].

Do not specify any sites to search but instead use the "Restrict Pages using Schema.org Types" under the "Advanced options".
For the most inclusive set, use the Schema: `Thing`. Make a note of the CSE ID.

##### 2. Enable Image Search

Go to your search engine **Setup**, and then in the **`Basics`** tab enable **Image search** by switching it to **ON**.

##### 3. Set up a Google Custom Search Engine API

Create a new project (or use an existing one if you wish) and enable Google Custom Search Engine API here: [Google Developers Console][google-dev]. Make note of the API key.

#### Set up Bing Image Search API v7

To search for images you need to either request a free 7-day trial for Microsoft's Cognitive Services, sign up for a free Azure account or sign in to your existing Azure account.
Here are the steps you need to follow:

##### Free 7-day Trial

Head to the [Bing Search API page][bing-image-search-try] and click on **`Get API Key`** for **Bing Search APIs v7** which includes Bing Web, Image, Video, News and Visual Search. We'll only need the Image Search API. When prompted, choose the **Guest** option by clicking on **`Getting started`** and register for the 7-day free trial. Eventually, you'll have access to your API key(s). Make note of the key(s).

##### Freemium with an Azure free account

The term _freemium_ was used because getting an API key through the Azure Portal will require you to select a paid tier for your Bing Search API, but signing up for an Azure free account will grant you free credits to use. Thus, until you surpass the free credits value, your API usage will technically be free.

###### 1. Sign up for an Azure free account

If you don't already have an Azure free account, you can sign up for one [here][azure-signup] and receive **CA$250** (US$200) in credits that you can then use with their Image Search API.

###### 2. Create a resource for your API

Head to Microsoft's [Azure Portal][azure-portal]. When logged in, click on the first result for **Bing Search v7** and create a resource for the API by clicking on **`Create`** in the lower right. There, you will be able to name your resource and select a pricing tier to fit your needs. For more information on the different pricing tiers, visit the Image Search API's [pricing details][bing-pricing]. Since we only need the Bing Image Search API, the **S3 tier offering** should be more than sufficient for our application. 

###### 3. Get your key

Once the resource for your Bing Image Search API has been created, you should have access to two keys. Make note of either one. As mentioned by Microsoft:

> Both keys work for accessing the API and you only need to specify one. These help you avoid downtime with your application. You may need or want to change the key used in your application, and with two keys you can avoid downtime by updating to one key while regenerating the other.

If you ever need to access your keys at a later time, you can always do so through your [resources][azure-resources]. Just click on the name of your Bing Search API resource, then in your resource's menu under the **`RESOURCE MANAGEMENT`** tab click on **`Keys`**.

<!-- Identifiers, in alphabetical order -->
[google-api-overview]:https://developers.google.com/custom-search/json-api/v1/overview
[cse]:https://cse.google.com/cse/all
[google-dev]:https://console.developers.google.com
[bing-image-search]:https://azure.microsoft.com/en-us/services/cognitive-services/bing-image-search-api/
[bing-image-search-try]:https://azure.microsoft.com/en-us/try/cognitive-services/?api=search-api-v7
[bing-pricing]:https://azure.microsoft.com/en-us/pricing/details/cognitive-services/search-api/image/
[bing-v7-ref]:https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-images-api-v7-reference
[azure-portal]:https://portal.azure.com/#blade/Microsoft_Azure_Marketplace/GalleryFeaturedMenuItemBlade/selectedMenuItemId/home/searchQuery/bing%20image%20search/resetMenuId/
[bing-api-keys]:https://cognitive.uservoice.com/knowledgebase/articles/864783-primary-vs-secondary-keys
[azure-signup]:https://azure.microsoft.com/en-us/free/
[azure-resources]:https://portal.azure.com/#blade/HubsExtension/Resources/resourceType/Microsoft.Resources%2Fresources