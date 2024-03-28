from bs4 import BeautifulSoup as bsp
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options

def tokenAbi(address, driver=None):
    try:
        filename = f"ABI_{address}.txt"
        with open(f"data/{filename}") as f:
                abi = f.readlines()
                return abi[0]
    except IOError:
        abi = findAbi(address, driver)
        return abi
    
def findAbi(address, driver):
    url = f"https://bscscan.com/address/{address}#code"
    if not driver:
        # options = Options()
        # options.headless =True
        driver = webdriver.Chrome()

    driver.get(url)

    page_soup = bsp(driver.page_source, features = "lxml")
    # print("page soup===========>",page_soup)

    abi = page_soup.find_all("pre", {"class": "wordwrap js-copytextarea2"})
    print("find abi =================>", abi)