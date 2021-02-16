import os
import csv
import subprocess as sp


# Calcula porcentagem de acertos
def calcula_percentual(valores):
    lista_percentual = []
    intervalo = len(valores) - 1
    for i in range(0, intervalo, 2):
        acertos = float(valores[i])
        lista_percentual.append(valores[i])
        questoes = float(valores[i + 1])
        lista_percentual.append(valores[i + 1])
        calculo = (acertos / questoes) * 100
        percentual = round(calculo, 2)
        lista_percentual.append(percentual)
    return lista_percentual


# Calcula total de acertos e total de questões
def total_acertos_questoes(valores):
    lista_totais = []
    intervalo = len(valores) - 3
    soma_acertos = 0
    soma_questoes = 0
    for i in range(0, intervalo, 4):
        soma_acertos = soma_acertos + (valores[i] + valores[i + 2])
        soma_questoes = soma_questoes + (valores[i + 1] + valores[i + 3])
    lista_totais.append(soma_acertos)
    lista_totais.append(soma_questoes)
    return lista_totais


def linha_resultado(valores, q):
    intervalo = len(valores) - 2

    if q == '1':
        linha1 = ''
        j = 1
        for i in range(0, intervalo, 3):
            linha1 = (linha1 +
                      'Simulado ' + str(j) +
                      ' - Total de Acertos: ' + str(valores[i]) +
                      '; Total de Questões: ' + str(valores[i + 1]) +
                      '; Porcentagem de Acerto: ' + str(valores[i + 2]) +
                      '%\n')
            j += 1
        return linha1
    elif q == '2a':
        linha2a = ('Total de Questões: ' + str(valores[1]) + '\n' +
                   'Total de Acertos: ' + str(valores[0]) + '\n')
        return linha2a

    elif q == '2b':
        linha2b = ('Porcentagem de Acertos: ' + str(valores[2]) + '%\n')
        return linha2b


def percorre_dicionario(quest):
    if quest == '1':
        with open(caminho_resultado + resultado, 'a+') as txt:
            txt.write('Porcentagem de acertos por simulado realizado por matéria:\n')
            for chave in dicionario:
                txt.write(chave + ':\n')
                porcentagem_acertos = calcula_percentual(dicionario[chave])
                linha1 = linha_resultado(porcentagem_acertos, QUEST1)
                txt.write(linha1)
                txt.write('\n')
    elif quest == '2':
        with open(caminho_resultado + resultado, 'a+') as txt:
            txt.write('Total de acertos, questões e porcentagem por matéria:\n')
            for chave in dicionario:
                txt.write(chave + ':\n')
                total_materia = total_acertos_questoes(dicionario[chave])
                porcentagem_acertos = calcula_percentual(total_materia)
                linha2a = linha_resultado(total_materia, QUEST2A)
                linha2b = linha_resultado(porcentagem_acertos, QUEST2B)
                txt.write(linha2a)
                txt.write(linha2b)
                txt.write('\n')
    else:
        with open(caminho_resultado + resultado, 'a+') as txt:
            txt.write('Total geral de acertos, questões e porcentagem:\n')
            lista_total = [0, 0]
            for chave in dicionario:
                lista_parcial = total_acertos_questoes(dicionario[chave])
                lista_total[0] = lista_total[0] + lista_parcial[0]
                lista_total[1] = lista_total[1] + lista_parcial[1]
            porcentagem_acertos = calcula_percentual(lista_total)
            linha3a = linha_resultado(lista_total, QUEST2A)
            linha3b = linha_resultado(porcentagem_acertos, QUEST2B)
            txt.write(linha3a)
            txt.write(linha3b)
            txt.write('\n')


def eh_numero(numero):
    try:
        int(numero)
        return True
    except ValueError:
        return False


# Programa principal
caminho = input('Informe a raiz dos diretórios de simulados com / no final do nome: ')  # /home/luan/Simulados/'
while caminho[-1] != '/':
    caminho = input('Caminho informado sem o / no final. Favor informar caminho com / no fim: ')

arquivo = input('Informar nome do arquivo txt com extensão: ')
while '.txt' not in arquivo:
    arquivo = input('Extensão não informada. Informar nome do arquivo txt com extensão: ')

pastas = os.listdir(caminho)
caminho_resultado = caminho
resultado = 'Resultado.txt'
try:
    os.remove(caminho_resultado + 'Resultado.txt')
except FileNotFoundError:
    pass
dicionario = {}
QUEST1 = '1'
QUEST2 = '2'
QUEST2A = '2a'
QUEST2B = '2b'
QUEST3 = '3'

for pasta in pastas:
    if os.path.isdir(os.path.join(caminho, pasta)):
        dicionario[pasta] = ""
        arquivo_final = caminho + pasta + '/' + arquivo

        try:
            with open(arquivo_final, newline='') as csvfile:
                lista = []
                simulados = csv.reader(csvfile, delimiter=',')

                for linha in simulados:
                    lista.append(int(linha[0]))
                    lista.append(int(linha[1]))

            dicionario[pasta] = lista
        except FileNotFoundError:
            print('Arquivo com nome inválido ou não existe. Script encerrado')
            print(arquivo_final)
            exit(1)

print('1) Obter o total de acertos, questões e a porcentagem de acerto para cada simulado de cada matéria')
print('2) Obter para cada matéria o total de acertos, questões e porcentagem de acertos')
print('3) Obter o total geral de acertos, questẽos e porcentagem de acertos')
print('4) Todas as opções acima\n')

escolha = input('Ecolha qual cálculo deseja obter (Digite o número da opção): ')
while not eh_numero(escolha):
    escolha = input('Entrada inválida. Digite um número de 1 a 4: ')

if escolha == '1':
    percorre_dicionario(QUEST1)
elif escolha == '2':
    percorre_dicionario(QUEST2)
elif escolha == '3':
    percorre_dicionario(QUEST3)
else:
    percorre_dicionario(QUEST1)
    percorre_dicionario(QUEST2)
    percorre_dicionario(QUEST3)

print('Resultado gerado em ' + caminho_resultado + ' como ' + resultado)
program = '/usr/bin/gedit'
file = caminho_resultado + resultado
sp.Popen([program, file])