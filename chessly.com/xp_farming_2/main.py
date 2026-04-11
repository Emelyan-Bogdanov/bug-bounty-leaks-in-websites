from funcs import getOpenningCourses, getCookies, getLegacyCourses, getProgressLesosns, readLesson, countAllLessonsVariations
from funcs import ChesslyClient
import time
import random


# if __name__ == "__main__":
#     client = ChesslyClient(
#         email="eldoradogpt2025@gmail.com",
#         password="JT1215060000",
#         interval=1.5
#     )

#     # Examples:
#     client.read_all_lessons()
#     # print(client.count_all_variations())
#     # print(client.get_opening_courses())

print("legacy courses")
lessons = getProgressLesosns()
for l in lessons:
    readLesson(l)

print("Reading openings")