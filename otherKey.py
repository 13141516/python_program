# -*- coding: utf-8 -*-
# @author 852802020@qq.com
import requests
from bs4 import BeautifulSoup
import sys
import random

class UCASEvaluate:
    __loginUrl = 'http://sep.ucas.ac.cn/slogin'
    __courserSelectionPage = 'http://sep.ucas.ac.cn/portal/site/226/821'
    __studentCourseIdentify = 'http://jwxk.ucas.ac.cn/login?Identity='
    __studentCourseEvaluateUrl = 'http://jwxk.ucas.ac.cn'
    __evaluateCouse = 'http://jwxk.ucas.ac.cn/evaluate/45462'
    __headers = {
                'Host': 'sep.ucas.ac.cn',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',

    }
    __meritList = ['本课程老师非常优秀，讲的知识也非常有用。','本课程老师上课非常吸引人，知识也是有用的。','本课程老师谈吐很幽默，讲的知识十分好。','本课程老师才华横溢，知识点讲解通透。','本课程老师一方面妙语连珠，一方面有才。']
    __suggestList = ['这个老师好','这个老师很好','这个老师太好了','这个老师好的难以形容','这个老师非常好']
    __flawList = ['好到没意见...','没意见...']
	
    def __init__(self, parausername, parauserpass):
        self.username= parausername
        self.password= parauserpass
        self.s = requests.Session()

    def login(self):
        postdata = {
            'userName' : self.username,
            'pwd' : self.password,
            'sb'       : 'sb'
        }
        response = self.s.post(UCASEvaluate.__loginUrl, data=postdata, headers = UCASEvaluate.__headers)
        if 'sepuser' in self.s.cookies.get_dict():
            return True
        return False

    def getCourse(self):
        response = self.s.get(UCASEvaluate.__courserSelectionPage, headers = UCASEvaluate.__headers)
        soup = BeautifulSoup(response.text,'html.parser')
        indentity = str(soup.noscript).split('Identity=')[1].split('"'[0])[0]
        coursePage = UCASEvaluate.__studentCourseIdentify + indentity
        self.s.get(coursePage)
        #目前使用的url是春季学期的，可能与秋季学期会不一样
        response = self.s.get(UCASEvaluate.__evaluateCouse)
        soup = BeautifulSoup(response.text,'html.parser')
        courseListResource = soup.body.table.tbody.find_all('tr')
        courseDict = {}
        if len(courseListResource) == 0:
            self.courseDict =  courseDict
        for course in courseListResource:
            tdList = course.find_all('td')
            if tdList[-1].a is None:
                continue
            courseUrl  = tdList[-1].a['href']
            courseName = tdList[1].a.string.strip()
            evaluateFlag = str(tdList[-1].a.string.encode('utf-8'),'utf-8','ignore')
            if evaluateFlag == '评估' or evaluateFlag == '修改评估':
                courseDict[courseName] = courseUrl
        self.courseDict =  courseDict

    def evaluateCourse(self):
        if len(self.courseDict) == 0:
            print('there is no course need to be evaluated...')
            return
        for course in self.courseDict:
            print('start evaluate ' + course + '...')
            evaluateUrl = UCASEvaluate.__studentCourseEvaluateUrl + self.courseDict[course]
            self.__evaluate(evaluateUrl)

    def __evaluate(self, evaluateUrl):
        postData = {}
        response = self.s.get(evaluateUrl)
        soup = BeautifulSoup(response.text,'html.parser')
        urlSave =  UCASEvaluate.__studentCourseEvaluateUrl + soup.body.form['action']
        rowListResource = soup.body.form.table.tbody.find_all('tr')
        for rowResource in rowListResource:
            tdRow = rowResource.find_all('input')[0]
            postData[tdRow['name']] = tdRow['value']
        postData['starFlag'] = 5
        postData['merit'] = random.choice(UCASEvaluate.__meritList)
        postData['suggest'] = random.choice(UCASEvaluate.__suggestList)
        postData['flaw'] =  random.choice(UCASEvaluate.__flawList)
        response = self.s.post(urlSave, data = postData)
        print('Done...')

if __name__ == '__main__':		
    ucasEvaluate = UCASEvaluate(sys.argv[1],sys.argv[2])
    if not ucasEvaluate.login():
        print('login error, please check your username and password')
        exit()
    print('login success...')
    ucasEvaluate.getCourse()
    if len(ucasEvaluate.courseDict) == 0:
        print('there is no course need to be evaluated...')
        exit()
    else:
        print((str)(len(ucasEvaluate.courseDict)) + ' courses need to be evaluated...')
        ucasEvaluate.evaluateCourse()
