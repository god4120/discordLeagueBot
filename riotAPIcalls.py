"""
Easy to access riot api endpoints and helper functions

"""
# imports
from dotenv import load_dotenv
import os
import requests
import re
from pathlib import Path

dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)
auth = os.getenv("Riot_Api_Key")

# Account-V1:


def parsepuuid(gamename, tag):
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
def topchamp(puuid, count=1):

    response = 5
    return response


if __name__ == "__main__":
    print (parsepuuid("tegotrick", "ttv"))
