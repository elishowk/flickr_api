#!/usr/bin/env python3

import os
import sys
from flickrapi import FlickrAPI

# Retrieve API key and Secret from the environment
API_KEY = os.environ.get('FLICKR_API_KEY')
API_SECRET = os.environ.get('FLICKR_API_SECRET')

if not API_KEY or not API_SECRET:
    print("Please set the FLICKR_API_KEY and FLICKR_API_SECRET environment variables.")
    sys.exit(1)

# Create Flickr API instance
flickr = FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

# Check if authentication is required and perform the authentication
def authenticate():
    if not flickr.token_valid(perms='write'):
        print("Token expired or not valid. Authenticating...")
        flickr.get_request_token(oauth_callback='oob')
        auth_url = flickr.auth_url(perms='write')
        print(f"Please visit this URL to authenticate: {auth_url}")
        
        # Prompt user for verifier code from the website
        verifier = str(input("Verifier code: "))
        flickr.get_access_token(verifier)

def upload_to_flickr(directory):
    """Recursively upload all images in directory to Flickr, set as private."""
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                filepath = os.path.join(root, file)
                print(f"Uploading {filepath}...")
            try:
                flickr.upload(filename=filepath, is_public=0, is_friend=0, is_family=0, format='rest')
                print(f"Uploaded {filepath} successfully!")
            except Exception as e:
                # Check if the error message contains the specific error we're looking for
                if "Expecting value: line 1 column 1 (char 0)" in str(e):
                    print(f"Uploaded {filepath} but encountered a response parsing error. Error: '{e}'")
                else:
                    print(f"Failed to upload {filepath}. Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./script_name <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        sys.exit(1)
    
    authenticate()
    upload_to_flickr(directory)
