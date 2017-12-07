import sys
import json
import os

'''A program to transform Facebook posts for NLTK '''

SOURCE_FILE_DIR = 'YOUR_DIR_HERE' # replace with your folder
TRANSFORM_FILE_DIR = 'YOUR_DIR_HERE' # replace with your folder

def print_messages(filename, outfp):
	with open(filename, 'r') as fp:
		for line in fp.readlines():
                    d = json.loads(line)
                    outfp.write(d['message'] + '\n')


def main():
	for f in os.listdir(SOURCE_FILE_DIR):
		with open(TRANSFORM_FILE_DIR + f, 'w+') as outfile:
			print_messages(SOURCE_FILE_DIR+f, outfile)

main()