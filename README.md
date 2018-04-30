# visproj-pub

visproj-pub repository

File Locations:
    
    Source Files: /visproj-pub/src

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

To run:
    
    python3 main.py

Notes on EEG data:

    Currently works with .txt files
    File should be arranged as follows:
        1st row: time stamps
        following rows: data

    All data points as well as time stamps should be delimited by a comma ","
