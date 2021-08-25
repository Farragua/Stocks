import pandas as pd

import json, operator



def to_json_append(df,file):
    '''
    Load the file with
    pd.read_json(file,orient='records',lines=True)
    '''
    df.to_json('tmp.json',orient='records',lines=True)
    #append
    f=open('tmp.json','r')
    k=f.read()
    f.close()
    f=open(file,'a')
    #f.write('\n') #Prepare next data entry
    f.write(k)
    f.close()



def get_sp500_list():
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    print("reading table...")
    df = table[0]
    df = df['Symbol']
    #df.to_csv('S&P500-Info.csv')
    #df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])
    return df

def save_list(df, nombrefichero):
    df.to_csv(nombrefichero)
#    df.to_csv(nombrefichero, columns=['Symbol'])
    print("Lista guardada")




def leer_fichero_resultados_pick25(name_fichero):
    #Le damos formato al fichero
    df = pd.read_csv(name_fichero, header=0, names=['Ticker', 'ROE', 'Debt2Eq', 'PriceFCF', 'Points'])
    

    df = df.sort_values(by='Points', ascending=False)
    df = df.head(25)
    print(df)
    return df

def dataframe2html(dataframe, nombreficherohtml):
    result = dataframe.to_html(classes='table table-striped', index_names='False', index='False')
    
    print(result)

    # write html to file
    text_file = open(nombreficherohtml, "w")
    text_file.write(result)
    text_file.close()

    return result


fichero_web_data = leer_fichero_resultados_pick25('Results.json')
save_list(fichero_web_data, 'Results_to_web.json')


