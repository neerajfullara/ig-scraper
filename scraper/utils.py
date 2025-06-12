import time
import random
import functools

def human_scroll(driver, steps=3):
    for _ in range(steps):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(random.uniform(1.5, 3))

def retry(max_retries=3, delay=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    wait = delay * (2 ** attempt)
                    print(f"Error: {e} — retrying in {wait:.1f}s...")
                    time.sleep(wait)
            raise Exception(f"Failed after {max_retries} retries")
        return wrapper
    return decorator
