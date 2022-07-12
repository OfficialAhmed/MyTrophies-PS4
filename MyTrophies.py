from ftplib import FTP
import eel

eel.init('UI')

class My_trophies:
    def __init__(self, ip: str, port: int):
        self.ftp = FTP()
        self.ip = ip
        self.port = port
        self.dir = ""

    def connect(self):
        try: 
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
        
playstation = None

@eel.expose
def init_connection(ip: str, port: str):
    global playstation
    playstation = My_trophies(ip, int(port.strip()))
    respond = playstation.connect()
    return respond    

    
eel.start('index.html', port=9764, host='localhost',  mode='chrome', size=(700, 600))