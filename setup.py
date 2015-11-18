from distutils.core import setup

setup(name='postgres_cloner',
      packages=['postgres_cloner'],
      version='1.0.0',
      description='Python library for cloning postgres tables',
      author='Nimesh Kiran (supported ably by DrCricket)',
      author_email='nimesh.aug11@gmail.com',
      url='https://github.com/nimeshkverma/postgres_cloner',
      download_url='https://github.com/nimeshkverma/postgres_cloner/archive/1.0.tar.gz',
      py_modules=['postgres_cloner'],
      install_requires=['psycopg2'],
      keywords=['postgresql','python'],
      classifiers=[],
      )
