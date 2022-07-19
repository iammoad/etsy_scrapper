import time


def page_loader(func):
    def wrapper(*args, **kwargs):
        counter = 0
        while 1:
            try:
                func(*args, **kwargs)
                break
            except Exception as exception:
                if counter > 30:
                    exit("error while loading page . Please check you internet connection.")
                counter += 1
                time.sleep(1)
                print(f"{exception.__name__}\nretrying ...")
    return wrapper
