import webbrowser
import re
import clipboard

STEAM_ID_REGEX = "^STEAM_"
STEAM_ID_3_REGEX = "^\[.*\]$"
ID64_BASE = 76561197960265728


def to_steamID3(steamID):
    id_str = str(steamID)

    if re.search(STEAM_ID_3_REGEX, id_str):
        return id_str

    elif re.search(STEAM_ID_REGEX, id_str):
        id_split = id_str.split(":")

        account_type = int(id_split[1])
        account_id = int(id_split[2])

        return (account_id + account_type) * 2 - account_type

    elif id_str.isnumeric():
        offset_id = int(id_str) - ID64_BASE

        account_type = offset_id % 2

        account_id = ((offset_id - account_type) // 2) + account_type

        return str(account_id * 2 - account_type)

    else:
        raise ValueError(f"Unable to decode steamID: {steamID}")


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
        steamid3 = to_steamID3(steamid)
        url = f"https://app.scope.gg/dashboard/{steamid3}"
        webbrowser.open(url)


if __name__ == "__main__":
    main()
