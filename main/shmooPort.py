import socket
import threading
import time
import sys

PORTS = [21, 22, 53, 80, 443]  # You can add more ports. but then find how you ping them
                               # in SERVICE_GET & their vulnerabilities 
                               # in VULNERABILITIES

results_lock = threading.Lock()  # This makes it so results_lock is limited to only one thread? 
                                 # I don't know exactly but the entire code doesn't work without it

SERVICE_GET = {
    21: lambda ip, s: s.sendall(b"USER anonymous\r\n"),
    22: lambda ip, s: s.sendall(b"SSH-2.0-Test\r\n"),
    53: lambda ip, s: s.sendall(b"GET /version\r\n"),
    80: lambda ip, s: s.sendall(b"HEAD / HTTP/1.1\r\nHost: {ip}\r\n\r\n"),
    443: lambda ip, s: s.sendall(b"HEAD / HTTP/1.1\r\nHost: {ip}\r\n\r\n"),
}

VULNERABILITIES = {  # => I did originally want to make this into a separate txt file outside the script but I am tired.
    21: [
        "1. Plain Text Authentication",
        "2. Anonymous Access",
        "3. Directory Traversal",
        "4. Buffer Overflow",
        "5. Malware Uploads",
        "6. Default Configuration Weaknesses"
    ],
    22: [
        "1. Leaked SSH Keys",
        "2. Brute-Forcing Credentials"
    ],
    53: [
        "1. Query Injection",
        "2. DDoS Attacks"
    ],
    80: [
        "1. Cross-site Scripting",
        "2. SQL Injections",
        "3. DDoS Attacks"
    ],
    443: [
        "1. Heartbleed (CVE-2014-0160)",
        "2. CCS (CVE-2014-0224)",
        "3. Secure Renegotiation (CVE-2009-3555)",
        "4. CRIME, TLS (CVE-2012-4929)",
        "5. BREACH (CVE-2013-3587)",
        "6. POODLE, SSL (CVE-2014-3566)",
        "7. FREAK (CVE-2015-0204)",
        "8. DROWN (CVE-2016-0800, CVE-2016-0703)",
        "9. LOGJAM (CVE-2015-4000)",
        "10. BEAST (CVE-2011-3389)",
        "11. RC4 (CVE-2013-2566, CVE-2015-2808)"
    ]
}

def connect(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => This took me half an hour to figure out IPV4 is socket.AF_INET and TCP/UDP is socket.SOCK_STREAM
        s.settimeout(1)
        s.connect((ip, port))
        return s
    except (socket.timeout, socket.error):
        return None

def get_service(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))

        if port in SERVICE_GET:
            SERVICE_GET[port](ip, s)

        banner = s.recv(2048).decode('utf-8', errors='ignore')  # => For more data increase the bytes.
        s.close()
        return banner.strip() if banner else None  #=in python this is called ternary operator. / (It just clears stuff)
    except socket.error:
        return None
    except Exception as e:
        print(f"\nError retrieving banner from port {port}: {e}")
        return None

def scan_port(ip, port, open_ports):
    if connect(ip, port):
        with results_lock:
            open_ports.append(port)

def enumerate_services(ip, open_ports):
    service_banners = {}
    for i, port in enumerate(open_ports):
        sys.stdout.write(f"\rEnumerating services on port {port}... ({i + 1}/{len(open_ports)}) \n")
        sys.stdout.flush()
        banner = get_service(ip, port)
        service_banners[port] = banner if banner else "\nNo banner received or timed out"
        time.sleep(1.5)
    sys.stdout.write("\n")
    return service_banners

def show_vulnerabilities(open_ports):
    print("\nKnown Vulnerabilities for Detected Services:")
    for port in open_ports:
        if port in VULNERABILITIES:
            print(f"\nPort {port}:\n " , end = " ")
            time.sleep(1)
            for vuln in VULNERABILITIES[port]:
                print(f"  - {vuln}")
                time.sleep(0.1)
        else:
            print(f"\nPort {port}: No known vulnerabilities found.")

def main():
    while True:
        open_ports = []
        ip = input("\nEnter IP to scan (Type 'exit' to exit): \n")

        if ip.lower() == 'exit':
            time.sleep(0.4)
            print("Thank", end = " ")
            time.sleep(0.4)
            print("you", end = " ")
            time.sleep(0.4)
            print("for", end = " ")
            time.sleep(0.4)
            print("whatever", end = " ")
            time.sleep(0.4)
            print("this", end = " ")
            time.sleep(0.4)
            print("thing", end = " ")
            time.sleep(0.4)
            print("was")

            time.sleep(3)

            print("This was made as a challenge", end = " ")
            time.sleep(1)
            print("to ''", end = " ")
            time.sleep(1)
            print("by shmoo", end = " ")
            time.sleep(1)
            print("the expert iPad father")
            time.sleep(1)                                                                        
            print("                                'immortalnot'                                ")
            time.sleep(2)
            print("Shmoo triggered my competitive nature and made me research about:")
            time.sleep(3)
            print("Port Scanning")
            time.sleep(0.5)
            print("Multi-Threading")
            time.sleep(0.5)
            print("Socket Library")
            time.sleep(1.5)
            print("Service Detecting.") # => I have no idea if this actually is working or effecient
            time.sleep(2)
            print("I thank you Shmoo for making me have to get up and do a lot.")
            time.sleep(1)
            print("This was a very cool project to work on")
            time.sleep(3)
            print("But now what? What's the next objective?", end = "\r") 
            time.sleep(1)
            print("Mr Director?")
            time.sleep(2)


            break

        print("\nScanning ports...\n")
        threads = []

        for port in PORTS:
            thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if open_ports:
            print("\nOpen ports found:")
            for port in open_ports:
                print(f"Port {port} is open\n")
                time.sleep(1)

            service_banners = enumerate_services(ip, open_ports)
            print("\nService Information:")
            for port, banner in service_banners.items():
                print(f"Port {port}: {banner}\n")
                time.sleep(1)
            show_vulnerabilities(open_ports)
        else:
            print("\nNo open ports found.\n")

if __name__ == "__main__":
    main()
