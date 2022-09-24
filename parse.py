from bs4 import BeautifulSoup
# import requests


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
