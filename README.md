# Goblin from Underworld Discord bot
Simple Discord bot by the name of Goblin from Underworld which can give you a smile or a kick.

## === This bot can ===
* Say hello to you (in his own peculiar manner)
* Give a kick to any user (with a proper image description, which is determined by you)
* Calculate complex math expressions
* Tell you what's the current day according to Tamriel calendar
* Display info about currencies (relative to Russian Rubble, yeah, because this Goblin is russian)

## === How to add Hello and Attack commands answers ===
Just add some phrases LINE BY LINE to `attack_command_answers.txt` and `hello_command_answers.txt`. Yes, LINE BY LINE separated just by a new line and nothing more.

## === How to add image description for a Kick ===
1. Create `attack_imgs` (so the directory will be on the same level as `discord_bot.py`) directory.
2. Drop images that you like (name it like `attack_1.png`, `attack_2.png` and something like that) to `attack_imgs`
3. Enjoy!

## === More features, please? When? ===
Someday.

## === Requirements ===
* [discord.py](https://discordpy.readthedocs.io/en/stable/)
* [requests](https://requests.readthedocs.io/en/latest/)
* [lxml](https://lxml.de/)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
