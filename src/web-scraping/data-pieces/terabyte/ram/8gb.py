from selenium import webdriver

# Item Lists
namesProducts = []
imgProducts = []
allData = []
linksProducts = []
pricesProducts = []

# WebDriver SELECT
driver = webdriver.Chrome()
driver.get('https://www.terabyteshop.com.br/hardware/memorias/ddr4')

# Crawling Products == Name Product
product = driver.find_elements('tag name', 'h2')
for i in product:
    if i.text == "":
        continue
    namesProducts.append(i.text)

# Crawling Products == Price Product
product = driver.find_elements('class name', 'prod-new-price')
for i in product:
    if i.text == "":
        continue
    pricesProducts.append(i.text)

# Crawling Products == Link Product
product = driver.find_elements('class name', 'commerce_columns_item_image')
for i in product:
    linksProducts.append(i.get_attribute('href'))
linksProducts = list(dict.fromkeys(linksProducts))  # Remove Links Duplicates
linksProducts.remove(None)  # Fixes a small bug in crawling

# Crawling Products == Image Product
product = driver.find_elements('tag name', 'img')
for i in product:
    if 'produto' in i.get_attribute('src'):  # Only separate images with product in the name
        imgProducts.append(i.get_attribute('src'))

# Separating data in dictionary for better reading
for i in range(len(pricesProducts)):
    pricesProducts[i] = pricesProducts[i].replace(' à vista', '') # 
    if '.' in pricesProducts[i]:
        pricesProducts[i] = pricesProducts[i].replace('.', '')
    changeablePrices = pricesProducts[i].replace('R$', '').replace(',', '.')
    dataDic = {'Name': namesProducts[i], 'Price': [pricesProducts[i], float(changeablePrices)],
               'Links': linksProducts[i], 'Images': imgProducts[i]}
    allData.append(dataDic)
print(allData)
