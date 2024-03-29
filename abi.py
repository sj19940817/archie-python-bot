# from bs4 import BeautifulSoup as bsp
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

# def tokenAbi(address, driver=None):
#     try:
#         filename = f"ABI_{address}.txt"
#         with open(f"data/{filename}") as f:
#                 abi = f.readlines()
#                 return abi[0]
#     except IOError:
#         abi = findAbi(address, driver)
#         return abi
    
# def findAbi(address, driver):
#     url = f"https://bscscan.com/address/{address}#code"
#     if not driver:
#         driver = webdriver.Chrome(ChromeDriverManager().install())

#     driver.get(url)

#     page_soup = bsp(driver.page_source, "html.parser")

#     abi_element = page_soup.find_all("pre", class_= "js-copytextarea2")
#     # abi_element = page_soup.find("pre", id = "js-copytextarea2")
#     abi = abi_element if abi_element else None

#     with open(f"data/ABI_{address}.txt", "w") as f:
#          f.write(abi[0].text)
        
#     driver.delete_all_cookies()
#     driver.get("chrome://settings/clearBrowserData")
#     driver.quit()

#     return abi[0].text


ERC20_ABI = [
    {
        'constant': False,
        'inputs': [
            {'name': '_spender', 'type': 'address'},
            {'name': '_value', 'type': 'uint256'}
        ],
        'name': 'approve',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'totalSupply',
        'outputs': [{'name': 'supply', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [
            {'name': '_from', 'type': 'address'},
            {'name': '_to', 'type': 'address'},
            {'name': '_value', 'type': 'uint256'}
        ],
        'name': 'transferFrom',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [],
        'name': 'decimals',
        'outputs': [{'name': 'digits', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [{'name': '_owner', 'type': 'address'}],
        'name': 'balanceOf',
        'outputs': [{'name': 'balance', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'constant': False,
        'inputs': [
            {'name': '_to', 'type': 'address'},
            {'name': '_value', 'type': 'uint256'}
        ],
        'name': 'transfer',
        'outputs': [{'name': 'success', 'type': 'bool'}],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'constant': True,
        'inputs': [
            {'name': '_owner', 'type': 'address'},
            {'name': '_spender', 'type': 'address'}
        ],
        'name': 'allowance',
        'outputs': [{'name': 'remaining', 'type': 'uint256'}],
        'payable': False,
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'anonymous': False,
        'inputs': [
            {'indexed': True, 'name': '_owner', 'type': 'address'},
            {'indexed': True, 'name': '_spender', 'type': 'address'},
            {'indexed': False, 'name': '_value', 'type': 'uint256'}
        ],
        'name': 'Approval',
        'type': 'event'
    }
]
