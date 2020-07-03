import paramiko
import os.path
import time
import sys
import re

#Solicitando e validando o arquivo com om as credenciais
user_file=input('A seguir insira o caminho do arquivo que possui as credenciais de acesso. Ex: C:\\user.txt \n'
                    'Insira o caminho:')

if os.path.isfile(user_file) == True:
    print(f'{user_file} Este é um caminho valido para um arquivo')
else:
    print(f'{user_file }Este NÃO é um caminho valido para um arquivo')

#Solicitando e validando o arquivo com os comandos
cmd_file=input('A seguir insira o caminho do arquivo que possui os comandos a serem executados. Ex: C:\\commands.txt \n'
                    'Insira o caminho:')

if os.path.isfile(cmd_file) == True:
    print(f'{cmd_file} Este é um caminho valido para um arquivo')
else:
    print(f'{cmd_file}Este NÃO é um caminho valido para um arquivo')

def ssh_connection(ips):

    try:
        #Definindo os parametros ssh
        select_user_file=open(user_file, 'r')

        #Colocando o cursor na posição 0
        select_user_file.seek(0)

        #Lendo o nome do usuario
        username=select_user_file.readlines()[0].split(',')[0].rstrip('\n')

        #Voltando o cursor para posição
        select_user_file.seek(0)

        #Lendo a senha
        password=select_user_file.readlines()[0].split(',')[1].split('\n')

        #Logando no dispositivo
        session = paramiko.SSHClient()

        #Por razões de teste, iremos aceitar as chaves de hosts desconhecidos
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #Conectando utilizando as variaveis username e password
        session.connect(ips.rstrip("\n"), username=username, password=password)

        #Comecando uma sessao interativa com o roteador
        connection = session.invoke_shell()

        #Desabilitando a paginação
        connection.send('ena\n')
        connection.send('terminal length 0')
        time.sleep(1)

        #Entrando no modo de configuração global
        connection.send('\n')
        connection.send('conf t\n')
        time.sleep(1)

        #Abrindo o arquivo com os comandos para leitura
        selected_cmd_file=open(cmd_file, 'r')

        #Colocando o cursor na posicao 0
        selected_cmd_file.seek(0)

        #Criando um for para executar cada comando dentro do arquivo
        for each_line in selected_cmd_file:
            connection.send=(each_line + '\n')
            time.sleep(2)

        #fechando os arquivos do usuario e dos comandos
        selected_cmd_file.close()
        select_user_file.close()

        router_output=connetion.recv(65535)

        if re.search(b"%Invalid Output", router_output):
            print(f'* Existe pelo menos um erro de sintaxe. Erro identificado ao configurar {ips}')

        else:
            print(f'Configuração aplicada com sucesso no dispositivo {ips}')

    except paramiko.AuthenticationException:
        print(
            "Usuário ou senha invalídos :( \n Por favor, verifique o arquivo que contem o usuário e a senha ou o dispositivo que esta tentando acessar.")
        print("Programa sendo encerrado")
