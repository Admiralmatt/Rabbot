import __init__
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import logging

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

def driveload():
    # Create GoogleDriveFile instance
    file1 = drive.CreateFile({'id': '0B-KACwkTF1mEdHZaTlZIX3kzd1k'})
    file1.GetContentFile('data.json')
    
def drivesave():
    file1 = drive.CreateFile({'id': '0B-KACwkTF1mEdHZaTlZIX3kzd1k'})
    file1.SetContentFile('data.json')
    try:
        file1.Upload()
    except Exception as a:
        pass

def drivelogin():
    # Create GoogleDriveFile instance
    file2 = drive.CreateFile({'id': '0B-KACwkTF1mERkhIR1k0Y0Z3R0E'})
    return file2.GetContentString()
