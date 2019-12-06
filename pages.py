import tkinter as tk
from tkinter import ttk
import adafruit_fingerprint
from digitalio import DigitalInOut, Direction
import busio
import board
import serial
import time
from db import Database
from adafruit_pn532.spi import PN532_SPI

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D8)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
pn532.SAM_configuration()

uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
for i in range(1, 100):
    
    finger.delete_model(i)

db = Database('students.db')

def read_UID(): 

    while True:
        uid = pn532.read_passive_target()
        if uid is not None:
            break

    return int.from_bytes(uid, byteorder='big', signed=False)

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_fast_search() != adafruit_fingerprint.OK:
        print("finished searching1")
        return False
    print("finished searching")
    return True

def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="", flush=True)
        else:
            print("Place same finger again...", end="", flush=True)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            elif i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="", flush=True)
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="", flush=True)
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="", flush=True)
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True

class Attendance(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.geometry("1024x600")
        container.grid(row=0, column=0, sticky=tk.N)
        self.frames = {}
        
        
        for F in (StartPage, CheckInPage, RegisterPage, EnrollNFCPage, AdminPage, ProfilePage):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        
        self.show_frame(StartPage)
        
    def show_frame(self, container):
        
        frame = self.frames[container]
        frame.tkraise()

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.label = tk.Label(self, text="Home")
        self.label.grid(row=0, column=1, sticky=tk.N)
        
        button_style = ttk.Style()
        button_style.configure('TButton', font=('calibri', 50, 'bold'), borderwidth='4')
        
        self.checkInButton = ttk.Button(self, text="Check In", style='TButton', command=lambda: controller.show_frame(CheckInPage))
        self.checkInButton.grid(row=1, column=0, padx=90, pady=50)
        
        self.registerButton = ttk.Button(self, text="Register", command=lambda: controller.show_frame(RegisterPage))
        self.registerButton.grid(row=1, column=2, padx=100, pady=50)
        
        self.profileButton = ttk.Button(self, text="My Profile", command=lambda: controller.show_frame(ProfilePage))
        self.profileButton.grid(row=2, column=0, padx=100, pady=50)
        
        self.adminButton = ttk.Button(self, text="Admin", command=lambda: self.goToAdmin(controller))
        self.adminButton.grid(row=2, column=2, padx=100, pady=50)
    
    def goToAdmin(self, controller):
        
        controller.frames[AdminPage].populate_list()
        controller.show_frame(AdminPage)
    
    def goToProfile(self, controller):
        
        controller.frames[ProfilePage].update_Profile()
        controller.show_frame(ProfilePage)
        
class CheckInPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        
        
        self.scanLabel = tk.Label(self, text="Please Scan NFC Card!", font=("Helvetica", 20))
        self.scanLabel.grid(row=0, column=1, padx=350, pady=30)
        
        self.fingerLabel = tk.Label(self, text="Then Scan your finger!", font=("Helvetica", 20))
        self.fingerLabel.grid(row=2, column=1, pady=30)
        
        self.backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        self.backButton.grid(row=4, column=1, pady=60)
        
        self.scanCardButton = ttk.Button(self, text="Scan Card", command=lambda: self.scanCard(controller))
        self.scanCardButton.grid(row=1, column = 1)
        
        self.scanFingerButton = ttk.Button(self, text="Scan Finger", command=lambda: self.scanFinger(controller))
        self.scanFingerButton.grid(row=3, column = 1)
    
    def scanCard(self, controller):
        
        uid = read_UID()
        sid = db.fetch_SID_from_UID(uid)
        controller.frames[ProfilePage].sid
        print(sid)
        
    def scanFinger(self, controller):
        
        
        temp_id = db.fetchID(controller.frames[ProfilePage].sid)
        print(temp_id)
        if get_fingerprint():
            print("scanned the finger")
            print("finger.finger_id = ", finger.finger_id)
            if temp_id == finger.finger_id:
                print("checked in")
                db.changeToPresent(temp_id)
            else:
                print("print doesnt match")
        else:
            print("could not get a fingerprint")
                
class RegisterPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.label = tk.Label(self, text="Register Page")
        self.label.grid(row=0, column=1)
        
        self.first_text = tk.StringVar()
        self.last_text = tk.StringVar()
        self.sid_text = tk.StringVar()
        
        self.first_label = tk.Label(self, text="First Name")
        self.first_label.grid(row=1, column=0, padx=50)
        self.first_entry = tk.Entry(self, textvariable=self.first_text)
        self.first_entry.grid(row=1, column=1)
        
        self.last_label = tk.Label(self, text="Last Name")
        self.last_label.grid(row=2, column=0)
        self.last_entry = tk.Entry(self, textvariable=self.last_text)
        self.last_entry.grid(row=2, column=1)
        
        self.sid_label = tk.Label(self, text="Student ID")
        self.sid_label.grid(row=3, column=0)
        self.sid_entry = tk.Entry(self, textvariable=self.sid_text)
        self.sid_entry.grid(row=3, column=1)
        
        self.back_button = tk.Button(self, text="Back", command= lambda: controller.show_frame(StartPage))
        self.back_button.grid(row=4, column=0)
        
        self.enter_button = tk.Button(self, text="Enter", command= lambda: self.add_student(controller))
        
        self.enter_button.grid(row=4, column=1)
    
    def getNewSID(self):
        
        return self.sid_text
    
    def add_student(self, controller):
        
        db.insert(self.sid_text.get(), self.first_text.get(), self.last_text.get())
        controller.frames[ProfilePage].first_name = self.first_text.get()
        controller.frames[ProfilePage].last_name = self.last_text.get()
        controller.frames[ProfilePage].sid = self.sid_text.get()
        
        controller.show_frame(EnrollNFCPage)
        
        
        
        
class EnrollNFCPage(tk.Frame):
    
     
    def __init__(self, parent, controller):
         
         tk.Frame.__init__(self, parent)
         
         self.enroll_label = tk.Label(self, text="Enroll Your NFC Card and Fingerprint!", font=("Helvetica", 20))
         self.enroll_label.grid(row=0, column=1, pady=50)
         
         self.enrollNFC_button = ttk.Button(self, text="Enroll Card", command=lambda: self.enrollNFC(controller))
         self.enrollNFC_button.grid(row=1, column=1, padx=350)
         
         self.enrollFingerPrint_button = ttk.Button(self, text="Enroll Fingerprint", command=lambda: self.enrollFingerprint(controller))
         self.enrollFingerPrint_button.grid(row=2, column=1, padx=50, pady=50)
         
         self.returnHome_button = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
         self.returnHome_button.grid(row=3, column=1)
         
    def enrollNFC(self, controller):
        
        uid = read_UID()
        sid = controller.frames[ProfilePage].sid
        index = db.fetchID(sid)
        db.registerUID(index, uid)
         
        
    def enrollFingerprint(self, controller):
        
        sid = controller.frames[ProfilePage].sid
        
        index = db.fetchID(sid)
        
        if enroll_finger(index):
            print("success")
        else:
            print("failed")
        
        
        
         
        
        

class AdminPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.admin_label = tk.Label(self, text="Admin View")
        self.admin_label.grid(row=0, column=0)
        
        self.list = tk.Listbox(self, height=20, width=50)
        self.list.grid(row=2, column=0, padx=20)
        
        self.back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        self.back_button.grid(row=3, column=0, pady= 20)
        
        self.reset_button = ttk.Button(self, text="Reset", command=lambda: self.reset_list())
        self.reset_button.grid(row=3, column=1)
        
        self.populate_list()
    
    def reset_list(self):
        
        db.resetToAbsent()
        
        self.populate_list()
    
    def populate_list(self):
        
        self.list.delete(0, tk.END)
        
        for row in db.fetch():
            
            self.list.insert(tk.END, row[0:5])
        
        
class ProfilePage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.first_name = ""
        self.last_name = ""
        self.sid = ""
        
        self.header_label = tk.Label(self, text="Check In or Register to view your profile")
        self.header_label.grid(row=0, column=0)
        
        self.back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        self.back_button.grid(row=1, column=0)
        
        
    def update_Profile(self):
        
        if self.first_name == "":
            self.header_label.text = "Check In or Register to view your profile"
            
        else:
            header_text = StringVar()
            header_text.set("Hello {} {} !".format(self.first_name, self.last_name))
            self.header_label.text = header_text
        
        
app = Attendance()
app.mainloop()        
        
        
        
        