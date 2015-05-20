__author__ = 'Kris'
from db_functions import dbFunctions
import subprocess
import threading

class PumpFunctions:
    #def __init__(self):
    #    print("You can control your pump settings here.")
    def assign_pump(self):
        print("1. Show pump assignments")
        print("2. Add pump assignment")
        choice = int(input("Please input your choice: "))
        if choice == 1:
            dbFunctions().db_connect(6)
        elif choice == 2:
            dbFunctions().db_connect(7)


    def opPump(self,pump_num,time):
        if time != 0:
            theCall = "sudo gpio mode %s out && sleep %s && gpio mode %s in" % (str(pump_num),str(time),str(pump_num))
        else:
            theCall = "sudo gpio mode %s in" % str(pump_num)
        subprocess.call(theCall, shell=True)

    def mainten(self):
        print("Here you can preform maintenance procedures on your pumps.")
        print("1. Prime Pumps")
        print("2. Back")
        choice = int(input("Please input your choice: "))
        if choice == 1:
            for x in range(0,8):
                threading.Thread(target=self.opPump, args=(x,str("6.5"))).start()
                #self.opPump(x,str("6.5"))

        else:
            print "returning to main menu"
