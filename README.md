# ice-breaker

### Author : Basile EL AZHARI

A GenAI application to gather information about a person, and find an ice breaker.

This package is used in the Ice Breaker application, available at this website : XXXX

You can also install the package locally to benefit from its functionalities



## Functionalities Overview

### Scraping

The package provides helper functions to scrape a public profile. Scraping may be done providing :
- only the name of the person, and eventually a few specific words. This uses GenAI to crawl the web 
- The direct link to profile or username

Following services are supported :
- LinkedIn
- X (Twitter)

### Ice breaker

Given 1 or multiple profiles about a person, or even textual description, generate a complete piece of advice 
about how to break the ice with this person when you meet or chat with them.



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

XXXXX export XXXXX


### Get an ice-breaker

XXXXXX ice-breaker get "Elon Musk SpaceX USA"

### Other functionalities

#### Download a profile given a name

XXXXXX ice-breaker download-profile "Elon Musk SpaceX USA"

#### Download a profile given a URL / username

XXXXXX ice-breaker download-profile-id XXXXXXXX

#### Generate an ice breaker from JSON profiles / text

From text / JSON file

XXXXXX ice-breaker generate --json path_to_json_file
XXXXXX ice-breaker generate --text path_to_text_file

From in-line text

XXXXXX ice-breaker generate --inline "Elon Musk is one of the most known... " 

## Pull Requests

Public pull requests are opened on this project, please proceed and I will review them.



## Testing

pytest tests



## Contact 

XXXXX