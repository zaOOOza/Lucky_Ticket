import time

from multiprocessing import Process, Queue
from threading import Thread

range1 = [000000, 250000]
range2 = [250001, 500000]
range3 = [500001, 750000]
range4 = [750001, 999999]


class ThreadWithResult(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.get_result = target(*args, **kwargs)

        super().__init__(group=group, target=function, name=name, daemon=daemon)


class MultiprocessorWithResult:
    def __init__(self):
        self.processes = []
        self.queue = Queue()

    @staticmethod
    def _wrapper(func, queue, args, kwargs):
        ret = func(*args, **kwargs)
        queue.put(ret)

    def run(self, func, *args, **kwargs):
        args2 = [func, self.queue, args, kwargs]
        p = Process(target=self._wrapper, args=args2)
        self.processes.append(p)
        p.start()

    def wait(self):
        rets = []
        for p in self.processes:
            ret = self.queue.get()
            rets.append(ret)
        for p in self.processes:
            p.join()
        return rets[0]


def thred_value(*args):
    jobs = []
    start = time.time()
    for i in args:
        thred = ThreadWithResult(target=ranger, args=(i,))
        jobs.append(thred)
        thred.start()
    for value in jobs:
        value.join()
    end = time.time()
    print('4 thread time', end - start)
    for i, res in enumerate(jobs):
        print(f'{args[i]} lucky:{len(res.get_result)}')


def process_value(*args):
    jobs = []
    result = []
    start = time.time()
    for i in args:
        proc = MultiprocessorWithResult()
        jobs.append(proc)
        proc.run(ranger, i)
    for poces in jobs:
        result.append(poces.wait())
    end = time.time()
    print('4 process time', end - start)
    for i, res in enumerate(result):
        print(f'{args[i]} lucky:{len(res)}')


def ranger(r):
    ticket = []

    for number in [int(i) for i in range(r[0], r[1] + 1)]:
        if lucky(number):
            ticket.append(number)
    return ticket


def lucky(num):
    res1 = sum(int(i) for i in str(num)[:3])
    res2 = sum(int(i) for i in str(num)[3:])
    return True if res1 == res2 else False


if __name__ == '__main__':
    thred_value(range1, range2, range3, range4)
    process_value(range1, range2, range3, range4)
