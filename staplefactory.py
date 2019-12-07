import shelve
import time
import math
import sys

global autosave
autosave=False
global exiting
exiting=False
global staples
staples=0
global multiplier
multiplier= 1
global layer
layer=0

buildingprice=[]
buildings=[]
buildingname=[]
lasttime= time.time()
try:
    savefile = shelve.open('savefile')
    staples = savefile['staples']
    multiplier = savefile['multiplier']
    buildings = savefile['buildings']
    buildingname = savefile['buildingname']
    lasttime = savefile['lasttime']
    autosave= savefile['autosave']
except KeyError:
    pass

savefile.close()
print("You start your staple company.......\n Press/hold enter to make a staple")
def namelayer():
    layer= int(input("Which tier would you like to rename?: "))
    name = str(input("What would you like to name this tier?: "))
    buildingname[layer] = name

def addsps(lasttime):
    global staples
    global multiplier
    global autosave
    countingsps=0
    for position in buildings:
        countingsps=countingsps + (5**position) * buildings[position]
    timenow=time.time()
    timedifference = int(timenow) - int(lasttime)
    lasttime = time.time()
    staples=staples + countingsps * timedifference * multiplier
    

def buy():
    global staples
    global multiplier
    global autosave
    global layer
    for i in buildings:
        try:
            print("cost: " + str((5**buildings[i])*buildings[i]) + " name: " +buildingname[i] + " amount: " + str(buildings[i]))
        except KeyError:
            buildingname[i]="unnamed"
            print(buildingname[i] + ": " + str(buildings[i]))
    layer = int(input("What building tier would you like to buy? (enter 0 for max): "))
    #tries to buy 1 of the highest building it can, else sets amount to 0
    max = 0
    prevmax = 0
    if layer == 0:
        solved = False
        while not solved:
            try:
                while (staples / ((((5**max) *10))* 1.15**buildings[layer])) > 1:
                    prevmax= max
                    max=max+1
                layer=prevmax
                solved=True
            except:
                buildings[layer]=0
        layer = prevmax
        
    
        
    # checks if you can afford what you want, otherwise sets it to buy max
    amount = int(input("How many would you like to buy? (enter 0 for max): "))
    try:
        if amount * buildingprice[layer] * 1.15**buildings[layer]  > staples:
            amount = 0
    except KeyError:
        buildingprice[layer]= 5**layer * 10
        if amount*buildingprice[layer] > staples:
            amount = 0
        
        
    #if 0 amount buy max of layer
    try:
        buildingprice[layer]=buildingprice[layer]
        if amount == 0:
            amount = math.floor(staples/ (buildingprice[layer] *1.15**buildings[layer])) 
    except KeyError:
        buildingprice[layer] = math.ceil(5**layer * 10 )
        if amount == 0:
            amount = math.floor(staples/ buildingprice[layer])
    staples=staples- buildingprice[layer] * amount
    
    #adds the number of buildings to the slot
    try:
        buildings[layer]=buildings[layer] + amount
    except KeyError:
        buildings[layer]=0
        buildingname[layer]= input("What would you like to name this building type?(layer "+str(layer)+ ")")
        buildings[layer]=buildings[layer] + amount
    
def status():
    global autosave
    global staples
    global multiplier
    print ("\nStaples: " + str(staples))
    print ("Multiplier: x"+str(multiplier))
    for i in buildingname:
        print (str(i) + ") costs " + str(math.ceil((5**i * 10)* 1.15**buildings[i])) + " )" + str(buildings[i])+" "+ str(buildingname[i]) + "s make " + str(5**i *buildings[i]*i) +  " staples per second. " + str(5**i * i)+" each")
def choose():
    global staples
    global multiplier
    global autosave
    global exiting
    prevmax=0
    for i in buildings:
        if buildings[i] !=0:
            prevmax = i + 1
        else:
            prevmax=1
    choice=int(input("What option would you like to choose?\n1) Buy a building\nNext building layer is "+ str(prevmax) + " and costs " + str(5**prevmax * 10)+"\n2) Buy multiplier\nNext multiplier costs "+str(10000**multiplier) + "\n3) Name a layer\n4) Toggle Autosave\n" + str(autosave) + "\n 5) Save and Quit\n"))
    if choice == 1:
        buy()
    if choice == 2:
        if staples >= (10000**multiplier):
            print("layer multiplier")
            staples=staples-10000**(multiplier)
            multiplier=multiplier+1
        else:
            print ("Can't afford that")
    if choice == 3:
        namelayer()
    if choice == 4:
        if autosave==True:
            autosave = False
        else:
            if autosave==False:
                autosave=True
    if choice == 5:
        global exiting
        exiting = True
       
   
while True:
    addsps(lasttime)
    lasttime= time.time()
    status()
    try:
        choose()
    except ValueError:
        staples=staples+1
    if exiting == 1:
        savefile = shelve.open('savefile')
        savefile['staples'] = staples
        savefile['multiplier'] = multiplier
        savefile['buildings'] = buildings
        savefile['buildingname'] = buildingname
        savefile['buildingprice'] = buildingprice
        savefile['lasttime'] = lasttime
        savefile['autosave'] = autosave
        savefile.close()
        sys.exit()
    if autosave==1:
        savefile = shelve.open('savefile')
        savefile['staples'] = staples
        savefile['multiplier'] = multiplier
        savefile['buildings'] = buildings
        savefile['buildingname'] = buildingname
        savefile['buildingprice'] = buildingprice
        savefile['lasttime'] = lasttime
        savefile['autosave'] = autosave
        savefile.close()
