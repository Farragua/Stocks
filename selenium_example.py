from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import re

# PATH = "C:\Program Files (x86)\chromedriver.exe" # path donde esta el chromedriver
#PATH = "/mnt/c/Program Files (x86)/chromedriver.exe"
#driver = webdriver.Chrome(PATH)

# def aceptar_coockies():
#   url = "https://finance.yahoo.com/quote/FB/balance-sheet?p=FB"
#   time.sleep(5)
#   print("esperando.....")
#   driver.get(url)
#   link = driver.find_element_by_xpath("/html/body/div/div/div/div/form/div[2]/div[2]/button") # boton de aceptar todas las coockies
#   link.click() # clicka en el aceptar todas las coockies!

fechas = '3/30/202112/30/20209/29/20206/29/20203/30/2020'


def ordenar_fechas(fechas):  # fechas es un string

    # ['3', '30', '202112', '30', '20209', '29', '20206', '29', '20203', '30', '2020']
    fechas1 = fechas.split('/')
    insertar = 'False'
    aux = []
    j = 1
    for j in fechas1:
        if len(j) > 4:
            for i in range(0, len(fechas1)):
                if insertar == 'True':
                    # insertamos los digitos tomados de la iteracion anterior.
                    fechas1.insert(i, aux)
                    aux = []
                    insertar = 'False'
                # Si la longitud es >4, tenemos que coger los 4 primeros digitos, y los siguientes insertalos en la siguiente posicion de la lista.
                if (len(fechas1[i]) > 4):
                    # reservamos los ultimos digitos para meterlos en la siguiente iteracion
                    aux = fechas1[i][4:]
                    # borramos todo lo que haya a partir del cuarto digito
                    fechas1[i] = fechas1[i][:4]
                    insertar = 'True'


    return fechas1

print(ordenar_fechas(fechas))
fechas1 = ['3', '30', '2021', '12', '30', '2020', '9',
   '29', '2020', '6', '29', '2020', '3', '30', '2020']
   











