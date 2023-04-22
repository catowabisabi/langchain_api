import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import io
from googleapiclient.http import MediaIoBaseDownload

# 許可作用域，這裡我們使用全域許可作用域
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDrive:
    def __init__(self):
        self.credentials = None
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        try:
            """驗證並獲取認證"""
            creds_file = os.path.join('config', 'credentials.json')
            token_file = os.path.join('config', 'token.pickle')

            if os.path.exists(token_file):
                # 如果存在保存的憑據，從文件中讀取它們
                with open(token_file, 'rb') as token:
                    self.credentials = pickle.load(token)
            else:
                # 否則通過瀏覽器授權
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
                self.credentials = flow.run_local_server(port=0)

                # 保存憑據以供將來使用
                with open(token_file, 'wb') as token:
                    pickle.dump(self.credentials, token)

            self.service = build('drive', 'v3', credentials=self.credentials)
        except Exception as e:
            print(f'認證失敗: {e}')
        
    def get_file_by_name(self, name):
        """通過文件名獲取Google Drive中的文件"""
        try:
            results = self.service.files().list(q=f"name='{name}'", fields="nextPageToken, files(id, name, parents)").execute()
            items = results.get('files', [])
            if not items:
                print('未找到該文件')
                return None
            else:
                print(f"找到文件：{items[0]['name']}")

                # 獲取文件的路徑
                file_id = items[0]['id']
                parents = items[0].get('parents')
                file_path = self.get_file_path(parents)
                print(f"文件路徑：{file_path}/{items[0]['name']}")

                return file_id
        except Exception as e:
            print(f"查詢文件時出現異常：{e}")
            return None
    
    def get_file_path(self, parents):
        """根據父文件夾ID獲取文件路徑"""
        if not parents:
            return 'My Drive'

        folder_id = parents[0]
        folder = self.service.files().get(fileId=folder_id, fields='name, parents').execute()
        parent_id = folder.get('parents')

        if parent_id:
            return f"{self.get_file_path(parent_id)}/{folder['name']}"
        else:
            return f"My Drive/{folder['name']}"

    def list_files(self):
        if not self.service:
            print("無法列出文件，因為認證失敗")
            return

        """列出Google Drive中的所有文件"""
        try:
            page_token = None
            while True:
                # 調用API方法列出所有文件
                results = self.service.files().list(pageSize=100, pageToken=page_token, fields="nextPageToken, files(id, name)").execute()
                items = results.get('files', [])

                # 列印所有文件名和ID
                if not items:
                    print('未找到任何文件')
                else:
                    print('找到以下文件：')
                    for item in items:
                        print(f"{item['name']} ({item['id']})")
                
                page_token = results.get('nextPageToken', None)
                if page_token is None:
                    break
        except Exception as e:
            print(f"列出文件時出現異常：{e}")
    
    def about(self):
        if not self.service:
            print("無法獲取帳戶信息，因為認證失敗")
            return
        """獲取Google Drive帳戶的基本信息"""
        try:
            # 調用API方法獲取關於帳戶的信息
            about = self.service.about().get(fields='user, storageQuota').execute()

            # 計算使用百分比和空間（以GB為單位）
            usage = int(about['storageQuota']['usage'])
            limit = int(about['storageQuota']['limit'])
            usage_gb = usage / (1024 * 1024 * 1024)
            limit_gb = limit / (1024 * 1024 * 1024)
            percent_used = (usage / limit) * 100

            # 列印帳戶信息
            print(f"用戶名: {about['user']['displayName']}")
            print(f"用戶空間: {usage_gb:.2f}GB/{limit_gb:.2f}GB ({percent_used:.2f}%)")
        except Exception as e:
            print(f"獲取帳戶信息時出現異常：{e}")
    
    def list_folders(self, folder_name=None):
        """列出Google Drive中的所有文件夾或指定名稱的文件夾"""
        if not self.service:
            print("無法列出文件夾，因為認證失敗")
            return [], []

        try:
            query = "mimeType='application/vnd.google-apps.folder' and trashed = false"
            if folder_name:
                query += f" and name='{folder_name}'"

            results = self.service.files().list(q=query, pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            folder_list = []

            if not items:
                print('未找到任何文件夾')
            else:
                print('找到以下文件夾：')
                for item in items:
                    print(f"{item['name']} ({item['id']})")
                    folder_list.append((item['name'], item['id']))

            return folder_list

        except Exception as e:
            print(f"列出文件夾時出現異常：{e}")
            return []
        
    def list_files_and_folders_in_folder(self, folder_id):
        """列出特定文件夾中的所有文件和文件夾"""
        if not self.service:
            print("無法列出文件和文件夾，因為認證失敗")
            return

        try:
            query = f"'{folder_id}' in parents and trashed = false"
            results = self.service.files().list(q=query, pageSize=100, fields="nextPageToken, files(id, name, mimeType)").execute()
            items = results.get('files', [])

            if not items:
                print('未找到任何文件或文件夾')
            else:
                print('找到以下文件和文件夾：')
                for item in items:
                    item_type = '文件夾' if item['mimeType'] == 'application/vnd.google-apps.folder' else '文件'
                    print(f"{item_type}: {item['name']} ({item['id']})")
        except Exception as e:
            print(f"列出文件和文件夾時出現異常：{e}")
    
    def list_files_in_all_folders(self, folder_name):
        folders = self.list_folders(folder_name)
        for folder_name, folder_id in folders:
            print(f"搜索文件夹... {folder_name} ({folder_id})")
            self.list_files_and_folders_in_folder(folder_id)
            print()
        return folders

    def get_file_content(self, file_id):
        if not self.service:
            print("無法獲取文件内容，因為認證失敗")
            return

        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"下載進度: {int(status.progress() * 100)}%.")

            file.seek(0)
            return file.read()

        except Exception as e:
            print(f"獲取文件事出現異常：{e}")