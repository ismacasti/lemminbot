#!/usr/bin/python
#https://hyperion.nvf.io/latest-image/f967a20a-7b8b-4afe-b9a5-8b45285627a9/thumbnail
#https://hyperion.nvf.io/latest-image/57068cd1-60ab-4545-915a-e568ee030fa5/thumbnail
#https://hyperion.nvf.io/latest-image/aa389088-02c6-4849-8785-da19683c50c4/thumbnail
#https://hyperion.nvf.io/latest-image/f437c149-5311-41f1-bddc-60369e69a000/thumbnail
#https://hyperion.nvf.io/latest-image/256035cb-c972-4e47-9eb9-def5dfc0f08a/thumbnail

#http://hyperion.nvf.io/latest-image/f437c149-5311-41f1-bddc-60369e69a000/?format=json

APIURL = dict()

APIURL["back-datacity"] = "https://hyperion.nvf.io/latest-image/f967a20a-7b8b-4afe-b9a5-8b45285627a9"
APIURL["side-ict"] = "https://hyperion.nvf.io/latest-image/57068cd1-60ab-4545-915a-e568ee030fa5"
APIURL["construction"] = "https://hyperion.nvf.io/latest-image/aa389088-02c6-4849-8785-da19683c50c4"
APIURL["lemminkaisenkatu"] = "https://hyperion.nvf.io/latest-image/f437c149-5311-41f1-bddc-60369e69a000"
APIURL["roof"] = "https://hyperion.nvf.io/latest-image/256035cb-c972-4e47-9eb9-def5dfc0f08a"

import os
BASE_DIR = "{0}/ismael/files/lemminbot".format(os.environ["OPENSHIFT_DATA_DIR"])


import json
import requests

def getJSONObject(url):
    #we get the jason data from the API
    json_text = requests.get(url, verify=False).text
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
    print("Lemminbot v0.2")
    #do this for all api endpoints
    for site in APIURL:
        #get the json object from API request
        obj = getJSONObject(APIURL[site])

        #get the timestamp
        ts = getDate(obj["timestamp"])
    

        #directory and file name 
        dest_dir = "{0}/{1:02}{2:02}{3:02}/{4}".format(BASE_DIR, ts.year, ts.month, ts.day, site)
        dest_filename = "{0}-{1}.jpg".format(site, obj["timestamp"].replace(":", "-"))
        path = "{0}/{1}".format(dest_dir, dest_filename)
        
        #check the destination dir, if it doesn't exist, just create it
        if not (os.path.isdir(dest_dir)):
            os.makedirs(dest_dir)
        
        #check if the file has already been downloaded
        if os.path.exists(path):
            print("We already got this {0} image!".format(site))
            continue
        
        #download file
        downloadJPEG(obj["file"], path)
        
        print("The file is downloaded to {0}.".format(path))



if __name__ == "__main__":
    # execute only if run as a script
    main()
