from win32api import GetSystemMetrics
from PIL import Image as Img
from customtkinter import *
from tkinter import messagebox
from datetime import datetime
import _thread
import sqlite3
import mouse
import time
import math
import sys
import os

class CandidateFrame(CTkFrame):
    def __init__(self, parent, info, **kwargs):
        kwargs['corner_radius'] = 20
        kwargs['fg_color'] = ("#c8c8c8", "#545454")
        super().__init__(parent, **kwargs)
        self.candidateName = info[1]
        self.id = info[0]
        partyName = info[2]
        partyArtPath = "PartyArt/"+info[3]

        pNameLbl = CTkLabel(self, text=self.candidateName+" - "+partyName, font=("Segoe UI", 20, "bold"))
        pNameLbl.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.1)

        try:
            pImage = CTkLabel(self, text="", image=CTkImage(None, Img.open(partyArtPath), (320, 260)))
            pImage.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.75)
        except:
            messagebox.showerror("ElectED Lite", f"Party Art image {partyArtPath} doesn't exist")
            sys.exit()

        self.bind("<Button-1>", self.callback)
        pNameLbl.bind("<Button-1>", self.callback)
        pImage.bind("<Button-1>", self.callback)
    
    def callback(self, e):
        waitingOverlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        db.execute(f"UPDATE Candidates SET NumVotes=NumVotes+1 WHERE CandidateID={self.id}")
        database.commit()
        updateVoteCount()
        f.write(f"Vote casted for {self.candidateName} -- {datetime.now().strftime('%I:%M %p')}\n")
        _thread.start_new_thread(self.afterCallback, ())
    
    def afterCallback(self):
        time.sleep(3)
        x = GetSystemMetrics(0)/2
        y = GetSystemMetrics(1)/2
        mouse.move(x, y)
        waitingOverlay.place_forget()

def updateVoteCount():
    global numVotes
    db.execute("SELECT SUM(NumVotes) FROM Candidates")
    numVotes = db.fetchall()[0][0]
    numVotesCounter.configure(text=f"Total Vote Count\n{numVotes}")

database = sqlite3.connect("database.db")
db = database.cursor()
try:
    db.execute("SELECT * FROM Candidates")
except:
    messagebox.showerror("ElectED Lite", "Please run the configurator")
    sys.exit()
data = db.fetchall()
if len(data) < 2:
    messagebox.showerror("ElectED Lite", "Please enter details of atleast two candidates in the configurator")
    sys.exit()

if len(data) > 8:
    messagebox.showerror("ElectED Lite", "Please enter details of not more than eight candidates in the configurator")
    sys.exit()

if not os.path.exists("categoryName"):
    messagebox.showerror("ElectED Lite", "Please run the configurator")
    sys.exit()

f = open("categoryName", "r")
categoryName = f.read()
f.close()

f = open("VoteLog.txt", "a+")
f.write(f"==== Session begins at {datetime.now().strftime('%I:%M %p')} ====\n")
numVotes = 0

root = CTk()
root.geometry("1920x1080")
root.resizable(False, False)
root.wm_attributes("-fullscreen", True)
root.after(0, lambda: root.state("zoomed"))

bgFrame = CTkFrame(root, corner_radius=0, fg_color=("#fff", "#333"))
bgFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

titleLbl = CTkLabel(bgFrame, text=f"Vote for {categoryName} candidate", font=("Segoe UI", 32, "bold"))
titleLbl.place(relx=0, rely=0, relwidth=1, relheight=0.125)

numVotesCounter = CTkLabel(bgFrame, text="Total Vote Count\n0", font=("Segoe UI", 24, "bold"))
numVotesCounter.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.125)

numRows = math.ceil(len(data) / 4)
horizontalSpacing = 0.015
verticalSpacing = 0.025
width = 0.23125
height = 0.4

if numRows == 1:
    j = 0.5
    numCols = len(data)
    for i in range(numCols):
        CandidateFrame(bgFrame, data[(math.floor(j) * 4) + i]).place(relx=((width * i) + horizontalSpacing * (i + 1)) + (((4 - numCols) * (width + horizontalSpacing)) / 2), rely=0.125 + (height * j) + verticalSpacing * (j + 1), relwidth=width, relheight=height)
elif numRows == 2:
    for j in range(2):
        numCols = 4 if j == 0 else len(data) - 4
        for i in range(numCols):
            CandidateFrame(bgFrame, data[(math.floor(j) * 4) + i]).place(relx=((width * i) + horizontalSpacing * (i + 1)) + (((4 - numCols) * (width + horizontalSpacing)) / 2), rely=0.125 + (height * j) + verticalSpacing * (j + 1), relwidth=width, relheight=height)

waitingOverlay = CTkFrame(root)
waitingLbl = CTkLabel(waitingOverlay, text="Vote casted successfully\nPlease wait a moment", font=("Segoe UI", 28, "bold"))
waitingLbl.place(relx=0, rely=0, relwidth=1, relheight=1)

updateVoteCount()
root.mainloop()
f.write(f"==== Session ends at {datetime.now().strftime('%I:%M %p')} ====\n\n")
f.close()