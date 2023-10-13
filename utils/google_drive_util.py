from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDriveUtil:

    # Define the directory ID as a class attribute
    DIRECTORY_ID = "19YrLkUeOH0PWz1Xc52KQBDrQhZ_TNqRk"
    
    def find_or_create_folder(self, service, folder_name):
        
        # Query to search for a folder with the provided name in the specific directory
        query = f"'{GoogleDriveUtil.DIRECTORY_ID}' in parents and mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"

        # Execute the query
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        # Check if the folder was found
        if items:
            print(f"Folder '{folder_name}' already exists with ID: {items[0]['id']}")
        else:
            print(f"Folder '{folder_name}' not found. Creating...")
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [GoogleDriveUtil.DIRECTORY_ID]
            }
            try:
                folder = service.files().create(body=folder_metadata, fields='id').execute()
                print(f"Folder '{folder_name}' created with ID: {folder['id']}")
            except Exception as e:
                print(f"An error occurred: {e}")