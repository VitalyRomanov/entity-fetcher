from distutils.core import setup

requirements = [
      "nltk",
      "gensim",
      "pymorphy2"
]

setup(name='fetcher',
      version='0.1',
      py_modules=['fetcher'],
      install_requires=requirements,
      extras_require={
      },
      scripts=[
      ],
      )
