
from setuptools import setup, find_packages

# try:
#     REQUIRES = list()
#     f = open("requirements.txt", "rb")
#     for line in f.read().decode("utf-8").split("\n"):
#         line = line.strip()
#         if "#" in line:
#             line = line[: line.find("#")].strip()
#         if line:
#             REQUIRES.append(line)
# except:
#     print("'requirements.txt' not found!")
#     REQUIRES = list()


setup(name='rlsd',
      version='0.1',
      include_package_data=True,
      description='RL Sentiment Stock Trading',
      author='Rick',
      author_email='rige3027@colorado.edu',
      url='https://github.com/r3g2/FinRL',
      packages=find_packages(),
     )