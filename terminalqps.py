#!/usr/bin/python3
# Author: [a-ghost-named-x]
# Date: [02/23/23]
# This is a GIT test :) 

import socket
import threading
from queue import Queue
from urllib.parse import urlparse
import time
import random

def port_scan(port, host, open_ports):
    """Scan the specified port on the given host and add to the list of open ports if successful.
    Args:
        port (int): Port number to scan.
        host (str): Host to scan the port on.
        open_ports (list): A list of open ports.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
    except Exception:
        pass
    finally:
        s.close()

def threader(queue, host, open_ports):
    """Retrieve a port number from the queue, scan it and add to the list of open ports if successful.
    Args:
        queue (Queue): A queue of port numbers to scan.
        host (str): Host to scan the ports on.
        open_ports (list): A list of open ports.
    """
    while True:
        try:
            port = queue.get(timeout=1)
            port_scan(port, host, open_ports)
            queue.task_done()
            time.sleep(0.1)  # add a delay between scans
        except:
            pass

def scan_ports(target):
    """Scan the specified ports on the specified host and display the open ports."""
    try:
        parsed_url = urlparse(target)
        if parsed_url.netloc:
            host = parsed_url.netloc
        else:
            host = target
    except Exception:
        print("Invalid URL or IP address")
        return

    # Commonly used ports to scan
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
    random.shuffle(common_ports)
    # Sort the list of ports to scan
    common_ports.sort()

    open_ports = []

    # Display "Scanning..." message
    print("Scanning...")

    # Limit the number of threads to 3
    max_threads = 3
    thread_pool = []
    queue = Queue()
    for i in range(max_threads):
        t = threading.Thread(target=threader, args=(queue, host, open_ports))
        t.daemon = True
        t.start()
        thread_pool.append(t)

    for port in common_ports:
        queue.put(port)

    queue.join()

    open_ports.sort()

    # Remove duplicates from open_ports list
    open_ports = list(set(open_ports))

    # Display the results
    if open_ports:
        print(f"Open ports for {host}: {open_ports}")
    else:
        print(f"No open ports found for {host}")

if __name__ == '__main__':
    target = input("Enter the target (IP or URL): ")
    scan_ports(target)
