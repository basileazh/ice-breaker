# ice-breaker

### Author : Basile EL AZHARI

A GenAI application to gather information about a person, and find an ice-breaker to start a conversation with them.

This package is used in the Ice Breaker application, available at this website : XXXX

You can also install the package locally to benefit from its functionalities :
 - Find a LinkedIn link from a name
 - Find a Twitter username from a name
 - Download a LinkedIn/Twitter profile
 - Generate an ice-breaker using profiles information



## Functionalities Overview

### Ice breaker

Using OpenAI GenAI SOTA algorithm, and given 1 or multiple profiles about a person, or even textual description, a complete piece of advice
about how to break the ice with this person when you meet or chat with them.

### Scraping

The package provides helper functions to scrape a public profile. Scraping may be done providing :
- only the name of the person, and eventually a few specific words. This uses GenAI to crawl the web
- The direct link to profile or username

Following services are supported :
- LinkedIn
- X (Twitter)



## Getting started

### Install package
To install the package, please download it via the following command :
XXXXXXXX

### Set up API keys
The following APIs are used in the project :
- ProxyCURL for LinkedIn profile scraping
- APIfy for X (Twitter) profile scraping

If you wish to use the scraping capabilities of the package (recommended), you must provide API keys to these services.

#### Create scraping API accounts

Please create accounts for ProxuCURL and APIfy to get your API keys, You should have free tokens at account creation.

1) ProxyCURL : XXXX. 10 free tokens at account creation, monthly free refill.
2) APIfy : XXXXX. Lots of free tokens, monthly free refill.

Retrieve you API keys in personal parameters.

#### Add API keys to ice-breaker

> XXXXX export XXXXX


### Get an ice-breaker
bash
> XXXXXX ice-breaker get "Elon Musk SpaceX USA"

python
ADD HERE


### Other functionalities

#### Download a profile given a name

> ice-breaker download-profile "Elon Musk SpaceX USA"

#### Download a profile given a URL / username

> ice-breaker download-profile linkedin https://www.linkedin.com/in/yann-lecun/ --force-scraping

> ice-breaker download-profile twitter ylecun --force-scraping


#### Generate an ice breaker from a profile saved as JSON / text

[//]: # ( - From text / JSON file)

> XXXXXX ice-breaker get --profile-json path_to_json_file

[//]: # (> XXXXXX ice-breaker get --profile-text path_to_text_file)

[//]: # ()
[//]: # ( - From in-line text)

[//]: # ()
[//]: # (> XXXXXX ice-breaker get --profile-inline "Elon Musk is one of the most known... " )



## Development

Public pull requests are opened and welcomed on this project, please proceed and I will review them.



## Testing

pytest tests



## Contact

XXXXX
