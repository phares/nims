import lipisha
from lipisha import Lipisha

<<<<<<< HEAD
api_key = ""
api_signature = ""
lipisha = Lipisha(api_key, api_signature, api_environment='live')
lipisha.api_base_url
'https://lipisha.com/payments/accounts/index.php/v2/api'
=======
api_key = "**********************************"
api_signature = "************************************************************************88"
lipisha = Lipisha(api_key, api_signature, api_environment='test')
lipisha.api_base_url
'http://lipisha.com/index.php/v2/api/'
>>>>>>> 1c397ea447c8373aebf3f07fe88b5cf2e784e640

class Lipisha_bulk():

        def __init__(self):
            pass

        #Get Balance
        def get_balance(self):
            c = lipisha.get_balance()
            content = c['content']
            status = c['status']
            return content,status

        #get float
        #account_number="01260"
        def get_float(self,account_number):
            float = lipisha.get_float(account_number)
            float_content = float['content']
            float_status = float['status']

        #confirm transaction
        #4V8KPI7JM
        def confirm_transaction(self,transaction):
            confirm = lipisha.confirm_transaction(transaction)
            confirm_content = confirm['content']
            confirm_status = confirm['status']

        #create account
        def create_account(self, transaction_account_type, transaction_account_name, transaction_account_manager):
            create_account = lipisha.create_payment_account(transaction_account_type,
                                       transaction_account_name,
                                       transaction_account_manager)

            create_content = create_account['content']
            create_status = create_account['status']

        #get transactions
        def get_transactions(self):
            get_transactions = lipisha.get_transactions()
            get_content = get_transactions['content']
            get_status = get_transactions['status']
            return get_content

        #get customers
        def customers(self):
            customers = lipisha.get_customers()
            customers_content = customers['content']
            customers_status = customers['status']

        #get a given customer
        def get_customers(self, customer_mobile_number):
            customer = lipisha.get_customers(customer_mobile_number)
            customer_content = customer['content']
            customer_status = customer['status']

        #send airtime
        #account_number="01261"
        # "SAF" #
        def send_airtime(self, account_number, mobile_number, amount, network):
            send_airtime = lipisha.send_airtime(account_number, mobile_number, amount, network)
            send_airtime_content = send_airtime['content']
            send_airtime_status = send_airtime['status']

        #send money
        #account_number="01260"
        def send_money(self, account_number, mobile_number, amount):
<<<<<<< HEAD
            lipisha.send_money(account_number, mobile_number, amount)
=======
            send_money = lipisha.send_money(account_number, mobile_number, amount)

            send_money_content = send_money['content']
            send_money_status = send_money['status']
>>>>>>> 1c397ea447c8373aebf3f07fe88b5cf2e784e640

        #authorize card transaction
        def authorize_card_transaction(self,account_number, card_number, address1 , address2, expiry, name, country, state, zip, security_code, amount, currency):
            authorize_card_transaction = lipisha.authorize_card_transaction(account_number,
                                           card_number,
                                           address1,
                                           address2,
                                           expiry,
                                           name,
                                           country,
                                           state,
                                           zip,
                                           security_code,
                                           amount,
                                           currency)

            authorize_card_transaction_content = authorize_card_transaction['content']
            authorize_card_transaction_status = authorize_card_transaction['status']

        #withdrawal account
        def create_withdrawal_account(self, transaction_account_type, transaction_account_name, transaction_account_number,
                                      transaction_account_bank_name, transaction_account_bank_branch, transaction_account_bank_address,
                                      transaction_account_swift_code, transaction_account_manager):
            create_withdrawal_account = lipisha.create_withdrawal_account(transaction_account_type,
                                   transaction_account_name,
                                   transaction_account_number,
                                   transaction_account_bank_name,
                                   transaction_account_bank_branch,
                                   transaction_account_bank_address,
                                   transaction_account_swift_code,
                                   transaction_account_manager)

            create_withdrawal_account_content = create_withdrawal_account['content']
            create_withdrawal_account_status = create_withdrawal_account['status']