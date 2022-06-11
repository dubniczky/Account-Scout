#!/usr/bin/env python3
import sys

from accscout import scout

def main():
    username = sys.argv[1]
    scout(username)

if __name__ == '__main__':
    main()