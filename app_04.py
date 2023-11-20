import threading
import time
from os import listdir
from os.path import isfile, join

mypath = '/Users/ainur/projects/PycharmProjects/4-flask-seminar/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
threads = []


def count_words(filename):
    file = open(mypath + filename, 'rt')
    data = file.read()
    words_count = len(data.split())
    print(f'filename {filename}, words count {words_count}')


for filename in onlyfiles:
    thread = threading.Thread(target=count_words, args=[filename])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
