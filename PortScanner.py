import optparse
from socket import *
from threading import *
screenLock = Semaphore(value=1)

def connScan(host, ports):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((host, ports))
        connSkt.send(b"Hello")
        results = connSkt.recv(100)
        screenLock.acquire()
        print(f"[+] {ports} tcp port open")
        print("[+]" + str(results))
        #connSkt.close()
    except:
        screenLock.acquire()
        print(f"[-] {ports} tcp port closed")
    finally:
        screenLock.release()
        connSkt.close()

def portScan(host, ports):
    try:
        tgtIP = gethostbyname(host)
    except:
        print(f"[-] Cannot resolve {host}: Unknown Host")
        return
    
    try:
        tgtName = gethostbyaddr(tgtIP)
        print("\nScanning results for: " + tgtName[0])
    except:
        print("\nScanning results for: " + tgtIP)
    
    setdefaulttimeout(1)
    for p in ports:
        t = Thread(target=connScan, args=(host, int(p)))
        t.start()

if __name__ == '__main__':
    parser = optparse.OptionParser('usage %prog -H'+'<target host> -p <target port>')
    parser.add_option('-H', dest='host', type='string', help='specify target host')
    parser.add_option('-p', dest='ports', type='string', help='specify target ports separated by comma')
    (options, args) = parser.parse_args()
    host = options.host
    ports = str(options.ports).split(', ')
    if (host==None) | (ports[0]==None):
        print(parser.usage)
        exit(0)

    portScan(host, ports) 