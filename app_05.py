import threading
import time
from multiprocessing import Process
from os import listdir
from os.path import isfile, join

mypath = '/Users/ainur/projects/PycharmProjects/4-flask-seminar/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
processes = []


def count_words(filename):
    file = open(mypath + '/' + filename, 'rt')
    data = file.read()
    words_count = len(data.split())
    print(f'filename {filename}, words count {words_count}')


if __name__ == '__main__':
    for filename in onlyfiles:
        process = Process(target=count_words, args=(filename,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
