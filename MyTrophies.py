from ftplib import FTP
from typing import final
import eel

eel.init('UI')

class My_trophies:
    def __init__(self):
        self.ftp = FTP()
        self.bronze_credit = 15
        self.silver_credit = 30
        self.gold_credit = 90
        self.plat_credit = 300
        self.users_dir = "user/home/"
        self.trophy_dir = "trophy/data/sce_trop/"
        self.connection = 0

        # Levels 1 - 99: 60 points
        # Levels 100 - 199: 90 points
        # Levels 200 - 299: 450 points
        # Levels 300 - 399: 900 points
        # Levels 400 - 499: 1350 points
        # Levels 500 - 599: 1800 points
        # Levels 600 - 699: 2250 points
        # Levels 700 - 799: 2700 points
        # Levels 800 - 899: 3150 points
        # Levels 900 - 999: 3600 points

        self.l1 = 6000  # Levels 1 - 99
        self.l2 = 9000  
        self.l3 = 45000 
        self.l4 = 90000 
        self.l5 = 135000
        self.l6 = 180000
        self.l7 = 225000
        self.l8 = 270000
        self.l9 = 315000  # Levels 900 - 999
        self.lvl = (self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9)

    def connect(self, ip: str, port: int) -> tuple:
        """
        #############################
            Init PS4 connection
        #############################
        """

        def is_PS4() -> tuple:
            """
            #############################
                Check if it's PS4 FTP
            #############################
            """
            try:
                self.ftp.login("", "")
                self.ftp.cwd(self.users_dir)
                self.connection = 1
                return (True, "PS4 listening...")
            except Exception as e:
                return (False, str(e))

        if self.connection != 0:
            return (True, "You've been already connected\nPS4 FTP refuses multiple connection \n*Reopen MyTrophies if you experience any issues after this message.\n")
        else:
            try: 
                self.ip = ip
                self.port = port
                self.ftp.connect(self.ip, self.port)
                return (is_PS4())
            except TimeoutError:
                error = "PS4 didn't respond...\n1.Make sure IP and Port entered correctly and PS4 running the FTP\n2.Make sure both PC and PS4 connected on same WI-Fi connection"
                return (False, error)
            except Exception as e:
                error = str(e)
                return (False, error)

    def login(self) -> bool:
        """
        ################################
            check connection
        ################################
        """
        if self.ftp.getwelcome():
            return True
        else:
            return False

    def get_users(self) -> dict:
        """
        #######################################
            Get usernames available in system
        #######################################
        """
        if self.login():
            user_id = []
            self.ftp.retrlines("LIST ", user_id.append)
            user_id = [x.strip().split(" ")[-1] for x in user_id if len(x)>4]
            user_id = user_id[2:] #[FIX v3.07] ignore first 2 FTP commands
            user_name = []

            def fetch_user_name(name):
                user_name.append(name.strip("\x00"))

            for id in user_id:
                self.ftp.cwd("/" + self.users_dir + id + "/")
                try:
                    self.ftp.retrlines("RETR username.dat", fetch_user_name)
                except:
                    fetch_user_name("Unknown\x00")
            
            user_name = dict(zip(user_id, user_name))
            return user_name
        return dict()

    def get_points(self, trophies: list) -> int:
        """
        ##################################################
            Calculate trophy points from (param:trophies)
        ##################################################
        """
        b, s, g, p = trophies

        b *= self.bronze_credit
        s *= self.silver_credit
        g *= self.gold_credit
        p *= self.plat_credit

        return b+s+g+p
        
    def get_all_trophies(self, user, user_bronze: int, user_silver: int, user_gold: int, user_plat: int) -> list:
        """
        ############################################
            Fetch user trophy data from trophy file
        ############################################
        """
        self.bronze, self.silver, self.gold, self.plat = 0,0,0,0

        def fetch_trophies_from_file(file):
            import json as js
            trophies = js.loads(file)
            trophies = trophies["earnedTrophies"]
            self.bronze = int(trophies["bronze"]) + user_bronze
            self.silver = int(trophies["silver"]) + user_silver
            self.gold = int(trophies["gold"]) + user_gold
            self.plat = int(trophies["platinum"]) + user_plat
        try:
            self.ftp.cwd(f"/{self.users_dir}/{user}/{self.trophy_dir}")
            self.ftp.retrlines("RETR trpsummary.dat", fetch_trophies_from_file)

        except Exception as e:
            print(str(e))
        finally:
            self.ftp.cwd("/")


        total = self.bronze + self.silver + self.gold + self.plat
        return [self.bronze, self.silver, self.gold, self.plat, total]

    def get_user_info(self, user_bronze: int, user_silver: int, user_gold: int, user_plat: int) -> tuple:
        def convert_points_to_level(points: int) -> int:
            """
            ########################################################################################
                                    Convert user points to level algo
            ########################################################################################
            """
            
            #####################################################################################################
            ######    Take out required levels' points to determine 100th number of the user level    ###########
            #####################################################################################################

            # one_level_up is the required points to level up by one
            # level_100th is the user level in 100th
            level_100th = 0
            one_level_up = self.l1
            for l in self.lvl:
                if points - l <= 0:
                    one_level_up = l
                    break
                
                points -= l
                level_100th += 100
                one_level_up = l

            #####################################################################################################
            ######             determine the 10th number by taking out one_level_up points          #############
            #####################################################################################################
            
            one_level_up /= 100 
            level_10th = int(points / one_level_up)
            return level_100th + level_10th


        def get_level_and_percent(points: int) -> int:
            """
            ##############################################################
                    Calculate user level and the percent to level up
            ##############################################################
            """

            # how many points to level up, each level require 
            if points <= self.l1:
                self.milestone = self.l1
                self.next_milestone = self.l2
            elif points <= self.l2:
                self.milestone = self.l2
                self.next_milestone = self.l3
            elif points <= self.l3:
                self.milestone = self.l3
                self.next_milestone = self.l4
            elif points <= self.l4:
                self.milestone = self.l4
                self.next_milestone = self.l5
            elif points <= self.l5:
                self.milestone = self.l5
                self.next_milestone = self.l6
            elif points <= self.l6:
                self.milestone = self.l6
                self.next_milestone = self.l7
            elif points <= self.l7:
                self.milestone = self.l7
                self.next_milestone = self.l8
            elif points <= self.l8:
                self.milestone = self.l8
                self.next_milestone = self.l9
            elif points <= self.l9:
                self.milestone = self.l9
                self.next_milestone = 360,000
            else:
                self.milestone = 360,000

            self.leveup_points = self.milestone // 100

            self.level = convert_points_to_level(points)
            tmp_num = (self.next_milestone - points) / self.leveup_points
            percent = tmp_num - int(tmp_num)
            self.percentage = int(percent * 100)

            return (self.level, self.percentage)

        def get_icon(level: int) -> str:
            """
            ####################################################
                    Determine what level icon to diplay
            ####################################################
            """
            icon = ""
            if level >= 1 and level <= 299:
                if level >= 200:
                    icon = "Bronze3" 
                elif level >= 100:
                    icon = "Bronze2"
                else:
                    icon = "Bronze1"
                    
            elif level >= 300 and level <= 599:
                if level >= 500:
                    icon = "Silver3" 
                elif level >= 400:
                    icon = "Silver2"
                else:
                    icon = "Silver1"

            elif level >= 600 and level <= 998:
                if level >= 800:
                    icon = "Gold3" 
                elif level >= 700:
                    icon = "Gold2"
                else:
                    icon = "Gold1"

            else:
                icon = "Platinum1"

            return icon

        self.user_accumulated_points = self.get_points([
            self.bronze + user_bronze,
            self.silver + user_silver,
            self.gold + user_gold,
            self.plat + user_plat
        ])

        level_and_percentage = get_level_and_percent(self.user_accumulated_points)
        level, percentage = level_and_percentage
        icon = get_icon(level)

        return (level, percentage, icon)

    def get_trophies_to_levelup(self) -> list:
        """
        #########################################################
            Determine how many each trophy required to level up
        #########################################################
        """
        import math
        next_milestone_points = self.milestone - self.user_accumulated_points
        next_level_points = next_milestone_points / self.leveup_points

        decimals, intgers = math.modf(next_level_points) #yield tuble (decimals: float, integer: float)
        next_level_trophies = self.leveup_points - (decimals * self.leveup_points)

        bronze = int(next_level_trophies / self.bronze_credit) + 1
        silver = int(next_level_trophies / self.silver_credit) + 1
        gold = int(next_level_trophies / self.gold_credit) + 1
        platinum = int(next_level_trophies / self.plat_credit) + 1

        # NOTE: if any trophy equal to 0, JS will increment it by 1
        return [bronze, silver, gold, platinum]

    def export_file(self, username) -> str:
        import datetime as dt

        t = dt.datetime.now()
        timestamp = str(t.day) + "_" + str(t.month) + "_" + str(t.year)[2:] + " " + str(t.hour) + "_" + str(t.minute) + "_" + str(t.second)
        try:
            with open(f"{username} ({timestamp}).txt", "w") as file:
                content = f"""
                * GENERATED FILE: MyTrophies v3 by @Officialahmed0

                Account: {username}
                Level: {self.level}
                Total Trophies: {self.bronze + self.silver + self.gold + self.plat}
                Total Points: {self.user_accumulated_points}
                ___________________________________________________
                Total Bronze: {self.bronze}
                Total Silver: {self.silver}
                Total Gold: {self.gold}
                Total Platinums: {self.plat}

                Time Stamp: {timestamp.replace("_", ":")}
                """
                file.write(content)
                status = "success"
        except Exception as e:
            status = str(e)

        return status

"""
###########################################################
   Functions of My trophies instance called by JavaScript
###########################################################
"""
ps4 = My_trophies()

@eel.expose
def init_connection(ip: str, port: str) -> tuple:
    global ps4
    return ps4.connect(ip, int(port.strip()))    

@eel.expose
def get_users():
    global ps4
    return ps4.get_users()

@eel.expose
def get_points(trophies: list):
    global ps4
    return ps4.get_points(trophies)

@eel.expose
def get_all_trophies(user, user_bronze, user_silver, user_gold, user_plat):
    global ps4
    return ps4.get_all_trophies(user, user_bronze, user_silver, user_gold, user_plat)

@eel.expose
def get_user_info(user_bronze, user_silver, user_gold, user_plat):
    global ps4
    return ps4.get_user_info(user_bronze, user_silver, user_gold, user_plat)

@eel.expose
def get_trophies_to_levelup():
    global ps4
    return ps4.get_trophies_to_levelup()

@eel.expose
def export_file(username):
    global ps4
    return ps4.export_file(username)
    
@eel.expose
def get_app_ver():
    return 3.05

eel.start('index.html', port=9764, host='localhost',  mode='chrome', size=(800, 700))