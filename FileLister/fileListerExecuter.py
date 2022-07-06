import sys
import importlib
sys.path.append("/Users/jingtan/Documents/GitHub/Python-Tools-for-Maya/FileLister")

import fileLister
importlib.reload(fileLister)
fileLister.UI()


