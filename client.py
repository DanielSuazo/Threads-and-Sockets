from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from sys import argv
from random import randint
from threading import Thread

serverAddressPort = (argv[1], int(argv[2]))

threadCount = 100
sleepRange = 2
jobRange = 10
numberJobs = 4


def device(id: int):
    global numberJobs, jobRange, sleepRange
    # Create socket
    s = socket(family=AF_INET, type=SOCK_DGRAM)

    for i in range(numberJobs):
        # Generate job time and sleep time
        jobTime = randint(1, jobRange)
        sleepTime = randint(1, sleepRange)

        # Create, encode and send message
        msg = str.encode(f"{id}:{jobTime}")
        s.sendto(msg, serverAddressPort)

        sleep(sleepTime)


def main():
    global threadCount, serverAddressPort
    thread = [0] * threadCount

    # Create n threads to fill the buffer and start the threads
    for i in range(threadCount):
        thread[i] = Thread(target=device, args=(i,))
        thread[i].start()

    # Make the original thread wait for the created threads.]
    for i in range(threadCount):
        thread[i].join()

    print("All done!")


if __name__ == "__main__":
    main()
