import sys
from urllib.parse import urlparse

import requests
from tqdm import tqdm
import wget


KNOWN_DOWNLOAD_EXTENSIONS = (".zip", ".mrpack", ".properties", ".txt", ".jar")


def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (
        current / total * 100, current, total)
    # Don't use print() as it will print in new line every time.
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def download_wget(url):
    final_url = requests.head(url, allow_redirects=True).url

    # filename = (final_url.split('/')[-1])

    download_filename = wget.download(url, bar=bar_progress)

    print("\nFinished downloading", download_filename)

    return download_filename


def get_download_file_name(url, filename=None):
    if filename:
        file_name = filename
    else:
        file_name_start_pos = urlparse(url).path.rfind("/") + 1
        file_name = urlparse(url).path[file_name_start_pos:]

    if not file_name.lower().endswith(KNOWN_DOWNLOAD_EXTENSIONS):
        file_name = file_name + ".zip"

    return file_name


def download(url, **kwargs):

    print("Downloading from:", url)

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    }

    file_name = get_download_file_name(url, kwargs.get('filename'))

    r = requests.get(url, stream=True, allow_redirects=True,
                     headers=HEADERS, timeout=60)
    if r.status_code == requests.codes.ok or r.status_code == 307:
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes,
                            unit='iB', unit_scale=True)
        with open(file_name, 'wb') as file:
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
    else:
        print("Someting went wrong...")
    print("\nFinished downloading", file_name)
    return file_name
