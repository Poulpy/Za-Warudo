import sys
import logging as log

from gui.app import App

if __name__ == "__main__":
    log.basicConfig(filename="log/dev.txt", level=log.DEBUG)
    app = App()
    app.mainloop()

