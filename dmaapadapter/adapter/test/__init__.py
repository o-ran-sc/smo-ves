import os
import sys

PROJECT_PATH = os.getcwd()
PROJECT_PATH = PROJECT_PATH[:PROJECT_PATH.rfind('/')]
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"code"
)
sys.path.append(SOURCE_PATH)