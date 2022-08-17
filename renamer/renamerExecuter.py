import importlib

renamerPath = "/Users/jingtan/Dropbox (Tripledot)/My Mac (Jings-MacBook-Pro.local)/Documents/GitHub/Python-Tools-for-Maya/renamer"
sys.path.append(renamerPath)
# doesSysPathExist = os.path.exists(renamerPath)

import renamer
importlib.reload(renamer)
renamer.UI()