#!/usr/bin/python3

import argparse
import asyncio
import os
import random
import re
import sys
import threading
from datetime import datetime

import requests

from API import socks

version = ".0.1"
proxyenabled = False
testing = True
http_proxy = ""
https_proxy = ""
Proxies = {"http": "", "https": ""}

try:
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    dorks = [line.strip() for line in open(path + "\\lists\\d0rks", "r", encoding="utf-8")]
    header = [line.strip() for line in open(path + "\\lists\\header", "r", encoding="utf-8")]
    xsses = [line.strip() for line in open(path + "\\lists\\xsses", "r", encoding="utf-8")]
    lfis = [line.strip() for line in open(path + "\\lists\\pathto_huge.txt", "r", encoding="utf-8")]
    tables = [line.strip() for line in open(path + "\\lists\\tables", "r", encoding="utf-8")]
    columns = [line.strip() for line in open(path + "\\lists\\columns", "r", encoding="utf-8")]
    search_Ignore = [line.strip() for line in open(path + "\\lists\\ignore", "r", encoding="utf-8")]
    random.shuffle(dorks)
    random.shuffle(header)
    random.shuffle(lfis)
except Exception as err:
    print(err)
    exit()


class menus:
    def __init__(self):
        self.s = scanner()

    def usage():
        print("usage: ./venom2.py <function> <arg1> <arg2> <arg3>")
        print("dorkscan: ./venom2.py scan 'ending' dorks threads")
        print("example: ./venom2.py scan '.com' 1000 500")
        print("or just ./venom2.py for gui")

    def logo(self):
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

    #    def pre_run(self):
    #        if func == 'scan':
    #            ending = arg1
    #            dorks = arg2
    #            threads = arg3
    #            self.s.scan(arg1, arg2, arg3)

    def main_menu(self):
        self.logo()
        print("[1] Dork and Vuln Scan")
        print("[2] Enable Tor/Proxy Support")
        print("[3] Cloudflare Resolving")
        print("[4] Misc Options")
        print("[5] Exit\n")
        choice = input(":")
        if choice == "1":
            self.s.scan()
        if choice == "2":
            p.Update_proxy()
        if choice == "3":
            pass
        if choice == "4":
            pass
        if choice == "5":
            exit()


class proxy:
    def __init__(self, **kwargs):
        self.proxy_type = ""
        self.proxy_ip = ""
        self.proxy_port = ""
        self.username = ""
        self.password = ""
        self.proxy_conf = ""
        if "proxy_type" in kwargs:
            self.proxy_type = kwargs.get("proxy_type")
        if "proxy_ip" in kwargs:
            self.proxy_ip = kwargs.get("proxy_ip")
        if "proxy_port" in kwargs:
            self.proxy_port = kwargs.get("proxy_port")
        if "username" in kwargs:
            self.username = kwargs.get("username")
        if "password" in kwargs:
            self.password = kwargs.get("password")
        if self.proxy_type and self.proxy_ip and self.proxy_port:
            self.proxy_conf = "{}://{}:{}".format(self.proxy_type, self.proxy_ip, self.proxy_port)
            Proxies["http"] = self.proxy_conf
            Proxies["https"] = self.proxy_conf
            print("%s proxy enabled!" % self.proxy_type)
            return
        elif (
            self.proxy_type
            and self.proxy_ip
            and self.proxy_port
            and self.username
            and self.password
        ):
            self.proxy_conf = "{}://{}:{}@{}:{}".format(
                self.proxy_type, self.username, self.password, self.proxy_ip, self.proxy_port
            )
            Proxies["http"] = self.proxy_conf
            Proxies["https"] = self.proxy_conf
            print("%s proxy enabled!" % self.proxy_type)
            return

    def proxy_main_menu(self):
        print("[1] Set proxy")
        print("[2] Update proxy")
        print("[3] Remove proxy")
        print("[5] Back to main menu")
        proxy_choice = input(":")
        if proxy_choice == "1":
            self.Update_proxy()
        if proxy_choice == "2":
            self.Update_proxy()
        if proxy_choice == "3":
            self.Remove_proxy()
        if proxy_choice == "4":
            return

    def Update_proxy(self):
        try:
            if testing is not True:
                self.proxy_type = input("Is the proxy socks4 or socks5?\n:")
                self.proxy_ip = input("Please enter the proxy ip\n:")
                self.proxy_port = input("Proxy port? for example tor socks default port is 9050\n:")
                self.username = input("Proxy username? Leave blank if not required\n:")
                self.password = input("Proxy password? Leave blank if not required\n:")
            if testing is True:
                self.proxy_type = "socks4"
                self.proxy_ip = "127.0.0.1"
                self.proxy_port = 9050
                self.username = ""
                self.password = ""
            if "socks4" not in self.proxy_type and "socks5" not in self.proxy_type:
                print("Unknown choice, retuning to main menu.")
            if (self.username == "") and (self.password == ""):
                proxy_conf = "{}://{}:{}".format(self.proxy_type, self.proxy_ip, self.proxy_port)
                proxyenabled = True
                Proxies["http"] = proxy_conf
                Proxies["https"] = proxy_conf
                print(proxy_conf, Proxies)
                print("%s proxy enabled!" % self.proxy_type)
            elif len(self.username) >= 1 and len(self.password) >= 1:
                proxy_conf = "{}://{}:{}@{}:{}".format(
                    self.proxy_type, self.username, self.password, self.proxy_ip, self.proxy_port
                )
                proxyenabled = True
                Proxies["http"] = proxy_conf
                Proxies["https"] = proxy_conf
                print(proxy_conf, Proxies)
                print("%s proxy enabled!" % self.proxy_type)
        except Exception as err:
            print(err)
            return


def main():
    while running is True:
        try:
            m = menus()
            m.main_menu()
        except KeyboardInterrupt or Exception as err:
            print(err)
            exit()
            datetime.now()


class scanner:
    def __init__(self):
        self.Final_list = []
        self.tld = ""
        self.dorks_in_memory = []
        self.progress = 0
        self.site = ""
        self.time_now = datetime.now()
        self.crawled_sites = []
        self.vuln_list = [
            "error in your SQL syntax",
            "mysql_fetch",
            "num_rows",
            "ORA-01756",
            "Error Executing Database Query",
            "SQLServer JDBC Driver",
            "OLE DB Provider for SQL Server",
            "Unclosed quotation mark",
            "ODBC Microsoft Access Driver",
            "Microsoft JET Database",
            "Error Occurred While Processing Request",
            "Microsoft JET Database",
            "Server Error",
            "ODBC Drivers error",
            "Invalid Querystring",
            "OLE DB Provider for ODBC",
            "VBScript Runtime",
            "ADODB.Field",
            "BOF or EOF",
            "ADODB.Command",
            "JET Database",
            "mysql_fetch_array",
            "Syntax error",
            "mysql_numrows()",
            "GetArray()",
            "FetchRow()",
            "Input string was not in a correct format",
        ]

        self.vuln_to = [
            "MySQL Classic",
            "MiscError",
            "MiscError2",
            "Oracle",
            "JDBC_CFM",
            "JDBC_CFM2",
            "MSSQL_OLEdb",
            "MSSQL_Uqm",
            "MS-Access_ODBC",
            "MS-Access_JETdb",
            "Processing Request",
            "MS-Access JetDb",
            "Server Error",
            "ODBC Drivers error",
            "Invalid Querystring",
            "OLE DB Provider for ODBC",
            "VBScript Runtime",
            "ADODB.Field",
            "BOF or EOF",
            "ADODB.Command",
            "JET Database",
            "mysql_fetch_array",
            "Syntax error",
            "mysql_numrows()",
            "GetArray()",
            "FetchRow()",
            "Input String Error",
        ]

    def scan(self):
        global proxyenabled
        try:
            if len(sys.argv) > 1:
                pass
            else:
                if testing is True:
                    self.tld = ".com"
                else:
                    self.tld = input("\nChoose your target domain or a search word ('*.com')\r\n:")
                self.sitearray = [self.tld]
                if testing is True:
                    dork_count = 10
                else:
                    dork_count = int(input("Choose the number of dorks (0 for all)\r\n:"))
                try:
                    if dork_count == 0:
                        i = 0
                        while i < dork_count:
                            self.dorks_in_memory.append(dorks[i])
                            i += 1
                    else:
                        i = 0
                        while i < dork_count:
                            self.dorks_in_memory.append(dorks[i])
                            i += 1
                except Exception as err:
                    print(err)
                    return
                if testing is True:
                    self.Threads = 50
                else:
                    self.Threads = int(input("How many threads do you want to use?\n:"))
                if testing is True:
                    self.Number_of_pages = 5
                else:
                    self.Number_of_pages = int(input("Enter number of pages to go through\n:"))
                self.loop = asyncio.get_event_loop()
                self.usearch = self.loop.run_until_complete(self.crawl())
        except KeyboardInterrupt:
            exit()

    async def crawl(self):
        timestart = datetime.now()
        for site in self.sitearray:
            for dork in self.dorks_in_memory:
                self.progress += 1
                page = 0
                query = "{}+site:{}".format(dork, site)
                while page < self.Number_of_pages:
                    loop = asyncio.get_event_loop()
                    futures = []
                    Search_query = (
                        "http://www.bing.com/search?q="
                        + query
                        + "&go=Submit&first="
                        + str(page * 50 + 1)
                        + "&count=50"
                    )
                    page += 1
                    if Search_query is not None:
                        futures.append(loop.run_in_executor(None, self.Send_Request, Search_query))
                stringreg = re.compile("(?<=href=')(http.*?)(?=')")
                urls = []
                domains = set()
                for future in futures:
                    result = await future
                    self.crawled_sites.extend(stringreg.findall(result))
                for url in self.crawled_sites:
                    basename = re.search(r"(?<=(\:\/\/))[^\/]*(?=\/)", url)
                    basename = basename.group(0)
                    dont_append_url = False
                    for i in search_Ignore:
                        if (basename is None) or re.search(i, basename):
                            dont_append_url = True
                            break
                    # still gives double urls
                    # basename =/= name in domains
                    # gotta figure out why later
                    if (basename not in domains) and (dont_append_url is not True):
                        domains.add(basename)
                        self.Final_list.append(url)
                    else:
                        if basename not in urls:
                            urls.append(url)
                m = menus()
                m.logo()
                percent = int((1 * self.progress / int(len(self.dorks_in_memory))) * 100)
                start_time = datetime.now()
                timeduration = start_time - timestart
                ticktock = timeduration.seconds
                hours, remainder = divmod(ticktock, 3600)
                minutes, seconds = divmod(remainder, 60)
                print(
                    "| Target: <%s> \r\n"
                    "| Collected urls: <%s> \r\n"
                    "| D0rks: <%s/%s> Progressed so far \r\n"
                    "| Percent Done: <%s> \r\n"
                    "| Dork In Progress: %s \r\n"
                    "| Elapsed Time: <%s> \r\n"
                    % (
                        self.tld,
                        len(self.Final_list),
                        self.progress,
                        len(self.dorks_in_memory),
                        percent,
                        dork,
                        "%s:%s:%s" % (hours, minutes, seconds),
                    )
                )
        print(self.Final_list)

    def Send_Request(self, search_query):
        try:
            response = requests.get(search_query, timeout=2)
            response.raise_for_status()
        except Exception as err:
            print(err)
        finally:
            return response.text


# main program code here #
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="store_true", help="increase output verbosity")
    # gotta fix accepting optional
    parser.add_argument(
        "-p",
        "--proxy",
        type=str,
        default="socks5://127.0.0.1:9050",
        required=False,
        nargs='*',
        help="Enable proxy, default is TOR proxy ie. socks5://ip:port"
    )
    parser.add_argument("-v", "--verbosity", action="store_true", help="increase output verbosity")
    args = parser.parse_args()
    if args.proxy:
        print(args.proxy)
        Proxies["http"] = args.proxy
        Proxies["https"] = args.proxy
        proxyenabled = True
        print(Proxies)
    m = menus()
    running = True
    main()
