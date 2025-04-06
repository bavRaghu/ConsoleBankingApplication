from operations import operations_menu
from details import details_menu, transaction_history
from settings import settings_menu
from colorama import Fore
from tabulate import tabulate

def sign_in(user, pw, mailID):
    while True:
        print(Fore.GREEN + 'Thank you for logging in to our bank. Given are a few features we provide:')
        print('1. Account Operations (Withdraw / Deposit / Transfer)\n2. Check Account Details (Balance / Monthly Interest Rate)\n3. Check Transaction History\n4. Account Settings\n5. Log Out')
        ch = int(input(Fore.LIGHTMAGENTA_EX + 'Enter your choice: '))

        match ch:
            case 1:
                operations_menu(user)
            case 2:
                details_menu(user)
            case 3:
                print(tabulate(transaction_history(user)[0], headers=["Transaction", "Amount", "Date"], tablefmt="grid"))
                print(f'Total amount spent: {transaction_history(user)[1]}')
            case 4:
                settings_menu(user, pw, mailID)
            case 5:
                break
            case _:
                print('Invalid option. Please try again.')
