import database
import random
import threading
import queue

class Game:

    def __init__(self, speechOut, brailleOut):

        self.__db = database.Database('gametexts.db')
        self.__allGameTexts = self.__db.getAllTexts() 

        self.__speechOut = speechOut
        self.__brailleOut = brailleOut

        self.__queue = queue.Queue()
        self.__listening = False

    def __enter__(self):

        self.__speech_thread = threading.Thread(target=self.startGame)
        self.__speech_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):

        del self.__db

    def startGame(self, conn):

        return self.__mainMenu(conn)
    
    def sendInput(self, inp):

        if self.__listening:

            self.__queue.put(inp)

    def __getType(typeNum):

        if type == 1:

            return "KEYBOARD"
        
        elif type == 2:

            return "MICROPHONE"
        
        elif type == 3:

            return "RANDOMTEXT"
        
        elif type == 4:

            return "GAMEKEY"
        
        return "UNKNOWN"

    def gameDict(self, type = 0, inp = None):

        if not inp:

            return self.__getType(type)
        
        return {"type": self.__getType(type), "input": inp}

    def __getInput(self):

        self.__listening = True
        while True:

            inp = self.__queue.get()
            if inp is not None:

                self.__listening = False
                return inp

    def getRandomText(self):

        return random.choice(self.__allGameTexts)
    
    def __addText(self, text):

        self.__db.addText(text)

    def __gameMenu(self, randomText):

        while True:

            inp = self.__getInput() 

            while inp["type"] != "MICROPHONE":

                inp = self.__getInput()

            if randomText == inp["input"]: 

                self.__speechOut("Well Done! You correctly identified the word")

            else:

                self.__speechOut("Ah, sorry but that's incorrect. The phrase that we were looking for is " + randomText["input"] + " and not " + inp["input"])

            self.__speechOut("Press enter to go again or f7 to quit")

            inp = self.__getInput()

            if inp == self.gameDict(4, "f7"):

                return
            
            elif inp["type"] == "RANDOMTEXT":

                return self.__gameMenu(inp["input"])

    def __addTextMenu(self):

        self.__speechOut("Type in the phrase you want to add, or press f7 to go back")
        inp = self.__getInput()

        if inp == self.gameDict(4, "f7"):

            return
        
        self.__addText(inp["input"])

    def __mainMenu(self):

        while True:

            self.__speechOut("press 1 to begin, press 2 to add a new phrase into the game, or press f7 to quit")
            inp = self.__getInput()

            if inp == self.gameDict(1, "1"):

                self.__gameMenu()

            elif inp == self.gameDict(1, "2"):

                self.__addTextMenu()
            
            elif inp == self.gameDict(4, "f7"):

                return
        