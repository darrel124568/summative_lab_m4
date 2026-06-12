import json

def read(filename):
    with open(filename) as f:
        return(json.load(f))