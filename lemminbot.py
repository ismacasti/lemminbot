#!/usr/bin/python

APIURL = "https://hyperion.nvf.io/latest-image/f437c149-5311-41f1-bddc-60369e69a000/?format=json"

BASE_DIR = "."

import json
import requests
import os

def getJSONObject(url):
    #we get the jason data from the API
    json_text = requests.get(url).text
    #and we parse it and return it
    return json.loads(json_text)

def getDate(rfc3339):
    import datetime as dt
    return dt.datetime.strptime(rfc3339, '%Y-%m-%dT%H:%M:%SZ')

def downloadJPEG(url, dest_path):
    r = requests.get(url, stream=True)
    f = open(dest_path, "wb")
    f.write(r.content)
    r.close()
    f.close()
    
        
        

def main():
    print("Lemminbot v0.1")
    #get the json object from API request
    obj = getJSONObject(APIURL)
    
    #get the timestamp
    ts = getDate(obj["timestamp"])
    
    #directory and file name 
    dest_dir = "{}/{}{}{}".format(BASE_DIR, ts.year, ts.month, ts.day)
    dest_filename = "{}.jpg".format(obj["timestamp"])
    path = "{}/{}".format(dest_dir, dest_filename)
    
    #check the destination dir, if it doesn't exist, just create it
    if not (os.path.isdir(dest_dir)):
        os.makedirs(dest_dir)
    
    #check if the file has already been downloaded
    if os.path.exists(path):
        print("We already got this image!")
        raise SystemExit(0)
    
    #download file
    downloadJPEG(obj["file"], path)
    
    print("The file is downloaded to {}.".format(path))



if __name__ == "__main__":
    # execute only if run as a script
    main()
    
