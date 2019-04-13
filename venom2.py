#!/usr/bin/python3
try:
    import argparse
    import asyncio
    import os
    import random
    import re
    import sys
    import threading
    from subprocess import call

    from datetime import datetime

    import requests

    from API import socks
except Exception as err:
    print(err)

version = ".0.1"
proxyenabled = False
testing = True
http_proxy = ""
https_proxy = ""
Proxies = {"http": "", "https": ""}
slash = "//"
clear = ""

if sys.platform == "win32":
    slash = "\\"
    clear = "cls"
elif sys.platform == "linux" or sys.platform == "linux2":
    slash = "//"
    clear = "clear"
else:
    slash = "//"
    print("System platform not recognized: %s" % sys.platform)

try:
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    dorks = [
        line.strip()
        for line in open(path + slash + "lists" + slash + "d0rks", "r", encoding="utf-8")
    ]
    header = [
        line.strip()
        for line in open(path + slash + "lists" + slash + "header", "r", encoding="utf-8")
    ]
    xsses = [
        line.strip()
        for line in open(path + slash + "lists" + slash + "xsses", "r", encoding="utf-8")
    ]
    lfis = [
        line.strip()
        for line in open(path + slash + "lists" + slash + "pathto_huge.txt", "r", encoding="utf-8")
    ]
    tables = [
        line.strip()
        for line in open(path + slash + "lists" + slash + "tables", "r", encoding="utf-8")
    ]
    columns = [
        line.strip()
        for line in open(path + slash + "lists" + slash + "columns", "r", encoding="utf-8")
    ]
    search_Ignore = [
        line.strip()
        for line in open(path + slash + "lists" + slash + "ignore", "r", encoding="utf-8")
    ]
    random.shuffle(dorks)
    random.shuffle(header)
    random.shuffle(lfis)
except Exception as err:
    print(err)
    exit()


def clear():
    call(clear)


class menus:
    def usage():
        print("usage: ./venom2.py <function> <arg1> <arg2> <arg3>")
        print("dorkscan: ./venom2.py scan 'ending' dorks threads")
        print("example: ./venom2.py scan '.com' 1000 500")
        print("or just ./venom2.py for gui")

    def logo(self):
        clear()
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

    def main_menu(self):
        self.logo()
        print("[1] Dork and Vuln Scan")
        print("[2] Enable Tor/Proxy Support")
        print("[3] Cloudflare Resolving")
        print("[4] Misc Options")
        print("[5] Exit\n")
        choice = input(":")
        if choice == "1":
            s = scanner()
            s.scan()
        if choice == "2":
            p = proxy()
            p.Update_proxy()
        if choice == "3":
            pass
        if choice == "4":
            pass
        if choice == "5":
            exit()


class proxy:
    def __init__(self):
        self.proxy_type = ""
        self.proxy_ip = ""
        self.proxy_port = ""
        self.username = ""
        self.password = ""
        self.proxy_conf = ""

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
                print("%s proxy enabled!" % self.proxy_type)
            elif len(self.username) >= 1 and len(self.password) >= 1:
                proxy_conf = "{}://{}:{}@{}:{}".format(
                    self.proxy_type, self.username, self.password, self.proxy_ip, self.proxy_port
                )
                proxyenabled = True
                Proxies["http"] = proxy_conf
                Proxies["https"] = proxy_conf
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
        self.headers_in_memory = {}
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

    def scan(self, **kwargs):
        global proxyenabled

        try:
            if "target" in kwargs:
                self.tld = kwargs.get("target")
            else:
                self.tld = input("\nChoose your target domain or a search word ('*.com')\r\n:")
            if "dorks" in kwargs:
                dork_count = kwargs.get("dorks")
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
            if "threads" in kwargs:
                Threads = kwargs.get("threads")
            else:
                self.Threads = int(input("How many threads do you want to use?\n:"))
            if "pages" in kwargs:
                self.Number_of_pages = kwargs.get("pages")
            else:
                self.Number_of_pages = int(input("Enter number of pages to go through\n:"))
            self.loop = asyncio.get_event_loop()
            self.usearch = self.loop.run_until_complete(self.crawl())
        except KeyboardInterrupt:
            m = menus()
            m.logo()
            print("Program Paused")
            print("[1] Unpause")
            print("[2] Skip rest of scan and Continue with current results")
            print("[3] Return to main menu")
            choise = input(":")
            if choise == "1":
                return
            if choise == "2":
                pass
            if choise == "3":
                m.main_menu()
            else:
                pass

    async def crawl(self):
        timestart = datetime.now()
        futures = []
        for dork in self.dorks_in_memory:
            self.progress += 1
            page = 0
            query = "{}+site:{}".format(dork, self.tld)
            while page < self.Number_of_pages:
                loop = asyncio.get_event_loop()
                Search_query = (
                    "http://www.bing.com/search?q="
                    + query
                    + "&go=Submit&first="
                    + str(page * 50 + 1)
                    + "&count=50"
                )
                page += 1
                future = loop.run_in_executor(None, self.Send_Request, Search_query)
                futures.append(future)
            stringreg = re.compile('(?<=href=")(http.*?(?="))')
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
            m.logo()
            print("\n\nURLS:", len(self.Final_list))

    def Testing_done_choise(self):
        m = menus()
        m.logo()
        print("[1] Save URLs to a file")
        print("[2] Print all URLs")
        print("[3] Back to main menu")
        choise = input(":")
        if choise == "1":
            print("\nSaving valid URLs (" + str(len(self.Final_list)) + ") to file")
            filename = input("Filename: ").encode("utf-8")
            save_file = open(filename, "w", encoding="utf-8")
            self.Final_list.sort()
            for url in self.Final_list:
                save_file.write(url + "\r\n")
            save_file.close()
            print("Urls saved to " + filename)
        elif choise == "2":
            print("\nPrinting all URLs:\n")
            self.Final_list.sort()
            for t in self.Final_list:
                print(t)
        elif choise == "4":
            m.main_menu()
        else:
            s.Testing_done_choise()

    def Send_Request(self, url):
        global proxyenabled
        response = {"text": ""}
        try:
            if testing is not True:
                response = requests.get(url, timeout=2)
                response.raise_for_status()
                return
            elif testing is True:
                if proxyenabled is True:
                    if Proxies.get("http") is not "":
                        response = requests.get(url, proxies=Proxies, timeout=2)
                        response.raise_for_status()
                    else:
                        check_if_dead_proxy = input(
                            "the proxy server might have died, continue y/N"
                        )
                        if check_if_dead_proxy == "N" or check_if_dead_proxy == "":
                            exit(0)
                        if check_if_dead_proxy == "y" or check_if_dead_proxy == "Y":
                            proxyenabled = False
                else:
                    response = requests.get(url, timeout=2)
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
        nargs="?",
        type=str,
        const="socks5://127.0.0.1:9050",
        help="Enable proxy, default is TOR proxy socks5://127.0.0.1:9050",
    )
    parser.add_argument("-t", "--target", type=str, help="Targeted Top Level Domain")
    parser.add_argument(
        "-T", "--threads", nargs="?", const=10, type=int, help="Amount of threads, Default 10"
    )
    parser.add_argument("-d", "--dorks", type=int, help="amount of dorks")
    parser.add_argument("-P", "--pages", type=int, help="Number of pages to go through")
    args = parser.parse_args()
    if args.proxy:
        Proxies["http"] = args.proxy
        Proxies["https"] = args.proxy
        proxyenabled = True
    if args.target and args.threads and args.dorks and args.pages:
        print(
            "target:"
            + args.target
            + "threads:"
            + str(args.threads)
            + "dorks:"
            + str(args.dorks)
            + "pages:"
            + str(args.pages)
        )
        s = scanner()
        s.scan(target=args.target, threads=args.threads, dorks=args.dorks, pages=args.pages)
    if testing is True:
        s = scanner()
        Proxies["http"] = "socks5://127.0.0.1:9050"
        Proxies["https"] = "socks5://127.0.0.1:9050"
        proxyenabled = True
    m = menus()
    running = True
    main()
