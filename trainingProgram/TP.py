#coding:utf-8

import urllib
from bs4 import BeautifulSoup

import sys, os
sys.path.append("..")
os.environ['DJANGO_SETTINGS_MODULE'] = 'gobye.settings'
from django.conf import settings
import django
django.setup()
from dataDeal.models import Professions, Plan, Courses

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

baseUrl = "http://192.168.2.224/pyfa/view_pyfa.asp"

def cleanAllDatabaseTable():
	print "clean Database:"
	print "Professions"
	cleanDatabaseTable(Professions)
	print "Plan"
	cleanDatabaseTable(Plan)
	print "Courses"
	cleanDatabaseTable(Courses)

def cleanDatabaseTable(table):
	table.objects.all().delete()

def getCollegesByGrade(grade):
	'''
		通过年级获取学院列表 
		@param grade
		@return jsonArray [
			{
				colNum: "01",
				colName: "人文学院"
			},
			...
		]
	'''
	print "获取" + grade + "级学院信息..."

	url = "http://192.168.2.224/pyfa/select_view_xy.asp"
	params = {
		"nj": grade
	}
	data = urllib.urlopen(url + "?%s" % urllib.urlencode(params)).read()
	# 01,人文学院,02,经济学院,03,法学院,04,管理学院,
	splitData = data.split(',')
	result = []
	for i in xrange(0, len(splitData) - 1, 2):
		result.append({
				"colNum": splitData[i],
				"colName": splitData[i+1]
			})
	return result

def getColleges():
	'''
		获取所有年级的学院列表
		@return [
			{
				grade: "2013".
				collegeList: collegeList
			},
			...
		]
	'''
	print "获取所有学院..."

	result = []

	html = urllib.urlopen(baseUrl)
	data = BeautifulSoup(html, "lxml")
	gradeSelect = data.find(id="bsy_nj")

	for option in gradeSelect.find_all("option"):
		# 获取年级列表
		grade = option['value']
		if grade != "00":
			collegeList = getCollegesByGrade(grade)
			result.append({
				"grade":grade,
				"collegeList": collegeList
				})
	return result

def getProfessionsName(colleges):
	'''
		通过学院列表获取学院所有的专业
		@param colleges [
			{
				grade: "2013",
				collegeList: [
					 {
							"colNum":"01",
							"colName": "人文学院"
					 },
					 ...
				]
			},
			...
		]
		@return [
			{
				professionId: professionId,
				url: "http://192.168.2.224/pyfa/view_pyfa_detail.asp?fid=2013011000"
			}
		]
	'''
	urlPre = "http://192.168.2.224/pyfa"

	result = []

	for college in colleges:
		grade = college["grade"]
		for collegeList in college["collegeList"]:
			print "获取" + grade +  "级" + collegeList["colName"] + "专业信息"

			params = {
				"nj": grade,
				"xydh": collegeList["colNum"]
			}
			html = urllib.urlopen(baseUrl + "?%s" % urllib.urlencode(params)).read()
			data = BeautifulSoup(html, "lxml")
			professions = data.find_all("td", class_="ncontents")
			for profession in professions:
				a = profession.find("a")

				# 专业名去除院名、年级、多余空格
				professionName = a.string.strip()
				professionName = professionName[professionName.rfind('，') + 1:]

				url = urlPre + a["href"].replace(".\\", "/")
				
				# 插入数据库
				proObj = Professions(grade=grade, college=collegeList["colName"], profession=professionName)
				proObj.save()
				# 添加到返回结果
				result.append({
					"professionId": proObj.id,
					"url": url
					})
	return result

def getTrainingProgramPages(professionInfo):
	'''
		处理所有培养方案页面数据
		@professionInfo [
			{
				professionId: professionId,
				url: "http://192.168.2.224/pyfa/view_pyfa_detail.asp?fid=2013011000"
			}
		]
	'''
	for profession in professionInfo:
		url = profession["url"]
		html = urllib.urlopen(url).read()
		# failCount = 5
		# while html == "": # 获取页面失败则重新获取，失败次数超过5次退出程序
		# 	failCount -= 1
		# 	if failCount == 0:
		# 		print "获取页面失败~请检查网络情况"
		# 		exit(1)
		# 	html = urllib.urlopen(url).read()
		print "获取专业id为" + str(profession["professionId"]) + "的课程信息..."

		handleTrainingProgramPage(html, profession["professionId"])

def handleTrainingProgramPage(html, professionId):
	'''
		处理单个培养费安敢页面数据
		@param html 处理页面的html代码
		@param professionId 数据库存储的profession表id
	'''
	html = BeautifulSoup(html, "lxml")

	print "获取培养方案学分最低要求..."

	tr = html.find(id="byyq_in")
	addPlan(tr, professionId)

	# 附表
	x = 1
	tr = html.find(id="fb" + str(x))
	while tr != None:
		print "获取附表" + str(x) + "的课程信息..."

		addCourses(tr, professionId)
		x += 1
		tr = html.find(id="fb" + str(x))

def addPlan(html, professionId):
	'''
		学分要求table的html代码提取出学分并添加到数据库中
		@param html table的html代码
		@param professionId 数据库存储的profession表id
	'''
	table = html.find("table")
	tr = table.find_all("tr")
	# 公共必修课学分
	pr = tr[1]
	pr = float(pr.find_all("td")[1].string) #所需学分
	# 学科专业核心课学分
	proR = tr[2]
	proR = float(proR.find_all("td")[1].string)
	# 选修课
	pe = tr[3]
	peTd = pe.find_all("td")
	pe = float(peTd[1].string)
	# 附加要求 从中获取最低学分要求
	ar = ""
	for x in peTd[2].strings:
		ar += x
	proEle = float(ar[ar.find("最低要求") + 4:ar.find("学分")]) # 专业选修要求
	artsS = None # 文科学分要求
	sciS = None # 理科学分要求
	if ar.find("理科学分") != -1: # 有理科学分最低要求
		sciS = float(ar[ar.rfind("最低要求") + 4:ar.rfind("学分")])
	else:
		artsS = float(ar[ar.rfind("最低要求") + 4:ar.rfind("学分")])
	# 创新创业实践与学生发展
	pra = tr[4]
	pra = float(pra.find_all("td")[1].string)

	Plan(professionId=professionId, publicRequired=pr, professionalRequired=proR, elective=pe, professionalElective=proEle, artsStream=artsS, scienceStream=sciS, practice=pra).save()

def addCourses(html, professionId):
	'''
		提取课程信息table并添加到数据库中
		@param html 课程信息table的html代码
		@param professionId 数据库存储的profession表id
	'''
	courseType = html.tr.td.find_all("h2")[1].string # 课程类型
	courseTable = html.table
	trList = courseTable.find_all("tr")[3:-1] # 除去前三个，前三个为表头信息，除去最后一个，最后一个为合计
	for tr in trList:
		td = tr.find_all("td")
		courseNum = td[1].string
		courseName = None
		courseNameEN = None
		for x in td[2].strings:
			if courseName == None:
				courseName = x
			else :
				courseNameEN = x
		credit = float(td[4].string)
		suggestion = int(td[14].string)
		creditType = td[15].string
		remark = td[16].string
		Courses(professionId=professionId, courseNum=courseNum, courseName=courseName, courseNameEN=courseNameEN, courseType=courseType, suggestion=suggestion, credit=credit, creditType=creditType, remark=remark).save()
		
def main():
	cleanAllDatabaseTable()

	colleges = getColleges()
	professionInfo = getProfessionsName(colleges)
	getTrainingProgramPages(professionInfo)

if __name__ == '__main__':
	main()