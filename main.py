from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging

from tkinter import font
from tkinter import ttk
from tkinter import *
import tkinter as tk

import threading
import time
import math



class moveWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.x = 0
        self.y = 0

        self.width = width
        self.height = height

        self.root.bind("<Button-1>", self.on_button_click)
        self.root.bind("<B1-Motion>", self.move_window)

    def on_button_click(self, event):
        self.x = event.x
        self.y = event.y

    def move_window(self, event):
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, event.x_root - self.x, event.y_root - self.y))


class getKeyAndList:
    def __init__(self, mainTypingWord, mainMainList, colomInt, rooting):

        self.colomLengthInt = colomInt

        self.fullWord = ""
        self.fullList = open("30000_Words.txt", "r")
        self.fullListArray = self.fullList.read().split("\n")

        self.typingWord = mainTypingWord
        self.mainList = mainMainList

        self.root = rooting

    def returnFilterdList(self, newWord):
        listToReturn = []

        for word in self.fullListArray:
            if(word[:len(newWord)] == newWord):
                listToReturn.append(word)

        return listToReturn


    def listToMainList(self, fullWord):
        self.mainList.delete("1.0", tk.END)
        wordList = self.returnFilterdList(self.fullWord)[:100]

        finalString = ""

        colomLength = self.colomLengthInt
        coloms = math.ceil(len(wordList) / colomLength)
        addToArray = colomLength - len(wordList) % colomLength

        for i in range(addToArray):
            wordList.append(" ")

        xx = 0
        ii = 0
        bb = 0

        for i in range(len(wordList)):
            finalString += wordList[ii] + "\t\t"

            xx += 1
            ii += colomLength

            if(xx > coloms - 1):
                ii = bb + 1
                bb += 1
                xx = 0
                finalString += "\n"

        self.mainList.insert(tk.INSERT, finalString)


    def getkeyThread(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        def on_press(key):

            if(len(str(key)) == 3):

                KeyToString = str(key)[1:][:-1]
                self.fullWord += KeyToString


                self.typingWord.insert(tk.INSERT, KeyToString)

                self.listToMainList(self.fullWord)

            elif (key == keyboard.Key.backspace):
                self.fullWord = self.fullWord[:-1]
                self.listToMainList(self.fullWord)
                self.typingWord.delete("end-2c", tk.END)


            if(key == keyboard.Key.space or key == keyboard.Key.enter or key == keyboard.Key.esc):
                if(len(self.fullWord) > 0):
                    self.typingWord.delete("1.0", tk.END)
                    self.listToMainList("")
                    self.fullWord = ""



        with Listener(on_press=on_press) as listener:
            listener.join()

    def start(self):
        threading.Thread(target=self.getkeyThread).start()


class mainWindow:
    def __init__(self):
        self.root = Tk()

        self.windowWidth = 500
        self.windowHeight = 500
        self.colomInt = 5

        self.windowName = "tkinter"


    def initMainWindow(self):

        font_textbox = font.Font(family='Helvetica', size=12, weight='bold')

        self.typingWord = Text(self.root, height = 1, width = 1000, bg='#3d4247', fg="white", relief="flat", font=font_textbox)
        self.mainList = Text(self.root, height = 1000, width = 1000, bg='#2C2F33', fg="white", relief="flat", font=font_textbox, wrap="none")

        self.root.title(self.windowName)
        self.root.overrideredirect(True)

        self.root.geometry(str(self.windowWidth) + "x" + str(self.windowHeight) + "+-1900+100")

        self.typingWord.pack()
        self.mainList.pack()


    def startSpellChecker(self):

        getKeyAndList(self.typingWord, self.mainList, self.colomInt, self.root).start()
        moveWindow(self.root, self.windowWidth, self.windowHeight)

        self.root.mainloop()



main = mainWindow()

main.windowWidth = 1000
main.windowHeight = 300
main.windowName = "Spell Checker"
main.colomInt = 14

main.initMainWindow()
main.startSpellChecker()

















##
