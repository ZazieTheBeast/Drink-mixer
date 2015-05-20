__author__ = 'Kris Kass'
__version__ = 'Mixer v0.1'
from pump_functions import PumpFunctions
from db_functions import dbFunctions
import threading
import subprocess

class MainMenu:
    def __init__(self):
        self.__choice = None

    def print_menu(self):
        print(30 * '-')
        print(10 * '-' + " MAIN-MENU " + 9 * '-')
        print(30 * '-')
        print("1. Mix Drink")
        print("2. Change Pump Assignments")
        print("3. Add Drinks or Recipes")
        print("4. Maintenance")
        print("5. About/Help")
        print("6. Exit")
        print(30 * '-')

    def get_input(self):
        return self.__choice

    def set_input(self, choice):
        self.__choice = choice

    def show_options(self):
        self.print_menu()
        self.set_input(int(raw_input("Please input your choice: ")))
        if self.get_input() == 1:
            DrinkMenu().show_available()
            self.show_options()
        elif self.get_input() == 2:
            PumpFunctions().assign_pump()
            self.show_options()
        elif self.get_input() == 3:
            dbFunctions().db_drink_prompt()
            self.show_options()
        elif self.get_input() == 4:
            PumpFunctions().mainten()
            self.show_options()
        elif self.get_input() == 5:
            HelpMenu()
            self.show_options()
        elif self.get_input() == 6:
            print("exiting. Shutting off all pumps.")
            subprocess.call("pkill sleep", shell=True)
            for x in range(0,8):
                PumpFunctions().opPump(x,0)
            raise SystemExit
        else:
            print("Invalid choice, please enter one of the following options.")
            self.show_options()

class DrinkMenu:
    def __init__(self):
        print("These are your available drinks.")

    def get_input(self):
        return self.__choice

    def set_input(self, choice):
        self.__choice = choice

    def show_available(self):
        results = dbFunctions().db_connect(8)
        num = 1
        for row in results:
            print "%d. - %s" % (num,row[1])
            num += 1
        self.set_input(int(raw_input("Please input your choice: ")))
        print results[self.get_input()-1]
        self.create_drink(results[self.get_input()-1])

    def create_drink(self,drinkArray):
        self.drinkArray = drinkArray
        size = self.get_drink_size()
        print "Creating '%s'" % drinkArray[1]
        # remove nones
        drinkArray = filter(lambda v:v is not None, drinkArray[2:])
        # retrieve pump assignments
        assignments = dbFunctions().db_connect(9)
        for x in assignments:
            for y in drinkArray:
                if x[0] == y:
                    print drinkArray[drinkArray.index(y)+1]
                    threading.Thread(target=PumpFunctions().opPump,args=((x[1]-1),float(drinkArray[drinkArray.index(y)+1])*size)).start()
                    #print "pump is %s ammount is %d" % ((x[1]-1),float(drinkArray[drinkArray.index(y)+1])*size)

    def get_drink_size(self):
        oneOz = float(20)
        print("Please select your drink size")
        print("1. Shot (1.5 oz.)")
        print("2. Rocks Glass (8 oz)")
        print("3. High ball (10 oz)")
        print("4. Collins Glass (14 oz)")
        print("5. Beer Mug (16 oz)")
        choice = int(input("Please input your choice: "))
        if choice == 1:
            return (oneOz * float(1.5))
        elif choice == 2:
            return (oneOz * float(8))
        elif choice == 3:
            return (oneOz * float(10))
        elif choice == 4:
            return (oneOz * float(14))
        elif choice == 5:
            return (oneOz * float(16))
        else:
            print "invalid choice"

class HelpMenu:
    def __init__(self):
        print("Welcome to the help menu.")
        print(__version__ + " Written by " + __author__)

if __name__ == '__main__':
    session = MainMenu()
    session.show_options()
