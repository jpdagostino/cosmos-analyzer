from rich.progress import  Progress
from pathlib import Path
import os
import requests

def download (path):
    filename = Path(path).name
    response = requests.get(path, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    
    with Progress() as progress:
        dltask = progress.add_task(f'Downloading {filename}', total=total_size)
    
        with open(filename, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                progress.update(dltask, advance=block_size)

def check (path):
    if os.path.exists(Path(path).name) or path.startswith('file://'):
        return True
    return False
    
def url_to_file (url):
    if(url.startswith("file://")):
        return url[7:]
    filename = Path(url).name
    return f'{os.getcwd()}/{filename}'