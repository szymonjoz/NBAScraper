# NBA.com Web Scraper Documentation

### get_boxscores(season, sub, group="players", segment="all", params=None, filters=None, driver=None, save=False)
Collect all boxscores from season or it's segment. Works since 1996-97 season.
> **Parameters**:
> * **season: int** <br>
>   Season from which data should be scraped
> * **sub: {"traditional", "advanced", "misc", "scoring", "usage" (player only), "four-factors" (teams only)}** <br>
>   Boxscore subtype 
> * **group: {"players", "teams"}** <br>
>   Choosing player or team boxscores
> * **segment: {"all", "Regular Season", "Playoffs", "PlayIn"}** <br>
>   Selecting season segments to scrape. If "all" will get all available segments that season.
> * **params: None or dict** <br>
>   Params to be added to final url. Dict should be in format {parameter: value}. Available params [here](#params-list)
> * **filters: None or list** <br>
>   Filters to be used on the table. Should be list with tuples like \[(filter, mode, value), ...\]. Filter format [here](#filter-format)
> * **driver: None or seleneium.webdriver** <br>
>   Initialized selenium webdriver to be used. If None than selenium.webdriver.Chrome is used.
> * **save: False or str** <br>
>   Dataframe save location

> **Returns**:
> * **pandas.DataFrame**

### get_advanced(season, sub, group="players", schedule=None, segment="all", params=None, filters=None, driver=None, save=False)
Collecting non-boxscore data by scraping each day separatley. Works on seasons depending on sub.
> **Parameters**:
> * **season: int** <br>
>   Season from which data should be scraped
> * **sub: str** <br>
>   Stat type. 
> * **group: {"players", "teams"}** <br>
>   Choosing player or team boxscores
> * **schedule: None or pandas.DataFrame** <br>
>   Pandas DataFrame in this [format](#Preschedule-format). If None will use data returned by load_preschedule()
> * **segment: {"all", "Regular Season", "Playoffs", "PlayIn"}** <br>
>   Selecting season segments to scrape. If "all" will get all available segments that season.
> * **params: None or dict** <br>
>   Params to be added to final url. Dict should be in format {parameter: value}. Available params [here](#params-list)
> * **filters: None or list** <br>
>   Filters to be used on the table. List should be in format \[(filter, mode, value), ...\]. Filter format [here](#filter-format)
> * **driver: None or seleneium.webdriver** <br>
>   Initialized selenium webdriver to be used. If None than selenium.webdriver.Chrome is used.
> * **save: False or str** <br>
>   Dataframe save location

> **Returns**:
> * **pandas.DataFrame**

### get_player_boxscores(player, season, sub, segment="all", save=False)
Collect all player's boxscores from season or it's segment. Is the same as using get_boxscores() with group "players" and filter ("PLAYER_NAME", "E", player). Works since 1997 season.
> **Parameters**:
> * **player: str** <br>
>   Player name in format "fname lname"
> * **season: int** <br>
>   Season from which data should be scraped
> * **sub: {"traditional", "advanced", "misc", "scoring", "usage", "four-factors"}** <br>
>   Boxscore subtype 
> * **segment: {"all", "Regular Season", "Playoffs", "PlayIn"}** <br>
>   Selecting season segments to scrape. If "all" will get all available segments that season.
> * **save: False or str** <br>
>   Dataframe save location

> **Returns**:
> * **pandas.DataFrame**

### get_player_advanced(playerid, season, sub, schedule=None, segment="all", save=False)
Collecting non-boxscore data by scraping each day separatley. Works on seasons depending on sub. Is the same as using get_boxscores() with group "players" and filter ("PLAYER_NAME", "E", player)
> **Parameters**:
> * **playerid: str** <br>
>   NBA.com player ID. 
> * **season: int** <br>
>   Season from which data should be scraped
> * **sub: str** <br>
>   Stat type. 
> * **schedule: None or pandas.DataFrame** <br>
>   Pandas DataFrame in this [format](#Preschedule-format). If None will use data returned by load_preschedule()
> * **segment: {"all", "Regular Season", "Playoffs", "PlayIn"}** <br>
>   Selecting season segments to scrape. If "all" will get all available segments that season.
> * **save: False or str** <br>
>   Dataframe save location

> **Returns**:
> * **pandas.DataFrame**

### get_team_boxscores(team, season, sub, segment="all", save=False)
Collect all team's boxscores from season or it's segment. Is the same as using get_boxscores() with group "team" and filter ("TEAM_ABBREVIATION", "E", team). Works since 1997 season.
> **Parameters**:
> * **team: str** <br>
>   Team tricode (like "MIL")
> * **season: int** <br>
>   Season from which data should be scraped
> * **sub: {"traditional", "advanced", "misc", "scoring", "usage", "four-factors"}** <br>
>   Boxscore subtype 
> * **segment: {"all", "Regular Season", "Playoffs", "PlayIn"}** <br>
>   Selecting season segments to scrape. If "all" will get all available segments that season.
> * **save: False or str** <br>
>   Dataframe save location

> **Returns**:
> * **pandas.DataFrame**

### get_team_advanced(player, season, sub, schedule=None, segment="all", save=False)
Collecting non-boxscore data by scraping each day separatley. Works on seasons depending on sub. Is the same as using get_boxscores() with group "teams" and filter ("TEAM_ABBREVIATION", "E", team)
> **Parameters**:
> * **team: str** <br>
>   Team tricode (like "MIL")
> * **season: int** <br>
>   Season from which data should be scraped
> * **sub: str** <br>
>   Stat type. 
> * **schedule: None or pandas.DataFrame** <br>
>   Pandas DataFrame in this [format](#Preschedule-format). If None will use data returned by load_preschedule()
> * **segment: {"all", "Regular Season", "Playoffs", "PlayIn"}** <br>
>   Selecting season segments to scrape. If "all" will get all available segments that season.
> * **save: False or str** <br>
>   Dataframe save location

> **Returns**:
> * **pandas.DataFrame**

### get_boxscores_between(start, end, season, sub, group="players", segment="all", date_format="%Y-%m-%d", save=False)
Collect all boxscores from given time period in a season. Works since 1996-97 season.
> **Parameters**:
> * **start: str** <br>
>   First date of time period. By default should be in format YYYY-MM-DD or can be in format specified in date_format
> * **end: str** <br>
>   Last date of time period. By default should be in format YYYY-MM-DD or can be in format specified in date_format
> * **season: int** <br>
>   Season from which data should be scraped
> * **sub: {"traditional", "advanced", "misc", "scoring", "usage" (player only), "four-factors" (teams only)}** <br>
>   Boxscore subtype 
> * **group: {"players", "teams"}** <br>
>   Choosing player or team boxscores
> * **segment: {"all", "Regular Season", "Playoffs", "PlayIn"}** <br>
>   Selecting season segments to scrape. If "all" will get all available segments that season.
> * **date_format: str** <br>
>   Start and end format. Must be in datetime [format code](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)
> * **save: False or str** <br>
>   Dataframe save location

> **Returns**:
> * **pandas.DataFrame**

### get_advanced(start, end, season, sub, group="players", schedule=None, segment="all", date_format="%Y-%m-%d", save=False)
Collecting non-boxscore data by scraping each day separatley from given time period in a season. Works on seasons depending on sub.
> **Parameters**:
> * **start: str** <br>
>   First date of time period. By default should be in format YYYY-MM-DD or can be in format specified in date_format
> * **end: str** <br>
>   Last date of time period. By default should be in format YYYY-MM-DD or can be in format specified in date_format
> * **season: int** <br>
>   Season from which data should be scraped
> * **sub: str** <br>
>   Stat type. 
> * **schedule: None or pandas.DataFrame** <br>
>   Pandas DataFrame containing containg columns \["date", "type", "season"\] with dates (in format YYYY-MM-DD), type and season of gamedays to be webscraped. Dataframe returned by get_boxscores() will work here. If None will use data returned by load_preschedule()
> * **segment: {"all", "Regular Season", "Playoffs", "PlayIn"}** <br>
>   Selecting season segments to scrape. If "all" will get all available segments that season.
> * **date_format: str** <br>
>   Start and end format. Must be in datetime [format code](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)
> * **save: False or str** <br>
>   Dataframe save location

> **Returns**:
> * **pandas.DataFrame**

### load_preschedule()
Returns preschedule. By default it's preinstalled dataframe with data from 1996-97 to 2022-23 seasons.
> **Returns**:
> * **pandas.DataFrame**

### update_preschedule(data)
Updates preschedule based on given dataframe.
> **Parameters**:
> * **data: pandas.DataFrame** <br>
>   Pandas DataFrame containing containg columns \["date", "type", "season"\] with dates (in format YYYY-MM-DD), type and season of gamedays that will be added to preschedule. Dataframe returned by get_boxscores() will work here.

### set_preschedule_path(data)
Sets preschedule path.
> **Parameters**:
> * **path: None or str** <br>
>   Path from which preschedule will be loaded. If None sets to default preschedule.

### set_preschedule_path()
Restores preschedule to default.

### Preschedule format
Preschedule is based on data returned by get_boxscores() for group "players". Any dataframe upon which preschedule will be updated should have columns: 
* gameid - NBA.com game ID
* date - Date of game in format YYYY-MM-DD
* type - Type of game (must be "regular", "playoff" or "playin")
* playerid - NBA.com player ID
* team - Name of the team
* home - Home team
* away - Away team

Example: 
| gameid     | date       | season | type    | playerid | team | home | away |
|------------|------------|--------|---------|----------|------|------|------|
| 0021300721 | 2014-02-04 | 2014   | regular | 202714   | ATL  | ATL  | IND  |
| 0042000406 | 2021-07-20 | 2021   | playoff | 203114   | MIL  | MIL  | PHX  |
| 0052200201 | 2023-04-14 | 2023   | playin  | 201942   | CHI  | MIA  | CHI  |

### Available advanced data subtypes
#### Both players and teams
General:<br>
'traditional', 'advanced', 'misc', 'scoring', 'opponent', 'defense', 'estimated-advanced'<br>
Clutch:<br>
'clutch-traditional', 'clutch-advanced', 'clutch-misc', 'clutch-scoring'<br>
Playtype:<br>
'isolation', 'transition', 'ball-handler', 'roll-man', 'playtype-post-up', 'spot-up', 'hand-off', 'cut', 'off-screen', 'putbacks', 'playtype-misc',<br>
Tracking:
'drives', 'defensive-impact', 'catch-shoot', 'passing', 'touches', 'pullup', 'rebounding', 'offensive-rebounding', 'defensive-rebounding', 'shooting-efficiency', 'speed-distance', 'elbow-touch', 'tracking-post-ups', 'paint-touch'<br>
Defense dashboard:
'defense-dash-overall', 'defense-dash-3pt', 'defense-dash-2pt', 'defense-dash-lt6', 'defense-dash-lt10', 'defense-dash-gt15'<br>
Shooting Dashboard:
'shots-general', 'shots-shotclock', 'shots-dribbles', 'shots-touch-time', 'shots-closest-defender', 'shots-closest-defender-10'<br>
Other:
'shooting', 'opponent-shooting', 'hustle', 'box-outs'
#### Teams exclusive
'four-factors', 'clutch-four-factors', 'clutch-opponent', 'opponent-shots-general', 'opponent-shots-shotclock', 'opponent-shots-dribbles', 'opponent-shots-touch-time', 'opponent-shots-closest-defender', 'opponent-shots-closest-defender-10'
#### Player exclusive
'usage', 'clutch-usage'

### Filter format
Filters should be in format **(filter, mode, value)** where:<br>
**filter**:<br>
Stat name (like "OFF_LOOSE_BALLS_RECOVERED" or "PCT_PTS_PAINT"),<br>
"PLAYER_NAME",<br>
"TEAM_ABBREVIATION",<br>
"AGE",<br>
"GP",<br>
"W",<br>
"L"<br>
**mode**:<br>
"E" for eqals,<br>
"NE" for not equals,<br>
"G" for greater,<br>
"GE" for greater or equal,<br>
"L" for lower,<br>
"LE" for lower or equal,<br>
"R" for contains<br>
### Params list
**Season**:<br>
Seson in format YYYY-YY (e.g 2014-15)<br>
**SeasonType**:<br>
Regular Season, Playoffs, All Star, PlayIn, IST<br>
**PlayerPosition**:<br>
F, C, G<br>
**PlayerExperience**:<br>
Rookie, Sophomore, Veteran<br>
**DraftYear**:<br>
Draft year in format YYYY-YY (e.g 2014-15)<br>
**DraftPick**:<br>
1st Round, 2nd Round, 1st Pick, Lottery Pick, Top 5 Pick, Top 10 Pick, Top 15 Pick, Top 20 Pick, Top 25 Pick, Picks 11 Thru 20, Picks 21 Thru 30, Undrafted<br>
**Collage**:<br>
Collage name<br>
**Country**:<br>
Country code (ISO 3166)<br>
**Height**:<br>
LT 6-0, GT 6-0, LT 6-4, GT 6-4, LT 6-7, GT 6-7, LT 6-10, GT 6-10, LT 7-0, GT 7-0<br>
**TeamID**:<br>
TeamID <br>
**OpponentTeamID**:<br>
TeamID <br>
**Division**:<br>
Atlantic, Central, Southeast, Northwest, Pacific, Southwest<br>
**VsDivision**:<br>
Atlantic, Central, Southeast, Pacific, Northwest, Southwest<br>
**Conference**:<br>
East, West<br>
**VsConference**:<br>
East, West<br>
**ISTRound**:<br>
All, Group, Knockout, Semi, Quarter, Championship, East Group A, East Group B, East Group C, West Group A, West Group B, West Group C<br>
**Outcome**:<br>
W, L<br>
**Location**:<br>
Home, Road<br>
**PORound**:<br>
1, 2, 3, 4<br>
**PerMode**:<br>
Totals, PerGame, Per48, Per40, Per36, PerMinute<br>
**Month**:<br>
Value 1-12 with 1 being October<br>
**SeasonSegment**:<br>
Pre All-Star, Post All-Star<br>
