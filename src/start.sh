eval "source /home/kenexareu-bot/venv/bin/activate"

if [ $# -eq 0 ]; then
screen -X -S kenexareu-bot kill
screen -U -m -d -S kenexareu-bot python3.8 __main__.py
echo "Bot is started"
exit 1
fi

if [ $1 == "-r" ]; then
screen -X -S kenexareu-bot kill
screen -U -m -d -S kenexareu-bot python3.8 __main__.py
screen -r kenexareu-bot
echo "Bot is started"
exit 1
fi



