"""
Easy to access riot api endpoints and helper functions

"""
# imports
from dotenv import load_dotenv
import os
import requests
import re
from pathlib import Path
import champions

dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)
auth = os.getenv("Riot_Api_Key")

# Account-V1:


def parsepuuid(gamename, tag):
    """
    Parses the players PUUID from account info
    Args: 2 strings gamename and a 3 letter tagline
    return: A string type containing the players PUUID
    """
    return account_by_riot_id(gamename, tag).text.split('"')[3]


def account_by_riot_id(gamename, tagline):
    """
    Retrieves account information by riot id
    Args: 2 strings gamename and a 3 letter tagline
    :return: A response type containing Puuid, gamename and tagline
    """
    url = "https://americas.api.riotgames.com"
    endpoint = ("/riot/account/v1/accounts/by-riot-id/" + gamename + "/" + tagline
                + "?api_key=" + auth)
    response = requests.get(url+endpoint)
    return response


# Champion-Mastery-V4:
def champsplayed(puuid):
    """
       Provides a list of all champs played and their level
       Args: A string puuid
       return: An array of strings champs played and their level
       """
    url = "https://na1.api.riotgames.com"
    endpoint = ("/lol/champion-mastery/v4/champion-masteries/by-puuid/" + puuid + "/"
                + "?api_key=" + auth)
    response = requests.get(url + endpoint)

    response = response.text
    response = re.split(r'[;,:"\s]+', response)
    champs = []
    level = []
    played = []

    for index, item in enumerate(response):
        spot = index
        if response[spot] == 'championId':
            try:
                champs.append(champions.champion_Names[int(response[spot+1])])
                level.append(response[spot+3])
            except KeyError:
                print('KeyError:' + response[spot+1] + 'not found')
    combo = 'Name: Level'
    played.append(combo)
    for champ in champs:
        combo = champ + ': ' + level[champs.index(champ)]
        played.append(combo)

    return played


def top3(puuid):
    """
    Provides a string of the top 3 champs played and their level
    args: A string puuid
    return: A string type containing the top 3 champs played and their level
    """
    top3 = ''
    i =0
    while i < 3:
        top3 += champsplayed(puuid)[i] + '\n'
        i += 1
    return top3


def totalchamplevel(puuid):
    """
    Provides the total mastery score obtained from all champs
    args: A string puuid
    return: A string type containing the total mastery score obtained from all champs
    """
    url = "https://na1.api.riotgames.com"
    endpoint = "/lol/champion-mastery/v4/scores/by-puuid/" + puuid + "?api_key=" + auth
    response = requests.get(url + endpoint).text
    return response


if __name__ == "__main__":
    name = "tegotrick"
    tag = "ttv"
    puuid = parsepuuid(name, tag)
    print(totalchamplevel(puuid))
