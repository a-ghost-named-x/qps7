#!/usr/bin/python3
# Author: [a-ghost-named-x]
# Date: [02/23/23]

import socket
import tkinter as tk
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

def scan_ports():
    """Scan the specified ports on the specified host and display the open ports."""
    global host, open_ports
    target = entry_target.get()
    try:
        parsed_url = urlparse(target)
        if parsed_url.netloc:
            host = parsed_url.netloc
        else:
            host = target
    except Exception:
        text_results.insert(tk.END, "Invalid URL or IP address\n")
        return

    # Commonly used ports to scan
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
    random.shuffle(common_ports)
    # Sort the list of ports to scan
    common_ports.sort()

    open_ports = []

    # Display "Scanning..." message
    text_results.insert(tk.END, "Scanning...\n")
    text_results.update()

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

    # Remove "Scanning..." message
    text_results.delete("end-2l", tk.END)

    # Display the results
    if open_ports:
        text_results.insert(tk.END, f"Open ports for {host}: {open_ports}\n")
    else:
        text_results.insert(tk.END, f"No open ports found for {host}\n")


def clear_results():
    """Clear the text in the text widget where the results are displayed."""
    text_results.delete("1.0", tk.END)


root = tk.Tk()
root.title("Port Scanner")
root.geometry("500x300")
root.configure(bg='#1C2331')

frame = tk.Frame(root, bg='#1C2331')
frame.pack(padx=10, pady=10)

label_target = tk.Label(frame, text="Target (IP or URL):", font=("Arial", 14), bg='#1C2331', fg='#BA55D3')

label_target.grid(row=0, column=0, padx=5, pady=5)

entry_target = tk.Entry(frame, font=("Arial", 14), bg='#353935', fg='#00FF00', insertbackground='#00FF00')
entry_target.grid(row=0, column=1, padx=5, pady=5)

button_scan = tk.Button(frame, text="Scan", font=("Arial", 14), command=scan_ports, bg='#BA55D3', fg='#1C2331')
button_scan.grid(row=3, column=0, padx=5, pady=5)

button_clear = tk.Button(frame, text="Clear Results", font=("Arial", 14), command=clear_results, bg='#BA55D3', fg='#1C2331')
button_clear.grid(row=3, column=1, padx=5, pady=5)

root.bind('<Return>', lambda event=None: scan_ports())

text_results = tk.Text(root, font=("Courier New", 12), bg='#1C2331', fg='#00FF00')
text_results.pack(padx=10, pady=10)

root.mainloop()
