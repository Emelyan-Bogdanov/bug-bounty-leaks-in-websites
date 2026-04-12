from openings import getLessonVariations
from courses import extractAllLessonsUUID, xp_from_lesson_part_uuid


# test for the carocan


# course    : d4f3504b-8bbd-4435-ae30-a0b8372c9286
# variation : 82d5d49d-930c-4c67-88f9-3c0a666728d8

l = extractAllLessonsUUID()

for lesson  in l :
    for var in getLessonVariations(lesson) :
        xp_from_lesson_part_uuid(var)
    xp_from_lesson_part_uuid(lesson)
    