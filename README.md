ArtistGraph
===========

ArtistGraph Project for Big Data CSCI.620.02 (RIT)

Requirements
============

* mwparserfromhell (http://mwparserfromhell.readthedocs.org/)
* pymw (https://github.com/eheien/pymw)
* mysql-python (http://mysql-python.sourceforge.net/)
* BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/)

The UI is based requires

* QtQuick (https://qt-project.org/doc/qt-5.1/qtquick/qtquick-index.html)
* PythonQt4 (http://www.riverbankcomputing.com/software/pyqt/intro) 
  
Instructions
============

* Setup your my.cnf file using the sample file provided
* Update your Python path to be able to use the modules provided here

  $ export PYTHONPATH=$PYTHONPATH:<full path to src folder> 

* Run the program from this directory using

  $ python src/artgraph/shell.py <artist name>
  
you can use the -d flag for debugging:
  
  $ python src/artgraph/shell.py -d <artist name>
  
To run the UI use the shell in the UI submodule

  $ python src/artgraph/ui/shell.py
  
Credits
=======

The font in the logo is
http://www.fontspace.com/khryskreations/kbshotinthedark

The background is
https://picasaweb.google.com/lh/photo/tQESi8xiZ3Z6plpz2QWlyNeBuGY5nSD5sJ6y0N6PJEk
