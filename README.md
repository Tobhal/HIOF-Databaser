# Databaser
Python script to crate and import data to a MySQL database. Gets all games for the given accaunt and stores the data.

## API used
- Steam API
- Steam Store API

## Scraped sites
- Wikipedia

## Data stored
### From Steam API
- appid
- name
- playtime_forever

### From Steam Sore API (per AppID)
- type
- required_age
- id_free
- website
- developers
- publishers
- price_overview
    - currency
    - final
    - final_formatted
- platforms
- metacritic
    - score
- categories
- genres
- recommendations
- release_date

### From Wikipedia infobar (Scraped)
#### Publisher / develpers
- type
- industry
- founded
- founders
- headquarters
- area serverd
- number of employees
- paren commpany
- native name
- romanized
- website