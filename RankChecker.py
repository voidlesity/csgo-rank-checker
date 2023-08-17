import re
import clipboard
import contextlib
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def open_profile_link(steamid64):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    try:
        with driver as d:
            d.execute_script("window.open('', '_blank');")
            tab_handles = d.window_handles
            d.switch_to.window(tab_handles[-1])

            d.get("https://www.scope.gg")

            input_field = WebDriverWait(d, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "Input-module--input--1TRsz")
                )
            )
            input_field.send_keys(steamid64)

            player_field = WebDriverWait(d, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "PlayerSearchItem-module--container--3WFye")
                )
            )
            player_field.send_keys(Keys.ENTER)

            WebDriverWait(d, 10).until(
                EC.url_contains("https://app.scope.gg/dashboard/")
            )

            webbrowser.open(d.current_url)
    finally:
        driver.quit()


def main():
    player_data = clipboard.paste()
    steamids = extract_steamids(player_data)

    with contextlib.suppress(Exception):
        with ThreadPoolExecutor(max_workers=len(steamids)) as executor:
            {
                executor.submit(
                    open_profile_link, to_steamID64(steamid, as_int=False)
                ): steamid
                for steamid in steamids
            }


if __name__ == "__main__":
    main()
