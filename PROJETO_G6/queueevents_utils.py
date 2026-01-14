def enqueue(q, ev):
    q.append(ev)
    q.sort(key=lambda x: x[0])
    return q

def dequeue(q):
    if len(q) == 0:
        return None, q
    ev = q.pop(0)  
    return ev, q

def queue_empty(q):
    return len(q) == 0
