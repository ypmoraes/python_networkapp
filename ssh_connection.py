import paramiko
import os.path
import time
import sys
import re

#Solicitando e validando o arquivo com om as credenciais
user_file=input('A seguir insira o caminho do arquivo que possui as credenciais de acesso. Ex: C:\\user.txt \n'
                    'Insira o caminho:')

if os.path.isfile(user_file) == True:
    print(f'{user_file} -- Este é um caminho valido para um arquivo')
else:
    print(f'{user_file } -- Este NÃO é um caminho valido para um arquivo')
    sys.exit()

#Solicitando e validando o arquivo com os comandos
cmd_file=input('A seguir insira o caminho do arquivo que possui os comandos a serem executados. Ex: C:\\commands.txt \n'
                    'Insira o caminho:')

if os.path.isfile(cmd_file) == True:
    print(f'{cmd_file} Este é um caminho valido para um arquivo')
else:
    print(f'{cmd_file}Este NÃO é um caminho valido para um arquivo')

def ssh_connection(ips):
    try:
        #Define SSH parameters
        selected_user_file=open(user_file, 'r')

        #Starting from the beginning of the file
        selected_user_file.seek(0)

        #Reading the username from the file
        username = selected_user_file.readlines()[0].split(',')[0].rstrip("\n")

        #Going back to the 0 position
        selected_user_file.seek(0)

        #Reading the password from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")

        #loggin into the device
        session = paramiko.SSHClient()

        #
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #Connect to the device using username and password
        session.connect(ips.rstrip("\n"), username = username, password = password)

        #Inicia a sessao shell
        connection = session.invoke_shell()

        #Desabilitando a paginacao e entrando no modo de configuracao global
        connection.send("ena\n")
        connection.send("terminal length 0\n")
        time.sleep(1)

        connection.send("\n")
        connection.send("conf t\n")
        time.sleep(1)

        #Abrindo e lendo o arquivo de comandos
        selected_cmd_file=open(cmd_file, 'r')

        #Posicionando o cursor na posicao 0
        selected_cmd_file.seek(0)

        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)

        selected_cmd_file.close()

        selected_user_file.close()

        #Checando a saida do comando
        router_output = connection.recv(65535)

        if re.search(b"% Invalid input", router_output):
            print(f"Existe pelo menos um erro de sintaxe. Erro identificado ao configurar {ips}")

        else:
            print(f'Configuração aplicada com sucesso no dispositivo {ips}')

        #Test for reading command output
        #print(str(router_output) + "\n")

    except paramiko.AuthenticationException:
            print("Usuário ou senha invalídos :( \n Por favor, verifique o arquivo que contem o usuário e a senha ou o dispositivo que esta tentando acessar.")
            print("Programa sendo encerrado")
