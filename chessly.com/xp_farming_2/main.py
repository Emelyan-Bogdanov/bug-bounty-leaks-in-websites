from funcs import getOpenningCourses, getCookies, getLegacyCourses


cookies = getCookies()

# extract all lessons
opLessons = getOpenningCourses(cookies)
LegacyLessons = getLegacyCourses(cookies)

# group all of them
allLessons = opLessons + LegacyLessons

