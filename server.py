from flask import Flask, redirect, send_from_directory
from pytube import YouTube
import os
import threading
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Henlo, fren.'

@app.route('/videos/<id>')
def download_and_convert_video(id):
    
    if os.path.isdir(id):
        dir_name = "{0}/output".format(id)
        files = os.listdir(dir_name)
        file_name = filter(lambda file: file.endswith('.mp3'), files)[0]

        return send_from_directory(dir_name, file_name)
    else:
        yt = YouTube("https://youtube.com/watch?v={0}".format(id))
        yt.register_on_complete_callback(on_download_finish)
        os.mkdir(id)
        os.mkdir(os.path.join(id, 'output'))
        yt.streams.filter(subtype="mp4").first().download(id)

    return "Download initiated. Check again in a minute."

def on_download_finish(stream, file_handle):
    convert_to_mp3(file_handle.name)

def convert_to_mp3(source_path):

    dest_prefix, _ = os.path.splitext(source_path)
    dest_dir = os.path.dirname(dest_prefix)
    dest_name = os.path.basename(dest_prefix)

    dest_path = os.path.join(dest_dir, "output", dest_name + '.mp3')

    command = ['ffmpeg', '-i', source_path, '-f', 'mp3', '-ab', '192000', '-vn', dest_path]
    popen_and_call(med, command)

def med():
    print('med')

def popen_and_call(on_exit, popen_args):
    def run_in_thread(on_exit, popen_args):
        proc = subprocess.Popen(popen_args)
        proc.wait()
        on_exit()
        return
    thread = threading.Thread(target=run_in_thread, args=(on_exit, popen_args))
    thread.start()
    return thread
