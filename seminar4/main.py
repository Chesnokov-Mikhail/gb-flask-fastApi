import threading
import multiprocessing
import asyncio
# import aiohttp
import requests
from pathlib import Path
import argparse
import time

# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
# Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию
# изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем
# времени выполнения программы.

# Многопоточность
def download(url):
    response = requests.get(url)
    filename = Path(url).name
    print(f'Имя файла {filename}')
    with open(filename, 'wb') as f:
        f.write(response.content)
        print(f'Downloaded {url} in {time.time()-start_time:.2f}seconds')

threads = []
start_time = time.time()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Argument parser')
    parser.add_argument('urls', metavar='urls', type=str, nargs=1, help='Enter url image download')
    args = parser.parse_args()
    urls = args.urls
    # Многопоточность
    for url in urls:
        thread = threading.Thread(target=download, args=[url])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
