# SpringBoot Actuator JSON Data Scraper

import requests
import os
import json
import argparse
import time
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

def scrap(url):
	results = []
	try:
		url = url.strip()
		print(f"Enumerating --- {url}")
		url = f"https://{url}/actuator;/"
		res = requests.get(url)
		if res.status_code == 200:
			data = res.json()
			if data:
				links = data["_links"]
				for links_name, links_value in links.items():
					for endpoints_name, endpoints_value in links_value.items():
						if endpoints_name == "href":
							print(endpoints_name)
							results.append(endpoints_name)
	except Exception as e:
		print(e)


def process_file(filename, output_file):
	try:
		with open(filename, "r") as urls, open(output_file, "a") as output:
			for url in urls:
				if url:
					results = scrap(url,output_file)
					for elem in results:
						output.write(f"{elem}\n")
					time.sleep(1)
	except FileNotFoundError:
		print("File not found!")
		exit()


def main():
    parser = argparse.ArgumentParser(description="SpringBoot Actuator JSON Data Scraper")
    parser.add_argument("-u", "--url", type=str, help="url to scrap")
    parser.add_argument("-f", "--file", type=str, help="file path of urls to scrap")
    parser.add_argument("-o", "--output", type=str, help="output file path (will not save if single url)", default="output.txt")
    args = parser.parse_args()

    output = args.output
    url = args.url
    file = args.file

    if url:
    	scrap(url, output)
    elif file:
    	process_file(file, output)


if __name__ == "__main__":
    main()
