import json
import sys
import os 

files = sys.argv[1:]

for file in files:
    if os.path.isdir(file): continue
    with open(file, "r") as wiki_file:
        for line in wiki_file:
            if line.strip():
                try:
                    print(json.loads(line.strip())['text'])
                except:
                    pass
