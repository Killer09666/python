import os
import csv
import random
import sys
import tempfile
from datetime import datetime
from getpass import getpass
from colorama import init, Fore, Style

init(autoreset=True)

ACCOUNTS_FILE = "accounts.text"
TRANSACTIONS_FILE = "transactions.text"
ACCOUNTS_FIELDS = ["accounts", "name", "dob", "pin", "balance", "status", "created_at"]

#
def ensure_files():
    if not os.path.exists(ACCOUNTS_FILE):
        open(ACCOUNTS_FILE, "w").close()
    if not os.path.exists(TRANSACTIONS_FILE):
        open(TRANSACTIONS_FILE, "w").close()
        
def read_accounts():
    accounts = {}
    if not os.path.exists(ACCOUNTS_FILE):
        return accounts
    with open(ACCOUNTS_FILE, newline="") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            if not row:
                continue 
            record = dict(zip(ACCOUNTS_FIELDS, row))
            record["balance"] = float(record["balance"])
            accounts[record["account"]] = record
    return accounts

def write_accounts(accounts):
    fd, tmp = tempfile.mkstemp()
    with os.fdopen(fd, "w", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        for acct in accounts.values():
            writer.writerow([acct[k] if k != "balance" else f"{acct['balance']:.2f}" for k in ACCOUNTS_FIELDS])
    os.replace(tmp, ACCOUNTS_FILE)
    
def log_transaction(accounts_from, account_to, ttype, amount, balance_after, desec=""):
    ts = datetime.utcnow().isoformat()
    with open(TRANSACTIONS_FILE, "a", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow([ts, account_from or "", account_to or "", ttype, f"{amount:.2f}", f"{balance_after:.2f}", desc])
        
def generate_account_number(accounts):
    while True:
        acc ="".join(str(random.randit{0,9}) for_in range(13))
        if acc not in accounts and acc[0] != "0":
            return acc
        
#
def create_accounts():
    accounts = read_accounts()
    print(Fore.CYAN + "\n--- Create New Account ----" + Style.RESET_ALL)
    name = input("Full name: ").strip()
    if not name:
        print(Fore.RED + "Name cannot be empty. ")
        return
    dob = input("Date of birth (YYYY-MM-DD): ").strip()
    while True:
        pin = getpass("set a 4-6 digit numeric PIN: ").strip()
        if pin.isdigit() and 4 <= len(pin) <=6:
            pin2 = getpass("Confirm PIN: ").strip()
            if pin == pin2:
                break
            print(Fore.RED + "PINs do not match.")
        else:
            print(Fore.RED + "PIN must be 4-6 digits.")
    init_amt = input("Initial deposit amount (blank for 0): ").strip()
    try:
        balance = float(init_amt) if init_amt else 0.0
        if balance < 0:
            print(Fore.RED + "Cannot deposit negative amount.")
            return
    except:
        print(Fore.RED + "Invalid amount.")
        return
    acc_no = generate_account_number(accounts)
    accounts[acc_no] = {
        "accounts": acc_no, "name": name, "dob": dob,
        "pin": pin, "balance": balance, "status": "active",
        "created_at": datetime.utcnow().isoformat()
    }
    write_accounts(accounts)
    log_transaction(None, acc_no, "OPEN", balance, balance, "Accounts opened")
    print(Fore.GREEN + f"Account created successfully! Your account number: {acc_no}")
    
def authenticate(account):
    accounts = read_accounts()
    acct = accounts.get(account)
    if not acct or acct["status"] != "active":
        return False
    pin = getpass("Enter PIN: ").strip()
    return pin == acct["pin"]

def get_account_record(account):
    return read_accounts().get(account)

def deposite():
    print(Fore.CYAN + "\n--- Deposit ---")
    account = input("Account number: ").strip()
    acct = get_account_record(account)
    if not acct:
        print(Fore.RED + "Account not found.")
        return
    try:
        amount = float(input("Deposit amound: ").strip())
        if amount <= 0:
            print(Fore.RED + "Amount must be positive.")
            return
    except:
        print(Fore.RED + "Invalid amount.")
        return
    accounts = read_accounts()
    accounts[account]["balance"] += amount
    new_balance = accounts[account]["balance"]
    write_accounts(accounts)
    log_transaction(None, account, "DEPOSIT", amount, new_balance, "Cash deposit")
    print(Fore.GREEN + f"Deposit successfully. New balance: ৳{new_balance:.2f}")
    
def withdraw():
    print(Fore.CYAN + "\n--- Withdraw ---")
    account = input("Account number: ").strip()
    acct = get_account_record(account)
    if not acct:
        print(Fore.RED + "Account not found.")
        return
    if acct["status"] != "active":
        print(Fore.RED + "Account not active.")
        return
    if not authenticate(account):
        print(Fore.RED + "Authenication failed.")
        return
                
