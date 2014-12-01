import __init__
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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
    file1.GetContentFile('test.json')
    

def drivesave():
    file1 = drive.CreateFile({'id': '0B-KACwkTF1mEdHZaTlZIX3kzd1k'})
    file1.SetContentFile('test.json')
    file1.Upload()
