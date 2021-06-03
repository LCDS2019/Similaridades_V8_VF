import pandas as pd
import numpy as np
import csv
import shutil
import os
import matplotlib.pyplot as plt
import seaborn as sns

from os import walk
from sklearn import preprocessing

from numpy.random import rand
from numpy.random import seed
from scipy.stats import spearmanr
seed(1)

def prep_arq_avaliacao():
    path = './data_out/'
    list=[]
    for path, diretorios, arquivos in walk(path) :
        for arq in arquivos:
            if arq != 'experiments.csv':
                list.append(arq)
    return(list)

def coef_spearman(df,i):
    #print('********************************')
    print('Coeficiente de Spearman')

    print(i)

    sum_d2=sum(df['d_i2'])
    print('sum_d2 = '+str(sum_d2))

    n=len(df['d_i2'])
    print('n = ' + str(n))

    tab_freq_in = pd.value_counts(df.res_in_rank).to_frame().reset_index()
    tab_freq_in=tab_freq_in[(tab_freq_in.res_in_rank > 1)]
    print(tab_freq_in['res_in_rank'])

    tab_freq_calc=pd.value_counts(df.res_calc_rank).to_frame().reset_index()
    #tab_freq_calc=tab_freq_calc[(tab_freq_calc.res_calc_rank > 1)]
    print(tab_freq_calc['res_calc_rank'])

    print('----------------------------------------')
    tab_freq=pd.concat([tab_freq_in['res_in_rank'], tab_freq_calc['res_calc_rank']], axis=0)

    mi=[]
    for i in tab_freq:
        calc_mi=i**3-i
        mi.append(calc_mi)

    mi_res=pd.DataFrame(mi)

    print(mi_res)

    coef_spearman_result=(1-6*(((sum_d2+(1/12)*sum(mi_res[0])))/(n * (n ** 2 - 1))))
    print('coef_spearman_result: '+str(coef_spearman_result))

    #print('********************************')
    return(coef_spearman_result)



def avalia_correlacao():

    print('---------------------------------------')
    print('Análise de dados - Similaridades')
    print('---------------------------------------')

    #print('Arquivo(s):')
    list=prep_arq_avaliacao()
    list=sorted(list)
    #print(list)

    colunas=['experimento','n_linhas','coef_spearman','mse']
    df_res=pd.DataFrame(columns=colunas)

    u = 1
    for i in list:
        if i!='experiments.csv' and i.startswith('similaridade'):
            scaler =preprocessing.StandardScaler()

            print(u,i)

            df=pd.read_csv('./data_out/'+str(i), sep='|', decimal='.')
            df.columns = ['c1','c2','res_in','res_calc']
            #df = df.sort_values(['res_in'])
            df['res_in_adj_std'] = scaler.fit_transform(df[['res_in']])
            df['res_calc_adj_std'] = scaler.fit_transform(df[['res_calc']])

            df['res_in_rank'] = df['res_in'].rank()
            df['res_calc_rank'] = df['res_calc'].rank()
            df['d_i']=df['res_calc_rank']-df['res_in_rank']
            df['d_i2']=df['d_i']**2

            print(df)
            print('')
            coef=coef_spearman(df,i)
            mse=df['d_i2'].mean()

            print('********************************')
            print('Spearmans correlation coefficient: %.4f' % coef)
            print('********************************')
            print('MSE:'+ str(mse))
            print('********************************')

            df.to_csv(r'./data_out_reports/experiments_'+str(u)+'_'+str(i)+'.csv', index=False, header=True,sep='|',decimal='.')
            to_append = [str(i),str(df.shape[0]),str('%.4f' % coef),str('%.4f' % mse)]

            df_res.loc[len(df_res),:]=to_append

        u=u+1
        #print('---------------------------------------')



    df_res.to_csv(r'./data_out_reports/experiments.csv', index=False, header=True, sep='|', decimal='.')
    #print(df_res)
    print('')
    print('')
    #print(df_res)

    print('---------------------------------------')
    print('fim')
    print('---------------------------------------')