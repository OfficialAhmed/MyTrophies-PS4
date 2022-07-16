from ftplib import FTP
import eel

eel.init('UI')

class My_trophies:
    def __init__(self):
        self.ftp = FTP()
        self.bronze_credit = 15
        self.silver_credit = 30
        self.gold_credit = 90
        self.plat_credit = 300
        self.users_dir = ""
        self.trophy_dir = ""
        self.ip = ""
        self.port = 0

    def connect(self, ip: str, port: int) -> tuple:
        """
        #############################
            Init PS4 connection
        #############################
        """
        try: 
            self.ip = ip
            self.port = port
            self.ftp.connect(self.ip, self.port)
            return (True, "listening")
        except TimeoutError:
            error = "PS4 didn't respond...\n1.Make sure IP and Port entered correctly and PS4 running the FTP\n2.Make sure both PC and PS4 connected on same WI-Fi connection"
            return (False, error)
        except Exception as e:
            error = str(e)
            return (False, error)

    def login(self) -> None:
        """
        ################################
            Login to and fetch users
        ################################
        """
        self.ftp.login("", "")
        if self.ftp.getwelcome():
            print("Connected!")

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
        
    def get_all_trophies(self) -> list:
        """
        ############################################
            Fetch user trophy data from trophy file
        ############################################
        """

        self.bronze = 936
        self.silver = 331
        self.gold = 122
        self.plat = 22
        total = self.bronze + self.silver + self.gold + self.plat
        return [self.bronze, self.silver, self.gold, self.plat, total]

    def get_user_info(self) -> tuple:
        def get_level_and_percent(points: int) -> int:
            """
            ##############################################################
                Calculate user level and the percent to reach next level
            ##############################################################
            """
            l100 = 5940 
            l200 = 9000 
            l300 = 45000 
            l400 = 90000 
            l500 = 135000
            l600 = 180000
            l700 = 225000
            l800 = 270000
            l900 = 315000
            
            # how many points to level up, each level require 
            if points <= l100:
                multiplier = 100
                level_points = l100
            elif points <= l200:
                multiplier = 200 
                level_points = l200
            elif points <= l300:
                multiplier = 300 
                level_points = l300
            elif points <= l400:
                multiplier = 400 
                level_points = l400
            elif points <= l500:
                multiplier = 500
                level_points = l500
            elif points <= l600:
                multiplier = 600
                level_points = l600
            elif points <= l700:
                multiplier = 700
                level_points = l700
            elif points <= l800:
                multiplier = 800
                level_points = l800
            elif points <= l900:
                multiplier = 900
                level_points = l900
            else:
                multiplier = 1000
                level_points = 360,000

            count = (points / level_points) * multiplier
            level = int(count)
            percentage = int((count - level) * 100)

            return (level, percentage)

        def get_icon(level: int) -> str:
            """
            ##########################################
                Determine what level icon to diplay
            ##########################################
            """
            if level >= 1 and level <= 299:
                return "Bronze"
            elif level >= 300 and level <= 599:
                return "Silver"
            elif level >= 600 and level <= 998:
                return "Gold"
            else:
                return "Platinum"

        points = self.get_points([
            self.bronze,
            self.silver,
            self.gold,
            self.plat
        ])

        level_and_percentage = get_level_and_percent(points)
        level, percentage = level_and_percentage
        icon = get_icon(level)

        return (level, percentage, icon)

    def get_trophies_to_levelup(self):
        """
        #########################################################
            Determine how many each trophy required to level up
        #########################################################
        """
        pass
    
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
def get_points(trophies: list):
    global ps4
    return ps4.get_points(trophies)

@eel.expose
def get_all_trophies():
    global ps4
    return ps4.get_all_trophies()

@eel.expose
def get_user_info():
    global ps4
    return ps4.get_user_info()

@eel.expose
def get_trophies_to_levelup(): #unimplemented
    global ps4
    return ps4.get_trophies_to_levelup()
    
@eel.expose
def get_app_ver():
    return 3.05

eel.start('index.html', port=9764, host='localhost',  mode='chrome', size=(800, 700))