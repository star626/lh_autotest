#coding:utf-8

import sys
sys.path.append("E:/ACE/project/p22naf/")
reload(sys)
import json
from base.runmethod import RunMethod
from data.get_data import GetData
from util.common_util import CommonUtil
from data.dependent_data import DependdentData
from util.send_email import SendEmail
from util.operation_header import OperationHeader
from util.operation_json import OperetionJson
class RunTest:
	def __init__(self):
		self.run_method = RunMethod()
		self.data = GetData()
		self.com_util = CommonUtil()
		self.send_mai = SendEmail()

	#程序执行的
	def go_on_run(self):
		res = None
		pass_count = []
		fail_count = []
		#10  0,1,2,3
		rows_count = self.data.get_case_lines()
		for i in range(1,rows_count):

			is_run = self.data.get_is_run(i)
			if is_run:
				url = self.data.get_request_url(i)
				method = self.data.get_request_method(i)
				request_data = self.data.get_data_for_json(i)
				# expect = self.data.get_expcet_data_for_mysql(i)
				expect = self.data.get_expcet_data(i)
				# print("except data is %s" %expect)
				header = self.data.is_header(i)
				depend_case = self.data.is_depend(i)
				response_value = self.data.get_response_result_field(i)
				is_post_previous_case = self.data.get_post_result(i)
				depend_excel_file = self.data.is_excel(i)
				is_save_result = self.data.is_save_result(i)

				if depend_case == None:
					if header == 'write':
						res = self.run_method.run_main(method, url, request_data)
						op_header = OperationHeader(res)
						op_header.write_cookie()
					elif header == 'yes':
						op_json = OperetionJson('../dataconfig/cookie.json')
						cookie = op_json.get_data('apsid')
						cookies = {
							'apsid': cookie
						}
						headers1 = op_json.get_data('Authorization')
						headers = {
							'Authorization': headers1
						}
						if depend_excel_file == 'Y':
							files = {'file': (
								'new1.xlsx', open("C:\\Users\\Aaron\\Desktop\\new1.xlsx", 'rb'),
								'application/vnd.ms-excel')}
							res = self.run_method.run_main(method, url, request_data, headers, files, cookies)
						else:
							convert_data = json.dumps(request_data)
							res = self.run_method.run_main(method,url=url,data=convert_data,headers=headers,cookies=cookies)
					else:
						res = self.run_method.run_main(method, url, request_data)
					# res = self.run_method.run_main(method, url, request_data)

				# elif depend_case == "write":
				# 	if header == 'write':
				# 		res = self.run_method.run_main(method, url, request_data)
				# 		op_header = OperationHeader(res)
				# 		op_header.write_cookie()
				#
				# 	elif header == 'yes':
				# 		op_json = OperetionJson('../dataconfig/cookie.json')
				# 		cookie = op_json.get_data('apsid')
				# 		cookies = {
				# 			'apsid': cookie
				# 		}
				# 		headers1 = op_json.get_data('Authorization')
				# 		headers = {
				# 			'Authorization': headers1
				# 		}
				# 		if depend_excel_file == 'Y':
				# 			files = {'file': (
				# 				'new1.xlsx', open("C:\\Users\\Aaron\\Desktop\\new1.xlsx", 'rb'),
				# 				'application/vnd.ms-excel')}
				# 			res = self.run_method.run_main(method, url, request_data, headers, files, cookies)
				# 		else:
				# 			res = self.run_method.run_main(method, url, request_data, headers, cookies)
				# 	else:
				# 		res = self.run_method.run_main(method, url, request_data)
				#
				# 	# res = self.run_method.run_main(method, url, request_data)
				# 	self.data.write_response_to_cell(i, res.content.decode("utf-8"))

				else:
					self.depend_data = DependdentData(depend_case)
					# 获取依赖的key
					depend_key = self.data.get_depend_field(i)
					depend_response_data = self.depend_data.get_data_for_key(i).decode('string_escape')

					# if is_post_previous_case == 'N':
					#
					# 	depend_response_data = self.depend_data.get_data_for_excel(i)
					# else:
					# 	#获取的依赖响应数据
					# 	depend_response_data = self.depend_data.get_data_for_key(i)
					# request_data[depend_key] = depend_response_data
					# headers_data[depend_key] = depend_response_data
					if header == 'write':
						res = self.run_method.run_main(method,url,request_data)
						op_header = OperationHeader(res)
						op_header.write_cookie()

					elif header == 'yes':
						op_json = OperetionJson('../dataconfig/cookie.json')
						cookie = op_json.get_data('apsid')
						cookies = {
							'apsid':cookie
						}
						# headers1 = op_json.get_data('Authorization')
						headers = {
							'Authorization': depend_response_data
						}

						files = {'file': (
						'new1.xlsx', open("C:\\Users\\Aaron\\Desktop\\new1.xlsx", 'rb'), 'application/vnd.ms-excel')}

						if depend_excel_file=="Y":
							res = self.run_method.run_main(method,url=url,data=request_data,files=files,headers=headers,cookies=cookies)
						else:
							# request_data = json.dumps(request_data)
							res = self.run_method.run_main(method,url=url,data=request_data,headers=headers,cookies=cookies)

						#新增一列，是否保存结果的判定列
						if is_save_result == "Y":
							self.data.write_response_to_cell(i, res.content.decode("utf-8"))
					else:
						res = self.run_method.run_main(method,url,request_data)



				# if depend_case == "write":
				# 	self.data.write_response_to_cell(i,res.decode("utf-8"))

				# if self.com_util.is_equal_dict(expect,json.dumps(res)) == 0:

				if self.com_util.is_contain(expect,res.content.decode("utf-8")) == True:
					self.data.write_result(i,'pass')
					pass_count.append(i)
				else:
					# self.data.write_result(i,json.dumps(res,ensure_ascii=False))
					self.data.write_result(i, res.content.decode("utf-8"))
					fail_count.append(i)
		self.send_mai.send_main(pass_count,fail_count)

	#将执行判断封装
	#def get_cookie_run(self,header):


if __name__ == '__main__':
	run = RunTest()
	run.go_on_run()
	print("已全部执行完成，请查收相关邮件!")

