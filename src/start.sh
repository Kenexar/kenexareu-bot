eval "source /home/sunside-bot/venv/bin/activate"

screen -X -S sunside-bot kill
screen -U -m -d -S sunside-bot python3.8 __main__.py

echo "Bot is started"

screen -X -S gitUpdaterSunside kill
screen -U -m -d -S gitUpdaterSunside python3.8 git-updater.py

echo "Git-Updater started"

