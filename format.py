import hashlib

def clean_special_char(input_string):
    return ''.join(e for e in input_string if e.isalnum() or e in ['/', ':', ' '])


def teacher_time_format(teacher_string, time_string):
    res = list()
    format_timelist = list()
    teacher_string = clean_special_char(teacher_string).replace(
        '正課', '*正課').replace('實習', '*實習')
    time_list = time_string.split('星期')[1:]

    # format course time
    for t in time_list:
        dayOfWeek = int(t.strip().split(':')[0])
        period_list = list(
            filter(None, (t.strip().split(':')[1].split(' '))[1:-1]))
        format_timelist.append(
            {'dayOfWeek': dayOfWeek, 'period_list': period_list})

    # print(teacher_string)
    for s in teacher_string.split('*')[1:]:
        if '正課' in s:
            res.append({'teacher_name': s.split(':')[1].strip(), 'teacher_hash': hashlib.md5(s.split(':')[1].strip().encode('utf-8')).hexdigest(), 'type': 'main',
                        'course_time': [format_timelist.pop(0)], })
        elif '實習' in s:
            res.append({'teacher_name': s.split(':')[1].strip(
            ), 'teacher_hash': hashlib.md5(s.split(':')[1].strip().encode('utf-8')).hexdigest(), 'type': 'sub', 'course_time': [format_timelist.pop(0)]})
        else:
            raise Exception('error teacher type ' + s)
    while len(format_timelist):
        res[-1]['course_time'].append(format_timelist.pop(0))

    return res


def teacher_format(teacher_string):
    res = list()
    teacher_string = clean_special_char(teacher_string).replace(
        '正課', '*正課').replace('實習', '*實習')

    for s in teacher_string.split('*')[1:]:
        if '正課' in s:
            res.append({'teacher_name': s.split(':')[1].strip(),'teacher_type': 'main'})
        elif '實習' in s:
            res.append({'teacher_name': s.split(':')[1].strip(
            ), 'teacher_type': 'sub'})
        else:
            raise Exception('error teacher type ' + s)
    return res

def classroomCampus_format(classroom_string):
    classroom_string = classroom_string.replace(' ', '').replace('】', '】,')
    classroom_list = list()
    campus_list = list()

    for ele in classroom_string.split(',')[:-1]:
        classroom_list.append(ele.split('【')[0])
        campus_list.append(ele.split('【')[1][:-1])

    return classroom_list, list(set(campus_list))
