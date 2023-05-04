import requests
import re
import csv

req = requests.get('https://ubu.com/sound/leidecker.html')
html = req.text

musicians_list = []

for line in html.split('\n'):
    # sometimes they use a &mdash; (em dash) sometimes they just use a hyphen, so normalize it
    line = line.replace('&mdash;','-')

    # look for the title split out by this regex
    search_result = re.search(r"(.*?)\s\-\s(.*?)\(([0-9]{4})\)<br>",line)
    
    if search_result:
        # that means the regex matched on this line, so add the parts to the list
        artist = search_result.group(1)
        title = search_result.group(2)
        year = search_result.group(3)
        musicians_list.append([artist, title, year])

# write the list to a CSV file
with open('music.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Artist', 'Title', 'Year'])
    writer.writerows(musicians_list)

print("Data written to music.csv")
