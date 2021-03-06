#!/usr/bin/python3
#
# Venom2
# Copyright (C) 2019  Da-vinci ( Leonard.nyholm@gmail.com )

# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

try:
    from argparse import ArgumentParser
    from asyncio import get_event_loop
    from os import path, system
    from random import shuffle
    from re import search, compile
    from sys import platform
    from subprocess import call
    from datetime import datetime
    from requests import get, status_codes
    from API import socks
    from time import time
except Exception as err:
    print(err)

version = ".1.1"
proxyenabled = False
Proxies = {"http": "", "https": ""}
slash = "//"
clr = ""


def check_platform():
    global clr
    global slash
    if platform == "win32":
        slash = "\\"
        clr = "cls"
    elif platform == "linux" or platform == "linux2":
        slash = "//"
        clr = "clear"
    else:
        slash = "//"
        print("System platform not recognized: %s" % platform)


def clear():
    if clr == "":
        return
    elif clr == "cls":
        system("cls")
    elif clr == "clear":
        system("clear")


class menus:
    def usage():
        print("usage: ./venom2.py <function> <arg1> <arg2> <arg3>")
        print("dorkscan: ./venom2.py scan 'ending' dorks")
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

    def main_menu(self):
        clear()
        self.logo()
        print("[1] Dork and Vuln Scan")
        print("[2] Enable Tor/Proxy Support")
        print("[3] Exit\n")
        choice = input(":")
        if choice == "1":
            s = scanner()
            s.scan()
        if choice == "2":
            p = proxy()
            p.proxy_main_menu()
        if choice == "3":
            exit(0)


class proxy:
    def __init__(self):
        self.proxy_type = ""
        self.proxy_ip = ""
        self.proxy_port = ""
        self.username = ""
        self.password = ""
        self.proxy_conf = ""

    def proxy_main_menu(self):
        clear()
        m = menus()
        m.logo()
        print("[1] Set proxy")
        print("[2] Update proxy")
        print("[3] Remove proxy")
        print("[4] Test proxy")
        print("[5] Back to main menu")
        proxy_choice = input(":")
        if proxy_choice == "1":
            self.Update_proxy()
        if proxy_choice == "2":
            self.Update_proxy()
        if proxy_choice == "3":
            self.Remove_proxy()
        if proxy_choice == "4":
            self.test_proxy()
        if proxy_choice == "5":
            return

    def Update_proxy(self):
        global proxyenabled
        try:
            self.proxy_type = input("Is the proxy socks4 or socks5?\n:")
            self.proxy_ip = input("Please enter the proxy ip\n:")
            self.proxy_port = input("Proxy port? for example tor socks default port is 9050\n:")
            self.username = input("Proxy username? Leave blank if not required\n:")
            self.password = input("Proxy password? Leave blank if not required\n:")
            if "socks4" not in self.proxy_type and "socks5" not in self.proxy_type:
                print("Unknown choice, retuning to main menu.")
            if (self.username == "") and (self.password == ""):
                proxy_conf = "{}://{}:{}".format(self.proxy_type, self.proxy_ip, self.proxy_port)
            elif len(self.username) >= 1 and len(self.password) >= 1:
                proxy_conf = "{}://{}:{}@{}:{}".format(
                    self.proxy_type, self.username, self.password, self.proxy_ip, self.proxy_port
                )
            Proxies["http"] = proxy_conf
            Proxies["https"] = proxy_conf
            proxyenabled = True
            print("%s proxy enabled!" % self.proxy_type)
            print("Testing proxy server...")
            self.test_proxy()
        except Exception as err:
            print(err)
            input("Press Enter to continue...")
            return

    def Remove_proxy(self):
        global proxyenabled
        Proxies = {"http": "", "https": ""}
        proxyenabled = False

    def test_proxy(self, **kwargs):
        global proxyenabled
        if "ip" in kwargs:
            ip = kwargs.get("ip")
        else:
            ip = input("URL, for example. 'http://google.com'")
            if ip == "":
                ip = "http://google.com"
        try:
            if proxyenabled is True:
                try:
                    s = get(ip, proxies=Proxies, timeout=2)
                    if s.status_code == 200:
                        """
                        Check external IP address
                        """
                        ext_ip = get("https://api.ipify.org?format=raw",
                                    proxies=Proxies,
                                    timeout=5)
                        print("external IP: %s" % str(ext_ip))
                        print("Proxyserver seems to work, verify the IP address")
                        input("Press Enter to continue...")
                        return
                except Exception as err:
                    print(err)
                    proxyenabled = False
                    input("Press Enter to continue...")
            else:
                print("Proxy is not enabled!")
                input("Press Enter to continue...")
        except Exception as err:
            print(err)
            print("Proxy is not working!")
            input("Press Enter to continue...")
            return


def main():
    check_platform()
    while running is True:
        try:
            m = menus()
            m.main_menu()
        except KeyboardInterrupt or Exception as err:
            print(err)
            exit(0)
            datetime.now()


class scanner:
    def __init__(self):
        full_path = path.realpath(__file__)
        local_path, filename = path.split(full_path)
        self.dorks = [
            line.strip()
            for line in open(local_path + slash + "lists" + slash + "d0rks", "r", encoding="utf-8")
        ]
        self.search_ignore = [
            line.strip()
            for line in open(local_path + slash + "lists" + slash + "ignore", "r", encoding="utf-8")
        ]
        shuffle(self.dorks)
        self.Final_list = []
        self.tld = ""
        self.dorks_in_memory = []
        self.headers_in_memory = {}
        self.site = ""
        self.time_now = datetime.now()
        self.crawled_sites = []
        self.use_final_list = False

    def scan(self, **kwargs):
        global proxyenabled

        try:
            try:
                if "target" in kwargs:
                    self.tld = kwargs.get("target")
                else:
                    self.tld = input("\nChoose your target domain or a search word ('*.com')\r\n:")
                    if self.tld == "":
                        self.tld = ".com"
                if "dorks" in kwargs:
                    dork_count = kwargs.get("dorks")
                else:
                    dork_count = input("Choose the number of dorks (0 for all)\r\n:")
                    if dork_count == "":
                        dork_count = "10"
                try:
                    i = 0
                    dork_count = int(dork_count)
                    while i < dork_count:
                        self.dorks_in_memory.append(self.dorks[i])
                        i += 1
                except Exception as err:
                    print(err)
                    input("Press Enter to continue...")
                    return
            except Exception as err:
                print(err)
                input("Press Enter to continue...")
                return
            if "pages" in kwargs:
                self.Number_of_pages = kwargs.get("pages")
            else:
                try:
                    self.Number_of_pages = input("Enter number of pages to go through\n:")
                    if self.Number_of_pages == "":
                        self.Number_of_pages = "10"
                except Exception as err:
                    print(err)
                    input("Press Enter to continue...")
                    return
            self.loop = get_event_loop()
            self.usearch = self.loop.run_until_complete(self.crawl())
        except KeyboardInterrupt:
            m = menus()
            clear()
            m.logo()
            print("Program Paused")
            print("[1] Unpause")
            print("[2] Skip rest of scan and Continue with current results")
            print("[3] Return to main menu")
            print("[4] Exit")
            choise = input(":")
            if choise == "1":
                return
            if choise == "2":
                self.Testing_done_choise()
            if choise == "3":
                m.main_menu()
            if choise == "4":
                exit(0)
            else:
                pass

    async def crawl(self):
        timestart = datetime.now()
        progress = 0
        futures = []
        self.Number_of_pages = int(self.Number_of_pages)
        stringreg = compile('(?<=href=")(http.*?(?="))')

        for dork in self.dorks_in_memory:
            progress += 1
            page = 0
            query = "{}+site:{}".format(dork, self.tld)
            while (page < self.Number_of_pages):
                loop = get_event_loop()
                search_query = (
                        "http://www.bind.com/search?a=" +
                        query +
                        "&go=Submit&first= " +
                        str(page * 50 + 1) +
                        "&count=50"
                        )
                page += 1
                urls = []
                self.domains = set()
                future = loop.run_in_executor(None, 
                            self.send_request, 
                            search_query)
                futures.append(future)

            for future in futures:
                result = await future
                if (result == None):
                    # Proxy server has stopped responding to us and user
                    # wants to quit now.
                    self.Testing_done_choise()
                    # Incase Testing_done_choise returns, return from here
                    return
                urls.extend(stringreg.findall(result))
            basename = search(r"(?<=(\:\/\/))[^\/]*(?=\/)", result)
            for url in urls:
                if ((basename is not None) and
                        ("microsoft" not in url) and
                        ("bing" not in url)):
                    self.crawled_sites.append(url)
            m = menus()
            clear()
            m.logo()
            percent = int((1 * progress / int(len(self.dorks_in_memory))) * 100)
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
                    len(self.crawled_sites),
                    progress,
                    len(self.dorks_in_memory),
                    percent,
                    dork,
                    "%s:%s:%s" % (hours, minutes, seconds),
                )
            )
        self.Testing_done_choise()

    def Testing_done_choise(self):
        m = menus()
        clear()
        if self.use_final_list is False:
            print("URLS:", len(self.crawled_sites))
        elif self.use_final_list is True:
            print("URLS:", len(self.Final_list))
        m.logo()
        print("[1] Sort URLs")
        print("[2] Save URLs to a file")
        print("[3] Print all URLs")
        print("[4] Back to main menu")
        choise = input(":")
        if choise == "1":
            self.pre_check_url()
        if choise == "2":
            if self.use_final_list is True:
                print("\nSaving URLs (" + str(len(self.Final_list)) + ") to file")
            else:
                print("\nSaving URLs (" + str(len(self.crawled_sites)) + ") to file")
            filename = input("Filename: ").encode("utf-8")
            save_file = open(filename, "w", encoding="utf-8")
            if self.use_final_list is True:
                self.Final_list.sort()
                for url in self.Final_list:
                    save_file.write(url + "\r")
            else:
                self.crawled_sites.sort()
                for url in self.crawled_sites:
                    save_file.write(url + "\r")
            save_file.close()
            print("Urls saved to " + str(filename.decode("utf-8")))
            input("Press enter to continue...")
        elif choise == "3":
            print("\nPrinting all URLs:\n")
            self.Final_list.sort()
            print(self.Final_list)
            input("Press enter to exit...")
            exit(0)
        elif choise == "4":
            m.main_menu()
        else:
            self.Testing_done_choise()

    def pre_check_url(self):
        self.use_final_list = True
        timestart = datetime.now()
        progress = 0
        fifth = 0
        for url in self.crawled_sites:
            self.app_url = True
            for i in self.search_ignore:
                basename = search(r"(?<=(\:\/\/))[^\/]*(?=\/)", url)
                if basename is None:
                    break
                else:
                    basename = basename.group(0)
                    x = search(i, url)
                    if x is not None:
                        self.app_url = False
                        break
            if (basename not in self.domains) and (self.app_url is True):
                self.domains.add(basename)
                self.Final_list.append(url)
            fifth += 1
            progress += 1
            if fifth == 5:
                fifth = 0
                m = menus()
                clear()
                m.logo()
                percent = int((1 * progress / int(len(self.crawled_sites))) * 100)
                start_time = datetime.now()
                timeduration = start_time - timestart
                ticktock = timeduration.seconds
                hours, remainder = divmod(ticktock, 3600)
                minutes, seconds = divmod(remainder, 60)
                print(
                    "| Collected urls: <%s> \r\n"
                    "| Sorted URLs: <%s> \r\n"
                    "| Sites: <%s/%s> Progressed so far \r\n"
                    "| Percent Done: <%s> \r\n"
                    "| Url In Progress: %s \r\n"
                    "| Elapsed Time: <%s> \r\n"
                    % (
                        len(self.crawled_sites),
                        len(self.Final_list),
                        progress,
                        len(self.crawled_sites),
                        percent,
                        url,
                        "%s:%s:%s" % (hours, minutes, seconds),
                    )
                )
        print("URLs sorted, there are now %s URLs" % len(self.Final_list))
        return

    def send_request(self, url):
        global proxyenabled
        response = None
        try:
            if proxyenabled is True:
                if Proxies.get("http") != "":
                    response = get(url, proxies=Proxies, timeout=2)
                    response.raise_for_status()
                    if response.status_code != 200:
                        raise response.status_code
                else:
                    check_if_dead_proxy = input("the proxy server might have died, continue y/N")
                    if (("n" in check_in_dead_proxy) or 
                            ("N" in check_in_dead_proxy)):
                        return None
            else:
                response = get(url, timeout=2)
                response.raise_for_status()
        except Exception as err:
            print(err)
        finally:
            if response.raise_for_status() is None:
                return response.text


# main program code here #
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-p",
        "--proxy",
        nargs="?",
        type=str,
        const="socks5://127.0.0.1:9050",
        help="Enable proxy, default is TOR proxy socks5://127.0.0.1:9050",
    )
    parser.add_argument("-t", "--target", type=str, help="Targeted Top Level Domain")
    parser.add_argument("-d", "--dorks", type=int, help="Amount of dorks")
    parser.add_argument("-P", "--pages", type=int, help="Number of pages to go through")
    args = parser.parse_args()
    if args.proxy:
        Proxies["http"] = args.proxy
        Proxies["https"] = args.proxy
        proxyenabled = True
    if args.target and args.dorks and args.pages:
        print("target:" + args.target + "dorks:" + str(args.dorks) + "pages:" + str(args.pages))
        s = scanner()
        s.scan(target=args.target, dorks=args.dorks, pages=args.pages)
    m = menus()
    running = True
    main()
