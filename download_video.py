#!/usr/bin/env python3

import os
import sys
import shutil

import shotgun_api3
from PySide2.QtWidgets import *

from handler import ShotgunAction
from file_dialog import FileDialog


class DownloadVideo:
    def __init__(self):
        self.protocol_url = sys.argv[1]
        self.sa = ShotgunAction(self.protocol_url)
        self.fd = FileDialog()

        SERVER_PATH = 'https://westrnd2.shotgrid.autodesk.com'
        SCRIPT_NAME = 'download_video'
        SCRIPT_KEY = '^trurx1vahkkezwyDotlzxvbs'

        self.sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)
        
        self.filter = self.sa.selected_ids_filter
        self.entity_type = self.sa.entity_type
        print(self.filter)
        print(self.entity_type)

        self.download_path = self.fd.download_path(self.sa.project['name'])
        print("downloadpath ==", self.download_path)
        if self.download_path:
            print(self.download_path)
            self.run_download()

    def run_download(self):
        for one_filter in self.filter:
            self.result_file = self.sg.find_one('Version', [one_filter], ['code', 'sg_path_to_movie', 'sg_uploaded_movie'])
            # print(self.result_file)
            self.path_to_movie = self.result_file['sg_path_to_movie']
            # self.local_file_path = "/westworld/show/%s/product" % self.sa.project['name']          
            self.file_path=self.download_path+"/%s" % self.result_file['code']

            # if self.result_file['sg_uploaded_movie'] == None:
            #     print('"sg_uploaded_movie" is None')
            # else:
            #     self.download_attachment()
                        
            # if self.result_file['sg_path_to_movie'] == None:
            #     print('"sg_path_to_movie" is None')
            # else:
            #     if os.path.isfile(self.path_to_movie):
            #         self.download_file_from_path()

            if self.result_file['sg_uploaded_movie'] == None and \
                self.result_file['sg_path_to_movie'] == None:
                print(self.result_file['code'], ", No Video...")
                pass

            elif self.result_file['sg_uploaded_movie'] == None and \
                self.result_file['sg_path_to_movie']:
                if os.path.isfile(self.result_file['sg_path_to_movie']):
                    self.download_file_from_path()
                else:
                    print("Wrong Path to Moive")

            elif self.result_file['sg_uploaded_movie'] and \
                self.result_file['sg_path_to_movie'] == None:
                self.download_attachment()
                    
            else :
                self.download_attachment()

            self.path_to_movie = None
            self.file_path = None
            self.result_file = None

    def download_attachment(self):
        # if not os.path.isdir(self.local_file_path):
        #     os.makedirs(self.local_file_path)
        if not os.path.isfile(self.file_path):
            self.sg.download_attachment(self.result_file['sg_uploaded_movie'], 
                                        file_path=self.file_path)
            print('download_attachment == ', self.result_file['code'])
        else:
            print('file exists')

    def download_file_from_path(self):
        # if not os.path.isdir(self.local_file_path):
        #     os.makedirs(self.local_file_path)
        if not os.path.isfile(self.file_path):
            shutil.copyfile(self.result_file['sg_path_to_movie'], self.file_path)
            print('download_file_from_path ==', self.result_file['code'])
        else:
            print('file exists')

# ----------------------------------------------
# Main Block
# ----------------------------------------------
if __name__ == "__main__":
    dv = DownloadVideo()
