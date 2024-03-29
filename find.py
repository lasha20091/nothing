import threading, time, requests, argparse, random
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print("""
...........................';cclooollloooooooollllccc::::::;;;,,''''''..
...........................';::cooooooooooooolllllccc:::::;;;;,,'''''...
............................',;:cllllooooooollllllcc:::;;;;;;,,,''''....
.......................      .',;:cloooodooolllcccc::;;;,,,,,,'''.......
...................           ..,:clooooodoollccc::::;;,,,,,''''........
................               .':looddddooolcc::::;;;,,,,,,''''........
.............                  .;coodddddooolc::;;;;;,,,,,,,,'''''''....
.'...''......       .,:loddddolc:lddxxdddoolc:;;;,,,,,,,,,,,'''''''''...
......'.. ..     .lOKKKKKKKKK00OOkkkkxxxddol:,..',,,,,,,,,,,,,''''''''''
'.''''.. ..    .o0KKKK00XXXKO0XXXX0OOOkxxdoc;....'''',,,,,,,,,,,''''''''
''''''.  .     xKK000k0WMOlo0OXXcxKK00OOkdl;..   ...''''''',,,,,,'''''''
''''''.        OXK0000WWo   'NXWO:x00000Okl.       ...''''',',,,,'''''''
'''''..        OXK000NW:    ,WMWWNKXK0000KOo.       ..'''''',,,,,'''''''
''''''. .      OXKKKXK'     kMMWNWNk0KKOdoOX0,      ...''''''',,''''''''
''''''....     xXKKXN.     .NWWNNWdONKXN0kloOkc.     ..'''''''''''''''''
'''''''....    'XXKXO     ,XWNWNMMKNMNNWNkkOOxl,     ..'''''''''''''''''
'''''''. ..     ;KKXN0kkOKNWWWWNWWMMMMMMMWklxOx.     ...''''''''''''''''
'''''''  ..      :KKKXWMNXWWXWWNWMWNXK0xd: .oxO.     ....'''''''''''''''
''''''.           :O0KXNXNMKKk'''..,;,..   'K;0.     ....'''''''''''.'''
''''''.            lOO00KKNWKKo;. .......  .Xo0o.    .....''''''...'''''
.'''''             .xOkkO0KXX0NWW0o;,'',;:coKWXOK'   ......'''......''''
..'''.               ,oOOO0KKKNWWWWWWWMMMMMMMMMN0x       ..'''...''.''''
.'''.                   ;x000KKXNWWNNNMMMMMMMMMWNo        ......''''''''
.',,.                     .:oox0XXXWWWMMMMMMMMWWNx         ...''''''''''
.',''.                         .,dO0KXNWWMMWWWWWWW0,        ..''''''''''
.',,,.                              ..,;clxKWWWWMMWK         ..'''''''''
.',,,,.                                     ,xXXNKO:          .'''''''''
.',,,,,'                                      .''..            .''''''''
.,,,,,,,'                                                      .''''''''
..........                                                     .........

""")

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="target url e.g. https://www.example.com", required=True)
parser.add_argument("-s", "--speed", help="slow, normal, aggressive", nargs='?', type=str, default="normal")
args = parser.parse_args()

if args.speed == "slow":
    lock = threading.Semaphore(1)
    tsleep = 2
elif args.speed == "normal":
    lock = threading.Semaphore(5)
    tsleep = 1
elif args.speed == "aggressive":
    lock = threading.Semaphore(50)
    tsleep = 0
else:
    lock = threading.Semaphore(5)
    tsleep = 1

if "/" not in args.url[-1]:
    target = (args.url + "/")
    print(target)
else:
    target = args.url
    print(target)

targetList = []
savelist = []


def printline(url):
    print(url, sep=' ', end='\r', flush=True)


def check_panel(url):
    with open("useragents.txt", "r") as agents:
        agent = random.choice(agents.readlines())
        a = agent.strip()
        header = {
            "User-Agent": str(a)
        }
        agents.close()
    get = requests.get(url, headers=header)
    status_code = get.status_code
    if get.status_code == 200:
        soup = BeautifulSoup(get.text, "html.parser")
        check_input = soup.find_all("input")
        valueuser = soup.find('input', {'name': 'username'})
        valueuser1 = soup.find('input', {'name': 'user'})
        valuepass = soup.find('input', {'name': 'password'})
        valuepass1 = soup.find('input', {'name': 'pass'})
        if len(check_input) >= 1:
            if valueuser or valuepass or valueuser1 or valuepass1 is not None:
                print("[{}]{} Found a Login Form!".format(str(status_code), url))
                savelist.append(url + "\n")
            else:
                print("[{}]{} Found a form! Please check it manually.".format(str(status_code), url))
                savelist.append(url + "\n")
        else:
            print("[{}]{} Please check it manually.".format(str(status_code), url))
            savelist.append(url+"\n")
    else:
        printline(url)
    time.sleep(int(tsleep))
    lock.release()



def multi_thread(urls):
    with open("paths.txt", "r") as panels:
        for panel in panels:
            targetList.append(urls + panel.strip())
    thread_pool = []
    for url in targetList:
        thread = threading.Thread(target=check_panel, args=(url,))
        thread_pool.append(thread)
        thread.start()
        lock.acquire()
    for thread in thread_pool:
        thread.join()


try:
    multi_thread(target)
    with open("found.txt", "w") as save:
        save.writelines(savelist)
        save.close()
        print("\nList saved to found.txt")

    print("Done !")
except:
    print("Error!")


