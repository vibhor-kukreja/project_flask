import concurrent.futures


def process_executor_in_chunks(func, context, chunk_size=100):
    """
    Concurrent processing using Processes. Suited for computational operations
    :param func: function that needs to be call concurrently
    :param context: list passed to be processed by the function
    :param chunk_size: break down the list with respect to the chunk size for
    for concurrent processing
    :return: On success returns True


    Example::
    import time

    def do_something(x):
        time.sleep(x)
        print("do_something called ", x)

    process_executor_in_chunks(do_something, [1,2,3,4,5], chunk_size=2)
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        try:
            executor.map(func, context, chunksize=chunk_size)
        except Exception as ex:
            print(ex)
            raise RuntimeError(ex)
    return True


def thread_executor_in_chunks(func, context, chunk_size=100):
    """
    Concurrent processing using Threads. Suited for IO operations.
    :param func: function that needs to be call concurrently
    :param context: list passed to be processed by the function
    :param chunk_size: break down the list with respect to the chunk size for
    for concurrent processing
    :return: On success returns True


    Example::
    import time

    def do_something(x):
        time.sleep(x)
        print("do_something called ", x)

    thread_executor_in_chunks(do_something, [1,2,3,4,5], chunk_size=2)
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            executor.map(func, context, chunksize=chunk_size)
        except Exception as ex:
            print(ex)
            raise RuntimeError(ex)
    return True
