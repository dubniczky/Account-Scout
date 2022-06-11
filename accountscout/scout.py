from requests import Session
from yaml import safe_load

# Load pages config
pages: None|dict = None
try:
    with open("pages.yml") as f:
        pages = safe_load( f.read() )
except:
    print('Error, coult not read page configuration.')

def printc(color: tuple[int,int,int], text: str) -> None:
    print( f"\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m" )

def scout(username):
    session = Session()
    success = 0
    for page in pages:
        name: str = page['name']
        url: str = page['url'].replace('{!!}', username)
        res = session.get( page['url'] )

        if (res.status_code == 200): # Success: green
            printc( (0, 255, 0),  f'[ {res.status_code} ] {name}: {url}' )
            success += 1
        elif (res.status_code == 404): # Fail: red
            printc( (255, 0, 0),  f'[ {res.status_code} ] {name}: {url}' )
        else: # Other: yellow
            printc( (255, 190, 0),  f'[ {res.status_code} ] {name}: {url}' )
    return success
