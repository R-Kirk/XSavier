import os
from os.path import exists
import datetime
#Use the below Library to copy files from one destination to another, instead of just moving
import shutil

class File_Manager():
    def __init__(self, *args, **kwargs):
        self.communicate("Connected to File Manager")
        #Class properties
        self.path = ""
        if not os.path.isdir('Accounts'):
            self.new_user_config()
    
    def new_user_config(self):
        os.mkdir("Accounts")
        os.mkdir("db_backups")
        
        self.communicate("New User Setup")

    def create_account(self, account_name):
        #check if folder already exists
        os.mkdir(f"Accounts/{account_name}")
        os.mkdir(f"Accounts/{account_name}/processed")

    def check_account(self, account_name):
        if not os.path.isdir(f"Accounts/{account_name}"):
            self.communicate("Directory Checked: Directory Does Not Exists")
            return True
        else:
            self.communicate("Directory Checked: Directory Already Exists")
            return False
        
    def get_import_data(self, accounts):
        acnt_files = []
        for account in accounts:
            fcount = 0
            acnt_fname = []
            for fname in os.listdir(f"Accounts/{account[1]}"):
                if fname.lower().endswith(".csv"):
                    fcount +=1
                    acnt_fname.append(fname)
                    #print(fname)
    
            item = [account[1], fcount, acnt_fname]
            acnt_files.append(item)

        #print(acnt_files)
        return acnt_files

    def move_files(self, original_path, fname, account):
        now = datetime.datetime.now()
        #need to rename so duplicate name dont pop an error
        fname = fname.replace(".csv", '')
        new_path = (f"Accounts/{account}/processed/{fname}_{now.year}_{now.month}_{now.day}_{now.minute}{now.second}.csv")
        self.communicate(f"original path: {original_path}, new path: {new_path}")
        os.rename(original_path, new_path)

    def backup_database(self):
        try:
            now = datetime.datetime.now()
            source = "database.db"
            fname = "database"
            destination = (f"db_backups/{fname}_{now.year}_{now.month}_{now.day}_{now.hour}{now.minute}{now.second}.db")
            shutil.copy(source, destination)
            return True
        except:
            return False
        
    def move_files_for_import(self, original_path, new_path):
        try:
            shutil.copy(original_path, new_path)
            return True
        except:
            return False


    def communicate(self, text):
        print(f"[FILE MANAGER]...{text}")
