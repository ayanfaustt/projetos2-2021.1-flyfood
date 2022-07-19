#   Aluno: Ayan Faustt
#   Professor: Cleviton Vinicius Fonseca Monteiro
#   Disciplina: Projento Interdisciplinar para Sistemas de Informação II

from random import choice, random
from math import ceil

def formataFilho(filhos):
    filhos_formatados = list()
    aux = ''

    for i in range(len(filhos)):
        for j in range(len(filhos[i])):
            aux += filhos[i][j]
        filhos_formatados.append(aux)
        aux = ''
    
    return filhos_formatados


def mutacao(filhos):
    taxa_mutacao = 0.1

    for i in range(len(filhos)):
        for j  in filhos[i]:
            resultado = random()
            if resultado <= taxa_mutacao:
                filhos[i][-1], filhos[i][-2] = filhos[i][-2], filhos[i][-1]
                break

    return formataFilho(filhos) 



def validaFilho(pais, filho,):
    pai = pais[:]
    filho_lista = [j for j in filho] 
    check = True
    filho_auxiliar = list()
    for i in range(len(filho_lista)):
        if not(filho_auxiliar):
            filho_auxiliar.append(filho_lista[i])
        else:
            if filho_lista[i] in filho_auxiliar:
                check = False
                for k in pais:
                    if not (k in filho_auxiliar):
                        filho_auxiliar.append(k)
                        pais.pop(pai.index(k))
                    else:
                        continue
            else:
                filho_auxiliar.append(filho_lista[i])
                continue

    if check:
        return filho_lista
    else:

        return filho_auxiliar

def crossover(casais):
    filhos = list()
    divisor = 0

    if len(casais[0][1]) % 2 == 0:
        divisor = int(len(casais[0][1]) / 2)
    else:
        divisor = int(ceil(len(casais[0][1]) / 2))

    for i in range(len(casais)):
            part1 = casais[i][0][:divisor]  
            part2 = casais[i][1][divisor:]
            filho1 = part1+part2
            filhos.append(validaFilho(filho1, casais[i][0]))

            part1 = casais[i][1][:divisor]  
            part2 = casais[i][0][divisor:]
            filho2 = part1+part2
            filhos.append(validaFilho(filho2, casais[i][1]))


    return filhos
               
def selecao(populacaoFitness):
    populacao = sorted(populacaoFitness, key=populacaoFitness.get, reverse = True)
    casais = list()
    aux = list()

    for i in populacao:
        if not(len(aux)):
            aux.append(i)
        else: 
            if len(aux) % 2 == 0:
                casais.append(aux) 
                aux = list()  
                aux.append(i) 
            else:
                aux.append(i)
            if i == populacao[-1]:
                casais.append(aux)
    
    return casais
    



def calculaMelhor(populacao, coordenadas, melhor =''):
     somador = 0 
     individuos = populacao
     fitness = dict()
     
     aux = 0
     for trajeto in range(len(individuos)):
        somador = 0
        for cidade in range(len(populacao[trajeto])):
            if individuos[trajeto][cidade] == individuos[trajeto][-1]:
                dist = abs(coordenadas[individuos[trajeto][cidade]][0]-coordenadas[individuos[trajeto][0]][0]) + abs(coordenadas[individuos[trajeto][cidade]][1]-coordenadas[individuos[trajeto][0]][1])
                somador += dist               
            else:
                dist = abs(coordenadas[individuos[trajeto][cidade]][0]-coordenadas[individuos[trajeto][cidade+1]][0]) + abs(coordenadas[individuos[trajeto][cidade]][1]-coordenadas[individuos[trajeto][cidade+1]][1])
                somador += dist
        
        aux2 = 1/somador
        fitness[individuos[trajeto]] = aux2
        if aux == 0:
            aux = aux2
            melhor = individuos[trajeto],aux2
        if aux <= aux2:
            melhor = individuos[trajeto],aux2


     return [fitness,(melhor)]        


def gerador_inicial(pontos):
    cidades = pontos[:]
    quantidade_cidades = len(cidades)
    populacao_inicial = list()
    individuo = 'R'
    cidades.pop(cidades.index('R'))
    count = 0
    delimitador = 8
    if len(cidades) <= 5:
         delimitador = 4
    while count < delimitador:

        while True:
            
            if not(len(cidades)):
                cidades = pontos[:]
            escolhido = choice(cidades)
            if not (escolhido in individuo):
                individuo+=escolhido
                cidades.pop(cidades.index(escolhido))


            
            if len(individuo) == quantidade_cidades:
                if not (individuo in populacao_inicial):
                    populacao_inicial.append(individuo)
                    individuo = 'R'
                    cidades = pontos[:]
                    cidades.pop(cidades.index('R'))
                    break
                else:
                    individuo = 'R'
                    continue
        count +=1
    
    return populacao_inicial


def map(arquivos):
    matriz = list()
    pontos = list()
    pontos_coordenados = dict()
    generator = arquivos[0:1]
    aux = 0
    for i in range(len(generator)):
        linha_coluna = list()
        for j in range(len(generator[i])):
            if generator[i][j] == ' ' or generator[i][j] == "\n":
                continue
            else:
                if generator[i][j] == generator[i][-2]:
                    continue
                if generator[i][j+1] == ' ' or generator[i][j+1] == '\n':
                    aux = generator[i][j]
                    linha_coluna.append(int(aux))
                    continue
                else:
                    aux = generator[i][j] + generator[i][j+1]
                    linha_coluna.append(int(aux))
    arquivos.pop(0)
    
    for linha in range(linha_coluna[0]):
        aux = list()
        for caractere in arquivos[linha]:
            if caractere == ' ' or caractere == "\n":
                continue
            else:
                aux.append(caractere)
        matriz.append(aux)
    
    for x in range(len(matriz)):
        for y in range(len(matriz[x])):
            if matriz[x][y] != '0':
                pontos.append(matriz[x][y])
                pontos_coordenados[matriz[x][y]] = [x,y]
            else:
                continue
    return [pontos, pontos_coordenados]



arq = open('ARQUIVO.txt')
dados = arq.readlines()
pontos_coordenadas= map(dados)


populacao_inicial = gerador_inicial(pontos_coordenadas[0])

populacaoFitness = calculaMelhor(populacao_inicial, pontos_coordenadas[1])





coordenadas = pontos_coordenadas[1]
dados_populacionais = ''
melhor = populacaoFitness[1]

counter = 0
while True:
    if not(dados_populacionais): 

        selecionados = selecao(populacaoFitness[0])

        cruzados = crossover(selecionados)

        individuos = mutacao(cruzados)


        fitness = calculaMelhor(individuos, coordenadas,melhor)
        dados_populacionais = fitness
        if fitness[1][1] > melhor[1]:
            melhor = fitness[1]

         
    else:  
        selecionados = selecao(dados_populacionais[0])

        cruzados = crossover(selecionados)

        individuos = mutacao(cruzados)

        fitness = calculaMelhor(individuos, coordenadas, melhor)
        dados_populacionais = fitness
        if fitness[1][1] > melhor[1]:
            melhor = fitness[1]


    counter +=1
    if counter <= 100:
        continue
    else:
        break


dest_final = ''
for i in melhor[0]:
    if i == 'R':
        continue
    else:
        dest_final += i+' '

print(dest_final)