#!/usr/local/bin/python2.7
# encoding: utf-8

import sys

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import miner

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # Setup argument parser
    parser = ArgumentParser(description="ArtistGraph Project", formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(dest="artist", help="Name of the artist to start mining (must match the name of the Wikipedia article)")
    parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="Turn debugging on", default=False)
    parser.add_argument("-n", "--depth", dest="depth", help="Set depth for graph analysis", default="5")
    
    # Process arguments
    args = parser.parse_args()
    m = miner.Miner(args.debug)
    
    m.mine(args.artist)

    return 0

if __name__ == "__main__":
    sys.exit(main())
