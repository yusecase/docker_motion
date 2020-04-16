# Dockerでレオパ見守りPGを動かす
# やること
# motionをinstall
# 以下PGをホストからコピーする
# /etc/motion/motion.conf
# /home/pi/rpi_workspace/motion_upload/upload_v2.py 
# /home/pi/slackbot/slack_notice.py
# usbカメラの設定調べる


FROM raspbian/jessie
# motion インストール
RUN apt-get update
#RUN apt-get upgrade -y
RUN apt-get install -y motion

# python 3.6.0 インストール todo 3以上にする
RUN apt-get install -yq wget build-essential gcc zlib1g-dev
WORKDIR /root/
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz \
				&& tar zxf Python-3.6.0.tgz \
				&& cd Python-3.6.0 \
				&& ./configure \
				&& make altinstall
ENV PYTHONIOENCODING "utf-8"

WORKDIR /

RUN apt-get install -y python
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN pip install -U pip

RUN pip install dropbox
RUN pip install boto3
RUN pip install awscli


#ディレクトリ作成　todo ディレクトリ構成きれいに
RUN mkdir -p /home/pi/
RUN mkdir -p /home/pi/rpi_workspace
RUN mkdir -p /home/pi/rpi_workspace/motion_upload
RUN mkdir -p /home/pi/slackbot

# ファイルコピー
COPY motion.conf /etc/motion
COPY upload_v2.py /home/pi/rpi_workspace/motion_upload/
COPY slack_notice.py /home/pi/slackbot/

# ポートセット
EXPOSE 80 8081

#CMD ["/bin/bash"]
