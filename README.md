ArtistGraph
===========

ArtistGraph Project for Big Data CSCI.620.02 (RIT)

Requirements
============

* mwparserfromhell (http://mwparserfromhell.readthedocs.org/)
* pymw (http://pymw.sourceforge.net/)
* mysql-python (http://mysql-python.sourceforge.net/)
* enum (https://pypi.python.org/pypi/enum/)

Instructions
============

* Setup your my.cnf file using the sample file provided
* Run the program from this directory using

  $ python artistgraph/shell <artist name>
  
  you can use the -d flag for debugging:
  
  $ python artistgraph/shell -d <artist name>