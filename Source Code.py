
import os
import time
from datetime import datetime as dt
#Created By @OfficialAhmed0

def play():
    def outro():
        
        print("\n")#2 SpaceLines
        time.sleep(2)
        print(
            """Thank you for using beta version of my tool .
        New version will be released as soon as I finish it. IT will be
        with GUI instead and more functionality stay toon.
        Follow me on Twitter for news and more tools 
        @OfficialAhmed0 .If you have any recommendation DM me.
        """)
        print("")#SpaceLine
        file2.close()
        os.remove("tmp2.txt")
        replay = input("Press Enter to quit")
        if replay == "":
            quit() 
    #Created By @OfficialAhmed0
    def intro():
        #Starting from here
        print("Please wait while I read your trophy file...")
        time.sleep(2)
        print("""
        1: My trophy level
        2: How many Platinum trophies
        3: How many Gold trophies
        4: How many Silver trophies
        5: How many Bronze trophies
        6: Total trophies
        7: Copy my trophies to a text file
        """)
        choosing()
        
    def today():
        now = dt.now()
        return now
    
    try:
        file = open("trpsummary.dat", "r")
        
    except:
        print(""" ERROR: Cannot find [trpsummary.dat] file
        Please make sure it's within the tool folder.
        Read [READ ME.txt] file to understand how it works.
        
        1: Quit  
        
        """)
        #Created By @OfficialAhmed0
        redo = input("Choose a number: ")
        if redo == "1":
            os.open("READ ME.txt")
        else:
            os.open("READ ME.txt")
            
    lines = file.readlines()
    line = lines[0]
    file2 = open("tmp2.txt", "w+")
    
    index_p = line.index(""""p""")
    
    wanted = ""
    for wanted_stuff in line[index_p:-2]:
        wanted += wanted_stuff
        
    for organize in wanted:
        if organize == ",":
            file2.write("\n")
        else:
            file2.write(organize)

    file2.write("\n" + "Created by @OfficialAhmed0")        
    file2 = open("tmp2.txt")
    lines = file2.readlines()
    count_lines = len(lines)    
        
    points = {
        
        "platinum" :  180,
        "gold" : 90,
        "silver" : 30,
        "bronze" : 15,
        
    }            
    
    #Created By @OfficialAhmed0
    def platinums():
        plats = ""
        for digit in lines[0]:
            check = digit
            if check.isdigit() == True:
                plats += check
            else:
                pass    
        return int(plats)
    #Created By @OfficialAhmed0
    def golds():
        golds = ""
        for digit in lines[1]:
            check = digit
            if check.isdigit() == True:
                golds += check
            else:
                pass        
        return int(golds)
    
    def silvers():
        silvs = ""
        for digit in lines[2]:
            check = digit
            if check.isdigit() == True:
                silvs += check
            else:
                pass            
        return int(silvs)
        
    def bronzes():
        brons = ""
        for digit in lines[3]:
            check = digit
            if check.isdigit() == True:
                brons += check
            else:
                pass           
        return int(brons)
    
    def total_trophies():
        x = platinums()
        y = golds()
        z = silvers()
        h = bronzes()
        result = ( x + y + z + h )
        return result
        
    def check_level(total_points):
        x = total_points
        if x < 200:
            y = 1
        if x < 600 and not x < 200:    
            y = 2
        if x < 1200 and not x < 600:    
            y = 3
        if x < 2400 and not x < 1200:    
            y = 4        
        if x < 4000 and not x < 2400:    
            y = 5
        #Created By @OfficialAhmed0
        if x < 6000 and not x < 4000:    
            y = 6
        if x < 8000 and not x < 6000:    
            y = 7        
        if x < 10000 and not x < 8000:    
            y = 8
        if x < 12000 and not x < 10000:    
            y = 9
        if x < 14000 and not x < 12000:    
            y = 10    
        if x < 16000 and not x < 14000:    
            y = 11
        if x < 24000 and not x < 16000:    
            y = 12
        if x < 32000 and not x < 24000:    
            y = 13        
        if x < 48000 and not x < 32000:    
            y = 14
        if x < 56000 and not x < 48000:    
            y = 15
        if x < 64000 and not x < 56000:    
            y = 16      
        if x < 72000 and not x < 64000:    
            y = 17
        #Created By @OfficialAhmed0
        if x < 80000 and not x < 72000:    
            y = 18
        if x < 88000 and not x < 80000:    
            y = 19   
        if x > 88000:
            y = "Impresive ,congrats my friend our system is only limited to level 20 so you passed that please let us know to add more [Twitter: @OfficialAhmed0].This is beta version"
        return  y
    
    def My_level():
        platinum_points = platinums() * points["platinum"]
        gold_points = golds() * points["gold"]
        silver_points = silvers() * points["silver"]
        bronze_points = bronzes() * points["bronze"]
        total_points = int(platinum_points + gold_points + silver_points + bronze_points)
        def show():
            print("Checking how many trophies you have...")
            time.sleep(2.5)
            print("") #Spaceline
            print("You are on level : " + str(check_level(total_points)))
            outro()
        show()        
        
    def choosing():
        choose = input("Choose the number:")    
        
        if choose == str(1): # My trophy level            
            print(My_level())
            outro()
            
        if choose == str(2): # How many Platinum trophies
            print("Calculating your Platinums...")
            time.sleep(2 )
            checking = platinums()
            if checking > 1:
                print("You have unlocked " + str(platinums()) + " Platinums")
                outro()
            else:
                print("You have unlocked " + str(platinums()) + " Platinum")
                outro()
        
        if choose == str(3 ): # How many Gold trophies
            print("Calculating your Gold...")
            time.sleep(2 )                
            checking = golds()
            if checking > 1:
                print("You have unlocked " + str(golds()) + " Gold trophies")
                outro()
            else:
                print("You have unlocked " + str(golds()) + " Gold trophy")  
                outro()
        #Created By @OfficialAhmed0
        if choose == str(4 ): # How many Silver trophies
            print("Calculating your Silvers...")
            time.sleep(2 )                
            checking = silvers()
            if checking > 1:
                print("You have unlocked " + str(silvers()) + " Silver trophies")
                outro()
            else:
                print("You have unlocked " + str(silvers()) + " Silver trophy")   
                outro()
        
        if choose == str(5 ): # How many Bronze trophies
            print("Calculating your Bronze...")
            time.sleep(2 )                
            checking = bronzes()
            if checking > 1:
                print("You have unlocked " + str(bronzes()) + " Bronze trophies")
                outro()
            else:
                print("You have unlocked " + str(bronzes()) + " Bronze trophy")
                outro()
        
        if choose == str(6 ): # Total trophies
    
            print("Calculating your trophies...")#Created By @OfficialAhmed0
            time.sleep(3)
            print("You have unlocked total trophies of " + str( total_trophies() ) )
            outro()
        
        if choose == str(7 ): # Copy my trophies to a text file
            print("Creating [My Trophies.txt] file within the tool folder...")
            time.sleep(1.9)
            print("<< Done >>")
            file = open("My Trophies.txt", "w+")
            file.write("As of [ " + str(today()) + " ]" + "\n" )
            file.write("\n")
            file.write("My Platinum trophies: " + str(platinums()) + "\n")
            file.write("My Gold trophies: " + str(golds()) + "\n")
            file.write("My Silver trophies: " + str(silvers()) + "\n")
            file.write("My bronze trophies: " + str(bronzes()) + "\n")
            file.write("\n")
            file.write("Total of: " + str(total_trophies()) + " trophies" + "\n")#Created By @OfficialAhmed0
            file.close()
            outro()
            
        if choose != str(1) and choose != str(2) and choose != str(3) and choose != str(4) and choose != str(5) and choose != str(6) and choose != str(7):
            print("Please choose a number between[1 - 7]")
            choosing()
            
        choosing()    
    intro()            
play()

#Created By @OfficialAhmed0
