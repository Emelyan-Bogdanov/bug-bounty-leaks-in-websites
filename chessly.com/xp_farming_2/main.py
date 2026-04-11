from funcs import getOpenningCourses, getCookies, getLegacyCourses, getProgressLesosns, readLesson, countAllLessonsVariations
import time

cookies = getCookies()

# extract all lessons
opLessons = getOpenningCourses(cookies)
LegacyLessons = getLegacyCourses(cookies)
progessLessons = getProgressLesosns(cookies)

# group all of them
allLessons = opLessons + LegacyLessons + progessLessons

# count all existant lessons
# print(countAllLessonsVariations(cookies))
# exit()

# start reading
for lesson in range(len(allLessons)):
    print(f"============= [{lesson}] ==========")
    readLesson(allLessons[lesson], cookies)
    time.sleep(1)
