from owlready2 import *
import pandas as pd
import pickle
import os
from os import walk
import shutil
from s02_plot import *
from s03_functions import *
###################################################################
# Encontrar arquivos no diretório de dados

def encontrar_arq():
    path = './data_in/'

    for path, diretorios, arquivos in walk(path) :
        for arq in arquivos:
            nome_arq=os.path.splitext(arq)[0]
            #print(nome_arq)

            if arq.endswith(".owl") or arq.endswith(".rdf"):
                onto = get_ontology(path+str(arq)).load()

                class root(Thing):
                    namespace = onto

                #Apresentação das classes
                classes=list(onto.classes())

                x=[]
                s = 0
                for i in classes:
                    for l in range(len(onto.get_children_of(i))):
                        b = (i.is_a[0],i)
                        x.append(b)
                        s = s + 1

                s = 0
                for i in classes:
                    for l in range(len(onto.get_children_of(i))):
                        b = (i, onto.get_children_of(i)[l])
                        x.append(b)
                        s = s + 1

                df = pd.DataFrame(x)
                df.columns = ['n1', 'n2']
                df['prop'] = 'is-a'
                df = df.drop_duplicates()

                df.to_csv('./data_in/'+nome_arq+'_adj.csv', index = False, sep='|')

                # ontologia
                df=carga_de_ontologia(nome_arq+"_adj.csv")

                # criando grafos da ontologia (direcionado e nao direcionado)
                nodes=nos(df)
                edges=arestas(df)

                qtd_nos(df)
                qtd_arestas(df)

                H=build_graph_nx(nodes,edges)
                G=build_Digraph_nx(nodes,edges)

                data = [H, G]
                graph_file = "./data_in/"+ nome_arq + "_ontology.graph"
                pickle.dump(data, open(graph_file, "wb"))


    return()

###################################################################
# Menu de arquivos de avaliação

def encontrar_arq_avaliacao():
    path = './data_in/'

    for path, diretorios, arquivos in walk(path) :
        for arq in arquivos:
            if arq.startswith("avalia_conceitos"):
                base_avaliacao = os.path.splitext(arq)[0]
    return()

###################################################################
# Menu de arquivos

def criar_menu_arq():
    path = './data_in/'

    arr = os.listdir(path)

    #lista = [arq for arq in arr if(arq.endswith(".graph"))]
    lista = [arq for arq in arr if (arq.endswith(".graph") or arq.endswith("_adj.csv") or arq.endswith(".owl"))]

    menu_list = []
    n = 1
    for i in lista:
        print(n, i)
        menu_list.append((n,i))
        n = n + 1

    dic=dict(menu_list)
    return dic

###################################################################
# Menu de arquivos de avaliação

def criar_menu_arq_avaliacao():
    path = './data_in/'

    arr_avaliacao = os.listdir(path)

    lista = [arq for arq in arr_avaliacao if
             (arq.startswith("avalia_conceitos"))]

    lista.sort()

    menu_avalia_list = []
    n = 1
    for i in lista:
        print(n, i)
        menu_avalia_list.append((n,i))
        n = n + 1

    dic_avalia=dict(menu_avalia_list)

    return dic_avalia

###################################################################
# Menu de arquivos
def carga_de_ontologia(base):
    #print('')
    #print('./data_in/'+str(base))
    #print('Layout do arquivo base: ontologia:')
    #df=pd.read_csv('./data_in/'+str(base),decimal=".",delimiter='|')

    dftext=pd.read_csv('./data_in/'+str(base),decimal=".",delimiter='|',chunksize=1000000)
    dflist=[]
    for df in dftext:
        dflist.append(df)

    df=pd.concat(dflist,sort=False)
    print(df.head(3))
    return df

def carga_de_avaliacao(avaliacao_nome):
    print('')
    print('Layout do arquivo de avaliação')
    df_avaliacao=pd.read_csv('./data_in/'+str(avaliacao_nome),decimal=".",delimiter='|')
    print(df_avaliacao) #.head(3)
    return df_avaliacao