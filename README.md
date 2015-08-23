# Domain Finder

A simple script which uses the whois module to perform a look up on any dictonary list provided. 

Three options are available

1. Will iterate through a provided dictionary list, and add the data to a SQLite DB. This then allows the user to search by expiry dates, to find domains of interest which are nearing the end of ownership.

2. Will dump out the database, so results can be filtered within a spreadsheer application, or futher processed by scripts.

3. Allows a manual look up, and adds the domain if not already in the database.

Current data captured is domain, country, expiry, updated, and registar (more can be added)

## Installation 

Best to use a virtualenv

    pip install whois
    
Configure options (config.ini)

    [config]
    dictionaryFile=test.txt
    tlds=.com,.net,.org

* Note, the tld list, which be used to iterate through words found in the dictionary file (so for example bbc.com,bbc.net,bbc.org)
## Dictionary File

Many can be found around on the internet, and here is one to get you started

https://raw.githubusercontent.com/eneko/data-repository/master/data/words.txt

Possible improvements to be made:

A search function, where expressions can be used, such as wildcards (football* returns footballscores * footballresults)

A flask based front end. 
