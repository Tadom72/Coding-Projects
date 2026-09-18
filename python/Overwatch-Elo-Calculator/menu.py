from tkinter import *  
from ow_calc import rank_change
from find_sr import get_srr, get_lobby_srr

def start():
   root = Tk()   
   root.title("Overwatch 2 Elo calc")

   def calculate():
      playerRank =  optPlayerR.get()
      playerDiv = optPlayerD.get()
      playerRankDivison = playerRank.lower() + "_" + playerDiv
      player_srr =get_srr(playerRankDivison)

      lowerRank =  optLowerR.get()
      lowerDiv = optLowerD.get()
      lowerRankDivison = lowerRank.lower() + "_" + lowerDiv

      HigherRank =  optHigherR.get()
      HigherDiv = optHigherD.get()
      higherRankDivison = HigherRank.lower() + "_" + HigherDiv
      lobby_srr = get_lobby_srr(lowerRankDivison, higherRankDivison)
      
      outcome = result.get()
      lbl.config(text=rank_change(player_srr, lobby_srr, outcome)) 

   # Dropdown options  
   rank = ["Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Master", "Grand Master", "Champion"]  
   divison = [5, 4, 3, 2, 1]

   # Selected option variable  
   optPlayerR = StringVar(value="Rank")  
   optPlayerD = StringVar(value="Division")
   optLowerR = StringVar(value="Rank")  
   optLowerD = StringVar(value="Division")
   optHigherR = StringVar(value="Rank")  
   optHigherD = StringVar(value="Division")


   # Dropdown menu  
   lP = Label(root, text = "Enter Player's Rank and Divison")
   lP.config(font =("Courier", 14))
   lP.pack()

   playerRank = OptionMenu(root, optPlayerR, *rank).pack() 
   playerDivison = OptionMenu(root, optPlayerD, *divison).pack()
   lL = Label(root, text = "Enter the Lobby's Lowest Rank and Divison")
   lL.config(font =("Courier", 14))
   lL.pack()

   lowerRank = OptionMenu(root, optLowerR, *rank).pack() 
   lowerDivison = OptionMenu(root, optLowerD, *divison).pack()  
   lH = Label(root, text = "Enter the Lobby's Highest Rank and Divison")
   lH.config(font =("Courier", 14))
   lH.pack()

   higherRank = OptionMenu(root, optHigherR, *rank).pack() 
   higherDivison = OptionMenu(root, optHigherD, *divison).pack()  

   result = BooleanVar()

   #win or lose
   Radiobutton(root, text="Win", variable=result, value=True).pack()
   Radiobutton(root, text="Lose", variable=result, value=False).pack()

   # Button to update label  
   Button(root, text="Calculate", command=calculate).pack()  


   lbl = Label(root, text=" ")  
   lbl.pack()  

   root.mainloop()