import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.transforms import Bbox
from graphviz import Digraph
import os
import shutil

# Plot de grafo
def draw_Digraph_old(nos,arestas,base):

    g = Digraph('G', filename='./data_out/'+str(base)+'_out_plot',format='pdf')
    g.attr(rankdir='RL', size='18,4', pad='1')
   # g.attr(rankdir='LR', size='8,4', nodesep='0.5', ranksep='1.25', pad='.5')

    #g.attr('node', shape='box', style='filled', fillcolor = 'lightgray')
    g.attr('node', shape='box', style='rounded,filled', fillcolor='lightgray')

    for i in nos:
        g.node(i)

    for i in arestas:
        #print(i[0],i[1],i[2])
        g.edge(i[1],i[0], label=str(i[2]))

    g.render()

    print('Plot - ok!')

    print('Arquivo disponível no diretório de saída')
    return (g)


def draw_Digraph(G, base):
    nome_arq = str(base).replace('.graph', '')

    drawing = Digraph('G', filename='./data_out/' + nome_arq + '_plot', format='pdf')
    drawing.attr(rankdir='RL', size='18,4', pad='1')
    # g.attr(rankdir='LR', size='8,4', nodesep='0.5', ranksep='1.25', pad='.5')

    # g.attr('node', shape='box', style='filled', fillcolor = 'lightgray')
    drawing.attr('node', shape='box', style='rounded,filled', fillcolor='lightgray')

    for i in G.nodes():
        drawing.node(i)

    for i in G.edges():
        # print(i[0],i[1],i[2])
        drawing.edge(i[1], i[0], label='is-a')

    drawing.render()

    print('Plot - ok!')

    print('Arquivo disponível no diretório de saída')
    # return (drawing)