from tkinter import simpledialog
from customtkinter import *
import pandas as pd
import sqlite3
import os

# TABLE: Candidates
# CandidateID INT PRIMARY KEY
# CandidateName VARCHAR
# PartyName VARCHAR
# PartyArt VARCHAR (stores the image name of the party's art present in Server/PartyArt/imageName.jpg)
# NumVotes INT

database = sqlite3.connect("database.db")
db = database.cursor()
db.execute("CREATE TABLE IF NOT EXISTS Candidates(CandidateID INT PRIMARY KEY, CandidateName VARCHAR(50), PartyName VARCHAR(50), PartyArt VARCHAR(20), NumVotes INT)")

root = CTk()
root.title("ElectED Lite - Configurator")
root.geometry("800x600")
root.resizable(False, False)

if os.path.isfile("categoryName"):
    f = open("categoryName", "r")
    categoryName = f.read().split(": ")[1]
    f.close()
else:
    categoryName = simpledialog.askstring("ElectED Lite - Configurator", "Enter category name:")
    f = open("categoryName", "w+")
    f.write(f"categoryName: {categoryName}")
    f.close()


root.mainloop()