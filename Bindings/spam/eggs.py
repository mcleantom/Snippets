from ctypes import cdll
from pathlib import Path


def wrap_bar():
    foo = cdll.LoadLibrary(str(Path(__file__).with_name('libfoo.dylib')))
    return foo.bar()
