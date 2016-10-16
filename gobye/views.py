#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect

from dataDeal.creditStatistics import CreditStatistics

def login(request):
	error = request.GET.get("error", "")
	(img, cookie) = CreditStatistics.getCaptcha()
	return render(request, 'login.html', {"cookie":cookie, "img":img, "error":error})

def result(request):
	if request.method == "POST":
		stuNum = request.POST.get("stuNum", "")
		stuPwd = request.POST.get("stuPwd", "")
		captcha = request.POST.get("captcha", "")
		capCookie = request.POST.get("capCookie", "")

		cs = CreditStatistics(stuNum, stuPwd, captcha, capCookie)
		while cs.finish == False:
			time.sleep(1)
		if cs.success:
			plan = cs.plan

			publicCreditGet = sum(cs.repairedPublicCourses)
			professionCreditGet = sum(cs.repairedProfessionCourses)
			professionElectiveGet = sum(cs.repairedProfessionElective)
			electiveGet = divedeArtsAndScienceCredit(cs.repairedElective)
			electiveSum = electiveGet["arts"] + electiveGet["science"]
			failCredit = sum(cs.failCourses)
			publicCreditNeed = plan["publicRequired"] - publicCreditGet
			professionCreditNeed = plan["professionalRequired"] - professionCreditGet
			tmp = plan["professionalElective"] - professionElectiveGet
			professionElectiveNeed = (0.0 if tmp<0 else tmp)
			electiveNeed = {}
			tmp = plan["artsStream"] - electiveGet["arts"]
			electiveNeed["arts"] = (0.0 if tmp<0 else tmp)
			tmp = plan["scienceStream"] - electiveGet["science"]
			electiveNeed["science"] = (0.0 if tmp<0 else tmp)
			tmp = plan["elective"] - professionElectiveGet - electiveGet["arts"] - electiveGet["science"]
			tmp = (0.0 if tmp<0 else tmp)
			electiveNeedSum = tmp + electiveNeed["arts"] + electiveNeed["science"]
			totalNeed = publicCreditNeed + professionCreditNeed + electiveNeedSum
			
			params = {
				"repairedPublicCourses":cs.repairedPublicCourses, 
				"repairedProfessionCourses":cs.repairedProfessionCourses, 
				"repairedProfessionElective":cs.repairedProfessionElective, 
				"repairedElective":cs.repairedElective, 
				"failCourses":cs.failCourses, 
				"nonRepairedPublicCourses":cs.nonRepairedPublicCourses, 
				"nonRepairedProfessionCourses":cs.nonRepairedProfessionCourses, 
				"optionalCourses":cs.optionalCourses,
				"publicCreditGet":publicCreditGet,
				"publicCreditNeed":publicCreditNeed,
				"professionCreditGet":professionCreditGet,
				"professionCreditNeed":professionCreditNeed,
				"professionElectiveGet":professionElectiveGet,
				"professionElectiveNeed":professionElectiveNeed,
				"electiveGet":electiveGet,
				"electiveSum":electiveSum,
				"electiveNeed":electiveNeed,
				"electiveNeedSum":electiveNeedSum,
				"failCredit":failCredit,
				"totalNeed":totalNeed
			}
			return render(request, 'result.html', params)

		(img, cookie) = CreditStatistics.getCaptcha()
		return HttpResponseRedirect("/?error=" + cs.errorInfo)

	# 非POST方法跳转到登录页面
	return HttpResponseRedirect("/")

def divedeArtsAndScienceCredit(dic):
	result = {
		"arts": 0.0,
		"science":0.0
	}
	for x in dic:
		if x["creditType"] == "文":
			result["arts"] += x["credit"]
		elif x["creditType"] == "理":
			result["science"] += x["credit"]
	return result

def sum(dic):
	result = 0.0
	for x in dic:
		result += float(x["credit"])
	return result