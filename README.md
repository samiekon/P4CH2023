# INFO-664-01 Programming for Cultural Heritage 
## Pratt Institute Spring 2023

### This project is a web-scraping workflow in Python, using a selection of musicians and composers originally featured in a 40-year audio retrospective, **Women In Electronic Music**, curated by Jon Leidecker and Barbara Golden for KPFA 94.1 FM between 2010-2013. The set-list and original radio broadcasts were archived to [UbuWeb](https://ubu.com/sound/leidecker.html), a web-based archive of avant garde materials, such as visual poetry, sound art and film. 


#### By pulling the identifying information from the track list on UbuWeb, I created a CSV to reconcile this information through Wikidata records using OpenRefine. From OpenRefine, I downloaded a simple HTML table which contains hyperlinks to each artist's Wikidata page. I used information from this table to produce a JSON file by gathering current information with Spotify's API to source their **Top Ten Songs** and **Genres** they are associated with, in addition to follower count and an image (if available). After this step was complete, I generated a simple HTML webpage to host the collected records. 


