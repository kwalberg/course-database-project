import requests, re, MySQLdb
import html
cnx = MySQLdb.connect(user='root', password='password',
                              host='aa10jiukchq7w6v.ci4kcng77lcj.us-east-2.rds.amazonaws.com',
                              database='course_db')

cursor = cnx.cursor()

response = requests.get("https://www.macalester.edu/registrar/schedules/2018fall/class-schedule/")
page_source = response.text.encode('latin-1','ignore').decode('latin-1')

course_list_html = re.search('<div class="class-schedule-wrapper">(.*)</div><!-- .class-schedule-wrapper -->', page_source, flags=re.DOTALL).group(1)

departments = re.findall('<td class="class-schedule-course-number">(.*)&nbsp;.*</td>', course_list_html)
course_ids = re.findall('<td class="class-schedule-course-number">.*&nbsp;(.*)</td>', course_list_html)
course_titles = re.findall('<td class="class-schedule-course-title">(.*)</td>', course_list_html)
instructors = re.findall('<td class="class-schedule-label"><span>Instructor: </span>(.*)</td>', course_list_html)
descriptions = re.findall('<div id="crs[0-9]+" class="expandable-body collapsed">\s+<p>\s+(?:<br/>)?(.*)\r\s+</p>', course_list_html)
days = re.findall('<td class="class-schedule-label"><span>Days: </span>(.*)</td>', course_list_html)
times = re.findall('<td class="class-schedule-label"><span>Time: </span>(.*)</td>', course_list_html)
gen_eds = re.findall('<p><strong>General Education Requirements:</strong><br>\s*(.*)<br />', course_list_html)
dist_reqs = re.findall('<p><strong>Distribution Requirements:</strong><br>\s*(.*)<br />', course_list_html)

for i in range(0, len(course_ids)):
    department = departments[i]
    course_id = course_ids[i]
    course_title = html.escape(course_titles[i])
    instructor = instructors[i]
    description = html.escape(descriptions[i])
    day = days[i]
    time = times[i]
    #gen_ed = gen_eds[i]
    #dist_req = dist_reqs[i]

    #query = 'INSERT INTO courseSite_course (course_id, full_title, course_number, department, description, instructor, days, times) '
    #query += "VALUES ('%s','%s',%s,'%s','%s','%s','%s','%s');" %(department + " " + course_id, course_title, course_id.split("-")[0], department, description, instructor, day, time)
    query = "UPDATE courseSite_course SET times='%s' WHERE course_id='%s'"%(time,department + " " + course_id)
    print(query)
    cursor.execute(query)

cnx.commit()
cnx.close()
