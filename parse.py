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
          course_id = ele.select('td')[0].text.strip()
          course_name = ele.select('td')[1].text.strip()
          course_att = ele.select('td > img')[0].attrs['title'].strip()
          courses.append({
              'course_id': course_id,
              'course_name': course_name,
              'course_att': course_att
          })
    except: pass

    info = {
        'studentName': studentName,
        'courses': courses
    }
    return info
