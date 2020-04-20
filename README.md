# scraper-py

Python web scraper for sofascore.it
Allow to scrape match statistics and players vote within the match

This scraper add those information inside a json file that must be passed to it.

Workflow:

Use calciocom-scraper (check this link https://github.com/gpellicci/calciocom-scraper) to build the json file
Use this repository to fill up with the remaining information the json file:
  Use scrapeV2.py to scrape statistics from sofascore.it
  Use voteFromCSV.py to add votes for "Serie A" from the csv in the repository at data/csv/
  Use changeType.py to post-process the json file, to change string types in integer when applicable
