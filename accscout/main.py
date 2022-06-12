#!/usr/bin/env python3

'''
Search for a list of usernames on popular sites
'''

from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import sys
import os
import requests
from yaml import safe_load, safe_dump


# Load pages config
pages: None|dict = None
try:
    file = os.path.join(os.path.dirname(__file__), 'pages.yml')
    with open(file, 'r', encoding='utf8') as f:
        pages = safe_load( f.read() )
except IOError:
    print('Error, coult not read page configuration.')
    sys.exit(1)


# Load header config
headers: None|dict = None
try:
    file = os.path.join(os.path.dirname(__file__), 'headers.yml')
    with open(file, 'r', encoding='utf8') as f:
        headers = safe_load( f.read() )
except IOError:
    print('Error, coult not read header configuration.')
    sys.exit(1)


def printc(color: tuple[int,int,int], text: str) -> None:
    '''Print colored text output'''
    print( f"\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m" )


def scout_page(session, username, page_name, url):
    '''Download a page and print the status result'''
    start = perf_counter()
    url = url.replace('{!!}', username)
    res = session.get(url)
    elapsed = int((perf_counter() - start) * 1000.)

    # Default color: yellow
    color = (255, 211, 0)
    if res.status_code == 200: # Success: green
        color = (38, 182, 82)
    elif res.status_code == 404: # Fail: red
        color = (250, 41, 41)

    # Print result
    printc( color,  f'[ {res.status_code} ] ({elapsed}ms) {page_name}: {url}' )


def scout(usernames: list[str]) -> None:
    '''Search for a list of usernames on popular sites'''
    session = requests.Session()

    # Print general info
    thread_count = min(32, os.cpu_count() * 5)
    print('Scouting user(s):', usernames)
    print('Page count:', len(pages))
    print('Maximum threads:', thread_count)
    print('Headers:')
    print('========================================')
    print(safe_dump(headers, indent=2).strip())
    print('========================================')

    # Set common headers
    # Some servers only return valid responses if these are set
    session.headers.update(headers)

    # Start threads for each request
    threads = []
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for user in usernames:
            for page in pages:
                page_name: str = page['name']
                url: str = page['url'].replace('{!!}', user)
                threads.append( executor.submit(scout_page, session, user, page_name, url) )


def main():
    '''Main CLI entry point for accscout'''
    start_time = perf_counter()
    if len(sys.argv) < 2:
        print('Usage: accscout [USERNAME]... ')
        print('Scout users on popular websites.')
        sys.exit(1)

    usernames = sys.argv[1:]
    scout(usernames)

    end_time = perf_counter()
    delta_time = end_time - start_time
    print('========================================')
    print(f'Completed {len(pages) * len(usernames)} requests in {round(delta_time, 2)}s')


if __name__ == '__main__':
    main()
