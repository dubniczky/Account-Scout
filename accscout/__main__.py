#!/usr/bin/env python3
import sys

from accscout import scout

def main():
    if len(sys.argv) < 2:
        print('accscout [USERNAME]')
        exit(1)
    
    username = sys.argv[1]
    scout(username)

if __name__ == '__main__':
    main()