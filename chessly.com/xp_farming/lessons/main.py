from funcs import getCourses, getCookie, getVariations, readOpLesson
import time


cookies = getCookie()


l = getCourses(cookies) + getCourses("legacy")

readOpLesson("b6c43711-79a1-420a-af3d-df4217faeb22")
