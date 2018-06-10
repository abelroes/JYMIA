import pandas as pd
import math

#def imprimi_arvore(no):
    

def entropia(ppos, pneg):
    #se as distribuições de positivo e negativo forem iguais, a entropia é 1 (indecisão total)
    if ppos == pneg:
        return 1
    #se todas as observações forem positivas (ppos == 1) ou negativas (ppos == 1), a entropia é 0
    elif ppos == 1 or pneg == 1:
        return 0
    else:
        return -(ppos*math.log(ppos, 2)) - (pneg*math.log(pneg, 2)) 

def ganho_atributo(df, coluna):
    
    tamanho_conjunto = len(df)
    
    ppos_conjunto = len(df[df[coluna_resposta] == resp_pos])/tamanho_conjunto
    pneg_conjunto = len(df[df[coluna_resposta] == resp_neg])/tamanho_conjunto      

    entropia_conjunto = entropia(ppos_conjunto, pneg_conjunto)
    
    ganho = entropia_conjunto
    
    for classe in list(set(df[coluna])):
        dist_classe = len(df[ df[coluna] == classe])
        ppos = len(df[ (df[coluna] == classe) & (df[coluna_resposta] == resp_pos)])/ dist_classe
        pneg = len(df[ (df[coluna] == classe) & (df[coluna_resposta] == resp_neg)]) / dist_classe
                
        ganho -= ((dist_classe/tamanho_conjunto) * entropia(ppos, pneg))
        
    return ganho

def get_melhor_ganho(df, entropia_conjunto, tamanho_conjunto):
    
    # dicionário com as classes e seus ganhos de informação
    ganhos = {}
    
    # para cada coluna do dataset, calcular o ganho de informação
    for coluna in df.columns:

        ganho = entropia_conjunto          
        
        if coluna != coluna_resposta:
            # para cada uma das classes da coluna 
            for classe in list(set(df[coluna])):
                dist_classe = len(df[ df[coluna] == classe])
                ppos = len(df[ (df[coluna] == classe) & (df[coluna_resposta] == resp_pos)])/ dist_classe
                pneg = len(df[ (df[coluna] == classe) & (df[coluna_resposta] == resp_neg)]) / dist_classe
                        
                ganho -= ((dist_classe/tamanho_conjunto) * entropia(ppos, pneg))
                
            ganhos[coluna] = ganho

    return max(ganhos, key=ganhos.get)


class No():
    
    def __init__(self, df):
        
        # tamanho do conjunto desse nó
        self.tamanho_conjunto = len(df)
        #print("Tamanho do conjunto:", self.tamanho_conjunto)
        
        # proporção de observações positivas
        self.ppos_conjunto = len(df[df[coluna_resposta] == resp_pos])/self.tamanho_conjunto
        #print("ppos_conjunto:", self.ppos_conjunto)
        
        # proporção de observações negativas
        self.pneg_conjunto = len(df[df[coluna_resposta] == resp_neg])/self.tamanho_conjunto      
        #print("pneg_conjunto", self.pneg_conjunto)
        
        
        # se todas as observações forem positivas, o nó é uma folha de resposta positiva, e a expansão para
        if self.ppos_conjunto == 1:
            self.valor = resp_pos
            print("\t", self.valor)
        # se todas as observações forem negativas, o nó é uma folha de resposta negativa, e a expansão para
        elif self.pneg_conjunto == 1:
            self.valor = resp_neg
            print("\t", self.valor)
        # se não houverem mais colunas, o nó é uma folha cujo valor é a resposta mais comum do conjunto pai
        elif len(df.columns) == 0:
            self.valor = resp_pos if self.ppos_conjunto > self.pneg_conjunto else resp_neg
        
        # senão, expandir a árvore
        else:
            
            # Atributo que melhor classifica o conjunto (df)
            self.valor = get_melhor_ganho(df, entropia(self.ppos_conjunto, self.pneg_conjunto),
                                          self.tamanho_conjunto)
            print("\nAtributo:", self.valor)
            # instanciar uma lista que conterá os filhos do nó atual
            self.filhos = []
            
            # Para cada classe do melhor atributo crie um nó filho que receba as observações do atributo = classe:
            for classe in list(set(df[self.valor])):
                print("\tClasse:", classe)
                novo_df = df[df[self.valor] == classe]
                del novo_df[self.valor]
                print("\tColunas do df:", novo_df.columns)
                self.filhos.append(No(novo_df))

############ MAIN

print("Passo1:")
df = pd.read_csv(".\PlayTennisDataSet.csv", delimiter=",")
df = df[["Outlook", "Temperature", "Humidity", "Wind", "PlayTennis"]]

coluna_resposta = "PlayTennis"
resp_pos = "Yes"
resp_neg = "No"

# Constrói a árvore
raiz = No(df)

