#coding:utf-8

import sys
sys.path.append('E:/ACE/project/p22naf/')
reload(sys)
import json
from util.operation_excel import OperationExcel
from base.runmethod import RunMethod
from data.get_data import GetData
from jsonpath_rw import jsonpath,parse
from util.operation_json import OperetionJson
import json


class DependdentData:
	def __init__(self,case_id):
		self.case_id = case_id
		self.opera_excel = OperationExcel()
		self.data = GetData()

	#通过case_id去获取该case_id的整行数据
	def get_case_line_data(self):
		rows_data = self.opera_excel.get_rows_data(self.case_id)
		return rows_data

	#执行依赖测试，获取结果
	def run_dependent(self):
		run_method = RunMethod()
		row_num = self.opera_excel.get_row_num(self.case_id)
		request_data = self.data.get_data_for_json(row_num)
		#header = self.data.is_header(row_num)
		method = self.data.get_request_method(row_num)
		header = self.data.is_header(row_num)
		url = self.data.get_request_url(row_num)
		files = {'file': (
			'new1.xlsx', open("C:\\Users\\Aaron\\Desktop\\new1.xlsx", 'rb'), 'application/vnd.ms-excel')}

		if header == "yes":
			op_json = OperetionJson('../dataconfig/cookie.json')
			cookie = op_json.get_data('apsid')
			cookies = {
				'apsid': cookie
			}
			headers1 = op_json.get_data('Authorization')
			headers = {
				'Authorization': headers1
			}
			res = run_method.run_main(method, url,request_data,headers,files,cookies)
		else:
			res = run_method.run_main(method,url,request_data)
		print("json,load is %s" %res.content)
		return res.content

	#根据依赖的key去获取执行依赖测试case的响应,然后返回
	def get_data_for_key(self,row):
		depend_data = self.data.get_depend_key(row)
		response_data = self.run_dependent()
		res_value = self.get_parse_field_value(depend_data,response_data)
		return res_value
		# json_exe = parse(depend_data)
		# madle = json_exe.find(response_data)
		# print("madle is %s"  %madle)
		# return [math.value for math in madle][0]
	#根据依赖的key获取用例中响应结果
	def get_data_for_excel(self,row):
		depend_data = self.data.get_depend_key(row)
		row_num = self.opera_excel.get_row_num(self.case_id)
		response_data = self.data.get_response_result_field(row_num)
		# json_exe = parse(depend_data)
		# madle = json_exe.find(response_data)
		# return [math.value for math in madle][0]
		part_value = self.get_parse_field_value(depend_data,response_data)
		return part_value

	#通过解析依赖的返回数据字段中内容，返回前一次解析结果中的值
	def get_parse_field_value(self,depend_data,response_data):

		json_exe = parse(depend_data)
		# print("response data is %s " %response_data)
		m = json.loads(response_data)
		madle = json_exe.find(json.loads(response_data))
		return [math.value for math in madle][0]

if __name__ == '__main__':
	order = {
		"data": {
			"_input_charset": "utf-8", 
			"body": "慕课网订单-1710141907182334", 
			"it_b_pay": "1d", 
			"notify_url": "http://order.imooc.com/pay/notifyalipay", 
			"out_trade_no": "1710141907182334", 
			"partner": "2088002966755334", 
			"payment_type": "1", 
			"seller_id": "yangyan01@tcl.com", 
			"service": "mobile.securitypay.pay", 
			"sign": "kZBV53KuiUf5HIrVLBCcBpWDg%2FnzO%2BtyEnBqgVYwwBtDU66Xk8VQUTbVOqDjrNymCupkVhlI%2BkFZq1jOr8C554KsZ7Gk7orC9dDbQlpr%2BaMmdjO30JBgjqjj4mmM%2Flphy9Xwr0Xrv46uSkDKdlQqLDdGAOP7YwOM2dSLyUQX%2Bo4%3D", 
			"sign_type": "RSA", 
			"string": "_input_charset=utf-8&body=慕课网订单-1710141907182334&it_b_pay=1d&notify_url=http://order.imooc.com/pay/notifyalipay&out_trade_no=1710141907182334&partner=2088002966755334&payment_type=1&seller_id=yangyan01@tcl.com&service=mobile.securitypay.pay&subject=慕课网订单-1710141907182334&total_fee=299&sign=kZBV53KuiUf5HIrVLBCcBpWDg%2FnzO%2BtyEnBqgVYwwBtDU66Xk8VQUTbVOqDjrNymCupkVhlI%2BkFZq1jOr8C554KsZ7Gk7orC9dDbQlpr%2BaMmdjO30JBgjqjj4mmM%2Flphy9Xwr0Xrv46uSkDKdlQqLDdGAOP7YwOM2dSLyUQX%2Bo4%3D&sign_type=RSA", 
			"subject": "慕课网订单-1710141907182334", 
			"total_fee": 299
			}, 
			"errorCode": 1000, 
			"errorDesc": "成功", 
			"status": 1, 
			"timestamp": 1507979239100
		}
	res = "data.out_trade_no"
	json_exe = parse(res)
	madle = json_exe.find(order)
	print [math.value for math in madle][0]


