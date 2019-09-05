import json
import sys

parking_lot = []
accepted = []

parking_lot = open("parking_lot.txt", "w")

def is_ambiguous(pattern):
    if len(pattern['super']) > 1 or any(len(sub) > 1 for sub in pattern['sub']):
        return True
    return False

def get_links(patter):
    for sub in pattern['sub']:
        yield (patter['super'], sub)  
    # return (patter['super'], sub)  

for line in sys.stdin:
    if line.strip():
        pattern = json.loads(line)

        if is_ambiguous(pattern):
            parking_lot.write(line)
        else:
            accepted.extend(get_links(pattern))

        