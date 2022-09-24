from bs4 import BeautifulSoup
from format import *


def parse_Homepage(text):

    courses = []
    studentName = ''

    # Parse the homepage
    soup = BeautifulSoup(text, 'html.parser')
    
    try:
    # Get the student name
      helloTitle = soup.select(
          '#___01 > tr:nth-child(1) > td:nth-child(3) > table > tr:nth-child(2) > td > table > tr:nth-child(1) > td')[0].text
      studentName = helloTitle.split('您好! ')[-1].split('同學')[0].strip()
    except: pass

    # get courses
    try:
      courseListSoup = soup.select(
          '#___01 > tr:nth-child(4) > td:nth-child(1) > table:nth-child(1) > tr:nth-child(2) > td > table:nth-child(1) > tr')
      
      for ele in courseListSoup:
          course_ID = ele.select('td')[0].text.strip()
          course_name = ele.select('td')[1].text.strip()
          course_att = ele.select('td > img')[0].attrs['title'].strip()
          courses.append({
              'course_ID': course_ID,
              'course_name': course_name,
              'course_att': course_att
          })
    except: pass

    info = {
        'studentName': studentName,
        'courses': courses
    }
    return info


def parse_CampusQueryPage(text):
    soup = BeautifulSoup(text, 'lxml')
    campus_soup = soup.select("[name=sch]")[0].find_all("option")
    campus_list = [{'name': campus.text.replace(
        '\xa0', ''), 'schID': campus.get('value')} for campus in campus_soup[1:]]

    department_soup = soup.select("[name=dept1]")[0].find_all("option")
    department_list = [{'name': department.text.split(
        '-')[-1].strip(), 'deptID': department.get('value')} for department in department_soup[1:]]

    schoolType = soup.select("[name=f26]")[0].find_all("option")
    schoolType_list = [{'name': schoolType.text.split(
        '-')[-1].strip(), 'schTypeID': schoolType.get('value')} for schoolType in schoolType[1:]]

    courseType = soup.select('[name=sel]')[0].find_all("option")
    courseType_list = [{'name': courseType.text.split(
        '-')[-1].strip(), 'courseTypeID': courseType.get('value')} for courseType in courseType[1:]]

    data = {
        'campus_list': campus_list
        , 'department_list': department_list
        , 'schoolType_list': schoolType_list
        , 'courseType_list': courseType_list
    }
    return data


def parse_Courses(text):
    all_courses = []
    soup = BeautifulSoup(text, 'lxml')

    # parse data
    course_tags = soup.select('tr')[1:]
    
    for course_tag in course_tags:
        course_data = [(t.text) for t in course_tag.find_all('td')]

        school_type = clean_special_char(course_data[0])
        course_id, course_name = clean_special_char(course_data[1].split(
            ' ')[0]), clean_special_char(course_data[1].split(' ')[1])
        class_id = clean_special_char(course_data[2]).split(' ')[0]
        if len(clean_special_char(course_data[2]).split(' ')) > 1:
            class_name =clean_special_char(course_data[2]).split(' ')[1]
        else: class_name = ''

        # stu_count,stu_limit = -1,int(course_data[3].split('／')[0])
        # teacher_time =  teacher_time_format(course_data[4], course_data[5])
        teacher_list = teacher_format(course_data[4])

        if course_data[4].find("實習") != -1 and course_data[4].find("實習") < course_data[4].find("正課"):
            raise Exception('嘿嘿學校順序跑掉要重寫摟 ' + course_data[4])

        course_grade = clean_special_char(course_data[6])
        classroom,campus = classroomCampus_format(course_data[7])
        units = int(clean_special_char(course_data[9]))
        special_type = clean_special_char(course_data[10])
        comments = course_data[13]

        
        if clean_special_char(course_data[11]) == 'Y':
            isgraduate = True
        elif clean_special_char(course_data[11]) == 'N':
            isgraduate = False
        else:
            raise Exception('error isgraduate  type' +
                            clean_special_char(course_data[11]))


        course_type = clean_special_char(course_data[8])
        # if clean_special_char(course_data[8]) == "通識":
        #     course_type = 0
        # elif clean_special_char(course_data[8]) == "必修":
        #     course_type = 1
        # elif clean_special_char(course_data[8]) == "選修":
        #     course_type = 2
        # elif clean_special_char(course_data[8]) == "教育":
        #     course_type = 3
        # else:
        #     raise Exception('error corse_type ' + clean_special_char(course_data[8]))

        semester = clean_special_char(course_data[12])
        # if clean_special_char(course_data[12]) == "全學年":
        #     semester = 0 
        # elif clean_special_char(course_data[12]) == "上學期":
        #     semester = 1
        # elif clean_special_char(course_data[12]) == "下學期":
        #     semester = 2
        # else:
        #     raise Exception('error semester ' + clean_special_char(course_data[12]))

    
        course = {
            'school_type': school_type,
            'course_id': course_id,
            'course_name': course_name,
            'class_id': class_id,
            'class_name': class_name,
            # 'stu_limit': stu_limit,
            # 'stu_count': stu_count,
            # 'teacher_time': teacher_time,
            'teacher_list': teacher_list,
            'course_grade': course_grade,
            'classroom': classroom,
            'campus':campus,
            'course_type': course_type,
            'units': units,
            'special_type': special_type,
            'isgraduate': isgraduate,
            'semester': semester,
            'comments': comments,
        }

        all_courses.append(course)
    return all_courses