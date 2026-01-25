#imports
from gamelib.data.version import print_version

#main lib class
class Engine():
    #Function at initiliazion engine in project
    def __init__(self):
        print("Engine was Started!")

    def print_engine_info(self):
        print_version()

    #Function at the end of the game
    def __del__(self):
        print("Engine ended his worked!")
