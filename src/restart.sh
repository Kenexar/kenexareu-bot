eval "source /home/kenexareu-bot/venv/bin/activate"

screen -X -S kenexareu-bot kill
screen -U -m -d -S kenexareu-bot python3.8 __main__.py