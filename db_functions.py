__author__ = 'Kris'
import MySQLdb as md

class dbFunctions:
    def __init__(self):
        print("Checking MySQL database connection.")

    def db_drink_prompt(self):
        print("What would you like to do?")
        print(30 * '-')
        print(10 * '-' + " DB Menu " + 9 * '-')
        print(30 * '-')
        print("1. Show database version / status")
        print("2. List all drinks")
        print("3. Add a drink")
        print("4. List all mixes")
        print("5. Add a mix")
        print("6. Return to main menu")
        print(30 * '-')
        choice = int(raw_input("Please input your choice: "))
        if choice == 1:
            self.db_connect(1)
            self.db_drink_prompt()
        elif choice == 2:
            self.db_connect(2)
            self.db_drink_prompt()
        elif choice == 3:
            self.db_connect(3)
            self.db_drink_prompt()
        elif choice == 4:
            self.db_connect(4)
            self.db_drink_prompt()
        elif choice == 5:
            self.db_connect(5)
            self.db_drink_prompt()
        elif choice == 6:
            print("not yet implemented")

    def db_connect(self,option):
        print("Connecting...")
        db = md.connect(
            host="localhost",
            user="root",
            passwd="password",
            db="MIXER")
        cur = db.cursor()
        if option == 1:
            if db.open:
                print("connection successful!")
                cur.execute("SELECT VERSION()")
                version = cur.fetchone()
                print "Database version: %s " % version
        elif option == 2:
            # show drink list
            self.show_drinks_list(cur)
        elif option == 3:
            # show add drink
            self.add_drink(cur)
        elif option == 4:
            # show mixes
            self.show_mix_list(cur)
        elif option == 5:
            self.add_mix_list(cur)
        elif option == 6:
            self.show_assignments(cur)
        elif option == 7:
            self.add_assignments(cur)
        elif option == 8:
            valid_rows = self.show_available_mix(cur,True)
            return valid_rows
        elif option == 9:
            assignments = self.show_assignments(cur)
            return assignments
        db.commit()
        db.close()

    def show_drinks_list(self,cur):
        self.cur = cur
        cur.execute("SELECT * FROM DRINK_LIST;")
        rows =  cur.fetchall()
        for row in rows:
            print row[1]

    def add_drink(self,cur):
        print("Please enter the new drinks information")
        self.cur = cur
        print("Warning! This will override any existing drink with this same ID!")
        choice_id = raw_input("lookup id of the drink: ")
        choice_nm = raw_input("drink name: ")
        choice_desc = raw_input("short description: ")
        qry_drop = "DELETE FROM DRINK_LIST WHERE drink_id = LOWER(\"%s\");" % choice_id
        qry_in = "INSERT INTO DRINK_LIST VALUES (\"%s\",\"%s\",\"%s\");" % (choice_id,choice_nm,choice_desc)
        cur.execute(qry_drop)
        cur.execute(qry_in)
        ans = raw_input("would you like to add another drink? (y/n) :")
        if ans == "y":
            self.add_drink(cur)
        else:
            self.db_drink_prompt()

    def show_mix_list(self,cur):
        self.cur = cur
        cur.execute("SELECT * FROM MIXES;")
        rows = cur.fetchall()
        for row in rows:
            print row

    def add_mix_list(self,cur):
        self.cur = cur
        print "Warning! Currently no error checking between tables, if keys don't match, it will not work!"
        print "Volumes must equal to 1 at the end!"
        choice_mix_nm = raw_input("Name of the mix: ")
        total = 0
        count = 0
        qry = "INSERT INTO MIXES "
        qry_columns = "(comb_desc,"
        qry_values = " VALUES ('%s'," % choice_mix_nm
        while total < 1:
            print "ingredient " + str(count+1)
            choice_nm = raw_input("id of drink " + str(count) +": ")
            choice_amt = float(raw_input("amount of drink 0-1: "))
            qry_columns = "%sdrink_id%d, drink_%d_amt," % (qry_columns,count,count)
            qry_values = "%s'%s','%f'," % (qry_values,choice_nm,choice_amt)
            count += 1
            total += choice_amt
        if total == 1:
            qry_columns = qry_columns[:-1] + ")"
            qry_values = qry_values[:-1] + ")"
            qry_in = "%s%s%s;" % (qry,qry_columns,qry_values)
            cur.execute(qry_in)
            print "New mix added!"
        else:
            print "an error! Did you make sure the the values are equal to exactly 1?"

    def show_available_mix(self,cur,pump):
        self.cur = cur
        self.pump = pump
        drink_list = []
        cur.execute("SELECT * FROM PUMP_DRINK;")
        rows =  cur.fetchall()
        for row in rows:
            drink_list.append(row[0])
        print drink_list
        valid_ids = []
        cur.execute("select * from MIXES where drink_id0 in (SELECT drink_id FROM PUMP_DRINK);")
        rows = cur.fetchall()
        for row in rows:
            done = False
            if (row[2] in drink_list) or (row[2] is None):
                if (row[4] in drink_list) or (row[4] is None):
                    if (row[6] in drink_list) or (row[6] is None):
                        if (row[8] in drink_list) or (row[8] is None):
                            if (row[10] in drink_list) or (row[10] is None):
                                if (row[12] in drink_list) or (row[12] is None):
                                    if (row[14] in drink_list) or (row[14] is None):
                                        if (row[16] in drink_list) or (row[16] is None):
                                            done = True
            if done == True:
                valid_ids.append(row)
                print row
        if pump == True:
            return valid_ids
        else:
            print row

    def show_assignments(self,cur):
        self.cur = cur
        cur.execute("SELECT * FROM PUMP_DRINK;")
        rows =  cur.fetchall()
        for row in rows:
            print "%s is assigned to pump number: %s" % (row[0],row[1])
        return rows

    def add_assignments(self,cur):
        self.cur = cur
        valid = False
        while valid == False:
            choice_nm = raw_input("Please input the id of the drink: ")
            qry = "SELECT drink_name from DRINK_LIST where drink_id = \"%s\";" % choice_nm
            cur.execute(qry)
            if cur.fetchone():
                valid = True
                print "%s exists!" % choice_nm
                print("Warning! This will override any existing drink assigned to this pump!")
                choice_pmp = int(raw_input("Please enter pump you wish to assign: 1-8: "))
                qry_in = "INSERT INTO PUMP_DRINK VALUES (\"%s\",%d);" % (choice_nm,choice_pmp)
                qry_drop = "DELETE FROM PUMP_DRINK WHERE pump_number = %d;" % choice_pmp
                cur.execute(qry_drop)
                cur.execute(qry_in)
            else:
                print("That ID is not found.")
