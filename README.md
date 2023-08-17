## CS:GO Rank Checker

This Python program extracts Steam IDs from the "status" command and opens CS:GO player stats on scope.gg for each ID.

### How to install

You can install the program [here](https://github.com/voidlesity/csgo-rank-checker/releases)

Or you can [build it yourself](#how-to-build-it-yourself)

### How to use it

1. Go into a Match of CS:GO.
2. Type `status` into the console.
3. Copy the Output which ends with `#end`.
4. Run the Program.

### What It Does

This program performs the following tasks:

1. Extracts Steam IDs from given "status" data.
2. Converts extracted Steam IDs to SteamID64 format.
3. Opens a web browser for each SteamID64, displaying CS:GO player statistics on scope.gg.

### How to Build It Yourself

To build and run this program on your own system, follow these steps:

1. Clone this Repo or Download the RankChecker.py File.
2. Install the Requirements by typing `pip install -r requirements.txt`.
3. Build the Program by typing `pyinstaller.exe --onefile RankChecker.py.
4. The EXE should be located in a new folder called dist.
