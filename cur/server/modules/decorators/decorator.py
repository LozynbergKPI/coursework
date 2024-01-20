import time

def track_execution_time(func):
    """
    A decorator that tracks and prints the execution time of a wrapped function.

    Args:
    - func (callable): The function to be wrapped.

    Returns:
    - wrapper: The wrapped function.
    """

    def wrapper(*args, **kwargs):
        """
        Calculates and prints the execution time of the wrapped function.

        Args:
        - *args: Positional arguments to be passed to the wrapped function.
        - **kwargs: Keyword arguments to be passed to the wrapped function.

        Returns:
        - result: The result of the wrapped function.
        """
        start_time = time.time()
        print(f"Executing operation '{func.__name__}'...")
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Operation '{func.__name__}' executed in {execution_time:.4f} seconds.")

        return result

    return wrapper
