import arrow
from selenium import webdriver
import socket
from time import sleep


def RAM_Crawl():
    # Memory specific data
    installmentPriceProducts = []  # Memory Installment Prices
    pricesProducts = []  # Memory Prices
    namesProducts = []  # Memory Name
    linksProducts = []  # Memory Links
    imgProducts = []  # Memory Image
    allData = []  # Memory all data
    local = arrow.utcnow()
    hostIP = socket.gethostname()
    IPAddr = socket.gethostbyname(hostIP)
    for i in range(10):
        driver = webdriver.Chrome()
        page = i + 1
        link = 'https://www.pichau.com.br/hardware/memorias?page='
        new_link = link + str(page)
        driver.get(new_link)
        height = driver.execute_script("return document.body.scrollHeight")
        scroll = 0
        driver.fullscreen_window()
        sleep(5)
        # Crawling Products == Image
        product = driver.find_elements('tag name', 'img')
        for e in product:
            if 'product' in e.get_attribute('src'):  # Only separate images with product in the name
                imgProducts.append(e.get_attribute('src'))
        while scroll < height:
            driver.execute_script(f"window.scrollTo(0, {scroll});")
            product = driver.find_elements('tag name', 'img')
            for e in product:
                if 'product' in e.get_attribute('src'):  # Only separate images with product in the name
                    imgProducts.append(e.get_attribute('src'))
            scroll += 200
        imgProducts = list(dict.fromkeys(imgProducts))

        # Crawling Products == Price
        if IPAddr == '192.168.2.38' or IPAddr == '192.168.2.75':  # Id verification
            product = driver.find_elements('class name', 'jss64')  # Possibles class name = jss191, jss69, jss64, jss201
            for i in product:
                if 'R$' in i.text:
                    pricesProducts.append(i.text)

            # Crawling Products == Installment Price
            product = driver.find_elements('class name', 'jss72')  # Possibles class name = jss199, jss77, jss72, jss209
            for i in product:
                if 'R$' in i.text:
                    installmentPriceProducts.append(i.text)

        else:  # Different ID

            # Crawling Products == Price
            product = driver.find_elements('class name', 'jss191')  # Possibles class name = jss191, jss69
            for i in product:
                if 'R$' in i.text:
                    pricesProducts.append(i.text)

            # Crawling Products == Installment Price
            product = driver.find_elements('class name', 'jss199')  # Possibles class name = jss199, jss77
            for i in product:
                if 'R$' in i.text:
                    installmentPriceProducts.append(i.text)

        # Crawling Products == Name
        product = driver.find_elements('tag name', 'h2')
        for i in product:
            if i.text == "":
                continue
            namesProducts.append(i.text)

        # Crawling Products == Links
        links = driver.find_elements('tag name', 'a')
        for i in links:
            if 'memoria' in i.get_attribute('href'):
                linksProducts.append(i.get_attribute('href'))
        driver.close()

    # Separating data in dictionary for better reading
    for i in range(len(installmentPriceProducts)):
        if '.' in pricesProducts[i]:
            pricesProducts[i] = pricesProducts[i].replace('.', '')
        changeablePrices = pricesProducts[i].replace('R$', '').replace(',', '.')
        if '.' in installmentPriceProducts[i]:
            installmentPriceProducts[i] = installmentPriceProducts[i].replace('.', '')
        changeableInstallmentPriceProducts = installmentPriceProducts[i].replace('R$', '').replace(',', '.')
        dataDic = {'Store': 'Pichau', 'Name': namesProducts[i], 'Price': [pricesProducts[i], float(changeablePrices)],
                   'Installment price': [installmentPriceProducts[i], float(changeableInstallmentPriceProducts)],
                   'Link': linksProducts[i], 'Image': imgProducts[i], 'Time': local.format('YYYY-MM-DD HH:mm:ss'),
                   'Logo': 'https://static.pichau.com.br/logo-pichau-2021-dark.png'}
        allData.append(dataDic)
    return allData

