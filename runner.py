import os, sys
import threading
import queue

def callMe(incomingFun, daemon=False):
    def execute(_queue, *args, **kwargs):
        result=incomingFun(*args, **kwargs)
        _queue.put(result)

    def wrap(*args, **kwargs):
        _queue=queue.Queue()
        _thread=threading.Thread(target=execute, args=(_queue,)+args, kwargs=kwargs)
        _thread.daemon=daemon
        _thread.start()
        _thread.result_queue=_queue        
        return _thread

    return wrap


# @callMe
# def localFunc(x):
#     import time
#     x = x + 5
#     time.sleep(5)
#     return x

# thread=localFunc(10)

# # this blocks, waiting for the result
# result = thread.result_queue.get()
# print result