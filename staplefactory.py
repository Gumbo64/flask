import shelve
import time
import math
import sys
# in table we will need:
# username
# staples
# buildingprice
# buildings
# buildingname={}
# lasttime= time.time()

#take variables from table


print("You start your staple company.......\n Press/hold enter to make a staple")


def namelayer():
    layer= int(input("Which tier would you like to rename?: "))
    name = str(input("What would you like to name this tier?: "))

    #into table
    buildingname[layer] = name

def addsps(lasttime):
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
    global bought
    for i in buildings:
        try:
            print("cost: " + str((5**buildings[i])*buildings[i]) + " name: " +buildingname[i] + " amount: " + str(buildings[i]))
        except KeyError:
            buildingname[i]="unnamed"
            print(buildingname[i] + ": " + str(buildings[i]))
    bought = int(input("What building tier would you like to buy? (enter 0 for max): "))
    #tries to buy 1 of the highest building it can
    max = 0
    prevmax = 0
    if bought == 0:
        solved = False
        while not solved:
            try:
                while (staples / ((((5**max) *10))* 1.15**buildings[bought])) > 1:
                    prevmax= max
                    max=max+1
                bought=prevmax
                solved=True
            except:
                buildings[bought]=0
        bought = prevmax
        
    
        
    # checks if you can afford what you want, otherwise sets it to buy max
    quantity = int(input("How many would you like to buy? (enter 0 for max): "))
    try:
        if quantity * buildingprice[bought] * 1.15**buildings[bought]  > staples:
            quantity = 0
    except KeyError:
        buildingprice[bought]= 5**bought * 10
        if quantity*buildingprice[bought] > staples:
            quantity = 0
        
        
    #if 0 quantity buy max of bought
    try:
        buildingprice[bought]=buildingprice[bought]
        if quantity == 0:
            quantity = math.floor(staples/ (buildingprice[bought] *1.15**buildings[bought])) 
    except KeyError:
        buildingprice[bought] = math.ceil(5**bought * 10 )
        if quantity == 0:
            quantity = math.floor(staples/ buildingprice[bought])
    staples=staples- buildingprice[bought] * quantity
    
    #adds the number of buildings to the slot
    try:
        buildings[bought]=buildings[bought] + quantity
    except KeyError:
        buildings[bought]=0
        buildingname[bought]= input("What would you like to name this building type?(layer "+str(bought)+ ")")
        buildings[bought]=buildings[bought] + quantity
    
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
            print("Bought multiplier")
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
    #save