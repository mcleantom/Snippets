import numpy.ctypeslib as ctl
import ctypes

libname = 'testlib.so'
libdir = './'
lib = ctl.load_library(libname, libdir)

add_one = lib.add_one
add_one.argtypes = [ctypes.c_int]
value = 5
results = add_one(value)
print(results)