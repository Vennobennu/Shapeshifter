RestrictedItems = [628,641,598]


ArmorTypes = [14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
WeaponSlots = [1,2,3,11]
SpellUse = [1,1,2,
    1,1,1,1,
    1,1,1,1,
    1,1,2,
    1,1,1,
    1,1,1,
    1,3,1,
    7,1,1,2,#Cleric Level 1
    7,1,1,2,
    7,7,2,
    7,7,3,2,
    7,1,1,1,
    7,7,1,1,
    1,7,6,1,
    1,1,1,0,#Alchemy Level 1
    1,1,1,
    1,1,1,
    1,1,1,
    1,1,1,3,
    1,1,2,
    1,0,2]


#indicating what natural weapons enemies should receive based on their level
#For each tuple, first value is the minimum level, second is weapon index
MonsterWeaponLevels = [(1,0),(3,1),(6,2),(13,3),(19,4),(26,5),(33,6),
    (39,7),(55,8),(66,9),(70,10),(100,11),(160,12),(200,13)]



#1H Swords are a special case; instead of indexing by level, we randomize weighted by level
#1H Swords are ordered in rough order of power
Swords = [19,14,1,6,15,2,20,16,21,8,25,321,18,17,3,22,7,12,9,5,4,23,26,10,24,13,11]

#For these groups, if in Sub-slot, reduce bracket by 1
Swords_2H = [1,1,27,29,28,34,33,30,38,31,35,36,38,30]
Daggers = [45,40,41,47,42,48,322,322,51,43,49,49,52,50]
WeakSpears = [97,97,97,97,106,110,98,107,109,103,116,116,114,114]
Spears = [105,105,92,93,112,99,113,100,94,95,96,96,104,115]
Hammers = [144,144,144,145,151,149,147,147,146,148,148,148,152,152]
Maces = [170,157,171,158,173,172,159,168,160,161,179,166,182,167]
Clubs = [196,196,183,198,185,190,186,199,189,195,192,193,192,207]
Bows = [222,222,209,209,210,216,211,212,229,220,217,213,218,221]
Whips = [248,235,253,237,242,243,255,256,238,244,257,252,258,245]
Claws = [660,660,300,294,307,311,311,306,312,312,304,309,310,310]
Strikes = [x for x in range(646,660)]
Slashes = [y for y in range(660,674)]
Charges = [z for z in range(674,688)]

#For these, don't reduce bracket if in sub-slot
Herbalist_ = [287,14,21,21,120,279,279,279,22,22,23,24,295,295]
Club_Shaman = [197,197,197,184,203,204,191,187,205,205,194,206,206,206]
Katana_Main = [53,53,54,60,55,57,61,320,62,64,64,56,63,65]
Katana_Sub = [66,66,67,68,73,71,72,69,75,77,78,70,76,76]
Katana_2H = [53,54,79,80,86,87,82,85,90,88,91,91,89,89]
Axes_Sub = [118,118,125,119,120,121,122,123,129,130,130,127,124,128]
Axes_2H = [131,131,132,133,138,134,136,142,135,137,139,140,143,141]
Throwing = [288,274,275,276,290,281,282,291,277,285,296,278,283,284]

#For staves and charms, roll among all that you qualify for
StaffLevels = [1,4,6,10,20,30,40,50,60,100,150,9999]
CharmLevels = [1,6,11,16,21,26,31,36,41,9999]
Staves = [261,262,268,266,269,267,265,272,270,273,271,271]
Charms = [508,536,509,537,510,538,540,511,539,539]

NoAdjustmentWeps = [Herbalist_,Club_Shaman,Katana_Main,Katana_Sub,Katana_2H,Axes_Sub,Axes_2H,Throwing,Claws]
RegularWeps = [Swords_2H,Daggers,WeakSpears,Spears,Hammers,Maces,Clubs,Bows,Whips,Strikes,Slashes,Charges]
RandomWeps = [(Staves,StaffLevels),(Charms,CharmLevels)]



#Defining power levels of spells to assign to items
#Some spells (Erod, Venom-Fei, Sosareo, Honey Restorer, Diomente) are not included at all
SpellTierOne = [1,2,3,4,7,24,25,26,31,33,34,58]
SpellTierTwo = [5,6,8,10,29,36,41,51,52,53,57,60,61,62,66]
SpellTierThree = [9,11,12,13,17,30,32,37,41,42,55,56,59,63,64,65,67]
SpellTierFour = [15,16,18,19,20,35,39,40,44,45,46,68,69,71]
SpellTierFive = [21,23,43,47,48,49,50]

SpellTiers = [[1,2,3,4,7,24,25,26,31,33,34,58],[5,6,8,10,29,36,41,51,52,53,57,60,61,62,66],
    [9,11,12,13,17,30,32,37,41,42,55,56,59,63,64,65,67],[15,16,18,20,35,39,40,44,45,46,68,69,71],
    [19,21,23,43,47,48,49,50]]

SpellTierWeights = [5,4,3,2,1]

BreakChancesLow = [5,10,15,20,25]
BreakChancesMid = [10,20,25,30,35,40]
BreakChancesHigh = [40,50,60,70,80,90,100]

#Mastery Skills
PhysUp = 0
PhysUpPlus = 1
MagicUp = 2
MagicUpPlus = 3
ClericUp = 4
ClericUpPlus = 5
AlchUp = 6
AlchUpPlus = 7
#generic Magic UP/+1 here
SoulRelease = 10
Removal = 11
Steal = 12
Disassemble = 13
HighPurity = 14
Apothecary = 15
PursuitSweep = 16
CombatInstinct = 17
AlterFate = 18
AncientRites = 19
BloodOath = 20
HolyLanceArt = 21
Sanctuary = 22
SwallowReturn = 23
SurpriseAttack = 24

#To exclude unused skills Banking and Magic Power UP
ValidSkills = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23,24,25,26,27,28]
ValidMasteries = [0,1,2,3,4,5,6,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]

#defaults
SkillWeights = [2,3,2,2,3,2,4,3,4,4,3,4,4,3,4,3,4,3,3,3,2,2,4,3,3,2,1,2]
MasteryWeights = [2,10,1,3,1,3,2,2,1,2,2,3,2,2,2,1,1,1,1,1,1,1,2]

#Defining skills with overlapping effects
MageSkills = [0,1,2]
ClericSkills = [3,4,5]
AlchSkills = [6,19]
ThiefSkills = [10,11]

FighterMasteries = [0,1]
MageMasteries = [2,3]
ClericMasteries = [4,5]
AlchMasteries = [6,7]

#What mastery skills are associated with each base skill?
MasteryArray = [[2,3],[2,3],[2,3],[4,5],[4,5],[4,5],[6,7],[20],[10],[],[],[],
    [14],[],[],[],[15],[],[],[6],[],[17],[18],[],[],[],[],[],[]]
#What basic skills are associated with each mastery skill?
BaseArray = [[],[],[0,1,2],[0,1,2],[3,4,5],[3,4,5],[6],[6,7],[],[],[8],[],[],[],
    [12],[16],[],[21],[22],[],[8],[],[],[],[]]

#Defining linked skills - not functional unless their matching base skill is also present

LinkedSkills = [10,14,15,17,18]#Soul Release, High Purity, Apothecary, Combative Instinct, Alter Fate

#As above, but for skills that are still functional without their associated base skill
#Basically just the spell masteries

SemiLinkedSkills = [2,3,4,5,6,7,20]


#Monsters which should never be shuffled - bosses mostly
#Avi, Locust, Mimic, Shadow, Norse Tyrant, Believer, Worker Wing, Shadow Wing, Agg.Mimic,
#Burglar, Dead Miner, Researcher, Lionel, Floor Masters, Spirit,
#more bosses, Pixie, Layer, Sacrifice, Organ Lizards, Masters, NPCs
#Doppelgangers too, Blue Flame Elemental, Apostate

#Burglar, Geed, Snow/Water Dragon, Edelite not restricted among others

#May want to have additional markers for "strong" slots in addition to Level-based logic

#Some of these could be added into the pool if they were modified to have spells etc
RestrictedMonsters = [0,21,51,93,262,280,282,285,289,290,291,296,325,326,327,329,330,331,
    332,333,334,335,336,337,338,339,342,343,344,345,346,347,348,349,350,351,352,353,
    354,355,356,357,376,377,381,382,384,387,388,391,392,393,394,395,396,397,398,399,
    400,401,402,403,404,405,406,407,408,409,410,411,412,413,416,417,418,419,420,421,
    422,423,424,425,426,427,428,429]


#individual tables of summon resistances - values selected based on level
S_Tiny = [10,10,20,60]
S_Low = [20,30,40,70]
S_Mid = [30,40,50,80]
S_High = [60,70,80,90]
S_Huge = [85,90,90,95]
#Tables of summon resistance values for various families
#Chimeric,Undead,Elemental,Insect,Animal,Mythical,Ghost,Devil,Fighter,Mage,Thief,Beast,Giant,
FamilySummonResists = [S_Low,S_Low,S_Low,S_Tiny,S_Tiny,S_Mid,S_Low,S_High,S_High,S_Mid,
    S_Mid,S_High,S_Mid,S_Mid,S_Mid,S_Huge]

#Defining power levels of status attacks - governs minimum level they can appear at,
#And how much they scale
#Sleep, Poison, Paralysis, Silence, Confusion, Charm, Petrify, Behead, Drain, in order
StatusAttackDanger = [1,2,3,2,4,6,7,8,12]

#Defining danger level of spells used by monsters

#For each spell, the min and max valid levels, downgrade, upgrade
#If no upgrade/downgrade applicable, delete spell
#for max level, may be slightly random eg enemies can upgrade from Glass at levels 10-12

#Some enemies will lose spells at their original level under this setup
#This mainly affects Witch and Abbess and their Ziakalad/Argeiss ways
MonsterSpellLevels = [
    (1,11,0,4),     #Balad
    (1,30,0,6),     #Misama
    (0,0,0,0),      #Dioseed
    (8,17,1,8),     #Balados
    (8,22,1,12),    #Glass
    (10,150,2,55),  #Ramisama
    (3,20,0,10),    #Venom
    (10,44,4,15),   #Mabalad
    (9,25,5,19),    #Ziakal
    (12,42,7,20),   #Ravenom
    (5,999,0,0),    #Robuti
    (10,51,5,18),   #Maglass
    (10,40,52,20),  #Stoma
    (0,0,0,0),      #Sosareo
    (15,200,8,21),  #Rabalad
    (13,200,4,95),  #Argeiss
    (7,999,0,0),    #Hallobuti
    (16,999,12,0),  #Raglass
    (13,999,9,0),   #Ziakalad
    (21,999,13,108),#Rastoma
    (19,999,106,0), #Enterook Mista
    (0,0,0,0),      #Diomente
    (30,999,0,0),   #Miracle
    (1,10,0,32),    #Feiria
    (0,0,0,0),      #Harias
    (2,27,0,29),    #Tashif
    (0,0,0,0),      #Erod
    (1,10,0,39),    #Venom-Fei
    (5,200,26,108), #Latasif
    (7,60,0,0),     #Hallobukan
    (0,0,0,0),      #Zomperi
    (9,34,24,43),   #Feirima
    (1,10,0,39),    #Roodfei
    (0,0,0,0),      #Eroma
    (12,48,32,48),  #Rafelima
    (2,25,0,39),    #Mirror Eyes
    (5,30,0,30),    #Hallobukarm
    (0,0,0,0),      #Honey Restorer
    (13,999,36,0),  #Sama Eyes
    (13,45,0,49),   #Zefeifus
    (6,54,0,0),     #Robukand
    (0,0,0,0),      #Psi Drain
    (16,999,32,0),  #Feireed
    (0,0,0,0),      #Rizefus
    (14,999,0,0),   #Elnam
    (0,0,0,0),      #Psi Breath
    (28,999,0,0),   #Immolarati
    (17,999,35,0),  #Rafeireed
    (0,0,0,0),      #Rezefeid
    (17,400,40,0),  #Razefeis
    (1,52,0,0),     #Pomedoon
    (6,20,0,55),    #Rood
    (0,0,0,0),      #Mahamaha
    (0,0,0,0),      #Portal
    (11,200,52,108),#Rarood
    (5,999,0,0),    #Bulafei
    (5,999,0,0),    #Skorekh
    (5,29,0,61),    #Karacha
    (7,999,0,0),    #Orath
    (12,999,57,0),  #Lascorek
    (13,200,58,68), #Makaracha
    (0,0,0,0),      #Bifei
    (13,65,0,0),    #Yuniwa Coat
    (10,30,58,68),  #Pinto
    (5,999,0,0),    #Rapoolfei
    (8,999,0,0),    #Ramialf
    (0,0,0,0),      #Pendeku
    (14,999,64,0),  #Rapinto
    (12,200,0,0),   #Rapidos
    (0,0,0,0),      #Pendea Coat
    (15,500,51,0),  #Zeo Nadar
    (0,0,0,0),      #High Portal
    (0,0,0,0),      #Protectorate
    (0,0,0,0),      #Contract 1
    (0,0,0,0),      #Summon
    (0,0,0,0),      #Return
    (0,0,0,0),      #Contract 2
    (0,0,0,0),      #Summon
    (0,0,0,0),      #Return
    (0,0,0,0),      #Contract 3
    (0,0,0,0),      #Summon
    (0,0,0,0),      #Return
    (0,0,0,0),      #Contract 4
    (0,0,0,0),      #Summon
    (0,0,0,0),      #Return
    (0,0,0,0),      #Contract 5
    (0,0,0,0),      #Summon
    (0,0,0,0),      #Return
    (0,0,0,0),      #Contract 6
    (0,0,0,0),      #Summon
    (0,0,0,0),      #Return
    (0,0,0,0),      #Contract 7
    (0,0,0,0),      #Summon
    (0,0,0,0),      #Return
    (15,999,0,0),   #Strange Miasma Wave
    (0,999,0,0),    #Bells of Judgement
    (10,80,1,15),   #Self-Destruct
    (0,999,0,0),    #Mirror Ring
    (4,999,0,0),    #Draw
    (0,0,0,0),      #Summon (Monster - useless, so it's got to go)
    (8,999,0,0),    #Inhale
    (0,999,0,0),    #Eclipse (unknown effect)
    (0,999,0,0),    #Nap (heals user but puts to sleep)
    (10,80,0,108),  #Lullaby
    (10,200,0,108), #Nightmare
    (7,18,1,21),    #Holmic Gate - repurposing this as a weaker Enterook Mista
    (15,60,0,108),  #Mind Crush
    (14,999,0,0),   #Soul Trap
    (0,999,0,0),    #Old Aim
    (0,999,0,0),]   #Holy Word (dispel?)
    

