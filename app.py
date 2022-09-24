from fastapi import FastAPI, Response, Request
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn
import requests
import mcu_url
from parse import parse_CampusQueryPage, parse_Homepage,parse_Courses

tags_metadata = [
    {
        "name": "Login/Logout",
        "description": "Please login first before using **Personal Data** APIs",
    },
    {
        "name": "Personal Data",
        "description": "Get the Personal information from the MCU-Student-System",
    },
    {
        "name": "Course Data",
        "description": "Some information about the courses",
    }
]

app = FastAPI(title="MCU API",openapi_tags=tags_metadata)
default_headers  = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}

class LoginInfo(BaseModel):
    student_id: str
    password: str

class CoursesQuery(BaseModel):
    campusID: str = ""
    departmentID: str = ""
    schoolTypeID: str = ""
    courseTypeID: str  = ""
    courseGrade: str ="" # 年級 
    week: str ="" # 0~6 0:星期日 1:星期一 2:星期二 3:星期三 4:星期四 5:星期五 6:星期六
    startSection: str="" # 節次開始
    endSection: str ="" # 節次結束
    semester: str="" # 當學期 0 上學期 1 下學期 2 
    courseNameQueryString: str=""
    teacherNameQueryString: str=""



@app.get('/')
async def root():
    response = RedirectResponse(url="/docs")
    return response



# Login/Logout
@app.post("/api/login", tags=["Login/Logout"])
async def Login(info: LoginInfo,response: Response):
    data = {
        't_tea_no': info.student_id,
        't_tea_pass': info.password,
    }
    login_res = requests.post(mcu_url.LoginUrl, headers=default_headers, data=data)

    if not 'std%5Fenm' in login_res.cookies: return 401
    else:
        for cookies in login_res.cookies:
            response.set_cookie(key=cookies.name, value=cookies.value)
        return 200

@app.post("/api/logout", tags=["Login/Logout"])
async def Logout(request: Request, response: Response):
    logout_res = requests.get(mcu_url.LogoutUrl, headers=default_headers, cookies=request.cookies)
    for ele in logout_res.cookies:
        response.set_cookie(key=ele.name, value=ele.value)
    return 200

### Personal Data ###
@app.get("/api/HomepageInfo", tags=["Personal Data"])
async def getHomepageInfo(request: Request):
    if 'std%5Fno' not in request.cookies or request.cookies['std%5Fno'] == "":
        return 401
    res = requests.get(mcu_url.HomePageUrl, headers = default_headers,cookies=request.cookies)
    res.encoding = 'big5-hkscs'
    res = parse_Homepage(res.text)
    return res

@app.get("/api/studentInfo", tags=["Personal Data"])
async def getStudentInfo(request: Request):
    if 'std%5Fno' not in request.cookies or request.cookies['std%5Fno'] == "":
        return 401
    res = requests.get(mcu_url.HomePageUrl, headers = default_headers,cookies=request.cookies)
    res.encoding = 'big5-hkscs'
    studentName = parse_Homepage(res.text)['studentName']
    res = {
        'studentName': studentName
    }
    return res


### Courses ###

@app.post("/api/courses", tags=["Course Data"])
async def getCourses(request: Request, query:CoursesQuery):
    data = {
        'sch': query.campusID,
        'dept1': query.departmentID,
        'yr1': query.courseGrade,
        'f26': query.schoolTypeID,
        'sel': query.courseTypeID,
        'courna': query.courseNameQueryString,
        'teana': query.teacherNameQueryString,
        'wk1': query.week,
        'ssec1': query.startSection,
        'esec1': query.endSection,
    }
    res = requests.post(mcu_url.CoursesQueryUrl, data=data, cookies={"ggdb": str(query.semester)})
    res.encoding = 'big5-hkscs'
    data = parse_Courses(res.text)
    return data

@app.get("/api/courses/Queryinfo", tags=["Course Data"])
async def getQueryInfo(request: Request):
    res = requests.get(mcu_url.CoursesQueryHomeUrl,headers=default_headers, cookies=request.cookies)
    res.encoding = 'big5-hkscs'
    query_info = parse_CampusQueryPage(res.text)
    return query_info

@app.get("/api/courses/campus", tags=["Course Data"])
async def getCampus(request: Request):
    res = requests.get(mcu_url.CoursesQueryHomeUrl,headers=default_headers, cookies=request.cookies)
    res.encoding = 'big5-hkscs'
    campus_list = parse_CampusQueryPage(res.text)['campus_list']
    return campus_list

@app.get("/api/courses/department", tags=["Course Data"])
async def getDepartment(request: Request):
    res = requests.get(mcu_url.CoursesQueryHomeUrl,headers=default_headers, cookies=request.cookies)
    res.encoding = 'big5-hkscs'
    department_list = parse_CampusQueryPage(res.text)['department_list']
    return department_list

@app.get("/api/courses/courseType", tags=["Course Data"])
async def getCourseType(request: Request):
    res = requests.get(mcu_url.CoursesQueryHomeUrl,headers=default_headers, cookies=request.cookies)
    res.encoding = 'big5-hkscs'
    courseType_list = parse_CampusQueryPage(res.text)['courseType_list']
    return courseType_list

@app.get("/api/courses/schoolType", tags=["Course Data"])
async def getSchoolType(request: Request):
    res = requests.get(mcu_url.CoursesQueryHomeUrl,headers=default_headers, cookies=request.cookies)
    res.encoding = 'big5-hkscs'
    schoolType_list = parse_CampusQueryPage(res.text)['schoolType_list']
    return schoolType_list


uvicorn.run(app, host="0.0.0.0",port=8000)
