import csv
import random
from email.message import EmailMessage
import ssl
import smtplib
from colorama import Fore
from email_validator import validate_email, EmailNotValidError


def settings_menu(user, pin, mailID):
    while True:
        print('1. Set Transaction Limit (Default - 10000)\n2. Reset PIN\n3. Change E-mail ID\n4. Exit')
        ch = int(input(Fore.LIGHTMAGENTA_EX + 'Enter your choice: '))

        match ch:
            case 1:
                set_transaction_limit(user)

            case 2:
                pinni = input('Enter existing PIN (Enter 0 if forgotten): ')
                if pinni == '0':
                    forgotPW(mailID, user)
                else:
                    reset_pin(user, pinni)

            case 3:
                change_mailID(user)

            case 4:
                break


def set_transaction_limit(user):
    rows = []
    with open('accounts.csv') as f:
        reader = csv.reader(f)
        for x in reader:
            rows.append(x)
    new_tl = input('Set transaction limit to: ')

    for x in rows:
        if x[0] == str(user):
            x[5] = new_tl
            break

    with open('accounts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(Fore.GREEN + 'The Transaction Limit has been set successfully.')


def change_mailID(user):
    rows = []
    with open('accounts.csv') as f:
        reader = csv.reader(f)
        for x in reader:
            rows.append(x)
    new_mail = input('Enter new mail ID: ')
    emailinfo = validate_email(new_mail, check_deliverability=False)
    email = emailinfo.normalized

    for x in rows:
        if x[0] == str(user):
            x[2] = email
            break

    with open('accounts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(Fore.GREEN + 'The Mail ID has been changed successfully.')


def forgotPW(mail, user):
    try:
        genPIN = random.randint(1000, 9999)
        sender = 'bubble.bank444@gmail.com'
        sender_pw = 'ywkk wbfp daaq ooxc'
        receiver = mail

        subject = 'Your new ATM PIN. Do not share with anyone.'
        body = f"Dear user,\n\nYour new PIN is: {genPIN}\n\nPlease log-in to the Bank Portal with this PIN.\n\nBest regards,\nBubble Bank."

        em = EmailMessage()
        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, sender_pw)
            smtp.sendmail(sender, receiver, em.as_string())

        setForgottenPW(user, genPIN)
        print(
            Fore.GREEN + 'The new PIN has been sent to the registered E-mail account. Please log-in again with that PIN.')

    except Exception as e:
        print(Fore.RED + 'Failed to send mail due to some error. Please try again later.')


def setForgottenPW(user, pin):
    rows = []
    with open('accounts.csv') as f:
        reader = csv.reader(f)
        for x in reader:
            rows.append(x)

    for x in rows:
        if x[0] == user:
            x[3] = pin

    with open('accounts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def reset_pin(user, pin):
    rows = []
    flag = False
    with open('accounts.csv') as f:
        reader = csv.reader(f)
        for x in reader:
            rows.append(x)
    new_pin = input('Enter new pin: ')

    for x in rows:
        if x[0] == str(user) and x[3] == str(pin):
            flag = True
            x[3] = new_pin

    if flag:
        with open('accounts.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(Fore.GREEN + 'The PIN has been reset successfully.')
    else:
        print(
            Fore.RED + 'The original PIN entered is incorrect. You can avail the \'Forgot Password\' option by entering 0 where Old PIN is taken.')
