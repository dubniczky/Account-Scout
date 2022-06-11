import os

from requests import Session
from yaml import safe_load, safe_dump
from threading import Thread

# Load pages config
pages: None|dict = None
try:
    with open(os.path.join(os.path.dirname(__file__), 'pages.yml')) as f:
        pages = safe_load( f.read() )
except:
    print('Error, coult not read page configuration.')
    exit(1)

# Load header config
headers: None|dict = None
try:
    with open(os.path.join(os.path.dirname(__file__), 'headers.yml')) as f:
        headers = safe_load( f.read() )
except:
    print('Error, coult not read header configuration.')
    exit(1)

def printc(color: tuple[int,int,int], text: str) -> None:
    print( f"\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m" )

def scout_page(session, username, page_name, url):
    url = url.replace('{!!}', username)
    res = session.get( url )

    if (res.status_code == 200): # Success: green
        printc( (0, 255, 0),  f'[ {res.status_code} ] {page_name}: {url}' )
    elif (res.status_code == 404): # Fail: red
        printc( (255, 0, 0),  f'[ {res.status_code} ] {page_name}: {url}' )
    else: # Other: yellow
        printc( (255, 190, 0),  f'[ {res.status_code} ] {page_name}: {url}' )

def scout(username):
    session = Session()

    # Print general info
    print('Scouting user:', username)
    print('Page count:', len(pages))
    print('Headers:')
    print('========================================')
    print(safe_dump(headers, indent=2).strip())
    print('========================================')

    # Set common headers
    # Some servers only return valid responses if these are set
    session.headers.update(headers)

    # Start threads for each request
    threads = []
    for page in pages:
        page_name: str = page['name']
        url: str = page['url'].replace('{!!}', username)
        t = Thread(target=scout_page, args=(session, username, page_name, url))
        threads.append(t)
        t.start()

    # Wait for finish
    for t in threads:
        t.join()
