# NBA-Scraper
Scraping data from nba.com/stats

**[Documentation](docs.md)**

## Install 
```
pip install git+https://github.com/szymonjoz/NBAScraper.git
```

## Example usage 
```
from NBAScraper import get_boxscores
get_boxscores(season=2023, sub="traditional", save="boxscores.csv")
```