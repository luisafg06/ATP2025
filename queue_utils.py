# queue_utils.py
"""
Funções para gestão de filas de eventos (heap) e fila de espera (FIFO)
"""
import heapq


def enqueue(q, ev):
    heapq.heappush(q, ev)
    return q


def dequeue(q):
    ev = heapq.heappop(q)
    return ev, q


def queue_empty(q):
    return len(q) == 0
