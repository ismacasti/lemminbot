#!/usr/bin/python3

import json 
import csv
import glob
import sys
import argparse
import os
import re

iso8601modified_regex = "(\d{4}-\d{2}-\d{2})T(\d{2}-\d{2}-\d{2})Z"
number_regex = "-?\d*\.?\d*"
fieldnames = ["time","baropressure", "dew", "rainfall", "relhumidity", "solarpower", "temp", "wind", "winddir", "windchill"]


def main(argv):
    
    parser = argparse.ArgumentParser(description="Gets all weather data from JSON to a nice CSV")
    parser.add_argument("from_dir", help="Where are the files?")
    args = parser.parse_args()

    file_iter = glob.iglob("{}/**/weather/weather*.json".format(args.from_dir), recursive=True)
    
    writer = csv.DictWriter(sys.stdout, fieldnames, dialect="unix")
    writer.writeheader()
    
    for filepath in file_iter:
        #print(filepath)
        output = dict()
        
        with open(filepath, "r") as f:
            data = json.load(f)
            #here you do data manipulation
            filename = os.path.basename(filepath)
            date_parsed = re.search(iso8601modified_regex, filename).group(1,2)
            
            output["time"] = "{} {} ".format(date_parsed[0], date_parsed[1].replace("-", ":"))
            
            
            output["baropressure"] = re.search(number_regex, data["baropressure"]).group(0)
            
            output["dew"] = data["dew"]
            
            output["rainfall"] = re.search(number_regex, data["rainfall"]).group(0)
            
            output["relhumidity"] = data["relhumidity"]
            
            output["solarpower"] = re.search(number_regex, data["solarpower"]).group(0)
            
            output["temp"] = re.search(number_regex, data["temp"]).group(0)
            
            output["wind"] = re.search(number_regex, data["wind"]).group(0)
            
            output["winddir"] = data["wind"].split()[3]
            output["windchill"] = re.search(number_regex, data["windchill"]).group(0)
            
        
            #blah blah
            
            writer.writerow(output)



if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
