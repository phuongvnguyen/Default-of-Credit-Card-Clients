#!/usr/bin/env python
# coding: utf-8

# In[73]:


from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('reload_ext', 'sql')
import sqlite3

class extract():
    
    def __init__(self):
        self.name_file='UCI_Credit_Card.csv'
        self.dat=self.load_data(self.name_file)
        
    def load_data(self,name_file):
        self.data=pd.read_csv(name_file)
        print('Data was loaded successfully!')
        return self.data
    
class transform():
    
    def __init__(self,extract):
        self.data=extract.data
        display(self.data.head(3))
        self.infor_data=self.get_info(self.data)
        self.name_column='default.payment.next.month'
        self.re_data=self.rename_colum(self.data,self.name_column)
        self.name_cat=['SEX','EDUCATION', 'MARRIAGE', 'DEFAULT']
        self.cat_plot=self.plot_cat(self.data,self.name_cat)
        self.cleaned_data =self.abnormal_solver(self.data)
        self.plot_numeric(self.cleaned_data)
            
    def get_info(self,data):
        self.infor=data.info()
        self.data_desribe=data[data.columns[1:25]].describe().T
        display(self.data_desribe)
        return self.data_desribe
    
    def rename_colum(self,data,name_column):
        self.data=data.rename(columns={name_column:'DEFAULT'})
        return self.data
    
    def plot_cat(self,data,name_columns):
        plt.figure(figsize=(15, 9))
        for i,col in enumerate(name_columns):
            print(col)
            print(data[col].value_counts())
            plt.subplot(3,2,i+1)
            sns.countplot(y=col,data=data)
            
    def abnormal_solver(self,data):
        data['EDUCATION']=data['EDUCATION'].replace([0,5,6],4)
        data['MARRIAGE']=data['MARRIAGE'].replace(0,3)
        self.data=data.drop(['ID'],axis=1)
        return self.data
    
    def plot_numeric(self,data):
        self.con_vars=data.loc[:,data.dtypes==np.float64].columns.tolist()
        plt.figure(figsize=(15, 5))
        boxplot=data.boxplot(column=self.con_vars,figsize=(10,5),rot=65,sym='go')
        plt.suptitle('The distribution of %d NT dollar-measured variables'%len(self.con_vars),fontweight='bold')
        plt.ylabel('NT dolar',fontweight='bold')
        plt.xlabel('The name of %d NT dollar-measured variables'%len(self.con_vars),fontweight='bold')
        plt.show()
        
class load():
    
    def __init__(self,transform):
        self.data=transform.cleaned_data
        self.insert_data=self.load_to_database(self.data)
        self.nam_file='Cleaned_UCI_Credit_Card'
        self.export=self.export_data(self.data,self.nam_file)
              
    def load_to_database(self,Credit_card_default):
        self.connect_db = get_ipython().run_line_magic('sql', 'sqlite:///Phuong_Credit.db')
        print(self.connect_db)
        print('The connection is successfully!')
        self.info_data = get_ipython().run_line_magic('sql', "SELECT name FROM sqlite_master WHERE type='table'")
        print(self.info_data)
        self.check = get_ipython().run_line_magic('sql', 'DROP TABLE IF EXISTS Credit_card_default')
        self.insert_data = get_ipython().run_line_magic('sql', 'PERSIST Credit_card_default')
        self.check = get_ipython().run_line_magic('sql', 'SELECT * FROM Credit_card_default LIMIT 3')
        display(self.check)
        return self.connect_db
    
    def export_data(self,data,nam_file):
        print('I am exporting data to the csv and excel files\n...')
        self.export_csv=data.to_csv(nam_file+'.csv')
        self.export_excel=data.to_excel(nam_file+'.xlsx')
        print('Data was exported successfully!')
        return self.export_csv
    
                                      
class main():
    extract=extract()
    transform=transform(extract)
    load=load(transform)
    
if __name__=='__main__':
    main()


# In[ ]:




