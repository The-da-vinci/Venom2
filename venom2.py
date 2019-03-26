#!/usr/bin/python3

import threading
import random
import sys
import os

version = '.0.1'
proxyenabled = False

vuln_list = ['error in your SQL syntax', 'mysql_fetch', 'num_rows', 'ORA-01756',
             'Error Executing Database Query', 'SQLServer JDBC Driver',
             'OLE DB Provider for SQL Server', 'Unclosed quotation mark',
             'ODBC Microsoft Access Driver', 'Microsoft JET Database',
             'Error Occurred While Processing Request', 'Microsoft JET Database',
             'Server Error', 'ODBC Drivers error', 'Invalid Querystring',
             'OLE DB Provider for ODBC', 'VBScript Runtime', 'ADODB.Field',
             'BOF or EOF', 'ADODB.Command', 'JET Database', 'mysql_fetch_array',
             'Syntax error', 'mysql_numrows()', 'GetArray()', 'FetchRow()',
             'Input string was not in a correct format']

vuln_to = ['MySQL Classic', 'MiscError', 'MiscError2', 'Oracle', 'JDBC_CFM', 'JDBC_CFM2',
           'MSSQL_OLEdb', 'MSSQL_Uqm', 'MS-Access_ODBC', 'MS-Access_JETdb', 'Processing Request',
           'MS-Access JetDb', 'Server Error', 'ODBC Drivers error', 'Invalid Querystring',
           'OLE DB Provider for ODBC', 'VBScript Runtime', 'ADODB.Field', 'BOF or EOF',
           'ADODB.Command', 'JET Database', 'mysql_fetch_array', 'Syntax error',
           'mysql_numrows()', 'GetArray()', 'FetchRow()', 'Input String Error']


def usage():
    print('usage: ./venom2.py <function> <arg1> <arg2> <arg3>')
    print("dorkscan: ./venom2.py scan 'ending' dorks threads")
    print("example: ./venom2.py scan '.com' 1000 500")
    print('or just ./venom2.py for gui')


def pre_run():
    if func == scan:
        ending = arg1
        dorks = arg2
        threads = arg3
        scan()


def logo():
    print("---------------------------------------------------")
    print(" __      ________ _   _  ____  __  __   ___  ")
    print(" \ \    / /  ____| \ | |/ __ \|  \/  | |__ \ ")
    print("  \ \  / /| |__  |  \| | |  | | \  / |    ) |")
    print("   \ \/ / |  __| | . ` | |  | | |\/| |   / / ")
    print("    \  /  | |____| |\  | |__| | |  | |  / /_ ")
    print("     \/   |______|_| \_|\____/|_|  |_| |____|" + version)
    print("                                              by Da-vinci")
    print("         Proxy Enabled " + " [", proxyenabled, "] ")
    print("---------------------------------------------------")


# main loop code here #
def main():
    while running is True:
        try:
            if arg1:
                pre_run()
            else:
                main_menu()
        except KeyboardInterrupt or Exception as err:
            print(err)
            exit()
# main loop code ends #


def load_dorks():
    try:
        d0rk = [line.strip() for line in open("lists/d0rks", "r", encoding="utf-8")]
        header = [line.strip() for line in open("lists/header", "r", encoding="utf-8")]
        xsses = [line.strip() for line in open("lists/xsses", "r", encoding="utf-8")]
        lfis = [line.strip() for line in open("lists/pathtotest_huge.txt", "r", encoding="utf-8")]
        tables = [line.strip() for line in open("lists/tables", "r", encoding="utf-8")]
        columns = [line.strip() for line in open("lists/columns", "r", encoding="utf-8")]
        search_Ignore = str([line.strip() for line in open("lists/ignore", "r", encoding="utf-8")])
        random.shuffle(d0rk)
        random.shuffle(header)
        random.shuffle(lfis)
    except Exception as err:
        print(err)
        exit()


def main_menu():
    logo()
    print("[1] Dork and Vuln Scan")
    print("[2] Admin page finder")
    print("[3] Enable Tor/Proxy Support")
    print("[4] Cloudflare Resolving")
    print("[5] Misc Options")
    print("[6] Exit\n")
    chce = input(":")


# main program code here #
if __name__ == "__main__":
    running = True
    if sys.argv[1]:
        try:
            func = str(sys.argv[1])
            arg1 = str(sys.argv[2])
            arg2 = sys.argv[3]
            arg3 = sys.argv[4]
            pre_run()
        except Exception as err:
            print(err)
            usage()
    else:
        main()
