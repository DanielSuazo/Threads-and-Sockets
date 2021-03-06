Scheduled compute server simulator by Daniel Suazo Arroyo

client.py simulates threadCount number of devices sending jobs in to a server whereas server.py accepts the messages until client sends a done message. The simulated compute server performs the jobs sent and then prints the amount of compute time each device used.

Requirements:
Python 3

Setup:
In client.py there are a few integer global variables you can change: threadCount, sleepRange, jobRange and numberJobs.

threadCount changes the number of deviced to be simulated.

sleepRange changes the range of time which each client will sleep for in between sending jobs.

jobRange changes the range of time that the jobs generated by each client will take (random from 1 to jobRange).

numberJobs changes the number of jobs that each device will send.

If you change threadCount or numberJobs in client.py you must change numberJobs in server.py according to the formula given in the comments of said file.


How to use:

1. Run "server.py <port>".
2. Run "client.py <ip> <port>" (if both files are being run on the same machine, ip is localhost).
3. Wait for client.py to send messages to server.py and for server.py to compute everything.

If you wish to run the server on a different machine, change the global variable named "ip" from localhost, to the server's ip address and run as normal

References used:
https://pythontic.com/modules/socket/udp-client-server-example

Eduardo Santin
Gabriel Santiago
Prof. Jose Ortiz