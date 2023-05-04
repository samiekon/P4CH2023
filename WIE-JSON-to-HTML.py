import json
from json2html import json2html

with open('artists.json') as f:
    data = json.load(f)

table = json2html.convert(json=data)

with open('Women-In-Electronic-Music-On-Spotify.html','w') as f:
    f.write(table)