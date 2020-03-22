import sys
import logging as log

from gui.app import App

if __name__ == "__main__":
    log.basicConfig(filename="log/dev.txt", level=log.INFO)
    # print the logs in the terminal
    log.getLogger().addHandler(log.StreamHandler(sys.stdout))
    app = App()
    app.mainloop()

