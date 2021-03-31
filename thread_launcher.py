import thread
import time

thread_queue = []
completion_map = dict()

def method1(gid):
    print("thread 1-" + str(gid))
    time.sleep(2)
    enqueue_subsequent_task(method2, gid)

def method2(gid):
    print("thread 2-" + str(gid))
    time.sleep(2)
    print(gid)
    completion_map[gid] = True

def enqueue_subsequent_task(method, gid, args = ()):
    thread_queue.append((method, (gid,) + args))

def add_task_group(gid, args = ()):
    thread_queue.append((method1, (gid,) + args))
    completion_map[gid] = False

add_task_group(1)
add_task_group(2)

try:
    going = True
    while going:
        going = False
        if len(thread_queue) > 0:
            new_boi = thread_queue.pop(0)
            _thread.start_new_thread(new_boi[0], new_boi[1])
        for key in completion_map.keys():
            if not completion_map[key]:
                going = True
except Exception as e:
    print(e)
