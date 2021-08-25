import pandas as pd
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import sys
import string
import lxml
from lxml import html
import requests

def quitar_comas_lista_de_strings(string_1):
    string_nueva=[]
    for i in range(0,len(string_1)):
        
        out = string_1[i].translate(str.maketrans('', '', string.punctuation))
        string_nueva.append(out) 

    return string_nueva

def quitar_comas_string(string_1):
    string_nueva=[]
    
    out = string_1.translate(str.maketrans('', '', string.punctuation))
    string_nueva.append(out) 

    return string_nueva

""" def quitar_comas_string(string_1):
    string_1 = string_1.replace(',', "")

    return string_1 """

    

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
    
    #print(tabla.text.split('\n'))

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

    # comprobamos que existe el campo 'Common Stock Equity' en el diccionario:
    if (dic.get('Common Stock Equity') != None):
        common_stock_eq = dic['Common Stock Equity']
        common_stock_eq=common_stock_eq.split()
        common_stock_eq=common_stock_eq[0]
        #common_stock_eq=quitar_comas(common_stock_eq)
    else:
        #como no podemos obtener el Equity desde yahoo, le ponemos 0 para que se vaya la empresa al final de la lista y no nos aparezca
        common_stock_eq="0.01"

    
    #Common Stock Equity
    #133,657,000 128,290,000 117,731,000 110,447,000 105,304,000
    
   
    # 'Common Stock Equity\n133,657,000 128,290,000 117,731,000 110,447,000 105,304,000'
    # comprobamos que existe el campo 'Total Debt' en el diccionario:
    if (dic.get('Total Debt') != None):
        if (dic.get('Total Debt')[0] == '-'):
            tdebt = "999999"
        else:     
            tdebt = dic['Total Debt']
            tdebt=tdebt.split() 
            tdebt=tdebt[0]
            #tdebt=quitar_comas(tdebt)


    else:
        #como no podemos obtener la total debt desde yahoo, le ponemos 999 para que se vaya la empresa al final de la lista y no nos aparezca
        tdebt="9999999"
    
     
        
    
        
      
    
        
    
    

    url_summary = 'https://finance.yahoo.com/quote/'+symbol+'?p='+symbol
    driver.get(url_summary)
    time.sleep(2)
    market_cap = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[1]/td[2]")
    market_cap = market_cap.text
    mcap_num = float(market_cap[:-1])
    multiplicador = market_cap[-1] #B or #M
    if multiplicador == 'B': # Si son billones
        mcap_num = mcap_num*1000000
    if multiplicador == 'T': 
        mcap_num = mcap_num*1000000000
    #print(mcap_num)


    print("**************************************************************************")

    signo_common_stock_equity = common_stock_eq[0] # guardamos el primer char por si acaso es negativo
    if common_stock_eq != 0.01:
        common_stock_eq = quitar_comas_string(common_stock_eq)
    tdebt = quitar_comas_string(tdebt)

    #Pasar de string a float:

    debt_float= [float(x) for x in tdebt]
    common_stock_eq_float= [float(x) for x in common_stock_eq]
    
    if signo_common_stock_equity == '-':
        common_stock_eq_float[0] = -common_stock_eq_float[0]
    

    d2e=[]
    for i in range(0, len(debt_float)):
        d2e.append(debt_float[i]/common_stock_eq_float[i])
        #print(d2e)
    print('Debt to Eq. comment:', d2e)


    print("Common Stock Eq comment: ", common_stock_eq_float)
    print("Total Debt comment: ", debt_float)
    print('Market Cap comment: ', mcap_num)

    if signo_common_stock_equity == '-':
        common_stock_eq[0] = '-' + common_stock_eq[0]
    if d2e[0] < 0:
        d2e[0] = 999.9

    return common_stock_eq, tdebt, d2e, mcap_num

#print(get_balance("FB"))


def crear_panda_balance(data):
    data_dic = {"Equity":data[0],
    "Total_Debt": data[1],
    "Debt/Eq": data[2],
    "Mcap": data[3]
    }

    frame=pd.DataFrame(data_dic)

    # Convertir las columnas del dataframe (tipo object) a tipo float
    #numeric_columns = list(frame.columns)[1::] # Take all columns, except the first (which is the 'Date' column)
    numeric_columns = list(frame.columns)[::] # Take all columns, except the first (which is the 'Date' column)


    for column_name in numeric_columns:
       # frame[column_name] = frame[column_name].str.replace(',', '') # Remove the thousands separator
        frame[column_name] = frame[column_name].astype(np.float64) # Convert the column to float64

    return frame

def get_debt2equity(frame):
    d2e= frame['Debt/Eq'][0]
    return d2e
def get_mcap(frame):
    mcap=frame['Mcap'][0]
    return mcap


#print(get_debt2equity(crear_panda_balance(get_balance("NVCR"))))
#url = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol
# los datos del balance los cojo con el otro script para poder coger el ultimo dato cuatrimestral.
def definir_url_financials(symbol):
    url_financials = 'https://finance.yahoo.com/quote/' + symbol + '/financials?p=' + symbol
    return url_financials

def definir_url_cashflow(symbol):
    url_cashflow = 'https://finance.yahoo.com/quote/' + symbol + '/cash-flow?p=' + symbol
    return url_cashflow
    

def get_pandas_yahoo(url):
    repetir = True
    while(repetir):
        # Set up the request headers that we're going to use, to simulate
        # a request by the Chrome browser. Simulating a request from a browser
        # is generally good practice when building a scraper
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Pragma': 'no-cache',
            'Referrer': 'https://google.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }


        page = requests.get(url, headers)
        time.sleep(1)
        #Tratar de conseguir directamente el dato de la tabla con Selenium .find_element

        # Parse the page with LXML, so that we can start doing some XPATH queries
        # to extract the data that we want
        tree = html.fromstring(page.content)

        # Smoke test that we fetched the page by fetching and displaying the H1 element
        tree.xpath("//h1/text()")
        #print(tree.xpath("//h1/text()"))    # Aqui tenemos el dato del nombre y ticker: ['Facebook, Inc. (FB)'] es tipo lista


        #---------------------------------------------------------------

        table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

        # Ensure that some table rows are found; if none are found, then it's possible
        # that Yahoo Finance has changed their page layout, or have detected
        # that you're scraping the page.
        if len(table_rows) > 0:

            parsed_rows = []

            for table_row in table_rows:
                parsed_row = []
                el = table_row.xpath("./div")   # la fila
                
                none_count = 0
                
                for rs in el:
                    try:
                        (text,) = rs.xpath('.//span/text()[1]')
                        parsed_row.append(text)
                    except ValueError:
                        parsed_row.append(np.NaN)
                        none_count += 1

                if (none_count < 4):
                    parsed_rows.append(parsed_row)

            df = pd.DataFrame(parsed_rows)
            #print(df)
            #print(type(df))

            #print('#----------------------------------------------------------------')
            # Recolocamos para que cada fila sea un año 

            df = pd.DataFrame(parsed_rows)
            df = df.set_index(0) # Set the index to the first column: 'Period Ending'.
            df = df.transpose() # Transpose the DataFrame, so that our header contains the account names

            #Rename the "Breakdown" column to "Date"
            cols = list(df.columns)
            cols[0] = 'Date'
            df = df.set_axis(cols, axis='columns', inplace=False)

            #print(df.dtypes)
            # Cada item dentro de la estructura panda es tipo object. Los pasamos a float para operar con ellos.

            numeric_columns = list(df.columns)[1::] # Take all columns, except the first (which is the 'Date' column)

            for column_name in numeric_columns:
                df[column_name] = df[column_name].str.replace(',', '') # Remove the thousands separator
                df[column_name] = df[column_name].astype(np.float64) # Convert the column to float64

            #print(df.dtypes)
            #print(df['Common Stock Equity'][1]) # con esto accedo a la fila! 1 dentro de Total Assets (es decir la del año mas reciente)
            #print(df)
            #print(df['Free Cash Flow'][1])
            repetir = False
        else:
            print('Yahoo ha detectado el webscraping! Esperamos 180s')
            repetir = True
            time.sleep(180)
            df=0

    return df