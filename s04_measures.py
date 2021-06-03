import networkx as nx
import pandas as pd
import seaborn as sns
import matplotlib as plt
import math
import time

###################################################################
# Apresenta a menor distância entre os nós
def shortest_path_length(H,i,j):

    short_parth=nx.shortest_path_length(H,source=i,target=j)
    if i == j:
        short_parth = 1.0
    return(float(short_parth))

###################################################################
# Medida de similaridade Spath
def sim_spath(H,i,j):

    res=1/shortest_path_length(H,i,j)

    if i == j:
        res = 1.0

    return(float(res))

def matriz_sim_path(H,base,avaliacao,df_avaliacao,avaliacao_nome):
    #print(avaliacao_nome)
    m = []
    if avaliacao == '1':
        for index, row in df_avaliacao.iterrows():
            res = sim_spath(H, row['c1'], row['c2'])
            m.append([row['c1'], row['c2'],row['res_in'], round(res, 4)])

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    else:
        for i in list(H.nodes):
            for j in list(H.nodes):
                res = sim_spath(H, i, j)
                m.append([i, j, 0, round(res, 4)])

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    base = str(base).replace('.graph', '')
    m.to_csv('./data_out/similaridade_' + str(avaliacao_nome) + '_01_sim_path.csv', index=False, sep='|',decimal='.')
    print('Lista de resultados: ' + './data_out/similaridade_' + str(avaliacao_nome) + '_01_sim_path.csv')

    return(m)

###################################################################
# Medida de similaridade Sim_wup

def sim_wup(G, i, j,root):
    # no raiz da snomed-ct:
    #root = "C3531735"

    if i == j:
        sim_wup = 1.0
        return sim_wup

    # definindo o no raiz da arvore
    for i in G.nodes():
        if (G.in_degree(i) == 0):
            root = i

    # calculando o Least Common Subsumer (Ancestor)
    LCS = nx.lowest_common_ancestor(G, i, j)

    H = G.to_undirected()
    # calculando a profundidade dos nos =  menor caminho do no até a raiz
    depth_lcs   = shortest_path_length(H, root, LCS)
    depth_node1 = shortest_path_length(H, root, i)
    depth_node2 = shortest_path_length(H, root, j)

    try:
        sim_wup = (2 * depth_lcs) / (depth_node1 + depth_node2)
    except ZeroDivisionError:
        sim_wup = 0

    return(sim_wup)

def matriz_sim_wup(G,base,avaliacao,df_avaliacao,avaliacao_nome):

    m = []
    root = 'C3531735'
    #definindo o no raiz da arvore


    #for i in G.nodes():
     #   if (G.in_degree(i) == 0):
      #    root = i


    print("raiz do grafo: " + str(root))

    if avaliacao == '1':
        for index, row in df_avaliacao.iterrows():
            res = sim_wup(G, row['c1'], row['c2'],root)
            m.append([row['c1'], row['c2'],row['res_in'], round(res, 4)])

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    else:
        for i in list(G.nodes):
            for j in list(G.nodes):
                res = sim_wup(G, i, j,root)
                m.append([i, j, '',round(res, 4)])

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    base = str(base).replace('.graph', '')
    m.to_csv('./data_out/similaridade_' + str(avaliacao_nome) + '_02_sim_wup.csv', index=False, sep='|',decimal='.')
    print('Lista de resultados: ' + './data_out/similaridade_' + str(avaliacao_nome) + '_02_sim_wup.csv')

    return(m)

###################################################################
# Medida de similaridade Sim_lch

def sim_lch(H, G, i, j):
    # medindo o menor caminho do grafo nao direcionado
    #G_undirected = G.to_undirected()

    #shortest_path = shortest_path_length(G_undirected, i, j)
    shortest_path=sim_spath(H, i, j)
    #print('shortest_path:'+str(shortest_path))
    #print('*********************************************')
    #print('i'+str(i))
    #print('j'+str(j))

    # calcula profundidade do grafo
    Depth_ontology = nx.dag_longest_path_length(G)
    #print('Depth_ontology: '+str(Depth_ontology))
    # formula:
    Qlch = shortest_path / (2 * Depth_ontology)
    #print('Quociente lch: '+str(Qlch))
    if(i == j):
        sim_lch = 1.0
    else:
        sim_lch = -math.log10(Qlch)
    #print('lch: '+str(sim_lch))
    #print('---------------')
    if i == j:
        sim_lch = 1.0

    #print('sim_lch'+str(sim_lch))

    return(sim_lch)

def matriz_sim_lch(H,G,base,avaliacao,df_avaliacao,avaliacao_nome):
    m = []
    if avaliacao == '1':
        for index, row in df_avaliacao.iterrows():
            res = sim_lch(H, G, row['c1'], row['c2'])
            m.append([row['c1'], row['c2'],row['res_in'], round(res, 4)])

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    else:
        u=0
        for i in list(G.nodes):
            for j in list(G.nodes):
                res = sim_lch(H, G, i, j)
                m.append([i, j, '',round(res, 4)])
                u=u+1
                print(u)

        m = pd.DataFrame(m)
        m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    base = str(base).replace('.graph', '')
    m.to_csv('./data_out/similaridade_' + str(avaliacao_nome) + '_03_sim_lch.csv', index=False, sep='|',decimal='.')
    print('Lista de resultados: ' + './data_out/similaridade_' + str(avaliacao_nome) + '_03_sim_lch.csv')

    return(m)

###################################################################
# Medida de information_content by Sanchez

def information_content(G, node):
    # calcula information content de um nó

    #print('++++++++++++++++++++++++'+str(node))
    descendants = nx.descendants(G, node)

    descendants_leaves = []
    for x in descendants:
        if (G.in_degree(x) != 0 and G.out_degree(x) == 0):
            descendants_leaves.append(x)

    num_descendants_leaves = len(descendants_leaves)
    #print('num_descendants_leaves:'+str(num_descendants_leaves))

    if (G.in_degree(node) == 0 and G.out_degree(node) != 0):
        num_subsumers = 1
    else:
        subsumers = nx.ancestors(G, node)
        num_subsumers = len(subsumers)
    #print('num_subsumers:' + str(num_subsumers))

    leaf_nodes=[]
    for nodes in G.nodes():
        if G.in_degree(nodes) != 0 and G.out_degree(nodes) == 0:
            leaf_nodes.append(nodes)

    max_leaves = len(leaf_nodes)
    #print('max_leaves:' + str(max_leaves))

    calc = (num_descendants_leaves / num_subsumers + 1) / (max_leaves + 1)
    #print('calc:' +str(node)+'|'+ str(calc))

    ic = -1*math.log10(calc)
    #print('ic:' +str(node)+'|'+ str(ic))

    #print(' ')

    return ic

###################################################################
# Medida de similaridade de lin

def sim_lin(G, i, j , lcs):
    if i == j:
        sim_lin = 1.0
        return sim_lin

    #print('i:'+str(type(i)))
    #print('j:'+str(type(j)))
    #print('lcs:'+str(type(lcs)))

    #print(str(i)+' | '+str(j)+' | '+str(lcs))

    ic_i = information_content(G, i)
    ic_j = information_content(G, j)
    ic_lcs = information_content(G, lcs)

    #time.sleep(1)
    #print('')
    #print('ic_i: ' + str(ic_i))
    #print('ic_j: ' + str(ic_j))
    #print('lcs : ' + str(ic_lcs))

    try:
        sim_lin = (2 * ic_lcs) / (ic_i + ic_j)
    except ZeroDivisionError:
        sim_lin = 1

    return sim_lin

#Matriz de similaridade Lin
def matriz_sim_lin(G,  base, avaliacao, df_avaliacao,avaliacao_nome):
    m = []
    #s = []

    nos=G.nodes()

    #print(avaliacao)


    if avaliacao == '1':

        #print(df_avaliacao[['c1','c2']])
        u=0
        for index, row in df_avaliacao.iterrows():
            lcs = nx.lowest_common_ancestor(G, row['c1'], row['c2'])

            #print('*****************************************************')
            #print('node_i:'+str(i))
            #print('node_j:'+str(j))
            #print('node_lcs:' + str(lcs))
            #print(' ')

            res = sim_lin(G, row['c1'], row['c2'], lcs)

            #print('sim_lin<<<<<<<<<<<<<<<<<' + str(res))

            m.append([row['c1'], row['c2'], '',round(res, 4)])

            u = u + 1
            # print('#:' + str(w) + str('|') + '#:' + str(u))
            print(u)
        #w = w + 1

        #m.append([row['c1'], row['c2'],row['res_in'], round(res, 4)])
        #print(row['c1'], row['c2'],row['res_in'],res)


    else:


        lista = []
        for x in nos:
            lista.append(x)

        w = 0
        for i in lista:
            u = 0
            for j in lista:
                lcs = nx.lowest_common_ancestor(G, i, j)
                # print('*****************************************************')
                # print('node_i:'+str(i))
                # print('node_j:'+str(j))
                # print('node_lcs:' + str(lcs))
                # print(' ')

                res = sim_lin(G, i, j, lcs)

                # print('sim_lin<<<<<<<<<<<<<<<<<' + str(res))

                #s.append([i, j, res])
                m.append([i, j, '',round(res, 4)])

                u = u + 1
                # print('#:' + str(w) + str('|') + '#:' + str(u))
                print(u)
            w = w + 1
            # time.sleep(1)

    m = pd.DataFrame(m)

    #print(m)

    #m = m.pivot_table(2, 0, 1, fill_value=0)
    m = pd.DataFrame(m)
    m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    base = str(base).replace('.graph', '')
    m.to_csv('./data_out/similaridade_' + str(avaliacao_nome) + '_04_sim_IC_lin.csv', index=False, sep='|',decimal='.')
    print('Lista de resultados: ' + './data_out/similaridade_' + str(avaliacao_nome) + '_04_sim_IC_lin.csv')

    return(res)


###################################################################
# Medida de similaridade de resnik

# Medida de Resnik
def sim_resnik(G, i, j):
    if i == j:
        sim_res = 1.0
        return sim_res

    lcs = nx.lowest_common_ancestor(G, i, j)
    print('lcs: '+str(lcs))
    sim_res = information_content(G, lcs)
    print('sim_res: '+str(sim_res))

    return sim_res

#Matriz de similaridade Lin
def matriz_sim_resnik(G, base,avaliacao,df_avaliacao,avaliacao_nome):
    m = []
    s = []
    nos = G.nodes()

    if avaliacao == '1':

        #print(df_avaliacao[['c1','c2']])
        u=0

        for index, row in df_avaliacao.iterrows():
            print(u)
            print('Row: '+str(row))
            res = sim_resnik(G, row['c1'], row['c2'])
            m.append([row['c1'], row['c2'],row['res_in'], round(res, 4)])
            print(row['c1'], row['c2'],row['res_in'],round(res, 4))
            u=u+1
            print('***************************************')

    else:
        for i in nos:
            for j in nos:
                res = sim_resnik(G, i, j)

                # print(i, j, res)

                m.append([i, j, round(res, 4)])

    m = pd.DataFrame(m)
    #m = m.pivot_table(2, 0, 1, fill_value=0)
    m = pd.DataFrame(m)
    m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    base = str(base).replace('.graph', '')
    m.to_csv('./data_out/similaridade_' + str(avaliacao_nome) + '_05_sim_IC_resnik.csv', index=False, sep='|',decimal='.')
    print('Lista de resultados: ' + './data_out/similaridade_' + str(avaliacao_nome) + '_05_sim_IC_resnik.csv')

    return(s)


###################################################################
# Medida de similaridade de Jiang and Conrath

# Medida de JCN
def sim_jcn(G, i, j):
    if i == j:
        sim_jcn = 1.0
        return sim_jcn

    lcs = nx.lowest_common_ancestor(G, i, j)

    #print('*****************************************************')
    #print('node_i:' + str(i))
    #print('node_j:' + str(j))
    #print('node_lcs:' + str(lcs))
    #print(' ')

    #print('**********')
    ic_i = information_content(G, i)
    #print(i)
    #print(ic_i)

    #print('**********')
    ic_j = information_content(G, j)
    #print(j)
    #print(ic_j)

    #print('**********')
    ic_lcs = information_content(G, lcs)
    #print(lcs)
    #print(ic_lcs)

    try:
        sim_jcn = 1 / (ic_i + ic_j-2 * ic_lcs)
    except ZeroDivisionError:
        sim_jcn = 1

    return sim_jcn


#Matriz de similaridade jcn
def matriz_sim_jcn(G, base, avaliacao, df_avaliacao,avaliacao_nome):
    m = []
    s = []
    nos = G.nodes()
    if avaliacao == '1':

        print(df_avaliacao[['c1','c2']])
        u=0
        for index, row in df_avaliacao.iterrows():
            print(u)
            res = sim_jcn(G, row['c1'], row['c2'])
            m.append([row['c1'], row['c2'],row['res_in'], round(res, 4)])
            print(row['c1'], row['c2'],row['res_in'],res)
            u=u+1


    else:
        for i in nos:
            for j in nos:

                res = sim_jcn(G, i, j)

                #print('*******************************')
                #print(i, j, res)
                #print('*******************************')

                m.append([i, j, round(res, 4)])

    m = pd.DataFrame(m)
    #m = m.pivot_table(2, 0, 1, fill_value=0)
    m = pd.DataFrame(m)
    m.columns = ['c1', 'c2', 'res_in', 'res_calc']

    base = str(base).replace('.graph', '')
    m.to_csv('./data_out/similaridade_' + str(avaliacao_nome) + '_06_sim_IC_jcn.csv', index=False, sep='|',decimal='.')
    print('Lista de resultados: ' + './data_out/similaridade_' + str(avaliacao_nome) + '_06_sim_jcn.csv')

    return(s)
