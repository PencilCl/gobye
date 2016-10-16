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
			return render(request, 'result.html')

		(img, cookie) = CreditStatistics.getCaptcha()
		return HttpResponseRedirect("/?error=" + cs.errorInfo)
	
	# 非POST方法跳转到登录页面
	return HttpResponseRedirect("/")