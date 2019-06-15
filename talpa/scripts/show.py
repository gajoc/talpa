import argparse
import json
from pprint import pprint

ap = argparse.ArgumentParser()
ap.add_argument('json_file', help='path to json file to display',
                nargs='?',
                default='../data/search_result-0b844514-8ee3-11e9-9bfb-080027183839.json')
args = ap.parse_args()


if __name__ == '__main__':
    data = json.load(open(args.json_file, 'r'))
    pprint(data)
