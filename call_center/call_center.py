"""
call_center

Here's the logic to work with the call center priority queue, that takes one archive of messages and read them, then it priorizes the cliente request and takes an agent to resolve the request of the client.
"""
from call_center_queue import CallCenterQueue
from messages import Message


def enqueue_messages(path: str):
    with open(path, 'r') as message_1:
        messages_list = message_1.readlines()
        messages_list = [msj.rstrip() for msj in messages_list]

        messages_queue = CallCenterQueue()

        for index in range(len(messages_list)):
            messages_queue.enqueue(Message(messages_list[index]))

        message_1.close()
    
    return messages_queue


if __name__ == "__main__":
    test1_path = 'data/messages_test1.txt'
    test2_path = 'data/messages_test2.txt'
    test3_path = 'data/messages_test3.txt'

    test1_queue = enqueue_messages(test1_path)
    test1_queue = enqueue_messages(test2_path)
    test1_queue = enqueue_messages(test3_path)