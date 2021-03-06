from datetime import datetime as dt, date
import re


def addDirector(con, cur):
    row = {}
    print("Enter the new director's details: ")

    row["aadharCard"] = input("12 digit AadharCard: ")
    if len(row["aadharCard"]) == 12 and row["aadharCard"].isnumeric():
        row["aadharCard"] = int(row["aadharCard"])
    else:
        print("\nError: Please enter valid 12 digit Aadhar Card Number\n")
        return

    row["name"] = input("Name: ")
    if len(row["name"]) <= 0:
        print("\nError: Please enter a name\n")
        return

    row["accountNo"] = input("Account Number: ")
    if len(
        row["accountNo"]) >= 8 and len(
        row["accountNo"]) <= 12 and row["accountNo"].isnumeric() and int(
            row["accountNo"]) > 0:
        row["accountNo"] = int(row["accountNo"])
    else:
        print("\nError: Please enter valid Account Number\n")
        return

    row["gender"] = input("Male / Female / Other: ")
    if row["gender"] != "Male" and row["gender"] != "Female" and row["gender"] != "Other":
        print("\nError: Please enter valid gender\n")
        return

    try:
        row["DOB"] = dt.strptime(input("Date of Birth in YYYY-MM-DD: "), "%Y-%m-%d")
    except Exception as e:
        print(e)
        print("\nError: Please enter valid Date of Birth\n")
        return

    age = date.today().year - row['DOB'].year - \
        ((date.today().month, date.today().day) <
         (row['DOB'].month, row['DOB'].day))

    row["DOB"] = str(row["DOB"])

    if age < 18:
        print("\nError: Very young director. Minimum age is 18\n")
        return

    row["salary"] = input("Salary: ")
    if row["salary"].isnumeric() and int(row["salary"]) >= 10000:
        row["salary"] = int(row["salary"])
    else:
        print("\nError: Please enter valid Salary above 10000\n")
        return

    try:
        row["joinDate"] = input("Date of Joining in YYYY-MM-DD: (Enter for today)")
        if row["joinDate"] == "":
            row["joinDate"] = str(date.today())
        else:
            row["joinDate"] = str(dt.strptime(row["joinDate"], "%Y-%m-%d"))
    except Exception as e:
        print(e)
        print("\nError: Please enter valid Date of Joining\n")
        return

    row["supervisorAadharCard"] = input("12 digit Supervisor AadharCard: (Enter to skip)")
    if len(row["supervisorAadharCard"]) == 12 and row["supervisorAadharCard"].isnumeric(
    ) and row["supervisorAadharCard"] != row["aadharCard"]:
        row["supervisorAadharCard"] = int(row["supervisorAadharCard"])
    elif row["supervisorAadharCard"] == "":
        row["supervisorAadharCard"] = "NULL"
    else:
        print("\nError: Please enter valid 12 digit Supervisor Aadhar Card Number\n")
        return

    row_phone = []
    try:
        num_phone = int(input("Number of director's phone number (>0): "))
        if num_phone == 0:
            print("Atleast one phone number is required.")
            num_phone = 1
    except Exception as e:
        print(e)
        print("\nError: Please enter a valid number\n")
        return
    for i in range(num_phone):
        phone = input("Phone Number: ")
        if phone.isnumeric() and int(phone) > 0 and len(phone) == 10:
            phone = int(phone)
            row_phone.append(phone)
        else:
            print("\nError: Please enter valid 10 digit Phone Number\n")
            return

    try:
        query = "INSERT INTO person(aadharCard, name, accountNo, gender, DOB) VALUES(%d, '%s', %d, '%s', '%s');" % (
            row["aadharCard"], row["name"], row["accountNo"], row["gender"], row["DOB"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    try:
        query = f"INSERT INTO director(aadharCard, joinDate, salary, supervisorAadharCard) VALUES \
            ({row['aadharCard']}, '{row['joinDate']}', {row['salary']}, {row['supervisorAadharCard']});"
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    for i in range(num_phone):
        try:
            query = "INSERT INTO phone(aadharCard, phoneNo) VALUES(%d, %d);" % (
                row["aadharCard"], row_phone[i])
            cur.execute(query)
        except Exception as e:
            con.rollback()
            print(e)
            print("\nError: PLEASE TRY AGAIN!\n")
            return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return


def addGuardian(con, cur):

    name = input("Name of Guardian: ")
    phone = input("Phone Number of Guardian: ")
    aadharCard = input("Aadhar Card of Guardian: ")
    if phone.isnumeric() and int(phone) > 0 and len(phone) == 10 and len(
            aadharCard) == 12 and aadharCard.isnumeric() and int(aadharCard) > 0 and len(name) > 0:
        phone = int(phone)
        aadharCard = int(aadharCard)
    else:
        print("\nError: Please enter valid details\n")
        return

    try:
        query = f'INSERT INTO guardianData(aadharCard, name, phone) VALUES( "{aadharCard}", "{name}", {phone});'
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return


def preAddActor(con, cur):
    res = input("Do you intend to add a junior Actor?(y,n) >")
    if res == 'n' or res == 'N':
        addActor(con, cur)
        return

    inp = input("Are the guardians for the actor already added?(y,n) >")
    if inp == 'n' or inp == 'N':
        print("Please add the guardians before.")
    else:
        addActor(con, cur)


def addActor(con, cur):
    row = {}
    print("--Enter the new actor's details--")

    row["aadharCard"] = input("12 digit AadharCard: ")
    if len(row["aadharCard"]) == 12 and row["aadharCard"].isnumeric():
        row["aadharCard"] = int(row["aadharCard"])
    else:
        print("\nError: Please enter valid 12 digit Aadhar Card Number\n")
        return

    row["name"] = input("Name: ")
    if len(row["name"]) <= 0:
        print("\nError: Please enter a name\n")
        return

    row["accountNo"] = input("Account Number: ")
    if len(
        row["accountNo"]) >= 8 and len(
        row["accountNo"]) <= 12 and row["accountNo"].isnumeric() and int(
            row["accountNo"]) > 0:
        row["accountNo"] = int(row["accountNo"])
    else:
        print("\nError: Please enter valid Account Number\n")
        return

    row["gender"] = input("Male / Female / Other: ")
    if row["gender"].capitalize() != "Male" and row["gender"].capitalize(
    ) != "Female" and row["gender"].capitalize() != "Other":
        print("\nError: Please enter valid gender\n")
        return

    try:
        row["DOB"] = dt.strptime(input("Date of Birth in YYYY-MM-DD: "), "%Y-%m-%d")
    except Exception as e:
        print(e)
        print("\nError: Please enter valid Date of Birth\n")
        return

    age = date.today().year - row['DOB'].year - \
        ((date.today().month, date.today().day) <
         (row['DOB'].month, row['DOB'].day))

    row["DOB"] = str(row["DOB"])

    row["experience"] = input("Experience in Years: ")
    if row["experience"].isnumeric() and int(row["experience"]) >= 0 and int(row["experience"]) < age:
        row["experience"] = int(row["experience"])
    else:
        print("\nError: Please enter valid Experience\n")
        return

    row["height"] = input("Height in cms: ")
    if row["height"].isnumeric() and int(row["height"]) > 0:
        row["height"] = int(row["height"])
    else:
        print("\nError: Please enter valid Height\n")
        return

    row["weight"] = input("weight in kgs: ")
    if row["weight"].isnumeric() and int(row["weight"]) > 0:
        row["weight"] = int(row["weight"])
    else:
        print("\nError: Please enter valid Weight\n")
        return

    row_phone = []
    try:
        num_phone = int(input("Number of actor's phone number: "))
        if num_phone == 0:
            print("Atleast one phone number is required.")
            num_phone = 1
    except Exception as e:
        print(e)
        print("\nError: Please enter a valid number\n")
        return
    for i in range(num_phone):
        phone = input("Phone Number: ")
        if phone.isnumeric() and int(phone) > 0 and len(phone) == 10:
            phone = int(phone)
            row_phone.append(phone)
        else:
            print("\nError: Please enter valid 10 digit Phone Number\n")
            return

    try:
        query = "INSERT INTO person(aadharCard, name, accountNo, gender, DOB) VALUES(%d, '%s', %d, '%s', '%s');" % (
            row["aadharCard"], row["name"], row["accountNo"], row["gender"], str(row["DOB"]))
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    try:
        query = "INSERT INTO actor(aadharCard, experience, height, weight) VALUES(%d, %d, %d, %d);" % (
            row["aadharCard"], row["experience"], row["height"], row["weight"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    for i in range(num_phone):
        try:
            query = "INSERT INTO phone(aadharCard, phoneNo) VALUES(%d, %d);" % (
                row["aadharCard"], row_phone[i])
            cur.execute(query)
        except Exception as e:
            con.rollback()
            print(e)
            print("\nError: PLEASE TRY AGAIN!\n")
            return

    if(age < 18):
        print("As the actor's age is less than 18, Guardian needs to be added before!")

        # get number of guardians
        try:
            num_guard = int(input("Number of actor's guardians: "))
        except Exception as e:
            print(e)
            print("\nError: Please enter a valid number\n")
            return

        # add aadhar card to juniorActor
        try:
            query = "INSERT INTO juniorActor(aadharCard) VALUES(%d);" % (
                row["aadharCard"])
            cur.execute(query)
        except Exception as e:
            con.rollback()
            print(e)
            print("\nError: PLEASE TRY AGAIN!\n")
            return

        _guardians = [0 for _ in range(num_guard)]

        for i in range(num_guard):
            _guardians[i] = input("12 digit AadharCard: ")
            if len(_guardians[i]) == 12 and _guardians[i].isnumeric():
                _guardians[i] = int(_guardians[i])
            else:
                print("\nError: Please enter valid 12 digit Aadhar Card Number\n")
                return
        aadharCard = row["aadharCard"]
        try:
            query = f"INSERT INTO guardian(jActorAadharCard, aadharCard) VALUES {','.join([f'({aadharCard},{_gac})' for _gac in _guardians])};"
            cur.execute(query)
        except Exception as e:
            con.rollback()
            print(e)
            print("\nError: PLEASE TRY AGAIN!\n")
            return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return
    return


def addBrand(con, cur):
    row = {}

    row["brandName"] = input("Enter Brand Name: ")
    if len(row["brandName"]) <= 0:
        print("\nError: Please enter a valid brand name\n")
        return

    row["email"] = input("POC Email: ")
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, row["email"]):
        print("\nError: Please enter a valid Email Id\n")
        return
    row["phone"] = input("Phone: ")
    if (not row["phone"].isnumeric()) or len(row["phone"]) != 10:
        print("\nError: Please enter a valid Phone Number\n")
        return
    row["phone"] = int(row["phone"])
    try:
        query = "INSERT INTO brand(brandName, pocEmail, pocPhone) VALUES('%s', '%s', %d);" % (
            row["brandName"], row["email"], row["phone"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return


def addChannel(con, cur):
    row = {}

    row["channelName"] = input("Enter Channel Name: ")
    if len(row["channelName"]) <= 0:
        print('Please enter a channel name')
        return
    row["baseprice"] = input("Baseprice: ")
    if row["baseprice"].isnumeric() and int(row["baseprice"]) > 0:
        row["baseprice"] = int(row["baseprice"])
    else:
        print("\nError: Please enter a valid Baseprice\n")
        return
    try:
        query = "INSERT INTO channel(channelName, baseprice) VALUES('%s', %d);" % (
            row["channelName"], row["baseprice"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return
    return


def addPrefers(con, cur):
    row = {}

    row["brandName"] = input("Enter Brand Name: ")
    if len(row['brandName']) <= 0:
        print("Please enter a brand name")
        return
    row["actorAadharCard"] = input("actorAadharCard: ")
    if len(row["actorAadharCard"]) == 12 and row["actorAadharCard"].isnumeric():
        row["actorAadharCard"] = int(row["actorAadharCard"])
    else:
        print("\nError: Please enter valid 12 digit Actor Aadhar Card Number\n")
        return

    try:
        query = "INSERT INTO prefers(actorAadharCard, brandName) VALUES(%d, '%s');" % (
            row["actorAadharCard"], row["brandName"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return
    return


def addProduct(con, cur):
    row = {}

    row["brandName"] = input("Enter Brand Name: ")
    if len(row['brandName']) <= 0:
        print("Please add brand name")
        return
    row["name"] = input("Enter Product Name: ")
    if len(row['name']) <= 0:
        print("Please add product name")
        return
    row["description"] = input("Enter Product description: (Enter to skip)")

    if len(row['description']) <= 0:
        row['description'] = 'NULL'
    else:
        row['description'] = '"' + row['description'] + '"'

    row["price"] = input("Enter price: ")
    if row["price"].isnumeric() and int(row["price"]) > 0:
        row["price"] = int(row["price"])
    else:
        print("\nError: Please enter valid price\n")
        return

    try:
        query = "INSERT INTO product(name, brandName, description, price) VALUES('%s', '%s', %s, %d);" % (
            row["name"], row["brandName"], row["description"], row["price"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return
    return


def addProduction(con, cur):
    row = {}

    row["brandName"] = input("Enter Brand Name: ")
    if len(row['brandName']) <= 0:
        print("Please add brand name")
        return
    row["productName"] = input("Enter Product Name: ")
    if len(row['productName']) <= 0:
        print("Please add product name")
        return
    row["actorAadharCard"] = input(
        "Enter Aadhar Card of actor working in that Ad: ")
    if len(row["actorAadharCard"]) == 12 and row["actorAadharCard"].isnumeric():
        row["actorAadharCard"] = int(row["actorAadharCard"])
    else:
        print("\nError: Please enter valid 12 digit Actor Aadhar Card Number\n")
        return
    row["directorAadharCard"] = input(
        "Enter Aadhar Card of director working in that Ad: ")
    if len(row["directorAadharCard"]) == 12 and row["directorAadharCard"].isnumeric():
        row["directorAadharCard"] = int(row["directorAadharCard"])
    else:
        print("\nError: Please enter valid 12 digit Actor Director Card Number\n")
        return

    try:
        row["signingDate"] = input("Enter Signing Date of Ad in YYYY-MM-DD: (Enter for today)")
        if row["signingDate"] == "":
            row["signingDate"] = str(date.today())
        else:
            row["signingDate"] = str(dt.strptime(row["signingDate"], "%Y-%m-%d"))
    except Exception as e:
        print(e)
        print("\nError: Please enter valid Signing Date\n")
        return

    row["productionCost"] = input("Enter Production Cost of Ad: ")
    if row["productionCost"].isnumeric() and int(row["productionCost"]) > 0:
        row["productionCost"] = int(row["productionCost"])
    else:
        print("\nError: Please enter valid Production Cost\n")
        return

    row["duration"] = input("Enter Duration of Ad in sec: ")
    if row["duration"].isnumeric() and int(row["duration"]) > 0:
        row["duration"] = int(row["duration"])
    else:
        print("\nError: Please enter valid duration\n")
        return

    row_genre = []
    genre_list = ['Comedy', 'Thriller', 'Romance',
                  'Suspense', 'Sci-fi', 'Action', 'Horror', 'Fantasy']
    try:
        num_genre = int(input("Number of genre in Ad: "))
    except Exception as e:
        print(e)
        print("\nError: Please enter a valid number\n")
        return
    for i in range(num_genre):
        name = input(
            "Genre from Comedy|Thriller|Romance|Suspense|Sci-fi|Action|Horror|Fantasy: ")
        if name in genre_list:
            row_genre.append(name)
        else:
            print("\nError: Please enter valid genre\n")
            return

    try:
        query = "INSERT INTO production(actorAadharCard, directorAadharCard, productName, brandName, signingDate, productionCost) VALUES(%d, %d, '%s', '%s', '%s', %d);" % (
            row["actorAadharCard"], row["directorAadharCard"], row["productName"], row["brandName"], row["signingDate"], row["productionCost"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    adId = cur.lastrowid

    try:
        query = "INSERT INTO ad(serialNo, duration) VALUES(%d, %d);" % (
            adId, row["duration"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    for i in range(num_genre):
        try:
            query = "INSERT INTO adGenre(name, adSerialNo) VALUES('%s', %d);" % (
                row_genre[i], adId)
            cur.execute(query)
        except Exception as e:
            con.rollback()
            print(e)
            print("\nError: PLEASE TRY AGAIN!\n")
            return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return


def addShow(con, cur):
    row = {}

    row["name"] = input("Enter Show Name: ")
    if len(row['name']) <= 0:
        print("Please add show name")
        return
    row["productName"] = input("Enter Product Name: ")
    if len(row['productName']) <= 0:
        print("Please add product name")
        return
    row["channelName"] = input("Enter Channel Name on which show is aired: ")
    if len(row['channelName']) <= 0:
        print("Please add channel name")
        return
    row["startTime"] = input("Enter Start Time of show in HH:MM:SS: ")
    try:
        row["startTime"] = str(dt.strptime(row["startTime"], "%H:%M:%S"))
    except Exception as e:
        print("Please enter a valid time")
        return
    try:
        row["date"] = str(dt.strptime(input("Enter Air Date of Show in YYYY-MM-DD: "), "%Y-%m-%d"))
    except Exception as e:
        print("\nError: Please enter valid Airing Date\n")
        return

    row["duration"] = input("Enter Duration of Show in min: ")
    if row["duration"].isnumeric() and int(row["duration"]) > 0:
        row["duration"] = int(row["duration"])
    else:
        print("\nError: Please enter valid duration\n")
        return

    row["surcharge"] = input("Enter Surcharge of Show: ")
    if row["surcharge"].isnumeric() and int(row["surcharge"]) > 0:
        row["surcharge"] = int(row["surcharge"])
    else:
        print("\nError: Please enter valid surcharge\n")
        return

    row_genre = []
    genre_list = ['Comedy', 'Thriller', 'Romance',
                  'Suspense', 'Sci-fi', 'Action', 'Horror', 'Fantasy']
    try:
        num_genre = int(input("Number of genre in Show: "))
    except Exception as e:
        print(e)
        print("\nError: Please enter a valid number\n")
        return
    for i in range(num_genre):
        name = input(
            "Genre from Comedy|Thriller|Romance|Suspense|Sci-fi|Action|Horror|Fantasy: ")
        if name in genre_list:
            row_genre.append(name)
        else:
            print("\nError: Please enter valid genre\n")
            return

    # show overlapping condition checked by mysql (`before_show_insert` trigger)

    try:
        query = "INSERT INTO `show`(date, startTime, channelName, duration, surcharge, name) VALUES('%s', '%s', '%s', %d, %d, '%s');" % (
            row["date"], row["startTime"], row["channelName"], row["duration"], row["surcharge"], row["name"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    for i in range(num_genre):
        try:
            query = "INSERT INTO showGenre(name, showDate, showStartTime, channelName) VALUES('%s', '%s', '%s', '%s');" % (
                row_genre[i], row["date"], row["startTime"], row["channelName"])
            cur.execute(query)
        except Exception as e:
            con.rollback()
            print(e)
            print("\nError: PLEASE TRY AGAIN!\n")
            return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return


def addAdinShow(con, cur):
    row = {}

    row["adSerialNo"] = input("Please enter Serial number of Ad: ")
    if row["adSerialNo"].isnumeric() and int(row["adSerialNo"]) > 0:
        row["adSerialNo"] = int(row["adSerialNo"])
    else:
        print("\nError: Please enter a valid serial Number\n")
        return

    row["channelName"] = input("Enter Channel Name on which show is aired: ")
    if len(row['channelName']) <= 0:
        print("Please add channel name")
        return
    row["showStartTime"] = input(
        "Enter Start Time of show (HH:MM:SS) in which Ad is to be displayed: ")
    try:
        row["showStartTime"] = str(dt.strptime(row["showStartTime"], "%H:%M:%S"))
    except Exception as e:
        print("Please enter a valid time")
        return

    try:
        row["showDate"] = str(dt.strptime(input("Enter Air Date of Show in YYYY-MM-DD: "), "%Y-%m-%d"))
    except Exception as e:
        print("\nError: Please enter valid Airing Date\n")
        return

    row["timesShown"] = input(
        "Please enter number of times Ad is shown during Show (Enter for 1): ")
    if row["timesShown"].isnumeric() and int(row["timesShown"]) > 0:
        row["timesShown"] = int(row["timesShown"])
    elif row["timesShown"] == "":
        row["timesShown"] = 1
    else:
        print("\nError: Please enter a valid number\n")
        return

    # total Ad duration < show duration constraint checked in mysql (`before_displaying` trigger)

    try:
        query = "INSERT INTO displayedBetween(showDate, showStartTime, channelName, adSerialNo, timesShown) VALUES('%s', '%s', '%s', %d, %d);" % (
            row["showDate"], row["showStartTime"], row["channelName"], row["adSerialNo"], row["timesShown"])
        cur.execute(query)
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return

    try:
        con.commit()
        print("\nADDITION SUCCESSFULL")
    except Exception as e:
        con.rollback()
        print(e)
        print("\nError: PLEASE TRY AGAIN!\n")
        return
