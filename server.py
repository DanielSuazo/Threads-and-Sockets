from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from sys import argv
from random import randint
from threading import Thread, Lock, Semaphore


ip = "localhost"
numberJobs = 400  # must be equal to threadCount * numberJobs in client.py
queueLock = Lock()
emptyQueue = Semaphore(numberJobs)
fullQueue = Semaphore(0)
queue = []
bufferSize = 1024
timeList = {}
serverAddressPort = (ip, int(argv[1]))


def consumer():
    global queue, queueLock, timeList, emptyQueue, fullQueue

    # Loop until producer recieves the "done" command and then until the queue is empty
    for i in range(numberJobs):

        # Block thread if queue is empty
        fullQueue.acquire()
        # Enter critical region (queue)
        queueLock.acquire()

        data = queue.pop(0)

        # Exit critical region (queue)
        queueLock.release()
        # increment empty
        emptyQueue.release()

        client = data[0]
        time = data[1]

        # Update timeList
        try:
            timeList[client] += time
        except KeyError:
            timeList[client] = time

        # Execute the job (sleep lmao)
        sleep(.1)
        print(f"slept {time} seconds for client {client}")
        # Catch any error with popping from the queue and release lock


def producer():
    global queue, serverAddressPort, queueLock, emptyQueue, fullQueue

    # Create and bind socket
    s = socket(family=AF_INET, type=SOCK_DGRAM)
    s.bind(serverAddressPort)

    for i in range(numberJobs):
        # Recieve message and decode to string
        bytesAddress = s.recvfrom(bufferSize)
        message = bytesAddress[0].decode("utf-8")

        # Create data tuple
        data = (int(message.split(sep=":")[0]), int(
            message.split(sep=":")[1]))

        # Enter critical region (queue)
        emptyQueue.acquire()
        queueLock.acquire()
        # Insert data to queue
        for i in range(len(queue)):
            if (data[1] < queue[i][1]):
                queue.insert(i, data)
                break
        else:
            queue.append(data)
        # Release semaphore blocking the consumer
        queueLock.release()
        fullQueue.release()
        # Exit critical region (queue)


def main():
    global timeList, queue

    # Create and start threads
    produce = Thread(target=producer, args=())
    consume = Thread(target=consumer, args=())
    produce.start()
    consume.start()

    # block main until threads finish
    produce.join()
    consume.join()

    # Print out list of clients and their respecive CPU time used

    for key in sorted(timeList):
        print(f"Client #{key} took {timeList[key]} seconds of CPU time")


if __name__ == "__main__":
    main()
