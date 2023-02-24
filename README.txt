qps7

This is a simple port scanner script that scans specified ports on a specified host and displays the open ports.


How it works
The user enters the target IP or URL into an entry field and clicks a button to start the scan. The script then scans commonly used ports, shuffling the order of the ports to be scanned to increase randomness. This script utilizes threading to improve performance and limits the number of threads to 3.


After the scan is complete, the script removes duplicates from the list of open ports and displays the results in the text widget.

The GUI is built using the Tkinter library, with a label for the target input, an entry field for the user to enter the target IP or URL, a "Scan" button to initiate the scan, a "Clear Results" button to clear the text widget where the results are displayed, and a text widget to display the results.

Requirements
This script requires the following libraries to be installed:

socket
tkinter
threading
queue
urllib.parse
time
random
Usage


To use this script, simply run it and enter the target IP or URL into the entry field. Then, click the "Scan" button to start the scan. The results will be displayed in the text widget. To clear the results, click the "Clear Results" button.

Author: GanndyD404
