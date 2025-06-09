import os
import path
from dotenv import load_dotenv
import os
import requests
from pathlib import Path
#import champions
import json
import asyncio
from playwright.async_api import async_playwright

#getting api key for riot api
dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)
auth = os.getenv("Riot_Api_Key")


def getauth():
    return auth
def getPuuid(gamename, tag, auth):
    response = requests.get("https://americas.api.riotgames.com/"
                            "riot/account/v1/accounts/by-riot-id/" +
                            gamename + "/" + tag +
                            "?api_key=" + auth)
    return response.json()["puuid"]


def getNameTag(puuid):
    response = requests.get("https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/" +
                            puuid + "?api_key=" + auth)
    json = response.json()
    nametag = json['gameName'] + '-' + json['tagLine']
    return nametag
def getMatches(puuid, howmany, auth):
    response = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
                            puuid + "/ids" + "?start=0&count=" + str(howmany) + "&api_key=" + auth)
    return response.json()

def getMatchInfo(matchid):
    response = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/" + matchid + "?api_key=" + auth)
    return response.json()


def assignTeams(puuid):
    team1 = []
    team2 = []
    matchid = getMatches(puuid, 1)[0]
    matchinfo = getMatchInfo(matchid)
    for i in range(10):
        if i < 5:
            team1.append(
                (matchinfo['info']['participants'][i]['championName'].lower(), getNameTag(matchinfo['metadata']['participants'][i])))
        else:
            team2.append(
                (matchinfo['info']['participants'][i]['championName'].lower(), getNameTag(matchinfo['metadata']['participants'][i])))
    return team1, team2


async def getPlayerWinrate(nametag):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto("https://www.leagueofgraphs.com/summoner/na/" + nametag, timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print("Page failed to load:", e)
            await browser.close()
            return "50"

        winrate = "50"
        max_attempts = 50  # Up to ~10 seconds
        attempt = 0

        while attempt < max_attempts:
            try:
                winrate = await page.evaluate("""
                    () => {
                        const chart = $('#graphDD5').data('plot');
                        if (chart && chart.getData) {
                            const data = chart.getData();
                            if (data && data[0] && data[0].data && data[0].data[0]) {
                                return data[0].data[0];  // This should be 54.8
                            }
                        }
                        return "50";
                    }
                """)
                if winrate:
                    break
            except:
                pass
            await asyncio.sleep(0.2)
            attempt += 1

        await browser.close()
        return winrate[1]


async def getChampWinrate(champname):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto("https://www.leagueofgraphs.com/champions/builds/" + champname, timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print("Page failed to load:", e)
            await browser.close()
            return "50"

        winrate = "50"
        max_attempts = 50  # Up to ~10 seconds
        attempt = 0

        while attempt < max_attempts:
            try:
                winrate = await page.evaluate("""
                    () => {
                        const chart = $('#graphDD2').data('plot');
                        if (chart && chart.getData) {
                            const data = chart.getData();
                            if (data && data[0] && data[0].data && data[0].data[0]) {
                                return data[0].data[0];  // This should be 54.8
                            }
                        }
                        return null;
                    }
                """)
                if winrate:
                    break
            except:
                pass
            await asyncio.sleep(0.2)
            attempt += 1

        await browser.close()
        return winrate[1]


if __name__ == '__main__':
    puuid = getPuuid("ageha","na1")
    matchid = getMatches(puuid,1)[0]
    matchinfo = getMatchInfo(matchid)
    players = matchinfo['metadata']['participants']

    team1 = assignTeams(puuid)[0]
    team2 = assignTeams(puuid)[1]


    file_path = "data.json"

    with open(file_path, 'w') as json_file:
        json.dump(matchinfo, json_file, indent=4)

    print(getNameTag(puuid))
    champ_and_player_winrate1 = []
    for player in team1:
        champ_and_player_winrate1.append((player[1], asyncio.run(getPlayerWinrate(player[1])),
                                         player[0], asyncio.run(getChampWinrate(player[0]))))
        print(champ_and_player_winrate1)
    champ_and_player_winrate2 = []
    for player in team2:
        champ_and_player_winrate2.append((player[1], asyncio.run(getPlayerWinrate(player[1])),
                                         player[0], asyncio.run(getChampWinrate(player[0]))))
        print(champ_and_player_winrate2)

    team1chance = 0
    team2chance = 0
    for i in range(len(champ_and_player_winrate1)):
        team1chance += float(champ_and_player_winrate1[i][1]) * float(champ_and_player_winrate1[i][3])
    for i in range(len(champ_and_player_winrate1)):
        team1chance += float(champ_and_player_winrate2[i][1]) * float(champ_and_player_winrate2[i][3])
    team1chance = team1chance / 5
    team2chance = team2chance / 5
    print(team1chance, team2chance)