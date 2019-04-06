#!/usr/bin/python3

import threading
import random
import sys
import os
import asyncio
from datetime import datetime
import requests
import re

version = ".0.1"
proxyenabled = False
testing = True

try:
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    dorks = [
        line.strip() for line in open(path + "\\lists\\d0rks", "r", encoding="utf-8")
    ]
    header = [
        line.strip() for line in open(path + "\\lists\\header", "r", encoding="utf-8")
    ]
    xsses = [
        line.strip() for line in open(path + "\\lists\\xsses", "r", encoding="utf-8")
    ]
    lfis = [
        line.strip()
        for line in open(path + "\\lists\\pathto_huge.txt", "r", encoding="utf-8")
    ]
    tables = [
        line.strip() for line in open(path + "\\lists\\tables", "r", encoding="utf-8")
    ]
    columns = [
        line.strip() for line in open(path + "\\lists\\columns", "r", encoding="utf-8")
    ]
    search_Ignore = [
        line.strip() for line in open(path + "\\lists\\ignore", "r", encoding="utf-8")
    ]
    random.shuffle(dorks)
    random.shuffle(header)
    random.shuffle(lfis)
except Exception as err:
    print(err)
    exit()


class menus:
    def __init__(self):
        if len(sys.argv) > 2:
            self.tld = sys.argv[1]
            self.dorks = sys.argv[2]
            self.threads = sys.argv[3]
            self.s = scanner()
        else:
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
        if testing is True:
            self.s.scan()
        self.logo()
        print("[1] Dork and Vuln Scan")
        print("[2] Enable Tor/Proxy Support")
        print("[3] Cloudflare Resolving")
        print("[4] Misc Options")
        print("[5] Exit\n")
        choice = int(input(":"))
        if choice == 1:
            self.s.scan()
        if choice == 2:
            pass
        if choice == 3:
            pass
        if choice == 4:
            pass
        if choice == 5:
            exit()


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
        if len(sys.argv) > 1:
            self.arg1 = arg1
            self.arg2 = arg2
            self.arg3 = arg3
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
        try:
            if len(sys.argv) > 1:
                pass
            else:
                if testing is True:
                    self.tld = '.com'
                else:
                    self.tld = input(
                        '\nChoose your target domain or a search word ("*.com")\r\n:'
                    )
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
                    self.Number_of_pages = int(
                        input("Enter number of pages to go through\n:")
                    )
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
                        futures.append(
                            loop.run_in_executor(None, self.checkdead, Search_query)
                        )
                stringreg = re.compile('(?<=href=")(http.*?)(?=")')
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
                        if (basename not in urls):
                            urls.append(url)
                m = menus()
                m.logo()
                percent = int(
                    (1 * self.progress / int(len(self.dorks_in_memory))) * 100
                )
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
                        "%s:%s:%s" % (hours, minutes, seconds)
                    )
                )
        print(self.Final_list)

    def checkdead(self, url):
        try:
            response = requests.get(url, timeout=2)
            response.raise_for_status()
        except Exception as verb:
            print(str(verb))
        finally:
            return response.text


# main program code here #
if __name__ == "__main__":
    m = menus()
    running = True
    print(sys.argv)
    if len(sys.argv) >= 2:
        try:
            func = str(sys.argv[1])
            arg1 = str(sys.argv[2])
            arg2 = sys.argv[3]
            arg3 = sys.argv[4]
            # m.pre_run()
        except Exception as err:
            print(err)
            m.usage()
    else:
        main()
