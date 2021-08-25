from datetime import datetime
import numpy as np
import pandas as pd
import time
import webscraping as web
import sp500 as sp500

def panda_symbol_final(symbol, roe, deb2eq, price2fcf):
    
    data_dic = {"TICKER: " : symbol,
    "ROE":roe,
    "Debt_to_Equity": deb2eq,
    "Price_FCF": price2fcf,
    "Ranking:": 0
    }
    df = pd.DataFrame(data_dic, index=[symbol])



    return df


def init_pandas():
   df=panda_symbol_final("XXX",0.0,0.0, 0.0)
   return df

# --------------------------------------=== MAIN ===-----------------------------------------------------#
#Algoritmo 1
nombrefichero1 = 'Results.json'
nombrefichero1_filtered = 'Results_to_web1.json'
nombreficherohtml1 = 'results.html'
#Algoritmo 2
nombrefichero2 = 'Results2.json'
nombrefichero2_filtered = 'Results_to_web2.json'
nombreficherohtml2 = 'results2.html'
#Obtenemos la lista de los 500 tickers
list_symbols = sp500.get_sp500_list()
#list_symbols = []
df1=init_pandas() #inicializo el dataframe panda por primera vez antes del bucle para luego ir añadiendo una fila en cada iteracion
df2=init_pandas()
#print(df)
#print(type(list_symbols))
for i in list_symbols[254:]:
#for i in list_symbols:
  # symbol='FB'
   print("TICKER", i)
   if i.__contains__('.'):
      i = i.replace(".", "-")
   #print('=================================|TICKER:',i,'|===============================================',(list_symbols.index(i)),'/',len(list_symbols),'===',(list_symbols.index(i)/len((list_symbols))*100),'%')
   print('=================================|TICKER:',i,'|===============================================')
   pdfinancials = web.get_pandas_yahoo(web.definir_url_financials(i))
   """ pdfinancials = pdfinancials.drop(['Cost of Revenue', 'Gross Profit', 'Tax Rate for Calcs', 'Tax Effect of Unusual Items', 'Operating Expense', 'Operating Income', 
   'Reconciled Cost of Revenue', 'Reconciled Depreciation', 'Net Non Operating Interest Income Expense', 'Other Income Expense',  'Pretax Income',  'Tax Provision',  
   'Interest Expense', 'Net Interest Income', 'Diluted NI Available to Com Stockholders', 'Interest Income', 'Basic Average Shares',
   'Normalized Income', 'Net Income from Continuing Operation Net Minority Interest', 'Net Income from Continuing & Discontinued Operation',
      'Total Operating Income as Reported', 'Total Expenses'   ], axis=1) """
   #print(pdfinancials)    # Total Revenue  Net Income Common Stockholders  Diluted Average Shares        EBIT  Normalized EBITDA son los ratos que uso de la pagina financials
   pdcashflow = web.get_pandas_yahoo(web.definir_url_cashflow(i))
   #print(pdcashflow)
   """ pdcashflow = pdcashflow.drop(['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'End Cash Position', 
   'Income Tax Paid Supplemental Data', 'Interest Paid Supplemental Data', 'Capital Expenditure' , 'Repayment of Debt' ], axis=1) """

   pdbalance_sele = web.crear_panda_balance(web.get_balance_selenium(i))

   # Extraccion de variables
   debt2eq=web.get_debt2equity(pdbalance_sele)
   net_income=pdfinancials['Net Income Common Stockholders'][1]
   equity=pdbalance_sele['Equity'][0]
   if equity == 1:
      roe = -999
   else:
      roe = net_income/equity #net income / equity actual

   # Si aqui llega un pdcashflow=0 el programa peta
   if (pdcashflow['Free Cash Flow'][1] != None):
        fcf = pdcashflow['Free Cash Flow'][1]
   else:
        #como no podemos obtener el fcf desde yahoo, le ponemos 0.01 para que se vaya la empresa al final de la lista y no nos aparezca
        fcf=0.01
   
   mcap = web.get_mcap(pdbalance_sele)
   price2fcf=mcap/fcf
   """ print("tipo roe", type(roe))
   print("tipo d2e", type(debt2eq))
   print("tipo roe", type(price2fcf))
   print(roe)
   print(mcap)
   print(debt2eq)
   print(fcf)
   print(price2fcf) """

   # SHIFT + ALT + A Para comentar varias lineas

   # crear panda con roe, deb2eq y price2fcf

   #Si el precio to fcf es negativo, lo mandamos al final de la lista (eliminamos)
   if price2fcf < 0:
      price2fcf = 999
   if roe < 0:
      roe = -999

   
   
   """ puntos1 = roe*100 - debt2eq*100 - price2fcf
   df1.loc[i]=[i, roe, debt2eq, price2fcf, puntos1 ]
   sp500.to_json_append(df1.loc[i],nombrefichero1)
   #print(df)
   print("Algoritmo 1: ")
   print(df1)  """

   puntos2 = roe*100*0.4 - debt2eq*100*0.4 - price2fcf*0.2
   df2.loc[i]=[i, roe, debt2eq, price2fcf, puntos2]
   sp500.to_json_append(df2.loc[i],nombrefichero2)
   print("Algoritmo 2: ")
   print(df2)
   
      #print(panda_symbol_final(i,roe,debt2eq, price2fcf))

# Una vez acabado el bucle cogemos las 25 empresas con mejores fundamentales:
""" datos_web_data1 = sp500.leer_fichero_resultados_pick25(nombrefichero1)
sp500.save_list(datos_web_data1, nombrefichero1_filtered)
sp500.dataframe2html(datos_web_data1) """

datos_web_data2 = sp500.leer_fichero_resultados_pick25(nombrefichero2)
sp500.save_list(datos_web_data2, nombrefichero2_filtered)
sp500.dataframe2html(datos_web_data2,nombreficherohtml2)


