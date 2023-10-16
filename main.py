import requests
from time import sleep

from config import *
from modules.capsolver import Capsolver

SITE_KEY = '6Lcx3V0oAAAAAJAXMNNDvwhIZI0wnZuM7-YjIIRx'
SITE_URL = 'https://genesis.celestia.org/'

def read_txt(filepath):
    with open(filepath, "r") as file:
        return [row.strip() for row in file]

def check_eligibility(address, captcha_solver):
    while True:
        try:
            task_id = captcha_solver.create_task()
            token = captcha_solver.get_captcha_solution(task_id)

            resp = requests.get(f'https://genesis-api.celestia.org/api/v1/airdrop/eligibility/{address}?recaptcha_token={token}')
            slug = resp.json()['slug']

            if (slug == 'recaptcha-verification'):
                print('ERROR: bad captcha token!')
                continue

            eligible = True if (slug == 'eligible') else False
            return eligible
        except Exception as error:
            print(f'ERROR checking eligibility: {error}')
            sleep(3)


def main():
    wallets = read_txt("wallets.txt")
    total_wallets = len(wallets)
    eligible_wallets = []
    print(f'Loaded {total_wallets} wallets')

    captcha_solver = Capsolver(API_KEY, SITE_URL, SITE_KEY, page_action='submit')

    for _id, address in enumerate(wallets):
        eligible = check_eligibility(address, captcha_solver)
        if (eligible):
            eligible_wallets.append(address)
        print(f'  Checking {_id+1}/{total_wallets}...', end='\r')

    print(f'\nEligible {len(eligible_wallets)} of {total_wallets}!')

    with open('eligible.txt', 'w') as file:
        for address in eligible_wallets:
            file.write(f'{address}\n')
    print("Saved results to 'eligible.txt'\nClosing...")
    sleep(5)


if (__name__ == '__main__'):
    main()
