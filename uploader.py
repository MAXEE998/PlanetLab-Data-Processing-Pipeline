import json
import multiprocessing as mp
import os
import pathlib
import queue
import sys

from googleapiclient.http import MediaFileUpload


class Uploader:

    def __init__(self, service, root_path, google_drive_root, include_folderID_in_meta=False):
        self.service = service
        self.root_path = root_path.replace(pathlib.os.sep, '/')
        self.google_drive_root = google_drive_root
        self.mapping = {google_drive_root[0]: google_drive_root[1]}
        self.include_folderID = include_folderID_in_meta

    def __create_directory(self, name, parent_name, indent):
        print(f"{' ' * indent * 4}| Creating folder {name} on {parent_name}...")
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.mapping[parent_name]]
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()
        self.mapping[parent_name+'/'+name] = file.get('id')
        print(f"{' ' * indent * 4}Folder {parent_name+'/'+name} created with id {self.mapping[parent_name+'/'+name]}|")

    def upload_file(self, name, path, parent_name, mqueue, mime_type="application/octet-stream"):
        print(f"{' ' * 12}| Uploading {name} to {parent_name}...")
        file_metadata = {
            'name': name,
            'parents': [self.mapping[parent_name]]
        }
        media = MediaFileUpload(path + '/' + name, mimetype=mime_type)
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        file_id = file.get('id')
        mqueue.put((name, file_id))
        print(f"{' ' * 12}{name} uploaded with id {file_id}|")
        return 0

    def upload_recursive(self):
        print(f"|Start uploading folder {self.root_path} to Google Drive...")
        root_name = self.root_path.split('/')
        root_name.remove("")
        root_name = root_name[-1]
        # format: (local_path, google_path, name)
        stack = [(self.root_path, self.google_drive_root[0]+'/'+root_name, root_name)]
        self.__create_directory(root_name, self.google_drive_root[0], 0)  # init
        pool = mp.Pool()
        m = mp.Manager()
        mqueue = m.Queue()

        while len(stack) != 0:
            current = stack.pop()
            # directory discovery
            walk = next(os.walk(current[0]))
            for directory in walk[1]:
                # create this directory
                self.__create_directory(directory, current[1], 1)
                stack.append((current[0] + '/' + directory,
                              current[1] + '/' + directory,
                              directory
                              ))
            # file upload
            for file in walk[2]:
                pool.apply_async(self.upload_file, args=(file, walk[0], current[1], mqueue),
                                 error_callback=lambda e: print(e, file=sys.stderr)
                                 )

        pool.close()
        pool.join()
        print(f"{self.root_path} uploaded|")
        print("producing metadata...")
        if not self.include_folderID:
            self.mapping = dict()
        while True:
            try:
                kv = mqueue.get(block=False)
                self.mapping[kv[0]] = kv[1]
            except queue.Empty:
                break

    def start(self):
        self.upload_recursive()
        meta_path = f"../metadata/{self.root_path.split('/')[-1]}.json"
        with open(meta_path, 'w') as f:
            json.dump(self.mapping, f, indent=4)

        print("----Done----")
        return meta_path
