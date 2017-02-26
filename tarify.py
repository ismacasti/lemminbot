#!/usr/bin/python3
import os
import sys
import re
import argparse
import lemminbot
import subprocess
import shutil
folder_date_regex = "^[0-9]{8,8}$"

tar_command = "LANG=C tar --create --file '{output_file}' --verbose -C '{input_dir}' ."



def main(argv):
    folder_date_compiled = re.compile(folder_date_regex)
    
    parser = argparse.ArgumentParser(description="Puts pics to nice tars")
    parser.add_argument("from_dir", help="Where are the files?")
    parser.add_argument("to_dir", help="Where to put the tars?")
    args = parser.parse_args()

    
    for date in os.listdir(args.from_dir):
        if (folder_date_compiled.match(date)):
            lemminbot.checkAndCreateDir(os.path.join(args.to_dir, date))
            print("mkdir {}".format(os.path.join(args.to_dir, date)))
        else:
            continue
            
        sites = os.listdir(os.path.join(args.from_dir, date))
        for site in sites:
            if(os.path.isdir(os.path.join(args.from_dir, date, site))): #if it's a directory, tar it to dest
                output_file = "{}.tar".format(os.path.join(args.to_dir, date, site))
                input_dir = os.path.join(args.from_dir, date, site)
                command = tar_command.format(output_file=output_file, input_dir=input_dir)
                print(command)
                subprocess.run(command,  stderr=subprocess.PIPE, check=True, shell=True) 
            else: #if it's a file, just copy it
                shutil.copy2(os.path.join(args.from_dir, date, site), os.path.join(args.to_dir, date, site))
                print("cp {}/{}".format(input_dir, site))



if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
