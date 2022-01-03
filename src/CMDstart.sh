screen -X -S sunside-bot kill
screen -U -m -d -S sunside-bot python3.8 __main__.py

echo "Bot is started"

screen -X -S git-updater-sunside kill
screen -U -m -d -S git-updater-sunside python3.8 git-updater.py

echo "Git-Updater started"

eval "screen -r kenexardcbot"
