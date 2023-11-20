import asyncio
from os import listdir
from os.path import isfile, join
import time

mypath = '/Users/ainur/projects/PycharmProjects/4-flask-seminar/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


async def count_words(filename):
    print(f'filename {filename}')
    file = open(mypath + '/' + filename, 'rt')
    data = file.read()
    words_count = len(data.split())
    print(f'filename {filename}, words count {words_count}')


async def main():
    tasks = []
    for filename in onlyfiles:
        task = asyncio.ensure_future(count_words(filename))
        tasks.append(task)
    await asyncio.gather(*tasks)

start_time = time.time()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())