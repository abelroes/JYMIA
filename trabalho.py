import pandas as pd
import math
import numpy as np
from sklearn.model_selection import KFold

#def imprimi_arvore(no):
    

def entropia(ppos, pneg):
    #se as distribuicoes de positivo e negativo forem iguais, a entropia e 1 (indecisao total)
    if ppos == pneg:
        return 1
    #se todas as observacoes forem positivas (ppos == 1) ou negativas (ppos == 1), a entropia e 0
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
    
    # dicionario com as classes e seus ganhos de informacao
    ganhos = {}
    # para cada coluna do dataset, calcular o ganho de informacao
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
        
        # tamanho do conjunto desse no
        self.tamanho_conjunto = len(df)
        #print("Tamanho do conjunto:", self.tamanho_conjunto)
        
        # proporcao de observacoes positivas
        self.ppos_conjunto = len(df[df[coluna_resposta] == resp_pos])/self.tamanho_conjunto
        #print("ppos_conjunto:", self.ppos_conjunto)
        
        # proporcao de observacoes negativas
        self.pneg_conjunto = len(df[df[coluna_resposta] == resp_neg])/self.tamanho_conjunto      
        #print("pneg_conjunto", self.pneg_conjunto)
        
        
        # se todas as observacoes forem positivas, o no e uma folha de resposta positiva, e a expansao para
        if self.ppos_conjunto == 1:
            self.valor = resp_pos
            print("\t", self.valor)
        # se todas as observacoes forem negativas, o no e uma folha de resposta negativa, e a expansao para
        elif self.pneg_conjunto == 1:
            self.valor = resp_neg
            print("\t", self.valor)
        # se nao houverem mais colunas, o no e uma folha cujo valor e a resposta mais comum do conjunto pai
        elif len(df.columns) == 0:
            self.valor = resp_pos if self.ppos_conjunto > self.pneg_conjunto else resp_neg
        
        # senao, expandir a arvore
        else:
            
            # Atributo que melhor classifica o conjunto (df)
            self.valor = get_melhor_ganho(df, entropia(self.ppos_conjunto, self.pneg_conjunto),
                                          self.tamanho_conjunto)
            print("\nAtributo:", self.valor)
            # instanciar uma lista que contera os filhos do no atual
            self.filhos = []
            self.classes = []
            
            # Para cada classe do melhor atributo crie um no filho que receba as observacoes do atributo = classe:
            for classe in list(set(df[self.valor])):
                print("\tClasse:", classe)
                self.filhos.append(No(df[df[self.valor] == classe]))
                self.classes.append(classe)


def discretizar(df):
    
    #ordenar os dados
    df_ordenado = df.sort_values(by="age")
    
    i = 0
    while i < 32560:
        
        
        
        
        i += 592
    print(i)
    #print(coluna_ordenada.value_counts().sort_values())


# Cria um DF para poder enviar ao No e criar a arvore
# "cat.age","type.employer","education","marital","occupation","relationship","race","sex","country","cat.capital.gain","cat.capital.loss","cat.hours.per.week","income"


def criaDF(folds):
    age = []
    employer = []
    education = []
    marital = []
    occupation = []
    relationship = []
    race = []
    sex = []
    country = []
    gain = []
    loss = []
    hoursperweek = []
    income = []
    for X in folds:
        
        age.append(linhas[X][0])
        employer.append(linhas[X][1])
        education.append(linhas[X][2])
        marital.append(linhas[X][3])
        occupation.append(linhas[X][4])
        relationship.append(linhas[X][5])
        race.append(linhas[X][6])
        sex.append(linhas[X][7])
        country.append(linhas[X][8])
        gain.append(linhas[X][9])
        loss.append(linhas[X][10])
        hoursperweek.append(linhas[X][11])
        income.append(linhas[X][12])

    raw_data = {}
    raw_data['cat.age'] = age
    raw_data['type.employer'] = employer
    raw_data['education'] = education
    raw_data['marital'] = marital
    raw_data['occupation'] = occupation
    raw_data['relationship'] = relationship
    raw_data['race'] = race
    raw_data['sex'] = sex
    raw_data['country'] = country
    raw_data['cat.capital.gain'] = gain
    raw_data['cat.capital.loss'] = loss
    raw_data['cat.hours.per.week'] = hoursperweek
    raw_data['income'] = income

    trainDf = pd.DataFrame(raw_data, columns = ["cat.age","type.employer","education","marital","occupation","relationship",
                                                "race","sex","country","cat.capital.gain","cat.capital.loss","cat.hours.per.week","income"])
    return trainDf

def classificaNaArvore(testDf, raiz, exemploValidacao):
    noAtual = raiz
    while noAtual:
    #Acha atributo
        atributo = testDf[noAtual.valor][exemploValidacao]
        #Acha filho
        proxFilho = 0
        for i in range (0, len(noAtual.filhos)):
            if(noAtual.classes[i] == atributo):
                proxFilho = i
                break
        if any(resp in noAtual.filhos[proxFilho].valor for resp in (resp_pos, resp_neg)):
            return noAtual.filhos[proxFilho].valor
        else:
            noAtual = noAtual.filhos[proxFilho]

    
    
############ MAIN

print("Passo1:")
df = pd.read_csv("adult2.csv", delimiter=",")

df = df[["cat.age","type.employer","education","marital","occupation","relationship",
         "race","sex","country","cat.capital.gain","cat.capital.loss","cat.hours.per.week","income"]]
############K-FOLD###################

linhas = []
acertou = 0
errou = 0
lines = 0 
while lines < len(df):
    linha = []
    for columns in df:
        linha.append(df[columns][lines])
    linhas.append(linha)
    lines = lines + 1 

kf = KFold(n_splits=10)
for train, test in kf.split(linhas):
    # Como quebramos o df em um array para fazermos os k-folds, fazemos o processo inverso agr para criando um df a partir de um array
    trainDf = criaDF(train)
    testDf = criaDF(test)
    print "Dados de Treinamento: \n", trainDf
    # print "Dados de Validacao: \n", testDf
    coluna_resposta = "income"
    resp_pos = " <=50K"
    resp_neg = " >50K"
    # Constroi a arvore
    raiz = No(trainDf)

    for exemploValidacao in range(0, len(testDf)):
        classificacaoNaArvore = classificaNaArvore(testDf, raiz, exemploValidacao)
        if(classificacaoNaArvore == testDf[coluna_resposta][exemploValidacao]):
            acertou += 1
            print "************************************"
            print "Acertou o//"
            print "************************************"
        else:
            errou += 1
            print "************************************"
            print "Errou =("         
            print "************************************"
print "Total de acertos: ", acertou
print "Total de erros: ", errou

n = acertou + errou
mediaErros = float(errou) / float(n)
print "Media de erros no modelo: ", mediaErros

SE = math.sqrt((mediaErros*(1-mediaErros))/n)
print "SE: ", SE

intervaloConfiancaInferior = (mediaErros - (1.96*SE))
print "Intervalo de confianca Inferior: ", intervaloConfiancaInferior
intervaloConfiancaSuperior = (mediaErros + (1.96*SE))
print "Intervalo de confianca Superior: ",intervaloConfiancaSuperior

    

#######################################



print("Passo 2:")
header = ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"]
df = pd.read_csv("adult.csv", delimiter=",")
df.columns = header

coluna_resposta = "income"
resp_pos = " <=50K"
resp_neg = " >50K"

# Eliminar nulls (nao encontrei nenhum??)

discretizar(df[["age", "income"]])

for i in range(1,32560):
    if 32560%i == 0 and i >= 500 and i <= 1001:
        print(i)
        
# dividir 32560 por 592, gerara 55 reparticoes
#discretizar(df, "fnlwgt")
#discretizar(df, "education-num")
#discretizar(df, "capital-gain")
#discretizar(df, "capital-loss")
#discretizar(df, "hours-per-week")


