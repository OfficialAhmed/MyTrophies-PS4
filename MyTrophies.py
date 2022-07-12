from ftplib import FTP
import eel

eel.init('UI')

class My_trophies:
    def __init__(self):
        self.ftp = FTP()
        self.ip = ""
        self.port = 0
        self.dir = ""

    def connect(self, ip: str, port: int):
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

    def login(self):
        self.ftp.login("", "")
        if self.ftp.getwelcome():
            pass

    def calculate_points(self, trophies):
        bronze_credit = 15
        silver_credit = 30
        gold_credit = 90
        plat_credit = 300

        b, s, g, p = trophies

        b *= bronze_credit
        s *= silver_credit
        g *= gold_credit
        p *= plat_credit

        return int(b+s+g+p)
        
ps4 = My_trophies()

@eel.expose
def init_connection(ip: str, port: str):
    global ps4
    respond = ps4.connect(ip, int(port.strip()))
    return respond    

    
eel.start('index.html', port=9764, host='localhost',  mode='chrome', size=(700, 600))

@eel.expose
def calculate(trophies):
    global ps4
    return ps4.calculate_points(trophies)

@eel.expose
def get_app_ver():
    return 3.05

eel.start('index.html', port=9764, host='localhost',  mode='chrome', size=(800, 700))