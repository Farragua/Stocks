from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import pandas as pd
import string

def quitar_comas(string_1):
    string_nueva=[]
    for i in range(0,len(string_1)):
        
        out = string_1[i].translate(str.maketrans('', '', string.punctuation))
        string_nueva.append(out) 

    return string_nueva

def clickar_en_texto (url, texto): 
    
    PATH = "C:\Program Files (x86)\chromedriver.exe" # path donde esta el chromedriver
    #PATH = "/mnt/c/Program Files (x86)/chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    #url = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol

    time.sleep(5)
    print("esperando.....")
    driver.get(url)

    link = driver.find_element_by_link_text(texto)
    print("link antes del click: ", link)
    link.click()
    print("link despues del click: ", link)

def aceptar_coockies(url):

    PATH = "C:\Program Files (x86)\chromedriver.exe" # path donde esta el chromedriver
    #PATH = "/mnt/c/Program Files (x86)/chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    print("esperando.....")
    driver.get(url)
    time.sleep(5)
    link = driver.find_element_by_xpath("/html/body/div/div/div/div/form/div[2]/div[2]/button") # boton de aceptar todas las coockies
    link.click() # clicka en el aceptar todas las coockies!


def get_balance_selenium(symbol):

    #driver.get(url)

    
    url = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol
    PATH = "C:\Program Files (x86)\chromedriver.exe" # path donde esta el chromedriver
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    time.sleep(2)
    link = driver.find_element_by_xpath("/html/body/div/div/div/div/form/div[2]/div[2]/button") # boton de aceptar todas las coockies
    link.click() # clicka en el aceptar todas las coockies!
    time.sleep(2)
    link = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[2]/button/div/span")
    link.click()
    time.sleep(2)
    #Common_stock_eq = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[3]/div[1]/div/div[2]/div[5]/div[1]/div[2]/span")
    

    url = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol

    # En este modulo obtenemos los datos del balance una vez clickamos en el boton "Quarterly", para automatizar el click se usa selenium. Por eso el procedimiento para obtener el balance es diferente.
    

    # Cogemos toda la tabla de la pagina balance. Obtenemos un string enorme.
    tabla=driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[3]/div[1]/div")
    
    print(tabla.text.split('\n'))

    tabla = tabla.text.split('\n')
    # Pasamos este string enorme a formato de diccionario
    dic = {}
    aux=[]
    for i in range(0, len(tabla)):
        if i==0:
            aux=tabla[i]
            #print(tabla[i])
        else:
            if i%2==1:
                dic[aux]=tabla[i]
            else:
                aux=tabla[i]


    common_stock_eq = dic['Common Stock Equity']
    #Common Stock Equity
    #133,657,000 128,290,000 117,731,000 110,447,000 105,304,000
    common_stock_eq=common_stock_eq.split()
   
    # 'Common Stock Equity\n133,657,000 128,290,000 117,731,000 110,447,000 105,304,000'
    tdebt = dic['Total Debt']
    tdebt=tdebt.split() 
    



    url_summary = 'https://finance.yahoo.com/quote/'+symbol+'?p='+symbol
    driver.get(url_summary)
    time.sleep(2)
    market_cap = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[1]/td[2]")
    market_cap = market_cap.text
    mcap_num = float(market_cap[:-1])
    multiplicador = market_cap[-1] #B or #M
    if multiplicador == 'B': # Si son billones
        mcap_num = mcap_num*1000000
    print(mcap_num)


    print("**********************************")

    tdebt=quitar_comas(tdebt)
    common_stock_eq=quitar_comas(common_stock_eq)
    print("Common Stock Eq comment: ", common_stock_eq)
    print("Total Debt comment: ", tdebt)


    #comprobar que los campos no esten vacios, ya que a veces los campos obtenidos de la web  Yahoo estan vacios

    #Lo pasamos de string a float para poder operar:

    debt_float= [float(x) for x in tdebt]
    common_stock_eq_float= [float(x) for x in common_stock_eq]

    d2e=[]
    for i in range(0, len(debt_float)):
        d2e.append(debt_float[i]/common_stock_eq_float[i])
        #print(d2e)
    print(d2e)
    return common_stock_eq, tdebt, d2e, mcap_num

   

get_balance_selenium("FB")





#tabla1=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[3]')
#tabla2=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[3]/div[1]')
#tabla3=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[3]/div[1]/div')