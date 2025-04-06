import csv
import random
from signIn import sign_in
from email_validator import validate_email, EmailNotValidError
from settings import forgotPW
from colorama import Fore, init

init(autoreset=True)

users = set()


class InvalidPassword(Exception):
    pass


class MinimumInitialDeposit(Exception):
    pass


class InvalidUser(Exception):
    pass


def createAccount(accNo, name, emailID, pwd, balance):
    with open('accounts.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([accNo, name, emailID, pwd, balance, 10000])


def genAccNo():
    while True:
        accNo = random.randint(10000, 99999)
        if accNo not in users:
            users.add(accNo)
            return accNo


def validPw(pw):
    return pw.isdigit() and len(pw) == 4


def validateUser(accno, pw):
    with open('accounts.csv', 'r') as f1:
        reader = csv.reader(f1)
        next(reader)
        for row in reader:
            if str(accno) == row[0] and str(pw) == row[3]:
                return row
    return None


def get_email(accno):
    with open('accounts.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if str(accno) == row[0]:  # Match account number
                return row[2]  # Return email ID
    return None


if __name__ == "__main__":
    try:
        with open('accounts.csv', 'x') as f:
            writer = csv.writer(f)
            writer.writerow(['Account No.', 'Name', 'EmailID', 'Password', 'Balance'])
    except FileExistsError:
        pass

    try:
        with open('transactions.csv', 'x') as f:
            writer = csv.writer(f)
            writer.writerow(['Account No.', 'Transaction Type', 'Amount', 'Date'])
    except FileExistsError:
        pass

    while True:
        print('1. Create an Account\n2. Sign in to your account\n3. Exit')
        ch = int(input(Fore.LIGHTMAGENTA_EX + 'Enter your choice: '))

        match ch:
            case 1:
                name = input('Enter your name: ')
                try:
                    pwd = input('Enter your password (4 - digit numeric value): ')
                    if not validPw(pwd):
                        raise InvalidPassword
                    emailID = input('Enter a valid Email ID: ')
                    emailinfo = validate_email(emailID, check_deliverability=False)
                    email = emailinfo.normalized
                    accNo = genAccNo()
                    print(f'Your Account Number is' + Fore.GREEN + ' ' + str(accNo))
                    bal = int(input('Enter your initial deposit: '))
                    if bal < 5000:
                        raise MinimumInitialDeposit
                except InvalidPassword:
                    print(Fore.RED + 'Invalid password! Your password must be a 4-digit numeric PIN. Please try again.')
                    continue
                except MinimumInitialDeposit:
                    print(Fore.RED +
                          'To open a Savings Bank Account, a minimum initial deposit of Rs. 5,000 is required. Please try again.')
                    continue
                except EmailNotValidError as e:
                    print(Fore.RED + str(e))
                    continue
                createAccount(accNo, name, email, pwd, bal)
                print(Fore.GREEN + 'Thank you! Your account has been created successfully!')

            case 2:
                try:
                    accno = input('Enter your account number: ')
                    pin = input('Enter your password: ')
                    user_data = validateUser(accno, pin)

                    if not user_data:
                        print(
                            Fore.RED + 'The account number or PIN you entered is incorrect. Please check and try again.')
                        forgot = input(Fore.GREEN + 'Have you forgotten PIN? (Y / N): ').lower()

                        if forgot == 'y':
                            emailID = get_email(accno)  # Retrieve email separately
                            if emailID:
                                forgotPW(emailID, accno)
                            else:
                                print(Fore.RED + "Email ID not found. Please contact support.")
                        continue
                        # continue

                    sign_in(accno, pin, user_data[2])


                except Exception as e:
                    print(Fore.RED + f"An unexpected error occurred: {e}")

            case 3:
                print(Fore.YELLOW + 'Exitting application, have a nice day 🤭')
                break

            case _:
                print(Fore.YELLOW + 'Invalid option. Please try again.')
