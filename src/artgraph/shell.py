#!/usr/local/bin/python2.7
# encoding: utf-8

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import miner

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_shortdesc = "Prototype for the ArtistGraph project"

    # Setup argument parser
    parser = ArgumentParser(description=program_shortdesc, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(dest="artist", help="Name of the artist to start mining (must match the name of the Wikipedia article)")
    parser.add_argument("-d", "--depth", dest="depth", action="count", help="Set depth for graph analysis", default="5")
    
    # Process arguments
    args = parser.parse_args()
    m = miner.Miner()
    
    m.mine(args.artist)

    return 0

if __name__ == "__main__":
    sys.exit(main())
