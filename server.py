from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from sys import argv
from random import randint
from threading import Thread, Lock, Semaphore


ip = "localhost"
queueLock = Lock()
emptyQueue = Semaphore()
producerDone = False
queue = []
bufferSize = 1024
timeList = {}
serverAddressPort = (ip, int(argv[1]))


def consumer():
    global producerDone, queue, queueLock, timeList, emptyQueue

    # Loop until producer recieves the "done" command and then until the queue is empty
    while(not producerDone or len(queue) > 0):

        # Block thread if queue is empty
        # Dont ask how it just works
        # La clear if you dont understand it text me, I swear it works
        emptyQueue.acquire()
        if (not producerDone or len(queue) == 0):
            emptyQueue.acquire()

        # Enter critical region (queue)
        queueLock.acquire()
        # Just in case the "done" message is done
        try:
            data = queue.pop(0)
        except:
            pass
        queueLock.release()
        # Enter critical region (queue)

        client = data[0]
        time = data[1]

        # Update timeList
        try:
            timeList[client] += time
        except KeyError:
            timeList[client] = time

        # Execute the job and release semaphore (sleep lmao)
        emptyQueue.release()
        sleep(time)
        # Catch any error with popping from the queue and release lock


def producer():
    global producerDone, queue, serverAddressPort, queueLock, emptyQueue

    # Create and bind socket
    s = socket(family=AF_INET, type=SOCK_DGRAM)
    s.bind(serverAddressPort)

    while (not producerDone):
        # Recieve message and decode to string
        bytesAddress = s.recvfrom(bufferSize)
        message = bytesAddress[0].decode("utf-8")

        # Test if client has completed
        if (message == "done"):
            producerDone = True
            emptyQueue.release()
        else:
            # Create data tuple
            data = (int(message.split(sep=":")[0]), int(
                message.split(sep=":")[1]))

            # Enter critical region (queue)
            queueLock.acquire()
            # Insert data to queue
            for i in range(len(queue)):
                if (data[1] < queue[i][1]):
                    queue.insert(i, data)
                    break
            else:
                queue.append(data)
            # Release semaphore blocking the consumer
            emptyQueue.release()
            queueLock.release()
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
    for key in timeList:
        print(f"Client #{key} took {timeList[key]} seconds of CPU time")


if __name__ == "__main__":
    main()
