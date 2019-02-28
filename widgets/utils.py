from PyQt5.QtGui import QIcon
from math import ceil

def newIcon(icon: str):
    return QIcon(':/' + icon)

def reduceString(string: str, lengthLimit: int = 35, fill: str = '...'):
    if len(string) > lengthLimit:        
        diff = len(string) - lengthLimit + len(fill)
        string = string[:ceil(len(string) / 2) - ceil(diff / 2)] + fill + string[ceil(len(string) / 2) + ceil(diff / 2):]
    return string