#coding:utf-8
import requests
import json
class RunMethod:
	def post_main(self,url,data,headers=None,files=None,cookies=None):
		res = None
		if headers !=None:
			res = requests.post(url=url,data=data,headers=headers,files=files,cookies=cookies)
		else:
			data =json.dumps(data)
			res = requests.post(url=url,data=data)
		return res

	def get_main(self,url,data=None,header=None):
		res = None
		if header !=None:	
			res = requests.get(url=url,data=data,headers=header,verify=False)
		else:
			res = requests.get(url=url,data=data,verify=False)
		return res

	def run_main(self,method,url,data=None,headers=None,files=None,cookies=None):
		res = None
		if method == 'Post':
			res = self.post_main(url,data,headers,files,cookies)
		else:
			res = self.get_main(url,data,headers)
		return res
		# return json.dumps(res,ensure_ascii=False)
		#return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)
