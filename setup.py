from distutils.core import setup, Extension

setup(name = "superfastmatch",
      version = "0.1",
      ext_modules = [Extension("superfastmatch.fast", ["src/superfastmatch/superfastmatch.c"])],
      packages=['superfastmatch'],
      package_dir={'superfastmatch': 'src/superfastmatch'},
      )

