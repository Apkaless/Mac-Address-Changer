import re
import time
import os
import subprocess
import random
import string





def generate_random_mac_address():

    letters = string.hexdigits

    special_chars = '2ae'

    generated_mac_address = ''.join(random.choice(letters)) + ''.join(random.choice(special_chars)) + ''.join(random.choice(letters) for i in range(10))

    return generated_mac_address.upper()

def cleaned_mac_address(mac_address):

    mac_address_chars_list = []

    for i in mac_address:
        mac_address_chars_list.append(i)
    
    new_mac_address = mac_address_chars_list[0] + mac_address_chars_list[1] + '-' + mac_address_chars_list[2] + mac_address_chars_list[3] + '-' + mac_address_chars_list[4] + mac_address_chars_list[5] + '-' + mac_address_chars_list[6] + mac_address_chars_list[7] + '-' + mac_address_chars_list[8] + mac_address_chars_list[9] + '-' + mac_address_chars_list[10] + mac_address_chars_list[11]

    return new_mac_address

def get_connected_adapters():

    '''This Function Will Return The Mac address and the Transport name'''

    global mac_address

    global transport_name

    mac_pattern = '[A-Z0-9:-]+'

    tran_pattern = '{.+}'

    res = subprocess.check_output('getmac').decode().splitlines()

    for current_mac in res:

        mac = re.search(mac_pattern, current_mac)

        transport = re.search(tran_pattern, current_mac)

        if mac:
            if len(mac.group()) > 1:
                mac_address = mac.group()

        if transport:
            if len(transport.group()) > 1:
                transport_name = transport.group()

    
    return mac_address, transport_name



def change_mac_address(new_mac_address, trans):
    
    n = 0

    while True:

        interface = 'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\\000%s' %(n)

        res = subprocess.check_output(f'reg QUERY {interface}').decode()

        if trans in res:

            print('Found it in ' + interface + '\n\n' + '#'*114)

            print('\n\n[!] Changing Mac Address...\n\n')

            time.sleep(2)

            change_mac_address = subprocess.check_output(f'reg ADD {interface} /v NetworkAddress /d {new_mac_address} /f').decode()

            print(change_mac_address)

            interface_index = n

            break
        else:
            print('\nNot Found in ' + interface + '\n\n' + '#'*114 + '\n')
            n = n + 1
            time.sleep(2)
            continue
    return interface_index



def disableInterface(interface_index):

    res = subprocess.check_output(f'wmic path win32_networkadapter where index={interface_index} call disable').decode()

    return res

def enableInterface(interface_index):

    res = subprocess.check_output(f'wmic path win32_networkadapter where index={interface_index} call enable').decode()

    return res



if __name__ == '__main__':

    os.system('cls')

    print('''
_______        ______        ______                   
___    |__________  /_______ ___  /___________________
__  /| |__  __ \_  //_/  __ `/_  /_  _ \_  ___/_  ___/
_  ___ |_  /_/ /  ,<  / /_/ /_  / /  __/(__  )_(__  ) 
/_/  |_|  .___//_/|_| \__,_/ /_/  \___//____/ /____/  
       /_/  


[x] Owner     : Apkaless

[x] Country   : Iraq

[x] Instagram : apkalees

[x] Status    : Online

''')

    start_process = input('\nPress Enter To Continue...\n')
    os.system('cls')
    mac_address, transport_name = get_connected_adapters()

    new_mac_address = generate_random_mac_address()

    interface_index = change_mac_address(new_mac_address, transport_name)

    if interface_index:

        print(f'[*] Old Mac Address: {mac_address}\n\n[+] New Mac Address: {cleaned_mac_address(new_mac_address)}\n\n')

        if disableInterface(interface_index):
            print('[+] Disabled Network Adapter\n')
        time.sleep(2)
        if enableInterface(interface_index):
            print('[+] Enabled Network Adapter\n')
    else:
        pass