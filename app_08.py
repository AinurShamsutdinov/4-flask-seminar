import asyncio
from multiprocessing import Process

import aiohttp
import requests
import threading
import time
urls = ['https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        'https://oracle.com/',
        'https://stepik.org/',
        'https://quora.com/',
        'https://yahoo.com/',
        'https://facebook.com/',
        'https://rbc.ru/',
        'https://vk.com/',
        'https://youtube.com/',
        'https://twitter.com/',
        ]


def download(url, type_name):
    response = requests.get(url)
    filename = type_name + '_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    with open(filename, "w", encoding='utf-8') as f:
        f.write(response.text)


def thread_download(download_urls):
    threads = []
    start_time = time.time()
    for url in download_urls:
        thread = threading.Thread(target=download, args=[url, "thread"])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Multiprocessor downloaded {len(download_urls)} in {time.time()-start_time:.2f} seconds")


def process_download(download_urls):
    processes = []
    start_time = time.time()
    if __name__ == '__main__':
        for url in download_urls:
            process = Process(target=download, args=(url,'process'))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
    print(f"Downloaded {len(download_urls)} in {time.time() - start_time:.2f} seconds")


async def async_download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            filename = 'asyncio_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
            with open(filename, "w", encoding='utf-8') as f:
                f.write(text)


async def main(download_urls):
    start_time = time.time()
    tasks = []
    for url in download_urls:
        task = asyncio.ensure_future(async_download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f"Downloaded {len(download_urls)} in {time.time() - start_time:.2f} seconds")


def divide_list_to_chunks(list_, n):
    return [list_[start::n] for start in range(n)]


if __name__ == '__main__':
    three_lists = divide_list_to_chunks(urls, 3)
    thread_download(three_lists[0])
    process_download(three_lists[1])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(three_lists[2]))
