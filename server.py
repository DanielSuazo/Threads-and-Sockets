from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from sys import argv
from random import randint
from threading import Thread, Lock

serverAddressPort = ("localhost", int(argv[1]))
queueLock = Lock()
producerDone = False
consumerDone = False
queue = []
bufferSize = 1024
timeList = {}


def consumer():
    global producerDone, queue, queueLock, timeList
    while(not producerDone or len(queue) > 0):
        try:
            queueLock.acquire()
            data = queue.pop(0)
            queueLock.release()
            client = int(data[0])
            time = int(data[1])
            try:
                timeList[client] += time
            except KeyError:
                timeList[client] = time
            # print(f"sleeping for client {client} for {time} seconds")
            sleep(time)
        except IndexError:
            queueLock.release()
            pass


def producer():
    global producerDone, queue, serverAddressPort, queueLock
    s = socket(family=AF_INET, type=SOCK_DGRAM)
    s.bind(serverAddressPort)
    while (not producerDone):
        bytesAddress = s.recvfrom(bufferSize)
        message = bytesAddress[0].decode("utf-8")
        if (message == "done"):
            producerDone = True
        else:
            data = (message.split(sep=":")[0], message.split(sep=":")[1])

            # Enter critical region (queue)
            queueLock.acquire()
            for i in range(len(queue)):
                if (data[1] > queue[i][1] and i+1 > len(queue) and data[1] > queue[i+1][1]):
                    pass
                else:
                    queue.insert(i+1, data)
                    break
            else:
                queue.insert(-1, data)
            queueLock.release()
            # Exit critical region (queue)


def main():
    global timeList
    produce = Thread(target=producer, args=())
    consume = Thread(target=consumer, args=())
    produce.start()
    consume.start()

    produce.join()
    consume.join()

    for key in timeList:
        print(f"Client {key} took {timeList[key]} seconds of CPU time")


if __name__ == "__main__":
    main()
