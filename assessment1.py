#!/usr/local/bin/python3

from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def checkAuth():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        service = build('drive', 'v3', credentials=creds)
        return service
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

def getContents(service, folderID):
    response = service.files().list(q="",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
    for i in response.get('files', []):
        print ('Found file: ' + i.get('name'), i.get('id'))
        # Process change
        # print 'Found file: %s (%s)' % (file.get('name'), file.get('id'))
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        return



def main():
    service = checkAuth()
    #getContents("1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V")
    getContents(service, "1y-mEO3jzEnT-dgu81jC_CaCVLhk6yxPh") # test folder






    # results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])
    # if not items:
    #     print('No files found.')
    #     return
    # print('Files:')
    # for item in items:
    #     print(u'{0} ({1})'.format(item['name'], item['id']))



if __name__ == '__main__':
    main()