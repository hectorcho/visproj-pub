# visproj-pub

This repository is the public repository storing the source files as well
as the visproj executable.

File Locations:
    
    Source Files: /visproj-pub/gui/src
    Executable File: /visproj-pub/gui/dist
    Package Files: /visproj-pub/gui/build

Dependencies:

    Python 3
    PyQt5
    pyqtgraph
    numpy
    pandas

Notes:

    It has been known that using conda distributed Python will break PyQt5.
    To avoid failures, please consider using Python3 distributed as part of
    your operating system. 

    
For MacOS:
    
    Do NOT use Homebrew to install PyQt5. 
    Please use the following commands:
    1. python3 -m pip install PyQt5
    OR
    2. pip3 install PyQt5

    If you do not trust your pip3 to be configured correctly, please use the
    first command
