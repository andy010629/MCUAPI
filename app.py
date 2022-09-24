from typing import Optional
from fastapi import FastAPI, Response, Request
from parse import parse_Homepage
from pydantic import BaseModel
import uvicorn
import requests
import mcu_url

app = FastAPI()
default_headers  = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}

class LoginInfo(BaseModel):
    student_id: str
    password: str


@app.post("/api/login")
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

@app.post("/api/logout")
async def Logout(request: Request, response: Response):
    logout_res = requests.get(mcu_url.LogoutUrl, headers=default_headers, cookies=request.cookies)
    for ele in logout_res.cookies:
        response.set_cookie(key=ele.name, value=ele.value)
    return 200

@app.get("/api/HomepageInfo")
async def getHomepageInfo(request: Request):
    if 'std%5Fno' not in request.cookies or request.cookies['std%5Fno'] == "":
        return 401
    res = requests.get(mcu_url.HomePageUrl, headers = default_headers,cookies=request.cookies)
    res.encoding = 'big5-hkscs'
    res = parse_Homepage(res.text)
    return res

@app.get("/api/studentInfo")
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

@app.get("/api/courses")
async def getCourses(request: Request):
    if 'std%5Fno' not in request.cookies or request.cookies['std%5Fno'] == "":
        return 401
    res = requests.get(mcu_url.HomePageUrl,
                       headers=default_headers, cookies=request.cookies)
    res.encoding = 'big5-hkscs'
    courses = parse_Homepage(res.text)['courses']
    return courses


uvicorn.run(app, host="0.0.0.0",port=8000)
