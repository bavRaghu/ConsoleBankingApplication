import csv
from datetime import datetime
from colorama import Fore

def details_menu(user):
    while True:
        ch = int(input('1. Check Balance\n2. Check Interest Rate\n3. Exit\nEnter your choice: '))

        match ch:
            case 1:
                print(Fore.GREEN + f'Current Balance of user {user}: Rs.{check_balance(user)}')
            case 2:
                month = int(str(datetime.now().date())[5:7])
                print(Fore.GREEN + f'Daily Interest on {user}\'s account: {check_interest(user, month) / 10:.2f}%')
            case 3:
                break


def check_balance(user):
    rows = []
    bal = None
    with open('accounts.csv', 'r') as f:
        reader = csv.reader(f)
        for x in reader:
            rows.append(x)

    for x in rows:
        if x[0] == str(user):
            bal = x[4]

    return bal


def check_interest(user, month):
    months = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    bal = check_balance(user)
    interest = int(bal) * (3.50 / 100) * (months[month] / 365)
    return interest

def transaction_history(user):
    rows = []
    user_rows = []
    ttl_transaction = 0
    with open('transactions.csv', 'r') as f:
        reader = csv.reader(f)
        for x in reader:
            rows.append(x)
    for x in rows:
        if x[0] == str(user):
            user_rows.append([x[1], x[2], x[3]])
            ttl_transaction += int(x[2])
    return user_rows, ttl_transaction

