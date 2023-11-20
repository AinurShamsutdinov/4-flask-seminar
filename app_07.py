import asyncio
import threading
import time
import random
from multiprocessing import Process, SimpleQueue


rand_arr = [random.randint(1, 100) for i in range(1000_000)]
thread_arr_sum = 0
async_arr_sum = 0


def sum_arr_num():
    sum_arr = 0
    for i in rand_arr:
        sum_arr += rand_arr[i]
    print(f'sum synchronous {sum_arr}')


def threads_sum_numbers(num):
    base = 100_000
    sum_arr = 0
    for i in range((num - 1) * base, num * base):
        sum_arr += rand_arr[i]
    global thread_arr_sum
    thread_arr_sum = thread_arr_sum + sum_arr


def process_sum_numbers(num, queue_sum):
    base = 100_000
    sum_arr = 0
    for i in range((num - 1) * base, num * base):
        sum_arr += rand_arr[i]
    queue_sum.put(sum_arr)


async def async_sum_numbers(num: int):
    base = 100_000
    sum_arr = 0
    for i in range((num - 1) * base, num * base):
        sum_arr += rand_arr[i]
    global async_arr_sum
    async_arr_sum += sum_arr


def thread_sum():
    threads = []
    start_time = time.time()
    for num in range(10):
        thread = threading.Thread(target=threads_sum_numbers, args=[num])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    global thread_arr_sum
    print(f'thread_arr_sum {thread_arr_sum} time = {end_time - start_time}')


def process_sum():
    processes = []
    queue_sum = SimpleQueue()
    start_time = time.time()
    for num in range(10):
        process = Process(target=process_sum_numbers, args=(num, queue_sum))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end_time = time.time()
    sum_process = 0
    while not queue_sum.empty():
        sum_process += queue_sum.get()
    print(f'multiprocesser sum of numbers = {sum_process} time = {end_time - start_time}')


async def async_sum():
    tasks = []
    start_time = time.time()
    for num in range(10):
        task = asyncio.ensure_future(async_sum_numbers(num))
        tasks.append(task)
    await asyncio.gather(*tasks)
    end_time = time.time()
    print(f'asynchronous sum of numbers = {async_arr_sum} time = {end_time - start_time}')


if __name__ == '__main__':
    sum_arr_num()
    thread_sum()
    process_sum()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_sum())
    loop.close()
