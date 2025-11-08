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
    
