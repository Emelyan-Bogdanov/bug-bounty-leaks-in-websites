from funcs import getOpenningCourses, getCookies, getLegacyCourses, getProgressLesosns, readLesson, countAllLessonsVariations
from funcs import ChesslyClient
import time
import random


if __name__ == "__main__":
    client = ChesslyClient(
        email="eldoradogpt2025@gmail.com",
        password="JT1215060000",
        interval=1.5
    )
    client.read_all_lessons()
