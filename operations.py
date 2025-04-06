import csv
import datetime
from colorama import Fore


class WithDrawError(Exception):
    pass


class TransactionLimitExceeded(Exception):
    pass


def operations_menu(user):
    while True:
        print('1. Withdraw\n2. Deposit\n3. Transfer\n4. Exit')
        ch = int(input(Fore.LIGHTMAGENTA_EX + 'Enter your choice: '))

        match ch:
            case 1:
                cash = int(input('Enter the amount needed to be withdrawn: '))
                date = datetime.datetime.now()
                print(f'Date and Time of the transaction: {date}')
                withdraw(user, cash)
                save_transaction(user, 'Withdraw', '-' + str(cash), date.date(), 'Withdrawer')

            case 2:
                cash = int(input('Enter the amount needed to be deposited: '))
                date = datetime.datetime.now()
                print(f'Date and Time of the transaction: {date}')
                deposit(user, cash)
                save_transaction(user, 'Deposit', '+' + str(cash), date.date(), 'Depositer')

            case 3:
                payee = input('Enter accno of the user to transfer the funds to: ')
                cash = int(input('Enter the amount needed to be transferred: '))
                date = datetime.datetime.now()
                print(f'Date and Time of the transaction: {date}')
                success = withdraw(user, cash)
                if success == 0:
                    deposit(payee, cash)
                    save_transaction(user, 'Transfer (Withdraw)', cash, date.date(), 'Payer')
                    save_transaction(payee, 'Transfer (Deposit)', cash, date.date(), 'Payee')
            case 4:
                break


def save_transaction(accno, tt, amt, date, role):
    with open('transactions.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if tt == 'Withdraw' or tt == 'Transfer (Withdraw)':
            writer.writerow([accno, tt, str(int(-1 * amt)), date, role])
        else:
            writer.writerow([accno, tt, amt, date, role])


def withdraw(accno, amt):
    rows = []
    balance = None
    accno = str(accno)
    with open('accounts.csv', 'r') as f:
        reader = csv.reader(f)
        for x in reader:
            rows.append(x)
    try:
        for x in rows:
            if x[0] == accno:
                if x[4] == '' or x[5] == '':
                    raise ValueError(Fore.RED + 'Bank Error')
                balance = int(x[4])
                if amt > int(x[5]):
                    raise TransactionLimitExceeded
                break

        new_bal = balance - amt
        if new_bal < 0:
            raise WithDrawError
        else:
            for x in rows:
                if x[0] == accno:
                    x[4] = str(new_bal)
        with open('accounts.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print(Fore.GREEN + f'Withdrawal Successful. New balance = {new_bal}')
        return 0
    except WithDrawError:
        print(Fore.RED + 'Amount to be withdrawn must be less than or equal to current balance.')
        return -1
    except TransactionLimitExceeded:
        print(Fore.RED + 'The amount entered is greater than the set transaction limit on your account.')


def deposit(accno, amt):
    rows = []
    balance = None
    accno = str(accno)
    with open('accounts.csv', 'r') as f:
        reader = csv.reader(f)
        for x in reader:
            rows.append(x)

    for x in rows:
        if x[0] == accno:
            balance = int(x[4])
            break

    new_bal = balance + amt
    for x in rows:
        if x[0] == accno:
            x[4] = str(new_bal)

    with open('accounts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(Fore.GREEN + f'Deposit Successful. New balance = {new_bal}')
