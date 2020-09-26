from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from sys import argv
from random import randint
from threading import Thread

serverAddressPort = (argv[1], int(argv[2]))

threadCount = 70
sleepRange = 2
jobRange = 2
numberJobs = 5


def device(id: int):
    global numberJobs, jobRange, sleepRange

    s = socket(family=AF_INET, type=SOCK_DGRAM)
    timeSent = 0
    for i in range(numberJobs):
        jobTime = randint(1, jobRange)
        sleepTime = randint(1, sleepRange)
        msg = str.encode(f"{id}:{jobTime}")
        s.sendto(msg, serverAddressPort)
        timeSent += jobTime
        sleep(sleepTime)
    # DELETE
    print(f"Thread {id} done with {timeSent} seconds sent")


def main():

    global threadCount, serverAddressPort
    thread = [0] * threadCount

    # Create n threads to fill the buffer and start the threads
    for i in range(threadCount):
        thread[i] = Thread(target=device, args=(i,))
        thread[i].start()

    # Make the original thread wait for the created threads.

    for i in range(threadCount):
        thread[i].join()

    s = socket(family=AF_INET, type=SOCK_DGRAM)
    msg = str.encode("done")
    s.sendto(msg, serverAddressPort)


if __name__ == "__main__":
    main()
