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
        self.ftp.connect(self.ip, self.port)
        self.ftp.login("", "")
        if self.ftp.getwelcome():
            print("Hello from PlayStation")
            return True
        else:
            print("Cannot connect")
            return False

@eel.expose
def initialize(input: str):
    user_input = input.split(",")
    playstation = My_trophies(user_input[0], user_input[1])
    playstation.connect()
    

eel.start('index.html', size=(700, 600))