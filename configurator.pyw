from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview, Style
from PIL import Image as Img
from customtkinter import *
import pandas as pd
import sqlite3
import os

class CreateEditCandidate():
    def __init__(self, editData=None):
        self.editData = editData
        self.bgFrame = CTkFrame(root, corner_radius=0, fg_color=("#333333", "#333333"))
        self.bgFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        createCandidateFrame = CTkFrame(self.bgFrame, corner_radius=20, fg_color=("#222222", "#222222"))
        createCandidateFrame.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.8)

        ccTitleLbl = CTkLabel(createCandidateFrame, text="Create Candidate" if editData == None else "Edit Candidate", font=("Arial", 20, "bold"))
        ccTitleLbl.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.2)

        ccCandNameLbl = CTkLabel(createCandidateFrame, text="Candidate Name: ", font=("Arial", 20), anchor="w")
        ccCandNameLbl.place(relx=0.1, rely=0.225, relwidth=0.4, relheight=0.1)
        self.ccCandNameEnt = CTkEntry(createCandidateFrame, placeholder_text="Candidate name...", font=("Arial", 20))
        self.ccCandNameEnt.place(relx=0.5, rely=0.225, relwidth=0.4, relheight=0.1)

        ccPartyNameLbl = CTkLabel(createCandidateFrame, text="Party Name: ", font=("Arial", 20), anchor="w")
        ccPartyNameLbl.place(relx=0.1, rely=0.375, relwidth=0.4, relheight=0.1)
        self.ccPartyNameEnt = CTkEntry(createCandidateFrame, placeholder_text="Party name...", font=("Arial", 20))
        self.ccPartyNameEnt.place(relx=0.5, rely=0.375, relwidth=0.4, relheight=0.1)

        ccPartyArtLbl = CTkLabel(createCandidateFrame, text="Party Art: ", font=("Arial", 20), anchor="w")
        ccPartyArtLbl.place(relx=0.1, rely=0.525, relwidth=0.4, relheight=0.1)
        self.ccPartyArtEnt = CTkEntry(createCandidateFrame, placeholder_text="Party Art...", font=("Arial", 20))
        self.ccPartyArtEnt.bind("<FocusIn>", self.ccPartyArtBind)
        self.ccPartyArtEnt.place(relx=0.5, rely=0.525, relwidth=0.4, relheight=0.1)

        ccNumVotesLbl = CTkLabel(createCandidateFrame, text="Number of votes: ", font=("Arial", 20), anchor="w")
        ccNumVotesLbl.place(relx=0.1, rely=0.675, relwidth=0.4, relheight=0.1)
        self.ccNumVotesEnt = CTkEntry(createCandidateFrame, placeholder_text="0", font=("Arial", 20))
        self.ccNumVotesEnt.configure(state="disabled")
        self.ccNumVotesEnt.insert(END, 0)
        self.ccNumVotesEnt.place(relx=0.5, rely=0.675, relwidth=0.4, relheight=0.1)

        cancelButton = CTkButton(createCandidateFrame, text="Cancel", font=("Arial", 20), command=self.bgFrame.place_forget)
        cancelButton.place(relx=0.1, rely=0.825, relwidth=0.375, relheight=0.1)

        createButton = CTkButton(createCandidateFrame, text="Create" if editData == None else "Edit", font=("Arial", 20), command=self.createFunc)
        createButton.place(relx=0.525, rely=0.825, relwidth=0.375, relheight=0.1)

        if editData != None:
            self.ccCandNameEnt.insert(END, editData[1])
            self.ccPartyNameEnt.insert(END, editData[2])
            self.ccPartyArtEnt.insert(END, editData[3])
            self.ccNumVotesEnt.configure(state="normal", placeholder_text="Number of votes...")
            self.ccNumVotesEnt.delete(0, END)
            self.ccNumVotesEnt.insert(END, editData[4])

    def createFunc(self):
        candName = self.ccCandNameEnt.get()
        if candName.isspace() or candName == "":
            messagebox.showerror("ElectED Lite - Configurator", "Please enter the candidate's name")
            return

        partyName = self.ccPartyNameEnt.get()
        if partyName.isspace() or partyName == "":
            messagebox.showerror("ElectED Lite - Configurator", "Please enter the party's name")
            return

        partyArt = self.ccPartyArtEnt.get()
        if partyArt.isspace() or partyArt == "":
            messagebox.showerror("ElectED Lite - Configurator", "Please enter select the party's art")
            return
        
        if self.editData == None:
            db.execute("SELECT CandidateID FROM Candidates")
            try:
                currentID = db.fetchall()[-1][0]
            except:
                currentID = 0
            db.execute(f"INSERT INTO Candidates VALUES({currentID+1}, \"{candName}\", \"{partyName}\", \"{partyArt}\", 0)")
            database.commit()
            messagebox.showinfo("ElectED Lite - Configurator", "Candidate created successfully")
        else:
            numVotes = self.ccNumVotesEnt.get()
            if numVotes.isspace() or numVotes == "":
                messagebox.showinfo("ElectED Lite - Configurator", "Please enter number of votes")
                return
            db.execute(f"UPDATE Candidates SET CandidateName=\"{candName}\", PartyName=\"{partyName}\", PartyArt=\"{partyArt}\", NumVotes={numVotes} WHERE CandidateID={self.editData[0]}")
            database.commit()
            messagebox.showinfo("ElectED Lite - Configurator", "Candidate edited successfully")

        self.bgFrame.place_forget()
        updateTV()
        
    def ccPartyArtBind(self, *_):
        self.bgFrame.focus_set()
        img = PartyImageForm(self.bgFrame, self.ccPartyArtEnt, CTkFrame(self.bgFrame))

class PartyImageForm(CTkFrame):
    def __init__(self, parent, ccPartyArtEnt, overlayFrame, *args, **kwargs):
        kwargs["corner_radius"] = 20
        kwargs["fg_color"] = ("#222222", "#222222")
        kwargs["bg_color"] = ("#2b2b2b", "#2b2b2b")
        super().__init__(parent, *args, **kwargs)
        self.path = None
        self.overlayFrame = overlayFrame
        self.pArtEnt = ccPartyArtEnt
        self.overlayFrame.bind("<Button-1>", self.closeForm)
        self.overlayFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.titleLbl = CTkLabel(self, text="Choose Image", font=("Segoe UI", 24, "bold"))
        self.titleLbl.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.15)

        self.mainFrame = CTkScrollableFrame(self)
        self.mainFrame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.7)

        self.lof = os.listdir("./PartyArt/")
        self.btns = []
        for i in range(len(self.lof)):
            btn = CTkLabel(self.mainFrame, text="", image=CTkImage(None, Img.open(f"./PartyArt/{self.lof[i]}"), (135,135)), corner_radius=20)
            btn.bind("<Button-1>", lambda *_, i=i: self.selectImage(i))
            btn.grid(row=i//2, column=i%2, ipadx=10, ipady=35)
            self.btns.append(btn)
        if self.btns == []:
            noImageLbl = CTkLabel(self, text="There are no images\nPlease put the party art images in the folder \"PartyArt\"", font=("Segoe UI", 16))
            noImageLbl.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.7)

        self.selectButton = CTkButton(self, text="Select", command=self.closeForm, font=("Segoe UI", 18))
        self.selectButton.place(relx=0.1, rely=0.89, relwidth=0.8, relheight=0.07)

        self.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.8)
    
    def closeForm(self, *_):
        self.overlayFrame.place_forget()
        self.place_forget()
        if self.path == None: return
        self.pArtEnt.delete(0, END)
        self.pArtEnt.insert(0, self.path)
    
    def selectImage(self, i, *_):
        self.path = self.lof[i]
        for x in self.btns:
            x.configure(fg_color="transparent")
        self.btns[i].configure(fg_color="#1f6aa5")

def editCandidate():
    if len(candidatesTV.selection()) == 0:
        messagebox.showerror("ElectED Lite - Configurator", "Please select a candidate to edit")
        return
    CreateEditCandidate(candidatesTV.item(candidatesTV.selection()[0], 'values')[1:])

def deleteCandidate():
    if len(candidatesTV.selection()) == 0:
        messagebox.showerror("ElectED Lite - Configurator", "Please select a candidate to delete")
        return
    if messagebox.askyesno("ElectED Lite - Configuator", "Are you sure you want to delete the candidate?\nThis action CANNOT be undone"):
        db.execute(f"DELETE FROM Candidates WHERE CandidateID={candidatesTV.item(candidatesTV.selection()[0], 'values')[1]}")
        database.commit()
        updateTV()
        messagebox.showinfo("ElectED Lite - Configurator", "Candidate deleted successfully")

def generateResults():
    db.execute("SELECT CandidateName, PartyName, NumVotes FROM Candidates")
    data = db.fetchall()
    highestVoted = ""
    highestVote = 0
    for i in data:
        if i[-1] > highestVote:
            highestVote = i[-1]
            highestVoted = i[0]
    data += (("", "", ""),
             ("", "", ""),
             ("Winner", highestVoted, highestVote))
    df = pd.DataFrame(data, columns=["Candidate Name", "Party Name", "Number of votes"])
    df.to_csv(f"{categoryName}.csv", index=False)
    messagebox.showinfo("ElectED Lite - Configurator", f"Results has been saved to {categoryName}.csv")

def editCategory():
    global categoryName
    categoryName = simpledialog.askstring("ElectED Lite - Configurator", "Enter new category name:", initialvalue=categoryName)
    if categoryName == None:
        return
    f = open("categoryName", "w+")
    f.write(categoryName)
    f.close()
    titleLbl.configure(text=f"\tConfigure category {categoryName}")

def updateTV():
    items = getAllChildren(candidatesTV)
    for item in items:
        candidatesTV.delete(item)
    db.execute("SELECT * FROM Candidates")
    candidate = db.fetchall()
    for i in range(len(candidate)):
        candidatesTV.insert('', 'end', values=(i+1, *candidate[i]))
    
def getAllChildren(tree, item=""):
        children = tree.get_children(item)
        for child in children:
            children += getAllChildren(tree, child)
        return children

# TABLE: Candidates
# CandidateID INT PRIMARY KEY
# CandidateName VARCHAR
# PartyName VARCHAR
# PartyArt VARCHAR (stores the image name of the party's art present in PartyArt/imageName.jpg)
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
    categoryName = f.read()
    f.close()
else:
    categoryName = simpledialog.askstring("ElectED Lite - Configurator", "Enter category name:")
    f = open("categoryName", "w+")
    f.write(categoryName)
    f.close()

titleLbl = CTkLabel(root, text=f"\tConfigure category {categoryName}", font=("Arial", 24, "bold"))
titleLbl.place(relx=0, rely=0, relwidth=0.9, relheight=0.15)

editCategoryBtn = CTkButton(root, text="✎", font=("Arial", 26), command=editCategory)
editCategoryBtn.place(relx=0.9, rely=0.04, relwidth=0.05, relheight=0.067)

style = Style()
style.theme_use("default")
style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=35, fieldbackground="#2a2d2e", bordercolor="#343638", borderwidth=0, font=("Segoe UI", 12))
style.map('Treeview', background=[('selected', '#22559b')])
style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=("Segoe UI", 14, 'bold'))
style.map("Treeview.Heading", background=[('active', '#565b5e')])

candidatesTV = Treeview(root, columns=("c1", "c2", "c3", "c4", "c5", "c6"), show="headings")
candidatesTV.column("#1", anchor=CENTER, width=30)
candidatesTV.heading("#1", text="S.NO")
candidatesTV.column("#2", anchor=CENTER, width=0, stretch=NO, minwidth=0)
candidatesTV.heading("#2", text="ID")
candidatesTV.column("#3", anchor=CENTER, width=275)
candidatesTV.heading("#3", text="Candidate Name")
candidatesTV.column("#4", anchor=CENTER, width=150)
candidatesTV.heading("#4", text="Party Name")
candidatesTV.column("#5", anchor=CENTER, width=150)
candidatesTV.heading("#5", text="Party Art")
candidatesTV.column("#6", anchor=CENTER, width=150)
candidatesTV.heading("#6", text="Number of votes")
candidatesTVScrollbar = CTkScrollbar(root, command=candidatesTV.yview)
candidatesTVScrollbar.place(relx=0.93, rely=0.15, relwidth=0.02, relheight=0.7)
candidatesTV.place(relx=0.05, rely=0.15, relwidth=0.88, relheight=0.7)

createCandidateBtn = CTkButton(root, text="Create Candidate", font=("Segoe UI", 18), command=CreateEditCandidate)
createCandidateBtn.place(relx=0.05, rely=0.875, relwidth=0.215, relheight=0.1)

editCandidateBtn = CTkButton(root, text="Edit Candidate", font=("Segoe UI", 18), command=editCandidate)
editCandidateBtn.place(relx=0.2775, rely=0.875, relwidth=0.215, relheight=0.1)

deleteCandidateBtn = CTkButton(root, text="Delete Candidate", font=("Segoe UI", 18), command=deleteCandidate)
deleteCandidateBtn.place(relx=0.505, rely=0.875, relwidth=0.215, relheight=0.1)

generateResultsBtn = CTkButton(root, text="Generate results", font=("Segoe UI", 18), command=generateResults)
generateResultsBtn.place(relx=0.7325, rely=0.875, relwidth=0.215, relheight=0.1)

updateTV()
root.mainloop()