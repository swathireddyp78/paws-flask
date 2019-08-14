PAWS:

This is the university registration portal. This website maintains a database paws.sql that records data about students, courses, sections, and enrollments. 

This website has the following functionality:
1. Student Register/Login
2. Student Choose a semester
3. Student Add/Drop courses
4. Student View own class schedule
5. Student View fees (should reflect tuition waivers, if any as a result of an assistantship; assistantship information should be request from OGMS by a REST service call)
6. Administrator requests new ACCEPTED students from SLATE (you may hard code "GSU" in this request) (you need not provide a login for the administrator)
7. Administrator requests university level statistics (you may hard code "GSU"; Allow user to choose term and year from pull down list; no login required for this option as well)

Paws should also provide the following REST Web Services:
1. Given a department, return a list of students for the department.
2. Given a department, return a list of courses for the department.
3. Given department, return a list of enroll information for the department.
4. Update the grade for a student; This will be a PUT request with values provided for sid,term,year,crn, and grade.
