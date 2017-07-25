#!/usr/local/bin/python3
# Script to download all Ciscolive session pdf and mp4 files. 

import requests
import logging
from sys import argv
import os.path

mp4baseurl = 'http://clnv.s3.amazonaws.com/2017/usa/'
pdfbaseurl = 'http://d2zmdbbm9feqrf.cloudfront.net/2017/usa/pdf/'

def get_session(url):
    logging.debug("Calling get_session()")
    session_filename = url.split('/')[-1]
    request = requests.get(url, stream=True)
    try:
        with open(session_filename, 'wbx') as f:
            for chunk in request.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    except IOError:
        logging.error(session_filename+" Already downloaded")
    return session_filename

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR)
    if len(argv) != 3:
       logging.error("Enter file name as First argument and file type pdf or mp4 as second argument!")
       exit()
    with open(argv[1]) as fh:
        for line in fh:
            # Extract session id
            sessionid = line.split()[0]
            logging.debug("Extracted session ID "+sessionid)
            # Selecting base url based on seccond argument
            if argv[2].strip() == 'pdf':
                url = pdfbaseurl+sessionid+'.'+argv[2].strip()
            elif argv[2].strip() == 'mp4':
                url = mp4baseurl+sessionid+'.'+argv[2].strip()
            else:
                logging.error("Missing or wrong file type, pdf or mp4 as second argument.")
                exit()
            logging.debug("Getting session {} from url {}".format(sessionid,url))
            try:
                print("Dowloading session {}".format(sessionid+'.'+argv[2]))
                print("Finished downloading " + get_session(url))
            except Exception as e:
                logging.debug(e)
                print("Issues with downloading file for session {}".format(sessionid))
                # sleep for a sec before getting another url 
