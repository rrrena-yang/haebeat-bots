# kcdf-bot

A Discord bot that checks views and likes data of KCDF submissions by user command. Built using web-scraping techniques (Selenium Webdrivers, Scrapy, Beautiful Soup 4)

How to use:
1. run python3 renas-bot.py
2. To check views/likes of dance1 by dancecrewA: $bot_check: dancecrewA dance1
e.g. $bot_check: Haebeat Paint The Town
(only putting part of dance name is also OK, e.g. $bot_check: Haebeat Paint The, however CASES must be correct)
(dance crew name can only be ONE WORD)
3. If you forget what dance is the dance crew doing. You can access a list of dancecrews with their song names by: $bot_what. If you think there is more options you would like me to add to the list, lmk and I'll add it!
4. To access a current leaderboard of submissions with the most views/likes: $bot_leaderboard view OR $bot_leaderboard like
