import fileinput
from slpp import slpp as lua

data = {'Shared': [{'model': 'buccaneer2', 'label': 'Gang Fahrzeug', 'price': 8000}], 'boss': [{'model': 'jugular', 'label': 'Boss Fahrzeug', 'price': 8000}]}

print(lua.encode(data), end='')
print(lua.decode("""Config.AuthorizedVehicles = {
	["Shared"] = {
		{
		["model"] = "buccaneer2",
		["label"] = "Gang Fahrzeug",
		["price"] = 8000
	}
	},
	["boss"] = {
			{
			["model"] = "jugular",
			["label"] = "Boss Fahrzeug",
			["price"] = 8000
		}
	}}"""), end='')

# str_ = ''
#
# with fileinput.FileInput('etc/config_preset', inplace=True) as file:
#     for line in file:
#         print(line.replace('config', str_), end='')
