
import math
import random
from pathlib import Path
#import glob
#from itertools import product

#import pandas as pd
from pandas import read_csv
#import csv
#import numpy as np

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from string import digits as Numbers
from string import ascii_letters as Letters

import eldefs as eld
import comp

class Gothic:
    '''
    Main class for the randomizer
    '''
    
    def __init__(self,title="Elminage Gothic Randomizer 1.0",dir="./"):
        self.baseDir = dir
        self.master = tk.Tk()
        self.master.title(title)
        try:
            self.master.iconbitmap('./shapeshifter.ico')
        except:
            pass
        center_x = str(int(self.master.winfo_screenwidth()/2 - 450))
        center_y = str(int(self.master.winfo_screenheight()/2 - 253))
        self.master.geometry(f"830x356+{center_x}+{center_y}")
        self.buildUI()
        self.master.mainloop()
        
        
        
        
        
    def buildUI(self):
        self.frames = {}
        self.values = {}
        self.widgets = {} #Hold widgets we need to access
        self.mainframe = ttk.Frame(self.master)

        
        self.welcomeLabel = ttk.Label(self.mainframe,text="Elminage Gothic Randomizer",font=("Arial",18))
        self.loadFilesLabel = ttk.Label(self.mainframe,text="Load your E:Gothic CSV data files")
        self.loadCSVsButton = ttk.Button(self.mainframe,text="Load game data",command=self.checkAllCSV)
        load_tooltip = CreateToolTip(self.loadCSVsButton, \
        "Select folder containing game files."
        "\nFiles in the Input folder will be auto-detected on startup.")
        
        #configure random seed UI
        self.values['seed'] = tk.StringVar()
        self.seedName = ttk.Label(self.mainframe,text="Seed:")
        # We validate, on any change to the field, the string being inserted or deleted
        vcmdS = self.master.register(self.validateSeed)
        vcmd_SpinboxPair = self.master.register(self.validateSpinboxPair)
        self.seedEntry = ttk.Entry(self.mainframe,textvariable=self.values['seed'],validate="key", validatecommand=(vcmdS, '%S'))
        self.seedChange = ttk.Button(self.mainframe,text="New Seed",command=self.genSeed)
        seed_tooltip = CreateToolTip(self.seedEntry, \
        "Alphanumeric characters only."
        "\nGenerates a random seed if left blank.")
        
        self.randoButton = ttk.Button(self.mainframe,text="Randomize!",state="disabled",command=self.randomize)
        
        #Layout for the top panel items
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=1)
        self.mainframe.grid(column=0,row=0,sticky=(tk.N))
        
        self.mainframe.columnconfigure(0,minsize=300,weight=6)
        self.mainframe.columnconfigure(1,minsize=150,weight=1)
        self.mainframe.columnconfigure(2,minsize=150,weight=1)
        self.mainframe.columnconfigure(3,minsize=100,weight=1)
        self.mainframe.rowconfigure(5,pad=20)
        
        self.welcomeLabel.grid(row=0,column=0,columnspan=4)
        self.loadFilesLabel.grid(row=1,column=0,rowspan=1)
        self.loadCSVsButton.grid(row=3,column=0)
        
        self.randoButton.grid(row=2,column=0,columnspan=1)
        
        self.seedEntry.grid(row=3,column=2,sticky=(tk.E,tk.W))
        self.seedName.grid(row=3,column=1,sticky=tk.E,padx=2)
        self.seedChange.grid(row=2,column=2,sticky=tk.W,padx=2,pady=2)
        
        #Setting up the tabber
        tabber = ttk.Notebook(self.mainframe)
        tabA = ttk.Frame(tabber)
        tabB = ttk.Frame(tabber)
        #tabC = ttk.Frame(tabber)
        
        tabber.add(tabA,text="Items")
        tabber.add(tabB,text="PCs and Enemies")
        #tabber.add(tabC,text="Enemies")
        #more to come
        tabber.grid(column=0,row=5,columnspan=4)
        
        self.checkAllCSV(directory="./Input/")
        
        ###TAB 1 - ITEMS
        ###
        self.itemStatsLab = ttk.Label(tabA,text = "Randomise item stats?")
        self.values['iMonsterItemBan'] = tk.BooleanVar()
        self.values['iMonsterItemBan'].set(True)
        self.widgets['monsterItemBanBox'] = ttk.Checkbutton(tabA,text="Exclude monster weapons",variable=self.values['iMonsterItemBan'],state="normal")
        
        
        self.values['iStatMode'] = tk.IntVar()
        self.values['iStatMode'].set(0)
        self.randoItemStatsRb1 = ttk.Radiobutton(tabA,text="No",value=0,variable=self.values['iStatMode'],command=self.iStatsNo)
        self.randoItemStatsRb2 = ttk.Radiobutton(tabA,text="By Variance",value=1,variable=self.values['iStatMode'],command=self.iStatsVariance)
             
        self.randoItemsACLabel = ttk.Label(tabA,text = "Armor Class")
        self.values['iACVar'] = tk.IntVar()
        self.values['iACVar'].set(2)
        self.widgets['itemACSpin'] = ttk.Spinbox(tabA,from_=0,to=10,textvariable=self.values['iACVar'],state="disabled",width=3)
        self.randoItemsAccLabel = ttk.Label(tabA,text="Accuracy")
        self.values['iAccuracyVar'] = tk.IntVar()
        self.values['iAccuracyVar'].set(3)
        self.widgets['itemAccuracySpin'] = ttk.Spinbox(tabA,from_=0,to=15,textvariable=self.values['iAccuracyVar'],state="disabled",width=3)
        self.randoItemsAtkLabel = ttk.Label(tabA,text="Damage Stats")
        self.values['iAttackVar'] = tk.IntVar()
        self.values['iAttackVar'].set(2)
        self.widgets['itemAttackSpin'] = ttk.Spinbox(tabA,from_=0,to=6,textvariable=self.values['iAttackVar'],state="disabled",width=3)
        
        self.values['iSpellChange'] = tk.BooleanVar()
        self.values['iSpellChange'].set(False)
        self.widgets['itemSpellBox'] = ttk.Checkbutton(tabA,text="Randomize item spells",variable=self.values['iSpellChange'],command=self.iSpellToggle,state="normal")
        
        self.itemSpellLabel = ttk.Label(tabA,text="Chance (%) for new magic items:")
        self.values['iSpellAddChance'] = tk.IntVar()
        self.values['iSpellAddChance'].set(0)
        self.widgets['itemSpellSpin'] = ttk.Spinbox(tabA,from_=0,to=100,increment=2,textvariable=self.values['iSpellAddChance'],state="readonly",width=3)
        
        self.values['iPriceMode'] = tk.BooleanVar()
        self.values['iPriceMode'].set(True)
        self.widgets['itemPriceBox'] = ttk.Checkbutton(tabA,text="Randomize item prices",variable=self.values['iPriceMode'],command=self.iPriceToggle,state="normal")
        self.itemPriceLabel = ttk.Label(tabA,text = "Price factor:")
        self.values['iPriceFac'] = tk.DoubleVar()
        self.values['iPriceFac'].set(100)
        self.widgets['itemPriceScale'] = tk.Scale(tabA,from_=100,to=500,orient=tk.HORIZONTAL,length=150,variable=self.values['iPriceFac'],state="normal")
        
        self.values['iShopMode'] = tk.BooleanVar()
        self.values['iShopMode'].set(False)
        self.widgets['itemShopBox'] = ttk.Checkbutton(tabA,text="Randomize shop inventory",variable=self.values['iShopMode'],state="normal")
        
        mItemBan_tooltip = CreateToolTip(self.widgets['monsterItemBanBox'], \
        "Excludes generic monster weapons (Slash, Charge etc) from randomization."
        "\nOther enemy-only gear will still be included.")
        randoItemStats_tooltip = CreateToolTip(self.randoItemStatsRb2, \
        "Each item stat gets +/- between 0"
        "\nand the specified value, if applicable.")
        itemAC_tooltip = CreateToolTip(self.widgets['itemACSpin'], \
        "Applies variance to armors' AC."
        "Weapons have a 1/8 chance of receiving variance.")
        itemAccuracy_tooltip = CreateToolTip(self.widgets['itemAccuracySpin'], \
        "Randomizes weapons' Accuracy score.")
        itemAttack_tooltip = CreateToolTip(self.widgets['itemAttackSpin'], \
        "Randomizes weapons' damage range and number of strikes.")
        itemSpell_tooltip = CreateToolTip(self.widgets['itemSpellBox'], \
        "Randomize the spells that are invoked by spell-casting items."
        "\nSpells' chance of appearing are based on their strength.")
        itemSpellAdd_tooltip = CreateToolTip(self.widgets['itemSpellSpin'], \
        "Set chance for items without spells to gain a spell invocation."
        "\nStronger spells are less likely to appear.")
        itemPrice_tooltip = CreateToolTip(self.widgets['itemPriceBox'], \
        "Randomizes prices of items. The price factor determines how much a price can vary from its base value. "
        "A factor of 350 means a range of price/3.5 to price*3.5.")
        itemShop_tooltip = CreateToolTip(self.widgets['itemShopBox'], \
        "Randomly adds items to the shop's starting inventory."
        "\nChance rises with the inverse of the item's price.")
        
        #TabA layout
        
        self.itemStatsLab.grid(row=1,column=0,columnspan=3)
        self.randoItemStatsRb1.grid(row=2,column=1)
        self.randoItemStatsRb2.grid(row=2,column=2)
        self.widgets['monsterItemBanBox'].grid(row=0,column=1,columnspan=3)
        self.randoItemsACLabel.grid(row=3,column=1,sticky=tk.E)
        self.widgets['itemACSpin'].grid(row=3,column=2,sticky=tk.W)
        self.randoItemsAccLabel.grid(row=4,column=1,sticky=tk.E)
        self.widgets['itemAccuracySpin'].grid(row=4,column=2,sticky=tk.W)
        self.randoItemsAtkLabel.grid(row=5,column=1,sticky=tk.E)
        self.widgets['itemAttackSpin'].grid(row=5,column=2,sticky=tk.W)
        
        self.widgets['itemShopBox'].grid(row=1,column=4)
        self.widgets['itemPriceBox'].grid(row=2,column=4)
        self.itemPriceLabel.grid(row=3,column=4)
        self.widgets['itemPriceScale'].grid(row=4,column=4,sticky=tk.N)
        self.widgets['itemSpellBox'].grid(row=5,column=4)
        self.itemSpellLabel.grid(row=6,column=4)
        self.widgets['itemSpellSpin'].grid(row=6,column=5)
        
        tabA.grid_columnconfigure(0,minsize=10)
        tabA.grid_columnconfigure(3,minsize=230)
        for i in range(0,10):
            tabA.rowconfigure(i,pad=5)
            
        ###TAB 2 - SPECIES (and classes?)
        self.raceStatsLab = ttk.Label(tabB,text="Randomize species base stats?")
        self.values['rStatMode'] = tk.IntVar()
        self.values['rStatMode'].set(0)
        self.raceStatsRb1 = ttk.Radiobutton(tabB,text="No",value=0,variable=self.values['rStatMode'],command=self.rStatsNo)
        self.raceStatsRb2 = ttk.Radiobutton(tabB,text="By Pool",value=1,variable=self.values['rStatMode'],command=self.rStatsYes)
        self.raceStatsRb3 = ttk.Radiobutton(tabB,text="By Variance",value=2,variable=self.values['rStatMode'],command=self.rStatsYes)
        self.raceStatsRb4 = ttk.Radiobutton(tabB,text="Chaos",value=3,variable=self.values['rStatMode'],command=self.rStatsChaos)
        
        self.raceStatMinLab = ttk.Label(tabB,text="Min:")
        self.values['rStatMin'] = tk.IntVar()
        self.values['rStatMin'].set(5)
        self.widgets['raceStatsMinSpin'] = ttk.Spinbox(tabB,from_=1,to=18,textvariable=self.values['rStatMin'],command=lambda:self.updateSpinbox(self.values['rStatMin'].get(),'rStatMax',True),state='disabled',width=3)

        self.raceStatMaxLab = ttk.Label(tabB,text="Max:")
        self.values['rStatMax'] = tk.IntVar()
        self.values['rStatMax'].set(14)
        self.widgets['raceStatsMaxSpin'] = ttk.Spinbox(tabB,from_=1,to=18,textvariable=self.values['rStatMax'],command=lambda:self.updateSpinbox(self.values['rStatMax'].get(),'rStatMin',False),state="disabled",width=3)
        #old validation stuff
        "validate='key',validatecommand=(vcmd_SpinboxPair,'%P','raceStatsMaxSpin','rStatMax','rStatMin',1,18,''),"
        
        self.raceStatVarLab = ttk.Label(tabB,text="Variance:")
        self.values['rStatVariance'] = tk.IntVar()
        self.values['rStatVariance'].set(3)
        self.widgets['raceStatsVarSpin'] = ttk.Spinbox(tabB,from_=0,to=16,textvariable=self.values['rStatVariance'],state="disabled",width=3)
        
        
        self.values['jobSafety'] = tk.BooleanVar()
        self.values['jobSafety'].set(True)
        self.widgets['jobSafetyBox'] = ttk.Checkbutton(tabB,text="Adjust class stat requirements",variable=self.values['jobSafety'],state='disabled')
        
        self.skillRandoLab = ttk.Label(tabB,text="Randomize class skills?")
        self.values['cSkillMode'] = tk.IntVar()
        self.values['cSkillMode'].set(0)
        self.classSkillsRb1 = ttk.Radiobutton(tabB,text="No",value=0,variable=self.values['cSkillMode'],command=self.cSkillsNo)
        self.classSkillsRb2 = ttk.Radiobutton(tabB,text="Shuffle",value=1,variable=self.values['cSkillMode'],command=self.cSkillsShuffle)
        self.classSkillsRb3 = ttk.Radiobutton(tabB,text="Chaos",value=2,variable=self.values['cSkillMode'],command=self.cSkillsChaos)
        
        self.skillMatchingLab = ttk.Label(tabB,text="Base/Mastery skill matching:")
        self.values['cSkillMatching'] = tk.IntVar()
        self.values['cSkillMatching'].set(1)
        self.widgets['skillMatchingRb1'] = ttk.Radiobutton(tabB,text="None",value=0,variable=self.values['cSkillMatching'],state='disabled')
        self.widgets['skillMatchingRb2'] = ttk.Radiobutton(tabB,text="Loose",value=1,variable=self.values['cSkillMatching'],state='disabled')
        self.widgets['skillMatchingRb3'] = ttk.Radiobutton(tabB,text="Strict",value=2,variable=self.values['cSkillMatching'],state='disabled')
        
        self.values['cOpt1'] = tk.BooleanVar()
        self.values['cOpt1'].set(False)
        self.widgets['cSettingBox'] = ttk.Checkbutton(tabB,text="More Alchemy skills",variable=self.values['cOpt1'],state='disabled')
        self.values['cAddID'] = tk.BooleanVar()
        self.values['cAddID'].set(False)
        self.widgets['cAddIDBox'] = ttk.Checkbutton(tabB,text="More Identification",variable=self.values['cAddID'],state='disabled')
        
       #need stuff for min/max under skill randomization?
        
        rStatPool_tooltip = CreateToolTip(self.raceStatsRb2, \
        "Adds up all stat points, applies random variance, then redistributes them.")
        rStatVariance_tooltip = CreateToolTip(self.raceStatsRb3, \
        "Applies between +/- variance for each stat point.")
        rStatChaos_tooltip = CreateToolTip(self.raceStatsRb4, \
        "Randomly generates new stat values between the set Min and Max values.")
        jobSafety_tooltip = CreateToolTip(self.widgets['jobSafetyBox'], \
        "Reduces class stat requirements as needed to ensure that all species can still qualify for all classes.")
        
        cSkillShuffle_tooltip = CreateToolTip(self.classSkillsRb2, \
        "Shuffle existing skills between classes. The total number of skills will remain about the same.")
        cSkillRandom_tooltip = CreateToolTip(self.classSkillsRb3, \
        "Randomly set skills for classes. The number of each kind of skill and the total number of skills will vary.")
        cMatchNone_tooltip = CreateToolTip(self.widgets['skillMatchingRb1'], \
        "Mastery skills can be assigned even where they have no use (eg, Alter Fate but no Tarot).")
        cMatchLoose_tooltip = CreateToolTip(self.widgets['skillMatchingRb2'], \
        "Mastery skills that require a base skill to function will only be assigned if the class possesses that base skill (eg, "
        "Alter Fate will only be assigned if Tarot was also assigned).")
        cMatchStrict_tooltip = CreateToolTip(self.widgets['skillMatchingRb3'], \
        "When a base skill is assigned, a matching Mastery skill will also be assigned, if applicable."
        "\nNB: under Chaos mode, a class can still be assigned Mage/Cleric/Alchemy spell power up even if they cannot cast those spells naturally.")
        self.cOpt1_tooltip = CreateToolTip(self.widgets['cSettingBox'], \
        "Adds an additional copy of Forging, Transmutation and either Alchemy Spells or Pursuit to the base skill pool.")
        cAddID_tooltip = CreateToolTip(self.widgets['cAddIDBox'], \
        "Adds a copy of Identification to the base skill pool.")
        
        #TabB layout
        self.raceStatsLab.grid(row=0,column=1,columnspan=4)
        self.raceStatsRb1.grid(row=1,column=1)
        self.raceStatsRb2.grid(row=1,column=2)
        self.raceStatsRb3.grid(row=1,column=3)
        self.raceStatsRb4.grid(row=1,column=4)
        self.raceStatMinLab.grid(row=2,column=0,sticky=tk.E,padx=5)
        self.widgets['raceStatsMinSpin'].grid(row=2,column=1,sticky=tk.W)
        self.raceStatMaxLab.grid(row=2,column=2,sticky=tk.E)
        self.widgets['raceStatsMaxSpin'].grid(row=2,column=3,sticky=tk.W)
        self.raceStatVarLab.grid(row=2,column=4,sticky=tk.E)
        self.widgets['raceStatsVarSpin'].grid(row=2,column=5,sticky=tk.W)
        self.widgets['jobSafetyBox'].grid(row=3,column=1,columnspan=3)
        
        self.skillRandoLab.grid(row=0,column=7,columnspan=3)
        self.classSkillsRb1.grid(row=1,column=7)
        self.classSkillsRb2.grid(row=1,column=8)
        self.classSkillsRb3.grid(row=1,column=9)
        self.skillMatchingLab.grid(row=2,column=7,columnspan=3)
        self.widgets['skillMatchingRb1'].grid(row=3,column=7)
        self.widgets['skillMatchingRb2'].grid(row=3,column=8)
        self.widgets['skillMatchingRb3'].grid(row=3,column=9)
        
        self.widgets['cSettingBox'].grid(row=4,column=8,columnspan=2)
        self.widgets['cAddIDBox'].grid(row=5,column=8,columnspan=2)
        
        tabB.grid_columnconfigure(6,minsize=200)
        tabB.grid_columnconfigure(0,minsize=10)
        
        ###TAB C - ENEMIES
        ##UNTIL MORE IS ADDED, THIS IS TEMPORARILY PART OF TAB B
        self.values['mMode'] = tk.BooleanVar()
        self.values['mMode'].set(False)
        self.widgets['mModeBox'] = ttk.Checkbutton(tabB,text = "Shuffle enemies",variable=self.values['mMode'],state='normal')
        
        mMode_tooltip = CreateToolTip(self.widgets['mModeBox'], \
        "Shuffle enemy appearences and levels."
        "\nWeapons, stats and abilities will be scaled according to the enemy's new level."
        "\nSome enemies and NPCs are excluded from the shuffle for gameplay or stability reasons.")
        
        self.widgets['mModeBox'].grid(row=6,column=1,columnspan=3,sticky=tk.W)
        
        
    def checkAllCSV(self,directory=None):
        #checks for the existence of all the required game data files
        dataDir = directory
        if not directory:
            dataDir = filedialog.askdirectory(initialdir="./",title="Select folder containing extracted CSV files") + "/"
        if not dataDir:
            return
        fileList = ['CHRTMPLT.csv','EMPLOY.csv','ITEM.csv','ITEM_HELP.csv','JOB_EX.csv','MONSTER1.csv','MONSTER2.csv','MONSTER3.csv',
            'SPELL.csv','SPLEARN.csv','SPMP.csv']
        try:
            for name in fileList:
                file = Path(dataDir,name)
                if not file.is_file():
                    raise FileNotFoundException
            self.values['csvDir'] = tk.StringVar()
            self.values['csvDir'].set(dataDir)
            self.randoButton.config(state="normal")
            self.loadFilesLabel.config(text="Game files detected.")
        except:
            self.randoButton.config(state="disabled")
            if not directory:
                messagebox.showwarning(message="Error loading csv files. Ensure all needed files are present in the selected folder.")
        return
        
    def iStatsNo(self):
        self.disableWidgets(['itemACSpin','itemAccuracySpin','itemAttackSpin'])
        return
        
    def iStatsVariance(self):
        self.enableWidgets(['itemACSpin','itemAccuracySpin','itemAttackSpin'])
        return
        
    def iSpellToggle(self):
        #self.toggleWidgets(self.values['iSpellChange'],['itemSpellSpin'],True)
        return
        
    def iPriceToggle(self):
        #self.toggleWidgets(self.values['iPriceMode'],['itemPriceScale'],True)
        if self.values['iPriceMode'].get() == True:
            self.widgets['itemPriceScale'].config(fg="black",state="normal")
        else:
            self.widgets['itemPriceScale'].config(fg="grey",state="disabled")
        return
        
    def rStatsNo(self):
        self.disableWidgets(['raceStatsMinSpin','raceStatsMaxSpin','raceStatsVarSpin','jobSafetyBox',])
        return
        
    def rStatsYes(self):
        self.enableWidgets(['raceStatsMinSpin','raceStatsMaxSpin','raceStatsVarSpin','jobSafetyBox'])
        return
        
    def rStatsChaos(self):
        #disables Variance setting
        self.enableWidgets(['raceStatsMinSpin','raceStatsMaxSpin','jobSafetyBox'])
        self.disableWidgets(['raceStatsVarSpin'])
        return
        
    def cSkillsNo(self):
        self.disableWidgets(['skillMatchingRb1','skillMatchingRb2','skillMatchingRb3','cSettingBox','cAddIDBox'])
        return
        
    def cSkillsShuffle(self):
        self.enableWidgets(['skillMatchingRb1','skillMatchingRb2','skillMatchingRb3','cSettingBox','cAddIDBox'])
        self.widgets['cSettingBox'].config(text="More Alchemy skills")
        self.cOpt1_tooltip.changetip("Adds an additional copy of Forging, Transmutation and either Alchemy Spells or Pursuit to the base skill pool.")
        return
        
    def cSkillsChaos(self):
        self.enableWidgets(['skillMatchingRb1','skillMatchingRb2','skillMatchingRb3','cSettingBox'])
        self.disableWidgets(['cAddIDBox'])
        self.widgets['cSettingBox'].config(text="All skills appear")
        self.cOpt1_tooltip.changetip("Ensures at least one of each basic skill will be assigned.")
        return

    
    
    def randomize(self):
        if not self.values['seed'].get(): self.genSeed()
        settings = copyTkDict(self.values)
        random.seed(settings['seed'])
        
        #making Holmic Gate a weaker Enterook Mista
        #When/if I add spell rando, this will go there
        spellFile = getCSV("SPELL.csv",settings['csvDir'])
        spellFile.iloc[113,6] = -28
        spellFile.iloc[113,14] = 7
        spellFile.iloc[113,15] = 7
        spellFile.iloc[113,17] = -7
        spellFile.iloc[113,18] = -49
        saveToCSV(spellFile,"SPELL.csv")
        
        
           
        randoRaces(settings)
        randoItems(settings)
        randoClasses(settings)
        randoMonsters(settings)
        messagebox.showinfo(title="Success", message="Randomization completed!\nModified files saved to Output folder.")


        
    def genSeed(self):
        newSeed = ''.join(random.choice(Numbers+Letters) for x in range(10))
        self.values['seed'].set(newSeed)
        return
        
    def validateSeed(self):
        returnValue = True
        for i in key:
            if i not in Numbers+Letters:
                returnValue = False
        return returnValue

    def validateSpinboxPair(self,newNum,widgetName,varName,pairedVar,minVal,maxVal,isMin):
        '''Handles validation/value-clamping for pairs of spinboxes.
        Doesn't seem reliable - probably won't use.'''
        if not newNum:
            self.master.after_idle(lambda:self.widgets[widgetName].config(validate="key"))
            return True
        else:
            try:
                min = int(minVal)
                max = int(maxVal)
                new = int(newNum)
                if new > max:
                    self.values[varName].set(max)
                    self.master.after_idle(lambda:self.widgets[widgetName].config(validate="key"))
                    if bool(isMin):
                        self.values[pairedVar].set(max)
                    return True
                    
                elif new < min:
                    self.values[varName].set(min)
                    self.master.after_idle(lambda:self.widgets[widgetName].config(validate="key"))
                    if not bool(isMin):
                        self.values[pairedVar].set(min)
                    return True
                    
                elif bool(isMin) and new > self.values[pairedVar].get():
                    self.values[pairedVar].set(new)
                    return True
                    
                elif (not bool(isMin)) and new < self.values[pairedVar].get():
                    self.values[pairedVar].set(new)
                    return True
                    
            except ValueError:
                return False

        
    def updateSpinbox(self,new_value,varName,isMin):
        #Updating paired spinboxes when min increased above max or max below min
        #varName is for the other spinbox, not the one being passed
        if isMin:
            if new_value > self.values[varName].get():
                self.values[varName].set(new_value)
        else:
            if new_value < self.values[varName].get():
                self.values[varName].set(new_value)

    def toggleWidgets(self,stateVar,widgets,toggleState):
        #For turning on/off other widgets based on the state of a checkbox widget
        if stateVar.get() == toggleState:
            self.enableWidgets(widgets)
        else:
            self.disableWidgets(widgets)
                
    def enableWidgets(self,widgets):
        for w in widgets:
            if "Spin" in w:#A little hacky, but oh well
                self.widgets[w].config(state="readonly")
            else:
                self.widgets[w].config(state="normal")
            
                
    def disableWidgets(self,widgets):
        for w in widgets:
            self.widgets[w].config(state="disabled")
            

                

class CreateToolTip(object):#credit to https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 270   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 45
        y += self.widget.winfo_rooty() + 28
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#fffff0", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
            
    def changetip(self,newText):
        self.text = newText
                
        
def randoItems(settings):

    #temp variables
    #specialChance = 10
    #specialCap = 2 #Max kinds of specials that can be assigned to one item
    #negSpecialCap = 2#Same, but for negative qualities
    
    #read ITEM.csv with no formatting
    itemFile = getCSV("ITEM.csv",settings['csvDir'])
    itemHelpFile = getCSV("ITEM_HELP.csv",settings['csvDir'])
    
    #For each item, roll some number of additional abilities?
    
    #Since item 0 is blank/nothing, we skip it
    for i in range(1,710):
        item = itemFile.iloc[6+i]
        itemHelp = itemHelpFile.iloc[4+i]
     
        #If item has no price - even 0 - it is not an existing item -> don't try to modify it
        try:
            #Randomize prices
            #Only in multiples of 10
            p = float(item[7])
        except ValueError:
            continue
        iType = int(item[1])
        #Exclude monster-only weapons like Strike/Slash if the option calls for it
        if (settings['iMonsterItemBan']==True) and p == 0:
            continue
        if settings['iPriceMode'] == True:
            priceFac = settings['iPriceFac'] / 100.0
            pMin = int(p / priceFac / 10.0)
            pMax = int(p * priceFac / 10.0)
            if pMax > pMin:
                item[7] = random.randrange(pMin,pMax) * 10
            #print(item[7])
        
        #Randomizing shop availability
        #Only for items not already in shop
        if settings['iShopMode'] == True and item[6].isnumeric() and int(item[6]) == 0 and p > 5 and i not in eld.RestrictedItems:
            shopChance = max(8,int(p ** 0.65))#p being item's unrandomized price
            #If item is added to shop, quadruple its price
            if random.randrange(shopChance) == 0:
                 item[6] = int(item[6]) + 1
                 item[7] = item[7] * 4
        
        #Randomize item combat stats
        if settings['iStatMode'] == 1:
            #Randomize AC
            #If item type is 13 or lower (not an armor) 87.5% chance to not randomize
            
            acFac = settings['iACVar']
            a = int(item[55])
            if (iType in eld.ArmorTypes) or (random.randrange(0,8) == 0):
                item[55] = a + random.randrange(-acFac,acFac+1)
                
                    
            #Randomize Accuracy, Damage and Strikes
            #Only randomize if base Strikes # is nonzero and item is not a monster weapon
            strikes = int(item[66])
            attackRand = settings['iAttackVar']
            if strikes != 0 and iType != 34 and attackRand > 0:
                acc = int(item[60])
                sides = int(item[61])
                dice = int(item[62])
                corr = int(item[63])
                accFac = settings['iAccuracyVar']
                sideFac = diceFac = corrFac = strikeFac = attackRand
            
                #sides, dice, strikes must be at least 1
                #correction cannot be more negative than the number of dice
                item[60] = acc + random.randrange(-accFac,accFac+1)
            
                #Dice + correction must be positive
                #Dice*Sides + correction must be < 128
                #Some vanilla items violate this principle; for safety's sake we'll clamp corr
                dice = max(dice + random.randrange(-diceFac,diceFac+1),1)
                if (corr + dice) < 1:
                    corr = -dice + 1
                
                corrMin = max((-dice+1),corr-corrFac)
                corrMax = min(128-dice,corr+corrFac)
                corr = random.randrange(corrMin,corrMax+1)
                sidesMin = max(sides-sideFac,1)
                sidesMax = int(min(sides+sideFac,(127-corr)/dice))
                
                if sidesMin > sidesMax:
                    sidesMin = sidesMax
                    #print("Dice sides too large: {}".format(item[4]))
                
                sides = random.randrange(sidesMin,sidesMax+1)
                
                item[61] = sides
                item[62] = dice
                item[63] = corr
            
                #Min,Max damage values are display-only
                #We calc them here based off the sides/dice/correction values
                item[64] = dice + corr
                item[65] = item[61] * item[62] + item[63]
                #Strikes capped at 10
                item[66] = min(max(strikes + random.randrange(-strikeFac,strikeFac+1),1),10)
        
        
        #adding negative modifiers
        '''
        z = 0
        nerfTypes = []
        availTypes = [1,2,3,4,7]#maybe let user select which ones are available
        #7 = no Forging
        while z < negSpecialCap:
            if random.randrange(specialChance) == 0:
                nerf = random.choice[availTypes]
                nerfTypes.append(nerf)
                availTypes.remove(nerf)
        '''
        #Then run through every type in nerfTypes
        
        
        #For adding special abilities/attributes
        '''
        k = 0
        specialTypes = [0,1,2,3,4,5,6]
        for x in nerfTypes:
            specialTypes.remove(x)
            while k < specialCap:
                if random.randrange(specialChance) == 0:
                    special = random.randrange(0,5)
                    if special == 0:#Recovery Rate
                        recoverySize = random.randint(30,65)
                        item[59] = max(recoverySize,int(item[59]))
                    if special == 1:#HP Regen
                        regenSize = random.randint(2,50)
                        if random.randrange(8) == 0:
                            regenSize = -regenSize
                k += 1
        '''
        
        #Randomizing HP Regen
        #Always vary if regen is nonzero; otherwise, chance to obtain regen (or hp leak)
        regen = int(item[56])
        if regen != 0:
            regMin = regen - int(abs(regen/2))
            regMax = regen + int(abs(regen/2))
            regen = random.randint(regMin,regMax)
            item[56] = regen
        
        #Randomizing Spell school resistances
        
        #Randomizing Elemental attributes
              
        #Randomizing Ailment attributes
        
        #Randomizing Effectiveness
        #either random to change, or shuffle between all
        
        #Range
        
        
        #Randomizing item spellcasting
        #Only equippable items are eligible
        #
        spellPathA = bool((int(item[47]) == 0 and random.randrange(100) < settings['iSpellAddChance']))
        spellPathB = bool(int(item[47]) != 0 and settings['iSpellChange'] == True)
        if iType < 29 and (spellPathA or spellPathB):
            w = random.choices([0,1,2,3,4],weights=eld.SpellTierWeights,k=1)
            tier = w[0]
            iSpellID = random.choice(eld.SpellTiers[tier])
            iBreakChance = 5
            if tier == 0:
                iBreakChance = random.choice(eld.BreakChancesLow)
            elif tier == 4:
                iBreakChance = random.choice(eld.BreakChancesHigh)
            else:
                iBreakChance = random.choice(eld.BreakChancesMid)
            #Setting usability (Town/Camp/Battle) based on spell ID
            iUsability = eld.SpellUse[iSpellID-1]
            if iUsability % 2 == 1:
                item[46] = 1
            if iUsability % 2 == 0:
                item[45] = 1
            if iUsability % 4 == 0:
                item[44] = 1
            item[47] = iSpellID
            item[49] = iBreakChance
            #Acquiring spell name
            spellNames = getCSV("SpellNames.csv")
            iSpellName = spellNames.iloc[iSpellID-1][0]
            itemHelp[2] = int(iSpellID)
            iHelpText = "Invokes {0}.".format(iSpellName)
            itemHelp[3] = iHelpText
    
    saveToCSV(itemFile,"ITEM.csv")
    saveToCSV(itemHelpFile,"ITEM_HELP.csv")
    return

def randoRaces(settings):
        '''
        randomizes species stats (may add innate abilities later)
        mode 0, pool, adds up all stat points, varies by +- statVar, and redistributes
        mode 1, delta, randomizes each stat points by +- statVar
        mode 2, chaos, just generates new stat points altogether
        Safety mode: when True, adjusts class requirements to ensure every race can become every class
        '''
        
        
        jobFile = getCSV("EMPLOY.csv",settings['csvDir'])
        raceFile = getCSV("CHRTMPLT.csv",settings['csvDir'])
        
        statMode = settings['rStatMode']
        minStat = settings['rStatMin']
        maxStat = settings['rStatMax']
        statVar = settings['rStatVariance']
        
        
        lowest = [10,10,10,10,10,10]
        for s in range(12):
            races = raceFile.iloc[:,4+s]
            if statMode == 1:
                '''POOL MODE'''
                newTotal = 0
                for c in races[25:31]:
                    newTotal += int(c)
                newTotal += random.randint(-statVar,statVar)
                #print(newTotal)
                newStats = comp.random_restricted_composition(newTotal,6,minStat,maxStat)
                for n in range(len(newStats)):
                    races[25+n] = newStats[n]
                    if lowest[n] > newStats[n]:
                        lowest[n] = newStats[n]
            elif statMode == 2:
                '''DELTA MODE'''
                for c in range(25,31):
                    indiv = int(races[c]) + random.randint(-statVar,statVar)
                    newInd = min(max(indiv,minStat),maxStat)
                    races[c] = newInd
                    if lowest[c-25] > newInd:
                        lowest[c-25] = newInd
            elif statMode == 3:
                '''CHAOS MODE'''
                for c in range(25,31):
                    newCh = random.randint(minStat,maxStat)
                    races[c] = newCh
                    if lowest[c-25] > newCh:
                        lowest[c-25] = newCh
            if settings['jobSafety'] == True:
                for j in range(16):
                    job = jobFile.iloc[:,3+j]
                    for w in range(6):
                        if lowest[w] + 10 < int(job[20+w]):
                            job[20+w] = lowest[w] + 10
                            job[13+w] = lowest[w] + 10
                    
        saveToCSV(raceFile,"CHRTMPLT.csv")
        saveToCSV(jobFile,"EMPLOY.csv")
        
        
        return

def randoClasses(settings):
    '''
    Randomizes class skills and sets MP pools as needed
    '''
    skillsFile = getCSV("JOB_EX.csv",settings['csvDir'])
    mpFile = getCSV("SPMP.csv",settings['csvDir'])
    learnFile = getCSV("SPLEARN.csv",settings['csvDir'])
    
    newMPFile = getCSV("HunterMP.csv","./")
    newLearnFile = getCSV("HunterLearning.csv","./")
    
    
 
    cMode = settings['cSkillMode']#0 for none, 1 for shuffle, 2 for randomized
    skillMatching = settings['cSkillMatching']
    #Level 0 makes no guarantees on skill usability
    #Level 1 forbids assignment of useless mastery skills
    #Level 2 proactively assigns related mastery skills during base skill assignment
    
    
    if cMode != 0:
    
        #In shuffle mode, adds alchemy-related skills to the pool
        #In chaos mode, ensures at least one of each basic skill will be assigned
        addAlch = atLeastOne = settings['cOpt1']
        addID = settings['cAddID']
        classBaseSkills = [[] for q in range(16)]
        classMasterySkills = [[] for g in range(16)]
        baseSkills = []
        masterySkills = []
        
        #counting base skills (for shuffle mode) and removing them from the csv (for both modes)
        for i in range(29):
            skillLine = skillsFile.iloc[4+i]
            for j in range(16):
                if bool(skillLine[3+j]) == True:#skill presence indicated by non=empty block
                    #on the count loop, we don't write to skill lists yet
                    baseSkills.append(i)
                skillLine[3+j] = ""#blank out the entry
        if addAlch == True:
            #adding a copy of Forging and Transmutation
            baseSkills.append(12)
            baseSkills.append(13)
            #Adding an instance of Alchemy spells or Pursuit
            if random.randrange(2) == 1: baseSkills.append(6)
            else: baseSkills.append(19)
        if addID == True:
            baseSkills.append(17)
        #counting mastery skills
        for k in range(25):
            skillLine = skillsFile.iloc[34+k]
            for g in range(16):
                if bool(skillLine[3+g]) == True:
                    masterySkills.append(k)
                skillLine[3+g] = ""
        if addAlch == True:
            masterySkills.append(eld.Disassemble)
            
        if cMode == 1:#Shuffle mode
            #setting skill counts: 0-4 base skills for each class
            classBaseCounts = comp.random_restricted_composition(min(80,len(baseSkills)+16),16,1,5)
            for c in range(16):
                classBaseCounts[c] -= 1
                
            classMasteryCounts = comp.random_restricted_composition(min(64,len(masterySkills)+16),16,1,4)
            for m in range(16):
                classMasteryCounts[m] -= 1
            
            for b in range(16):
                for h in range(classBaseCounts[b]):
                    loopA = 0
                    while loopA < 10:
                        loopA += 1
                        newSkill = random.choice(baseSkills)
                        if checkSkillOverlap(classBaseSkills[b],newSkill):
                            classBaseSkills[b].append(newSkill)
                            baseSkills.remove(newSkill)
                            #print(newSkill)
                            if skillMatching == 2:
                                matchedSkill = getMatchingMastery(newSkill)
                                if matchedSkill is not None:
                                    classMasterySkills[b].append(matchedSkill)
                                    classMasteryCounts[b] -= 1
                                    if matchedSkill in masterySkills:
                                        masterySkills.remove(matchedSkill)
                            break
                for m in range(classMasteryCounts[b]):
                    loopB = 0
                    #print(masterySkills)
                    while loopB < 10 and len(masterySkills) > 0:
                        loopB += 1
                        newMastery = random.choice(masterySkills)
                        if checkMasteryOverlap(classMasterySkills[b],newMastery):
                            if skillMatching == 1:
                                prereqSkills = getMatchingBase(newMastery)
                                if prereqSkills is not None:
                                    if not any(z in classBaseSkills[b] for z in prereqSkills):
                                        continue
                            classMasterySkills[b].append(newMastery)
                            masterySkills.remove(newMastery)
                            break
                        

        elif cMode == 2:#Chaos mode
            #maybe let user pick min/max?
            classBaseCounts = [random.randint(0,4) for x in range(16)]
            classMasteryCounts = [random.randint(1,3) for y in range(16)]

            if atLeastOne == True:#add one of each base skill to the classes
                for v in eld.ValidSkills:
                    p = 0
                    while True:
                        p = random.randint(0,15)
                        if len(classBaseSkills[p]) < 4 and checkSkillOverlap(classBaseSkills[p],v): break
                    classBaseSkills[p].append(v)
                    classBaseCounts[p] -= 1
                    if skillMatching == 2:
                        matchedSkill = getMatchingMastery(v)
                        if matchedSkill is not None:
                            classMasterySkills[p].append(matchedSkill)
                            classMasteryCounts[p] -= 1
            
            for b in range(16):
                for h in range(classBaseCounts[b]):
                    while True:
                        newSkill = random.choices(eld.ValidSkills,weights=eld.SkillWeights,k=1)[0]
                        if checkSkillOverlap(classBaseSkills[b],newSkill):
                            classBaseSkills[b].append(newSkill)
                            if skillMatching == 2:
                                matchedSkill = getMatchingMastery(newSkill)
                                if matchedSkill is not None:
                                    classMasterySkills[b].append(matchedSkill)
                                    classMasteryCounts[b] -= 1
                            break
                for m in range(classMasteryCounts[b]):
                    while True:
                        newMastery = random.choices(eld.ValidMasteries,weights=eld.MasteryWeights,k=1)[0]
                        if checkMasteryOverlap(classMasterySkills[b],newMastery):
                            if skillMatching == 1 or newMastery > 9:
                                prereqSkills = getMatchingBase(newMastery)
                                if prereqSkills is not None:
                                    if not any(z in classBaseSkills[b] for z in prereqSkills):
                                        continue
                            classMasterySkills[b].append(newMastery)
                            break
        
        #write back changes
        #TODO: if you get Holy Lance art, gain Lance access
        #TODO: if you get Ancient Rites, gain Talisman+ access
        # May need to rework how the csvs are saved and accessed
        itemFile = getCSV("ITEM.csv","./Output/")
        for u in range(16):
            classCol = skillsFile.iloc[:,3+u]
            for w in classBaseSkills[u]:
                classCol[4+w] = "1"
                if w == 7:
                    classCol[92] = "4"#unlocking Spirit Pact
                    classCol[93] = "4"#and Master Therion
                    
            for v in classMasterySkills[u]:
                classCol[34+v] = "2"
                if v == 21:#Holy Lance Art
                    for w in range(92,118):
                        item = itemFile.iloc[6+w]
                        valkPerm = int(item[20])
                        if valkPerm != 0 and random.randint(1,10) < 9:
                            item[8+u] = valkPerm
                elif v == 19:#Ancient Rites
                    for w in [508,509,510,511,536,537,538,539,540]:
                        item = itemFile.iloc[6+w]
                        shamanPerm = int(item[18])
                        item[8+u] = shamanPerm
        saveToCSV(itemFile,"ITEM.csv")
                
        #Updating preset characters
        #Should consider updating MP counts/spell learning too
        presetFile = getCSV("PLAYER.csv",settings['csvDir'])
        for t in range(8):
            preset = presetFile.iloc[:,4+t]
            pClass = int(preset[18]) - 1
            preset[243] = preset[244] = preset[245] = preset[246] = 0
            for q in range(len(classBaseSkills[pClass])):
                preset[243+q] = classBaseSkills[pClass][q] + 1
        
        saveToCSV(presetFile,"PLAYER.csv")
                
    saveToCSV(skillsFile,"JOB_EX.csv")
    
    #Adding Alchemy charges to Pursuit
    for i in range(23):
        learnLine = learnFile.iloc[55+i]
        learnLine[20] = newLearnFile.iloc[i,0]
        learnLine[21] = newLearnFile.iloc[i,1]
    for i in range(35):
        mpLine = mpFile.iloc[3+i]
        mpLine[57:63] = newMPFile.iloc[i,0:6]
    
    saveToCSV(learnFile,"SPLEARN.csv")
    saveToCSV(mpFile,"SPMP.csv")
    


def randoMonsters(settings):
    '''Shuffles enemies.
    Equipment, stats, spells and status ailments are modified based
    on the level of the slot a monster is randomized to.'''
    monsterFileA = getCSV("MONSTER1.csv",settings['csvDir'])
    monsterFileB = getCSV("MONSTER2.csv",settings['csvDir'])
    monsterFileC = getCSV("MONSTER3.csv",settings['csvDir'])
    mFiles = [monsterFileA,monsterFileB,monsterFileC]
    newMFileA = monsterFileA.copy()
    newMFileB = monsterFileB.copy()
    newMFileC = monsterFileC.copy()
    newMFiles = [newMFileA,newMFileB,newMFileC]
    if settings['mMode'] == True:
        
        mList = [m for m in range(429) if m not in eld.RestrictedMonsters]
        mRand = mList.copy()
        random.shuffle(mRand)
        levelList = [0]*429
        #collect the levels of all monsters before we start moving data around
        for x in range(len(mList)):
            slotEntry = getMonsterCol(mFiles,mList[x])
            levelList[mList[x]] = int(slotEntry[13])  
        
        for x in range(len(mList)):
            mEntry = getMonsterCol(mFiles,mRand[x]).copy()
            slotEntry = getMonsterCol(newMFiles,mList[x])
            slotLevel = levelList[mList[x]]
            mLevel = int(mEntry[13])
            mEntry[13] = slotLevel
            
            oldHP = max(int(mEntry[23]),8)
            newHP = getLevelScaledStat(mLevel**1.08,slotLevel**1.08,oldHP)
            mEntry[23] = newHP
            if int(slotEntry[22]) > 0:#Minibosses, etc
                mEntry[22] = newHP
            else:
                mEntry[22] = 0
            #For other stats - maybe by square root of the ratio?
            
            #For AC; 0.363 based on trend of AC values in vanilla game
            #RN no special accounting for Natural AC monsters
            ACMod = math.floor((min(mLevel,200) - min(slotLevel,200))*0.363) + random.randint(-2,2)
            #Accounting for very early monsters having bad AC
            if slotLevel < 5:
                ACMod += 2
            if mLevel < 5:
                ACMod -= random.randint(1,3)
            mEntry[24] = int(mEntry[24]) + int(ACMod)
            
            #For # of Actions and recovery rate; scale up and down slightly by level
            #Could have options instead of flat 60 value?
            mActions = int(mEntry[39])
            mRecovery = int(mEntry[255])
            thresh = min(slotLevel + 1, 201)#so that Divine Dragon slot doesn't have 10 actions or w/e
            mCap = min(mLevel,200)
            recoveryChoices = [0,5,10,15,20,25,30]
            actionScale = 50
            if thresh > mCap:
                while (thresh - mCap) > actionScale:
                    mActions += 1
                    mRecovery += random.choice(recoveryChoices)
                    thresh -= actionScale
                if random.randint(0,actionScale) < (thresh - mCap):
                    mActions += 1
            elif thresh < mCap:
                while (mCap - thresh) > actionScale:
                    mActions -= 1
                    mRecovery -= random.choice(recoveryChoices)
                    thresh += actionScale
                if random.randint(0,actionScale) < (mCap - thresh):
                    mActions -= 1
            mEntry[39] = min(max(mActions,1),8)
            mEntry[255] = min(max(mRecovery,0),100)
        
            
            
            #For Str/Vit/Agi etc - use slots's numbers, but ordered from highest -> lowest same as original
            #And then add a little variance
            mStats = [int(m) for m in mEntry[25:31]]
            slotStats = [int(j) for j in slotEntry[25:31]]
            newStats = translateStats(mStats,slotStats)
            for i in range(6):
                mEntry[25+i] = newStats[i] + random.choice([-2,-1,-1,0,0,1,1,2])#could add option here
            
                
            #For XP/GP - probably just use slot values
            #otherwise, would want to mark miniboss/one-time slots
            #plus, distinctions between enemies that appear solo vs in big groups
            newEP = int(slotEntry[43])
            newGP = int(slotEntry[44])
            if newEP > 7:
                newEP += random.randint(-newEP//8,newEP//8)
            if newGP > 7:
                newGP += random.randint(-newGP//8,newGP//8)
            mEntry[43] = newEP
            mEntry[44] = newGP
            
            
            #Spells - will get upgraded or downgraded depending on new level
            for s in range(1,111):
                if int(mEntry[55+s]) == 1:
                    checkSpellPerm(slotLevel,s,mEntry)
            
            #For Summon Resistance
            if int(slotEntry[254]) == 100:
                mEntry[254] = 100
            else:
                mEntry[254] = getNewSummonResist(slotLevel,int(mEntry[14])-13)
                
            #For Turn Recovery - scale level like HP
            if int(mEntry[256]) != 0:
                newRegen = getLevelScaledStat(mLevel**1.08,slotLevel**1.08,int(mEntry[256]),clamp=False)
                mEntry[256] = newRegen
            
            #For Status Attack/Defence
            thresh = min(slotLevel,200)
            if thresh < mCap:
                for s in range(9):
                    threat = eld.StatusAttackDanger[s]
                    rate = int(mEntry[289+s])
                    if not rate: continue
                    if thresh < threat:
                        mEntry[289+s] = 0
                    else:
                        rate = int(max(rate - random.randint(0,min(threat,8))*((mCap-thresh)/8),1))
                        mEntry[289+s] = rate
            else:
                for s in range(9):
                    threat = eld.StatusAttackDanger[s]
                    rate = int(mEntry[289+s])
                    if not rate: continue
                    threat = min(8,threat)#So that poison,sleep etc don't scale too hard
                    rate = int(min(rate + (thresh-mCap)/8 * random.randint(0,15-threat),95))
                    mEntry[289+s] = rate
                        
            #Weapons!
            mainHand = int(mEntry[331])
            weaponChanged = False
            if mainHand != 0:
                weapOne = translateWeapon(slotLevel,mLevel,mainHand,False)
                mEntry[331] = weapOne
                if weapOne != mainHand: weaponChanged = True
                #print("{0}, Level {1} - New weapon: {2}".format(mEntry[6],slotLevel,weapOne))
            subHand = int(mEntry[332])
            if subHand != 0:
                weapTwo = translateWeapon(slotLevel,mLevel,subHand,True)
                mEntry[332] = weapTwo
                if weapTwo != subHand: weaponChanged = True
                #print("{0}, Level {1} - New weapon: {2}".format(mEntry[6],slotLevel,weapTwo))
            #for monsters which have not gotten an upgrade or downgrade to a weapon
            if not weaponChanged and mainHand != 0:
                if (slotLevel - mLevel) > 7:
                    strBoost = (slotLevel - mLevel) // 8
                    mEntry[25] = min(int(mEntry[25]) + strBoost,60)
                    #print("Boosted Strength for {0} by {1}".format(mEntry[6],strBoost))
                elif (mLevel - slotLevel) > 7:
                    strPenalty = (mLevel - slotLevel) // 8
                    mEntry[25] = max(int(mEntry[25]) - strPenalty,1)
                    #print("Reduced Strength for {0} by {1}".format(mEntry[6],strPenalty))
            
            
            
            
            
            
            setMonsterCol(newMFiles,mList[x],mEntry)
        
    saveToCSV(newMFileA,"MONSTER1.csv")
    saveToCSV(newMFileB,"MONSTER2.csv")
    saveToCSV(newMFileC,"MONSTER3.csv")
    

def addMastery(skillArray,skill,limit):
    if len(skillArray) >= limit:
        return False
    else:
        skillArray.append(skill)
        return True
        
def checkSkillOverlap(skillList,newSkill):
    '''
    Check if new skill overlaps with already assigned skills
    Duplicates and also skills with the same effect
    '''
    if newSkill in skillList:
        return False
    elif (newSkill in eld.MageSkills) and any(u in eld.MageSkills for u in skillList):
        return False
    elif (newSkill in eld.ClericSkills) and any(u in eld.ClericSkills for u in skillList):
        return False
    elif (newSkill in eld.AlchSkills) and any(u in eld.AlchSkills for u in skillList):
        return False
    elif (newSkill in eld.ThiefSkills) and any(u in eld.ThiefSkills for u in skillList):
        return False
    else:
        return True
        
def checkMasteryOverlap(mastList,newMast):
    if newMast in mastList:
        return False
    elif (newMast in eld.FighterMasteries) and any(u in eld.FighterMasteries for u in mastList):
        return False
    elif (newMast in eld.MageMasteries) and any(u in eld.MageMasteries for u in mastList):
        return False
    elif (newMast in eld.ClericMasteries) and any(u in eld.ClericMasteries for u in mastList):
        return False
    elif (newMast in eld.AlchMasteries) and any(u in eld.AlchMasteries for u in mastList):
        return False
    else:
        return True
        
def getMatchingMastery(skill):
    #For a given base skill, get a list of mastery skills that it "unlocks".
    match = eld.MasteryArray[skill]
    if len(match) == 0: return None
    return random.choice(match)
            
def getMatchingBase(mastery):
    #For a given mastery skill, get a list of base skills that could lead to it.
    if len(eld.BaseArray[mastery]) == 0: return None
    return eld.BaseArray[mastery]
    
def translateWeapon(level,oldLvl,initWeapon,isSub=False):
    '''Gives enemy a weapon of matching type and appropriate power for their level.'''
    if initWeapon in eld.Swords:#Swords get special handling
        currIndex = eld.Swords.index(initWeapon)
        diff = int(math.sqrt(abs(level - oldLvl)))
        
        if diff != 0:
            diff = random.randint(diff//4,diff)
        if level < oldLvl: diff = -diff
        newIndex = max(min(currIndex + diff,len(eld.Swords)-1),0)
        return eld.Swords[newIndex]
    bracket = getWeaponBracket(level)
    for wSet in eld.RandomWeps:
        if initWeapon in wSet[0]:
            randomMax = 0
            for cap in wSet[1]:
                if level < cap: break
                randomMax += 1
            if randomMax == 0:
                return wSet[0][0]
            newIndex = random.randint(0,randomMax)
            return wSet[0][newIndex]
    for wList in eld.NoAdjustmentWeps:
        if initWeapon in wList:
            newIndex = bracket + random.choice([-1,0,0,0,0,1])
            newIndex = max(min(newIndex,len(wList)-1),0)
            return wList[newIndex]
    if isSub:
        bracket = max(bracket - random.randint(1,2),0)
    for wList in eld.RegularWeps:
        if initWeapon in wList:
            newIndex = bracket + random.choice([-1,0,0,0,0,1])
            newIndex = max(min(newIndex,len(wList)-1),0)
            return wList[newIndex]
    if initWeapon < 326:
        #print("No match found for {0}".format(initWeapon))
        pass
    return initWeapon
            
            
def getWeaponBracket(level):
    #Utility function for translateWeapon.
    for x in range(len(eld.MonsterWeaponLevels)):
        if level < eld.MonsterWeaponLevels[x][0]:
            return eld.MonsterWeaponLevels[x-1][1]
    return eld.MonsterWeaponLevels[-1][1]
        
    
def getLevelScaledStat(mLvl,slotLvl,mStat,clamp=True):
    '''Scales a stat by the ratio of original to slot HP.
    Can also clamp it to positive values.'''
    ratio = mLvl / slotLvl
    newStat = mStat // ratio
    if newStat >= 8:
        newStat += random.randrange(-(newStat//8),1 + newStat//8)
    elif newStat < 1 and clamp==True: newStat = 1
    return int(newStat)

def translateStats(entryL,destL):
    '''Given stats of entry and destination foes,
    Reorder destination list so that the highest-to-lowest
    order is the same as in the entry list.'''
    #entryL.sort(key=lambda a: a[1])
    destL.sort()
    newList = [0]*6
    for i in range(6):
        lowest = entryL.index(min(entryL))
        entryL[lowest] = 100
        newList[lowest] = destL.pop(0)
    return newList
    
def checkSpellPerm(level,spell,entry):
    '''Check if the given spell is legal at the given level .
    If not, upgrade or downgrade the spell, if possible.'''
    checker = eld.MonsterSpellLevels[spell-1]#MSL is 0-indexed
    if checker[0] <= level <= checker[1]:
        entry[55+spell] = 1
        return#Outside of this branch, the original spell is getting wiped
    elif level < checker[0] and checker[2] != 0:
        checkSpellPerm(level,checker[2],entry)
    elif level > checker[1] and checker[3] != 0:
        checkSpellPerm(level,checker[3],entry)
    entry[55+spell] = 0
    
def getNewSummonResist(level,family):
    '''Generates a new summon resistance value based on enemy level and family.'''
    familyResists = eld.FamilySummonResists[family]
    resist = 0
    if level < 30:
        r = random.randint(0,2)
        resist = familyResists[r]
    elif level < 50:
        r = random.choice([0,1,2,2,3,3])
        resist = familyResists[r]
        if random.randint(level,50) > 42:
            resist += 10
    else:
        resist = familyResists[3]
        if random.randint(0,2) == 0:
            resist += 10
    return min(95,resist)


def getMonsterCol(mFiles,mID):
    '''Given a monster ID, retrieves its data column from
    the matching monster data file.'''
    if 0 <= mID <= 151:
        return mFiles[0].iloc[:,4+mID]
    elif 152 <= mID <= 261:
        return mFiles[1].iloc[:,4 + (mID-152)]
    elif 262 <= mID <= 429:
        return mFiles[2].iloc[:,4 + (mID-262)]
    else:
        raise ValueError
        
def setMonsterCol(mFiles,mID,mCol):
    '''Overwrites monster data at the defined position
    with new data.'''
    if 0 <= mID <= 151:
        mFiles[0].iloc[:,4+mID] = mCol
    elif 152 <= mID <= 261:
        mFiles[1].iloc[:,4 + (mID-152)] = mCol
    elif 262 <= mID <= 429:
        mFiles[2].iloc[:,4 + (mID-262)] = mCol
    return

def getCSV(filename,root="./",):
    fullname = root + filename
    return read_csv(fullname, sep=",", encoding="shift_jis", header=None, skip_blank_lines=False,na_filter=False,dtype='str')

    
def saveToCSV(file,filename):
    savePathName = "Output/" + filename
    savePath = Path(savePathName)
    savePath.parent.mkdir(parents=True,exist_ok=True)
    file.to_csv(savePath,header=False,index=False,encoding="shift_jis")
    return
    
def copyTkDict(dict):
    #copies key/value pairs containing TKinter Variables to key/value pairs of their underlying data
    newDict = {k:v.get() for k,v in dict.items()}
    return newDict


if __name__ == '__main__':
    app = Gothic()
