import os
import pandas as pd


class Account:
    def __init__(self):
        self.account = pd.read_csv('./account.csv')
        self.account['card_number'] = self.account['card_number'].astype(str)
    
    def deposit(self, user_account):
        self._show_account_balance(user_account)
        money = input("How much will you deposit? : ")
        money = check_digits(money)
        
        idx = self._get_pd_idx(user_account)
        self.account.at[(idx.to_list()[0]),'balance'] = int(user_account.balance) + int(money)
        self._save_csv(self.account)
        print(f"Your balance is {int(user_account.balance) + int(money)}")

    def _get_pd_idx(self, pd ):
        return self.account.index[(self.account['card_number'] == pd.card_number) & \
                (self.account['pin_number'] == pd.pin_number) & \
                (self.account['account'] == pd.account)]

    def _save_csv(self, pd):
        pd.to_csv('./account.csv',
        sep=',',
        na_rep='NaN', 
        index = False)



    def withdraw(self, user_account):
        self._show_account_balance(user_account)
        money = input("How much will you withdraw? : ")
        money = check_digits(money)
        
        idx = self._get_pd_idx(user_account)
        self.account.at[(idx.to_list()[0]),'balance'] = int(user_account.balance) - int(money)
        self._save_csv(self.account)
        print(f"Your balance is {int(user_account.balance) - int(money)}")
    
    def _show_account_balance(self, account, cls=True):
        if cls:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print(f" account: {account['account']} \n balance {account['balance']}")
        
    def check_card_pin_number(self, card_number: str, pin_number: int):
        card_check = self.account['card_number'] == card_number
        pin_num_check = self.account['pin_number'] == pin_number
        account_list = self.account[card_check & pin_num_check]
        
        return account_list
    
        
        
def cls_input(str):
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    return input(f"{str}")
    
def check_digits(str):
    while True:
        try:
            str = int(str)
            break
        except:
            str = input("Please enter a number : ")
    return str

def check_choice_range(idx, range_list):
    while True:
        if not idx in range_list:
            idx = input(f"Please select within the range {range_list}: ")
            idx = check_digits(idx)
        else:
            break
    return idx
    
    

def run():
    account = Account()
    cls_input("hello this is bear bank \n If you inserted the card, press any key.")
    card_num = cls_input("Please enter your card number: ")
    pin_num = cls_input("Please enter your pin number(4 digits.): ")
    pin_num = check_digits(pin_num)
    account_list = account.check_card_pin_number(card_num, pin_num)
    
    if account_list.empty:
        cls_input("The card information and pin number do not match. Close the program.")
        exit()

    idx_account = cls_input(f"{account_list.drop(['card_number', 'pin_number'], axis=1)} \n"\
                            f"select account {list(account_list.index.values)}: ")
    idx_account = check_digits(idx_account)
    idx_account = check_choice_range(idx_account, list(account_list.index.values))
    user_account = account_list.loc[idx_account]
    
    func_idx = cls_input("0 deposit \n1 withdraw \n\n Choose the function you want [0, 1]: ")
    func_idx = check_digits(func_idx)
    
    
    if func_idx == 0:
        account.deposit(user_account)
    elif func_idx == 1:
        account.withdraw(user_account)
    
    
if __name__ == "__main__":
    run()