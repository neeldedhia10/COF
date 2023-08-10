import os
import csv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Set up the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = None

# The token.json file should be generated when you set up API credentials
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Initialize the Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

# ID of the Google Drive folder containing your images
folder_id = '16SrNF5v-4HVnvKixynls20_Z-NnHGCrN'

# Initialize variables for pagination
page_token = None
all_files = []

# Retrieve list of files in the folder using pagination
while True:
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/'",
        fields="files(id, name, webViewLink), nextPageToken",
        pageToken=page_token).execute()

    files = results.get('files', [])
    all_files.extend(files)

    page_token = results.get('nextPageToken')
    if not page_token:
        break

# Write file names and sharing links to a CSV file
with open('image_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['File Name', 'Sharing Link'])

    for file in all_files:
        file_name = file['name']
        file_id = file['id']
        csvwriter.writerow([file_name, file_id])

print("CSV file created successfully.")
