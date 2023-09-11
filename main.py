import typing
from typing import Callable, Any

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'


def dec(c: str) -> Callable[[Any], Callable[[Any], None]]:
    def decorator(f):
        def wrapper():
            print(c)
            f()
            print(c)
        return wrapper
    return decorator


def func():
    print('func')


f1 = dec('$')(func)


if __name__ == '__main__':
    f1()
    a = 3


