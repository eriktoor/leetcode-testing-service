import multiprocessing

from multiprocessing import Process, Manager

import time 

def func(a,b): 
    time.sleep(4)

    print(a+b)
    # ret["ans"] = (a+b)
    # print(ret)
    return a + b 

def closure(func, mem, info, args): 
    print(func, mem, info, args)
    ret = func(*args)
    mem[info["filename"]] = ret
    print(mem)

def start_get_page(args, function, timeout):
    # ret = []
    ret = {}
    ret["filename"] = "user1"
    manager = Manager()
    mem = manager.dict()
    p = multiprocessing.Process(target=closure, args=(func, mem, ret, args))
    p.start()
    p.join(timeout)
    if p.is_alive():
        # stop the downloading 'thread'
        p.terminate()
        print("in here")
        # and then do any post-error processing here
        print(mem)

    return mem


if __name__ == "__main__":

    timeout = 4

    args = (1,2)

    func = func

    ret = start_get_page(args, func, timeout)
    print(ret)
    # print(ret)
