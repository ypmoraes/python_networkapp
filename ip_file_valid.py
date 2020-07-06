import sys
import os.path

def ip_file_valid():
    ip_file = input('A seguir insira o caminho do arquivo que possui os enderecos de IP. Ex: C:\\ips.txt \n'
                    'Insira o caminho:')

    if os.path.isfile(ip_file) == True:
        print(f'{ip_file} --  É um arquivo valido.')
    else:
        print(f'{ip_file} -- Não é um arquivo valido')
        sys.exit()


    ips=open(ip_file, 'r')

    ips.seek(0)

    ip_list = ips.readlines()

    ips.close()

    return ip_list