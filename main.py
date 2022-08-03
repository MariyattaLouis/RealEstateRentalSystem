import sqlite3
import pandas as pd

pd.set_option('display.max_columns', 100)
connection = sqlite3.connect("rentalproperty.db")

def userid_validation(connection, email, password, option):
    """ validation function for checking the user is existing"""
    cur = connection.cursor()
    if option == 1:
        cur.execute(
            'select * from CUSTOMER where EMAIL = "' + str(email) + '";')
    elif option == 2:
        cur.execute(
            'select * from CUSTOMER where EMAIL = "' + str(email) + '" AND PASSWORD = "' + str(
                password) + '";')
    elif option == 3:
        cur.execute(
            'select * from ADMIN where ADMIN_USERNAME = "' + str(name) + '" AND ADMIN_PASSWORD = "' + str(
                password) + '";')
    results = cur.fetchall()
    cur.close()
    return results


def tenant_response(connection):
    print()
    print(""" Choose the option:
                        (1) Booking
                        (2) Payment
                        """)
    TenantResponse = int(input("1, 2 : "))
    if TenantResponse == 1:
        dframe = pd.read_sql_query("SELECT * from BUILDING ", connection)
        print(dframe)
        print()
        print(""" Enter the BUILDING_ID if you would like to book an apartment
                                """)
        BuildingID = int(input("BUILDING_ID: "))
        dataf = pd.read_sql_query("SELECT * from APARTMENT_LISTING where BUILDING_ID ==" + str(BuildingID) + ";",
                                  connection)
        print()
        print("The apartments available in the BuildingID: " + str(BuildingID) + "are below")
        print(dataf)
        print(""" Enter the APARTMENT_ID you would like to book""")
        ApartmentID = int(input("APARTMENT_ID: "))
        StartDate = int(input("Starting Date(dd-mm-yyyy): "))
        print("Booking confirmed!")
    if TenantResponse == 2:
        print("payment")


Start = True
while Start == True:
    print("")
    try:
        print("""Choose an option:
                  (1) Tenant
                  (2) Staff
                  (3) Quit
                  """)
        option = int(input("1, 2, 3 : "))
    except ValueError:
        continue
    Cursor = connection.cursor()
    Cursor.execute("CREATE TABLE IF NOT EXISTS CUSTOMER(CUSTOMER_ID Integer NOT NULL PRIMARY KEY AUTOINCREMENT,"
                   "NAME varchar(255) NOT NULL,EMAIL Varchar(100) NOT NULL, PASSWORD varchar(255) NOT NULL,"
                   "PHONE int NOT NULL,PROPERTY_ID int DEFAULT 0,ACCESS_COUNT int DEFAULT 0);")

    Cursor.execute("CREATE TABLE IF NOT EXISTS BUILDING(BUILDING_ID Integer NOT NULL PRIMARY KEY AUTOINCREMENT, "
                   "BUILDING_NAME varchar(255) NOT NULL, NO_OF_FLOORS Integer NOT NULL, APARTMENT_SIZE varchar(255) "
                   "NOT NULL, STREET_ADDRESS varchar(255) NOT NULL, CITY varchar(255) NOT NULL, PROVINCE varchar(255) NOT NULL,"
                   " POSTAL_CODE varchar(255) NOT NULL, PRICE FLOAT NOT NULL);")

    Cursor.execute(
        "CREATE TABLE IF NOT EXISTS APARTMENT_LISTING(APARTMENT_ID Integer NOT NULL PRIMARY KEY AUTOINCREMENT, "
        "APARTMENT_NAME varchar(255) NOT NULL,BUILDING_ID Integer NOT NULL, FLOOR Integer NOT NULL, APARTMENT_SIZE "
        "varchar(255) NOT NULL, PRICE FLOAT NOT NULL );")

    if option == 1:
        try:
            category = "tenant"
            print()
            print("""Choose an option:
                              (1) Login
                              (2) Sign Up
                              """)
            print()
            tenant_option = int(input("1, 2 : "))
            if tenant_option == 1:
                print()
                email = input("Enter Email Address: ")
                password = input("Enter Password: ")
                validation = userid_validation(connection, email, password, tenant_option)
                if len(validation) == 1:
                    UpdateQueryCount = 'UPDATE CUSTOMER SET ACCESS_COUNT = ACCESS_COUNT + 1 WHERE EMAIL = "' + str(
                        email) + '" AND PASSWORD = "' + str(password) + '";'
                    Cursor.execute(UpdateQueryCount)
                    Cursor.execute("COMMIT;")
                    tenant_response(connection)
                else:
                    print()
                    print("Invalid credentials. Please try again!")

            elif tenant_option == 2:
                print()
                name = input("Your Name: ")
                email = input("Email Address: ")
                phone = input("Phone Number: ")
                password = input("Create a password: ")
                access_count = 0
                validation = userid_validation(connection, email, password, tenant_option)
                if len(validation) != 0:
                    print()
                    print(" You already registered an account with this mail id! ")
                else:
                    InsertQuery = 'INSERT INTO CUSTOMER (NAME,EMAIL,PASSWORD,PHONE,ACCESS_COUNT) VALUES ("' + str(
                        name) + '","' + str(email) + '","' + str(password) + '","' + str(phone) + '",' + str(
                        access_count) + ');'
                    Cursor.execute(InsertQuery)
                    Cursor.execute("COMMIT;")
                    tenant_response(connection)
        except ValueError:
            continue
    elif option == 2:
        try:
            print()
            name = input("username: ")
            password = input("Password: ")
            admin_option = 3
            validation = userid_validation(connection, email, password, admin_option)
            if len(validation) == 1:
                UpdateQueryCount = 'UPDATE ADMIN SET ADMIN_ACCESS_COUNT = ADMIN_ACCESS_COUNT + 1 WHERE ADMIN_USERNAME = "' + str(
                    name) + '" AND ADMIN_PASSWORD = "' + str(password) + '";'
                Cursor.execute(UpdateQueryCount)
                Cursor.execute("COMMIT;")
                # admin options
            else:
                print()
                print("Invalid credentials. Please try again!")
        except ValueError:
            continue
    else :
        try:
            print()
            print("Thank you for visiting!")
            print()
            Start = False
        except ValueError:
            continue
connection.close()
