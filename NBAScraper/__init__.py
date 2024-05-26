from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
from datetime import datetime

_preschedule = "preschedule.csv"
TEAM_IDS = {'ATL': 1610612737, 'BKN': 1610612751, 'BOS': 1610612738, 'CHA': 1610612766, 'CHH': 1610612766,
            'CHI': 1610612741, 'CLE': 1610612739, 'DAL': 1610612742, 'DEN': 1610612743, 'DET': 1610612765,
            'GSW': 1610612744, 'HOU': 1610612745, 'IND': 1610612754, 'LAC': 1610612746, 'LAL': 1610612747,
            'MEM': 1610612763, 'MIA': 1610612748, 'MIL': 1610612749, 'MIN': 1610612750, 'NJN': 1610612751,
            'NOH': 1610612740, 'NOK': 1610612740, 'NOP': 1610612740, 'NYK': 1610612752, 'OKC': 1610612760,
            'ORL': 1610612753, 'PHI': 1610612755, 'PHX': 1610612756, 'POR': 1610612757, 'SAC': 1610612758,
            'SAS': 1610612759, 'SEA': 1610612760, 'TOR': 1610612761, 'UTA': 1610612762, 'VAN': 1610612763,
            'WAS': 1610612764}


def get_boxscores(season: int, sub: str, group: str = "players", segment: str = "all",
                  params: dict = None, filters: list = None, driver=None, save: str = False):
    if group not in ["players", "teams"]:
        raise ValueError("Argument 'group' must be 'players' or 'teams'")

    if segment == "all":
        if season >= 2020:
            segment = ["Regular Season", "PlayIn", "Playoffs"]
        else:
            segment = ["Regular Season", "Playoffs"]
    else:
        if segment not in ["Regular Season", "PlayIn", "Playoffs"]:
            raise ValueError("Argument 'segment' must be 'all', 'Regular Season', 'Playoffs' or 'PlayIn'")
        segment = [segment]

    tables = []

    # Create webdriver
    if not driver:
        driver = Chrome()

    for s in segment:
        url = f"https://www.nba.com/stats/{group}/boxscores-{sub.lower()}?" \
              f"Season={season - 1}-{str(season)[2:]}&" \
              f"SeasonType={s.replace(' ', '+')}&" \
              f"dir=A&sort=GDATE"

        # Add filters and params
        if filters:
            url += "&CF="
            f = [f"{f[0]}*{f[1]}*{f[2].replace(' ', '%20')}" for f in filters]
            url += ":".join(f)

        if params:
            url += "&"
            p = [str(k) + '=' + str(v) for k, v in params.items()]
            url += "&".join(p)

        driver.get(url)
        time.sleep(1)

        # Skip if there is no data
        try:
            driver.find_element("class name", "NoDataMessage_base__xUA61")
            print("Passed " + s)
            driver.close()
            continue
        except NoSuchElementException:
            pass

        time.sleep(1)

        select = None
        # Do not use select for team playin data
        if group == "teams" and s == "PlayIn":
            retries = 0
        else:
            retries = 10

        while retries > 0:
            try:
                select = driver.find_element("class name", "Pagination_pageDropdown__KgjBU")
                break
            except NoSuchElementException:
                print("Awaiting pagination")
                time.sleep(2)
                retries -= 1

        if (group != "teams" or s != "PlayIn") and (s != "PlayIn" or season == 202):
            if select:
                select = Select(select.find_element("class name", "DropDown_select__4pIg9"))

            try:
                select.select_by_index(0)
            except ElementClickInterceptedException:
                # Accepting cookies
                try:
                    time.sleep(0.5)
                    driver.find_element("id", "onetrust-accept-btn-handler").click()
                    time.sleep(0.5)
                except NoSuchElementException:
                    pass
                select.select_by_index(0)
            except NotImplementedError:
                pass
            except AttributeError:
                pass

        time.sleep(1)
        try:
            table = driver.find_element("class name", "Crom_table__p1iZz").get_attribute("outerHTML")
        except NoSuchElementException:
            print("Awaiting table")
            table = driver.find_element("class name", "Crom_table__p1iZz").get_attribute("outerHTML")
        driver.close()

        game_ids = re.findall("\/game\/(\d{10})", table)
        if group == "players":
            player_ids = re.findall("\/stats\/player\/(\d+)", table)
        else:
            team_ids = re.findall("\/stats\/team\/(\d+)", table)

        table = pd.read_html(table)[0]
        if len(table) > 0:
            table.columns = [c.upper().replace(u'\xa0', u' ') for c in table.columns]

            table["gameid"] = game_ids

            if group == "players":
                table["playerid"] = player_ids
                table["player"] = table["PLAYER"]
            else:
                table["teamid"] = team_ids

            table["team"] = table["TEAM"]

            table[["home", "away"]] = table["MATCH UP"].apply(
                lambda x: x.split(" vs. ") if "vs." in x else x.split(" @ ")[::-1]).tolist()

            table["date"] = table["GAME DATE"].apply(lambda x: datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d"))

            table["win"] = (table["W/L"] == "W").astype(int)

            if s == "Regular Season":
                table["type"] = "regular"
            elif s == "PlayIn":
                table["type"] = "playin"
            elif s == "Playoffs":
                table["type"] = "playoff"

            columns = list(table.columns)

            if group == "players":
                table = table[["gameid", "date", "type", "playerid", "player", "team", "home", "away"] +
                              columns[columns.index("MIN"):-9] +
                              ["win"]]
            else:
                table = table[["gameid", "date", "type", "teamid", "team", "home", "away"] +
                              columns[columns.index("MIN"):-8] +
                              ["win"]]

            tables.append(table)

    if len(tables) > 1:
        df = pd.concat(tables)
    else:
        df = tables[0]

    df = df.sort_values(["date", "gameid"])
    df["season"] = season

    if save:
        df.to_csv(save, index=False)

    return df


def get_advanced(season: int, sub: str, group: str = "players", schedule: pd.DataFrame = None, segment: str = "all",
                 params: dict = None, filters: list = None, driver=None, save: str = False):
    if str(type(schedule)) == "<class 'NoneType'>":
        schedule = load_preschedule()

    if segment == "all":
        if season >= 2020:
            segment = ["Regular Season", "Playoffs", "PlayIn"]
        else:
            segment = ["Regular Season", "Playoffs"]
    else:
        segment = [segment]

    schedule = schedule[schedule["season"] == season]
    re_date = lambda x: f"{x[5:7]}/{x[8:]}/{x[:4]}"
    re_type = {"Regular Season": "regular", "Playoffs": "playoff", "PlayIn": "playin"}
    segment = [s for s in segment if re_type[s] in set(schedule["type"])]

    dates = {s: sorted(list(map(re_date, set(schedule[schedule["type"] == re_type[s]]["date"])))) for s in segment}
    data = {s: [] for s in segment}

    if not driver:
        driver = Chrome()

    for s in segment:
        url = f"https://www.nba.com/stats/{group}/{sub.lower()}?" \
              f"Season={season - 1}-{str(season)[2:]}&" \
              f"SeasonType={s.replace(' ', '+')}&" \
              f"dir=A&sort=GDATE"

        if filters:
            url += "&CF="
            f = [f"{f[0]}*{f[1]}*{f[2].replace(' ', '%20')}" for f in filters]
            url += ":".join(f)

        if params:
            url += "&"
            p = [k + '=' + v for k, v in params.items()]
            url += "&".join(p)

        driver.get(url)

        # Accepting cookies
        try:
            time.sleep(0.5)
            driver.find_element("id", "onetrust-accept-btn-handler").click()
            time.sleep(1)
        except NoSuchElementException:
            pass
        time.sleep(1)

        # Opening filters
        try:
            driver.find_element("class name", "StatsAdvancedFiltersPanel_safArrow__EqRgu").click()
        except:
            time.sleep(0.5)
            driver.find_element("class name", "StatsAdvancedFiltersPanel_safArrow__EqRgu").click()

        try:
            date_in = driver.find_elements("class name", "SplitDateInput_sdiInput__MfE3B")
            button = driver.find_elements("class name", "Button_button__L2wUb")[1]
        except:
            time.sleep(0.5)
            date_in = driver.find_elements("class name", "SplitDateInput_sdiInput__MfE3B")
            button = driver.find_elements("class name", "Button_button__L2wUb")[1]

        for date in dates[s]:
            print(date, end=" ")
            start = time.time()
            # Date input
            try:
                date_in[0].send_keys(date)
                date_in[1].send_keys(date)
            except:
                date_in = driver.find_elements("class name", "SplitDateInput_sdiInput__MfE3B")
                date_in[0].send_keys(date)
                date_in[1].send_keys(date)

            # Clicking Get Stats button
            try:
                button.click()
            except:
                button = driver.find_elements("class name", "Button_button__L2wUb")[1]
                button.click()
            time.sleep(1)

            # Waiting for overlay to disappear
            while driver.find_element("class name", "LoadingOverlay_loader__iZ0Nm").size["height"] != 0:
                pass

            # Using pagination
            if group == "players":
                loops = 3
            else:
                loops = 0

            while loops > 0:
                try:
                    sel = driver.find_element("class name", "Pagination_content__f2at7")
                    sel = Select(sel.find_element("tag name", "select"))
                    sel.select_by_index(0)
                    break
                except NotImplementedError:
                    print(" (Did not use select)", end="")
                    break
                except NoSuchElementException:
                    time.sleep(0.5)
                    loops -= 1

            # Saving table
            try:
                driver.find_element("class name", "NoDataMessage_base__xUA61")
                print(" (No data!!!)", end="")
            except NoSuchElementException:
                table = driver.find_element("class name", "Crom_table__p1iZz").get_attribute("outerHTML")
                data[s].append((table, date))

            # Clearing date inputs
            date_in[0].send_keys(10 * Keys.BACKSPACE)
            date_in[1].send_keys(10 * Keys.BACKSPACE)

            print(f': {(time.time() - start):.3f}s')

    driver.close()

    tables = []
    for s in segment:
        player_ids = {d: re.findall("\/stats\/player\/(\d+)", t) for t, d in data[s]}
        team_ids = {d: re.findall("\/stats\/team\/(\d+)", t) for t, d in data[s]}

        dfs = {d: pd.read_html(t)[0] for t, d in data[s]}

        for d in dfs:
            dfs[d]["date"] = f"{d[-4:]}-{d[:2]}-{d[3:5]}"
            dfs[d]["type"] = re_type[s]
            if group == "players":
                dfs[d]["playerid"] = player_ids[d]
            else:
                dfs[d]["teamid"] = team_ids[d]

        dfs = pd.concat([i for i in dfs.values()])
        if group == "players":
            dfs["playerid"] = dfs["playerid"].astype("int64")
            dfs = pd.merge(dfs,
                           schedule[["date", "playerid", "gameid", "team", "home", "away"]],
                           on=["date", "playerid"])
            meta_cols = ["gameid", "date", "type", "playerid", "Player", "team", "home", "away"]

        else:
            dfs["teamid"] = dfs["teamid"].astype("int64")
            dfs = pd.merge(dfs,
                           schedule[["date", "teamid", "gameid", "team", "home", "away"]],
                           on=["date", "teamid"])
            meta_cols = ["gameid", "date", "type", "teamid", "team", "home", "away"]
        drop_cols = meta_cols + ["Team", "Age", "GP", "W", "L"]
        dfs = dfs[meta_cols + [c for c in dfs.columns if c not in drop_cols]]

        tables.append(dfs.dropna(axis=1))

    df = pd.concat(tables).sort_values(["date", "gameid"])
    df["season"] = season

    if save:
        df.to_csv(save, index=False)

    return df


def get_player_boxscores(player, season: int, sub: str, segment: str = "all", save: str = False):
    bxs = get_boxscores(season, sub, "players", segment, filters=[("PLAYER_NAME", "E", player)], save=save)
    return bxs


def get_player_advanced(playerid, season: int, sub: str, schedule: pd.DataFrame = None, segment: str = "all",
                        save: str = False):
    if str(type(schedule)) == "<class 'NoneType'>":
        schedule = load_preschedule()
        schedule = schedule[schedule["playerid"] == playerid]
        schedule = schedule[schedule["season"] == season]

    bxs = get_advanced(season, sub, "players", schedule, segment, save=save)
    bxs = bxs[bxs["playerid"] == playerid]
    return bxs


def get_team_boxscore(team, season: int, sub: str, segment: str = "all", save: str = False):
    bxs = get_boxscores(season, sub, "teams", segment, filters=[("TEAM_ABBREVIATION", "E", team)], save=save)
    return bxs


def get_team_advanced(team, season: int, sub: str, schedule: pd.DataFrame = None, segment: str = "all",
                      save: str = False):
    if str(type(schedule)) == "<class 'NoneType'>":
        schedule = load_preschedule()
        schedule = schedule[schedule["team"] == team]
        schedule = schedule[schedule["season"] == season]

    bxs = get_advanced(season, sub, "players", schedule, segment, filters=[("TEAM_ABBREVIATION", "E", team)], save=save)
    return bxs


def get_boxscores_between(start, end, season: int, sub: str, group: str = "players", segment: str = "all",
                          date_format="%Y-%m-%d", save: str = False):
    start = datetime.strptime(start, date_format).strftime("%m/%d/%Y").replace("/", "%2F")
    end = datetime.strptime(end, date_format).strftime("%m/%d/%Y").replace("/", "%2F")

    bxs = get_boxscores(season, sub, group, segment, save=save,
                        params={"DateFrom": start, "DateTo": end})
    return bxs


def get_advanced_between(start, end, season: int, sub: str, group: str = "players", schedule: pd.DataFrame = None,
                         segment: str = "all", date_format: str = "%Y-%m-%d", save: str = False):
    if str(type(schedule)) == "<class 'NoneType'>":
        schedule = load_preschedule()

    start = datetime.strptime(start, date_format).strftime("%Y-%m-%d")
    end = datetime.strptime(end, date_format).strftime("%Y-%m-%d")

    schedule = schedule[schedule["date"].between(start, end)]
    return get_advanced(season, sub, group, schedule, segment, save=save)


def load_preschedule():
    return pd.read_csv(_preschedule, dtype={"gameid": str})


def update_preschedule(data: pd.DataFrame):
    pre = load_preschedule()
    pre = pd.concat([pre, data[["gameid", "date", "type", "season", "playerid", "team", "home", "away"]]])
    pre["teamid"] = pre["team"].replace(TEAM_IDS)
    pre.drop_duplicates().to_csv(_preschedule, index=False)


def set_preschedule_path(path):
    global _preschedule
    if type(path) == str:
        _preschedule = path
    elif type(path) == 'Nonetype':
        _preschedule = 'data/preschedule.csv'


def restore_preschedule():
    pre = pd.read_csv('data/preschedule.backup.csv')
    pre.to_csv(_preschedule, index=False)
