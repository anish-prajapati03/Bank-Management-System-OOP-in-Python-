import json
import random
import string
from pathlib import Path

class Bank:
    database= 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
              data = json.loads(fs.read())
        else:
            print("No such file exist")
    except Exception as err:
        print(f"An exception occured as {err}")

    @classmethod
    def __update(cls):
        with open(Bank.database,'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits,k=3)
        spchar = random.choices("!@#$%^&*", k =1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)



    def createaccount(self):
         info={
             "name": input("Tell your name: "),
              "age": int(input("Tell your age: ")),
              "email": input("Tell your email: "),
              "pin": int(input("Tell your pin: ")),
              "account No.": Bank.__accountgenerate(),
              "balance": 0
         }
         if info['age'] < 18 or len(str(info['pin'])) != 4:
             print("Sorry You can't create ur account")
         else:
             print("Account has been create successfully")
             for i in info:
                 print(f"{i} : {info[i]}")
             print("Plz note ur account No.")

             Bank.data.append(info)
             Bank.__update()

    def depositmoney(self):
        accnumber = input("Enter your account number : ")
        pin = int(input("Plz Tell ur pin as well"))

        userdata = [i for i in Bank.data if i['account No.'] == accnumber and i['pin'] == pin]
        
        if userdata == False:
            print("Sorry no data found")
        else:
            amount = int(input("How much you want to deposit"))
            if amount > 10000 or amount < 0:
                print("You can't deposit more than 10000 and negative amount")
            else:
                userdata[0]['balance'] += amount
                print(f"You have sucessfully deposited {amount}")
                print(f"Your total balance is {userdata[0]['balance']}")

                Bank.__update()
    def withdrawmoney(self):
        accnumber = input("Enter your account number : ")
        pin = int(input("Plz Tell ur pin as well"))

        userdata = [i for i in Bank.data if i['account No.'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("Sorry no data found")
        else:
            amount = int(input("How much you want to withdraw"))
            if amount > userdata[0]['balance']:
                print("Insufficient Balance")
            else:
                userdata[0]['balance'] -= amount
                print(f"You have sucessfully withdrawn {amount}")
                print(f"Your total balance is {userdata[0]['balance']}")

                Bank.__update()
                
           

user=Bank()
print("Press 1 forcreating an account")
print("Press 2 Depositing the money in the bank")
print("Press 3 for withdrawing the money")
print("Press 4 for detail")
print("Press 5 for updating the detail")
print("Press 6 for deleting your account")

check = int(input("Tell you Response : "))

if check == 1:
    user.createaccount()

if check == 2:
    user.depositmoney()

if check == 3:
    user.withdrawmoney()

