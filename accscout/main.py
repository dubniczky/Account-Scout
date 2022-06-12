#!/usr/bin/env python3
import sys
import os
from time import perf_counter, process_time
from requests import Session
from yaml import safe_load, safe_dump
from concurrent.futures import ThreadPoolExecutor


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
    start = perf_counter()
    url = url.replace('{!!}', username)
    res = session.get( url )
    elapsed = int((perf_counter() - start) * 1000.)

    # Default color: yellow
    color = (255, 211, 0)
    if (res.status_code == 200): # Success: green
        color = (38, 182, 82)
    elif (res.status_code == 404): # Fail: red
        color = (250, 41, 41)

    # Print result
    printc( color,  f'[ {res.status_code} ] ({elapsed}ms) {page_name}: {url}' )


def scout(usernames):
    session = Session()

    # Print general info
    print('Scouting user(s):', usernames)
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
    with ThreadPoolExecutor(max_workers=min(32, os.cpu_count() * 5)) as executor:
        for user in usernames:
            for page in pages:
                page_name: str = page['name']
                url: str = page['url'].replace('{!!}', user)
                threads.append( executor.submit(scout_page, session, user, page_name, url) )


def main():
    start_time = perf_counter()
    if len(sys.argv) < 2:
        print('Usage: accscout [USERNAME]... ')
        print('Scout users on popular websites.')
        exit(1)
    
    usernames = sys.argv[1:]
    scout(usernames)

    end_time = perf_counter()
    delta_time = end_time - start_time
    print('========================================')
    print(f'Completed {len(pages) * len(usernames)} requests in {delta_time}s')


if __name__ == '__main__':
    main()
