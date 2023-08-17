import webbrowser
import re
import clipboard


STEAM_ID_REGEX = "^STEAM_"
STEAM_ID_3_REGEX = "^\[.*\]$"
ID64_BASE = 76561197960265728


def to_steamID64(steamID, as_int=False):
    id_str = str(steamID)
    id_split = id_str.split(":")

    if id_str.isnumeric():
        if len(id_str) != 17:
            raise ValueError(f"Incorrect length for steamID64: {id_str}")
        return int(id_str) if as_int else id_str
    elif re.search(STEAM_ID_REGEX, id_str):
        account_type = int(id_split[1])
        account_id = int(id_split[2])

    elif re.search(STEAM_ID_3_REGEX, id_str):
        account_id3 = int(id_split[2][:-1])

        account_type = account_id3 % 2

        account_id = (account_id3 - account_type) // 2

    else:
        raise ValueError(f"Unable to decode steamID: {steamID}")

    id64 = ID64_BASE + (account_id * 2) + account_type

    return id64 if as_int else str(id64)


def extract_steamids(player_data):
    steamids = []
    lines = player_data.strip().split("\n")
    for line in lines:
        parts = line.split()
        for part in parts:
            if part.startswith("STEAM_"):
                steamid = part.strip('"')
                steamids.append(steamid)
    return steamids


def main():
    player_data = clipboard.paste()
    steamids = extract_steamids(player_data)

    for steamid in steamids:
        steamid64 = to_steamID64(steamid, as_int=False)
        url = f"https://csgostats.gg/player/{steamid64}"
        webbrowser.open(url)


if __name__ == "__main__":
    main()
