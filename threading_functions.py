import threading
import time


def client(lock):
    with lock:
        print(threading.current_thread().name)
        time.sleep(2)


def client_entery_point():
    lock = threading.Lock()
    client_threads = []
    for i in range(3):
        client_thread = threading.Thread(target=client, kwargs=dict(lock=lock))
        client_threads.append(client_thread)
        client_thread.start()

    for thread in client_threads:
        thread.join()


def tourist(tourist_number, condition):
    with condition:
        condition.wait()
        print(tourist_number)


def boarder_guard(condition):
    for i in range(3):
        with condition:
            condition.notify()
        time.sleep(1)

    time.sleep(1)
    with condition:
        condition.notify_all()


def boarder_guard_entery_point():
    condition = threading.Condition()
    tourists = []
    for i in range(6):
        tourist_thread = threading.Thread(target=tourist, kwargs=dict(tourist_number=i, condition=condition))
        tourists.append(tourist_thread)
        tourist_thread.start()

    time.sleep(3)

    boarder_guard_thread = threading.Thread(target=boarder_guard, kwargs=dict(condition=condition))
    boarder_guard_thread.start()

    for thread in tourists:
        thread.join()

    boarder_guard_thread.join()


def client_2(thread_number, semaphore):
    with semaphore:
        print(thread_number)
        time.sleep(thread_number * 0.5)


def client_2_entery_point():
    client_2_threads = []
    semaphore = threading.Semaphore()

    for i in range(9):
        client_2_thread = threading.Thread(target=client_2, kwargs=dict(thread_number=i, semaphore=semaphore))
        client_2_threads.append(client_2_thread)
        client_2_thread.start()

    for thread in client_2_threads:
        thread.join()


def tourist_2(tourist_number, condition):

    condition.wait()
    print(tourist_number)


def interval_access(condition):
    time.sleep(4)
    condition.set()
    time.sleep(2)
    condition.clear()
    time.sleep(4)
    condition.set()


def boarder_guard_2_entery_point():
    condition = threading.Event()
    boarder_guard = threading.Thread(target=interval_access, kwargs=dict(condition=condition))
    boarder_guard.start()

    tourists = []
    for i in range(9):
        tourist_thread = threading.Thread(target=tourist_2, kwargs=dict(tourist_number=i, condition=condition))
        tourists.append(tourist_thread)
        tourist_thread.start()
        time.sleep(1)

    boarder_guard.join()
    for thread in tourists:
        thread.join()


def roller_coaster(thread_number, barrier):

    try:
        barrier.wait(timeout=4)
    except threading.BrokenBarrierError:
        barrier.reset()
    finally:
        print(thread_number)


def roller_coaster_entery_point():
    roller_coaster_threads = []
    barrier = threading.Barrier(5)

    for i in range(20):
        roller_coaster_thread = threading.Thread(target=roller_coaster, kwargs=dict(thread_number=i, barrier=barrier))
        roller_coaster_threads.append(roller_coaster_thread)
        roller_coaster_thread.start()
        time.sleep(0.5)

    for i in range(20, 30):
        roller_coaster_thread = threading.Thread(target=roller_coaster, kwargs=dict(thread_number=i, barrier=barrier))
        roller_coaster_threads.append(roller_coaster_thread)
        roller_coaster_thread.start()
        time.sleep(1)

    for i in range(30, 35):
        roller_coaster_thread = threading.Thread(target=roller_coaster, kwargs=dict(thread_number=i, barrier=barrier))
        roller_coaster_threads.append(roller_coaster_thread)
        roller_coaster_thread.start()
        time.sleep(2)

    for thread in roller_coaster_threads:
        thread.join()


if __name__ == '__main__':
    print("First")
    client_entery_point()
    print("Second")
    boarder_guard_entery_point()
    print("third")
    client_2_entery_point()
    print("Fouth")
    boarder_guard_2_entery_point()
    print("Fifth")
    roller_coaster_entery_point()