from bs4 import BeautifulSoup as bsp
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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
        driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)

    page_soup = bsp(driver.page_source, "html.parser")

    abi_element = page_soup.find_all("pre", class_= "js-copytextarea2")
    # abi_element = page_soup.find("pre", id = "js-copytextarea2")
    abi = abi_element if abi_element else None

    with open(f"data/ABI_{address}.txt", "w") as f:
         f.write(abi[0].text)
        
    driver.delete_all_cookies()
    driver.get("chrome://settings/clearBrowserData")
    driver.quit()

    return abi[0].text