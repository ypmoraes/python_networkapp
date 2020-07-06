import sys

from ip_file_valid import  ip_file_valid
from ip_adr_valid import ip_adr_valid
from ip_reach import ip_reach
from ssh_connection import ssh_connection
from create_threads import  create_threads

ip_list = ip_file_valid()

try:
    ip_adr_valid(ip_list)

except KeyboardInterrupt:
    print('\n\n Programa abortado pelo usuário. Fechando...')
    sys.exit()

try:
    ip_reach(ip_list)

except KeyboardInterrupt:
    print('\n\n Programa abortado pelo usuário. Fechando...')
    sys.exit()

create_threads(ip_list, ssh_connection)