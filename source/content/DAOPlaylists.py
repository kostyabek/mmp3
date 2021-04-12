import sqlite3


class DAOPlaylists:
    def __init__(self):
        self.__connection = sqlite3.connect("playlists.db")
        self.__cursor = self.__connection.cursor()

    def one(self):
        pass