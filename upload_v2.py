#coding=utf-8
# 引数で指定したファイルをdropboxにアップロードする
# アップロード先フォルダは固定
import dropbox
import sys
import os.path
from datetime import datetime
import requests
import time
import os
#import RPi.GPIO as GPIO
import math
import json
import boto3
import ntpath


DEBUG = 0

# s3アップロード設定
bucket_name = "YOUR_S3_BUCKET"
s3 = boto3.resource('s3')

param = sys.argv

access_token = 'ENTER_YOUR_DROPBOX_ACCESS_TOKEN'

# Dropboxのクライアント作成
client = dropbox.Dropbox(access_token)
meta = dropbox.files.FileMetadata()

upload_path = '/Slack_Snake' + param[1]
print(upload_path)

# s3にもアップロード
# todo 日付(YYYYMMDDのフォルダを作り、そこにファイルを格納)
s3_folder = datetime.today().strftime('%Y-%m-%d')
basename = ntpath.basename(param[1])
s3.Bucket(bucket_name).upload_file(param[1], 'motion/' + s3_folder + '/' + basename)

#f = open(param[1], 'rb')
with open(param[1], "rb") as f : client.files_upload(f.read(), upload_path)

# リンク作成
share_link = client.sharing_create_shared_link(upload_path, True)
print(type(share_link.url))			# unicode


filesize = os.path.getsize(param[1])
print "filesize = ", filesize, "byte"

#slack 通知


PROXIES = {
    #"http": "http://hogehoge:port/",
    #"https": "https://fugafuga:port/",
}



class SlackWrapper:
    #slack
    __token = 'ENTER_YOUR_SLACK_TOKEN'
    __channel = '#rpi_monitoring'  # channel name
    __postSlackUrl = 'https://slack.com/api/chat.postMessage'
    __icon_url = 'ENTER_YOUR_ICON_URL'  # icon url
    __username = 'USERNAME'  # user name

    def __init__(self):
        pass

    def post(self, posttext):
        params = {'token': self.__token,
                  'channel': self.__channel,
                  'text': posttext,
                  'icon_url': self.__icon_url,
                  'username': self.__username,
                  'unfurl_links': 'false'
                  }
        r = requests.post(self.__postSlackUrl, params=params, proxies=PROXIES)
        # r = requests.post(self.__postSlackUrl, params=params)


if __name__ == '__main__':
	slack = SlackWrapper()
	nowtime = datetime.now().strftime("%H時%M分%S秒")

	numdigit = int(math.log10(filesize) + 1)
	print numdigit

	if numdigit >= 7:
		byteunit = 'MBです。'
		filesize = filesize / 1048576
	else:
		byteunit = 'KBです。'
		filesize = filesize / 1024

	#filesize = float(filesize)

	basename = os.path.basename(param[1])
	message = nowtime + ' ' + basename + \
	' をアップロードしました。サイズは' + str(filesize) + byteunit + 'URL: ' + str(share_link.url)
	slack.post(message)

	#slack.post(nowtime)
