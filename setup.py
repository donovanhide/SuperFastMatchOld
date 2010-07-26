from distutils.core import setup, Extension

setup(name = "superfastmatch",
      version = "0.1",
      ext_modules = [Extension("superfastmatch", ["superfastmatch.c"])])

