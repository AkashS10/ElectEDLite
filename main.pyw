from win32api import GetSystemMetrics
from PIL import Image as Img
from customtkinter import *
from tkinter import messagebox
from datetime import datetime
import _thread
import sqlite3
import mouse
import time
import sys
import os

class CandidateFrame(CTkFrame):
    def __init__(self, parent, id, candidateName, partyName, partyArtPath, **kwargs):
        kwargs['corner_radius'] = 20
        super().__init__(parent, **kwargs)
        self.candidateName = candidateName
        self.id = id

        nameLbl = CTkLabel(self, text=candidateName, font=("Seoge UI", 24, "bold"), corner_radius=20)
        nameLbl.place(relx=0.1, rely=0.04, relwidth=0.8, relheight=0.15)

        pNameLbl = CTkLabel(self, text=partyName, font=("Segoe UI", 20))
        pNameLbl.place(relx=0.2, rely=0.19, relwidth=0.6, relheight=0.1)

        try:
            pImage = CTkLabel(self, text="", image=CTkImage(None, Img.open(partyArtPath), (200, 200)))
            pImage.place(relx=0.175, rely=0.315, relwidth=0.65, relheight=0.65)
        except:
            messagebox.showerror("ElectED Lite", f"Party Art image {partyArtPath} doesn't exist")
            sys.exit()

        self.bind("<Button-1>", self.callback)
        nameLbl.bind("<Button-1>", self.callback)
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
if len(data) <= 1:
    messagebox.showerror("ElectED Lite", "Please enter details of atleast two candidates in the configurator")
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

titleLbl = CTkLabel(root, text=f"Vote for {categoryName} candidate", font=("Segoe UI", 32, "bold"))
titleLbl.place(relx=0, rely=0, relwidth=1, relheight=0.15)

numVotesCounter = CTkLabel(root, text="Total Vote Count\n0", font=("Segoe UI", 24, "bold"))
numVotesCounter.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.15)

match len(data):
    case 2:
        CandidateFrame(root, data[0][0], data[0][1], data[0][2], "PartyArt/"+data[0][3]).place(relx=0.2, rely=0.375, relwidth=0.225, relheight=0.4)
        CandidateFrame(root, data[1][0], data[1][1], data[1][2], "PartyArt/"+data[1][3]).place(relx=0.575, rely=0.375, relwidth=0.225, relheight=0.4)

    case 3:
        CandidateFrame(root, data[0][0], data[0][1], data[0][2], "PartyArt/"+data[0][3]).place(relx=0.1225, rely=0.375, relwidth=0.225, relheight=0.4)
        CandidateFrame(root, data[1][0], data[1][1], data[1][2], "PartyArt/"+data[1][3]).place(relx=0.3925, rely=0.375, relwidth=0.225, relheight=0.4)
        CandidateFrame(root, data[2][0], data[2][1], data[2][2], "PartyArt/"+data[2][3]).place(relx=0.6625, rely=0.375, relwidth=0.225, relheight=0.4)

    case 4:
        CandidateFrame(root, data[0][0], data[0][1], data[0][2], "PartyArt/"+data[0][3]).place(relx=0.0625, rely=0.375, relwidth=0.2, relheight=0.4)
        CandidateFrame(root, data[1][0], data[1][1], data[1][2], "PartyArt/"+data[1][3]).place(relx=0.2875, rely=0.375, relwidth=0.2, relheight=0.4)
        CandidateFrame(root, data[2][0], data[2][1], data[2][2], "PartyArt/"+data[2][3]).place(relx=0.5125, rely=0.375, relwidth=0.2, relheight=0.4)
        CandidateFrame(root, data[3][0], data[3][1], data[3][2], "PartyArt/"+data[3][3]).place(relx=0.7375, rely=0.375, relwidth=0.2, relheight=0.4)

    case 5:
        CandidateFrame(root, data[0][0], data[0][1], data[0][2], "PartyArt/"+data[0][3]).place(relx=0.0225, rely=0.375, relwidth=0.18, relheight=0.38)
        CandidateFrame(root, data[1][0], data[1][1], data[1][2], "PartyArt/"+data[1][3]).place(relx=0.2125, rely=0.375, relwidth=0.18, relheight=0.38)
        CandidateFrame(root, data[2][0], data[2][1], data[2][2], "PartyArt/"+data[2][3]).place(relx=0.4025, rely=0.375, relwidth=0.18, relheight=0.38)
        CandidateFrame(root, data[3][0], data[3][1], data[3][2], "PartyArt/"+data[3][3]).place(relx=0.5925, rely=0.375, relwidth=0.18, relheight=0.38)
        CandidateFrame(root, data[4][0], data[4][1], data[4][2], "PartyArt/"+data[4][3]).place(relx=0.7825, rely=0.375, relwidth=0.18, relheight=0.38)

    case 6:
        CandidateFrame(root, data[0][0], data[0][1], data[0][2], "PartyArt/"+data[0][3]).place(relx=0.0625, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[1][0], data[1][1], data[1][2], "PartyArt/"+data[1][3]).place(relx=0.2875, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[2][0], data[2][1], data[2][2], "PartyArt/"+data[2][3]).place(relx=0.5125, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[3][0], data[3][1], data[3][2], "PartyArt/"+data[3][3]).place(relx=0.7375, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[4][0], data[4][1], data[4][2], "PartyArt/"+data[4][3]).place(relx=0.2, rely=0.595, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[5][0], data[5][1], data[5][2], "PartyArt/"+data[5][3]).place(relx=0.575, rely=0.595, relwidth=0.2, relheight=0.38)

    case 7:
        CandidateFrame(root, data[0][0], data[0][1], data[0][2], "PartyArt/"+data[0][3]).place(relx=0.0625, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[1][0], data[1][1], data[1][2], "PartyArt/"+data[1][3]).place(relx=0.2875, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[2][0], data[2][1], data[2][2], "PartyArt/"+data[2][3]).place(relx=0.5125, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[3][0], data[3][1], data[3][2], "PartyArt/"+data[3][3]).place(relx=0.7375, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[4][0], data[4][1], data[4][2], "PartyArt/"+data[4][3]).place(relx=0.1225, rely=0.595, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[5][0], data[5][1], data[5][2], "PartyArt/"+data[5][3]).place(relx=0.3925, rely=0.595, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[6][0], data[6][1], data[6][2], "PartyArt/"+data[6][3]).place(relx=0.6625, rely=0.595, relwidth=0.2, relheight=0.38)

    case 8:
        CandidateFrame(root, data[0][0], data[0][1], data[0][2], "PartyArt/"+data[0][3]).place(relx=0.0625, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[1][0], data[1][1], data[1][2], "PartyArt/"+data[1][3]).place(relx=0.2875, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[2][0], data[2][1], data[2][2], "PartyArt/"+data[2][3]).place(relx=0.5125, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[3][0], data[3][1], data[3][2], "PartyArt/"+data[3][3]).place(relx=0.7375, rely=0.17, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[4][0], data[4][1], data[4][2], "PartyArt/"+data[4][3]).place(relx=0.0625, rely=0.595, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[5][0], data[5][1], data[5][2], "PartyArt/"+data[5][3]).place(relx=0.2875, rely=0.595, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[6][0], data[6][1], data[6][2], "PartyArt/"+data[6][3]).place(relx=0.5125, rely=0.595, relwidth=0.2, relheight=0.38)
        CandidateFrame(root, data[7][0], data[7][1], data[7][2], "PartyArt/"+data[7][3]).place(relx=0.7375, rely=0.595, relwidth=0.2, relheight=0.38)
        

waitingOverlay = CTkFrame(root)
waitingLbl = CTkLabel(waitingOverlay, text="Vote casted successfully\nPlease wait a moment", font=("Segoe UI", 28, "bold"))
waitingLbl.place(relx=0, rely=0, relwidth=1, relheight=1)

updateVoteCount()
root.mainloop()
f.write(f"==== Session ends at {datetime.now().strftime('%I:%M %p')} ====\n\n")
f.close()