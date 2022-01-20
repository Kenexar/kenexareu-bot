import fileinput

with fileinput.FileInput('etc/config_preset', inplace=True) as file:
    for line in file:
        print(line.replace('config', 'esx_mg13'), end='')
