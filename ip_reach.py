import sys
import subprocess

#list=['10.10.10.2', '10.10.10.3', '10.10.10.4']

def ip_reach(list):
    for ip in (list):
        ip= ip.rstrip('\n')

        ping_request=subprocess.call((f'ping {ip}  /n 2'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if ping_request == 0:
            print(f'O IP {ip} esta respondendo na rede')
        else:
            print(f'O IP {ip} nao esta respondendo na rede')
            sys.exit()