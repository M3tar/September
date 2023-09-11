# -*- coding: utf-8 -*-
import unittest
import requests
import sys
sys.path.append("../..")  # 提升2级到项目根目录下
from config.config import *
from lib.read_excel import *  # 从项目路径下导入
from lib.case_log import log_case_info  # 导入日志方法

class TestUserLogin(unittest.TestCase):  # 类必须Test开头，继承TestCase才能识别为用例类
    @classmethod
    def setUpClass(cls):  # 整个测试类只执行一次
        cls.data_list = excel_to_list(os.path.join(data_path, "test_data.xls"), "TestUserLogin")  # 增加data路径

    def test_user_login_normal(self):
        case_data = get_test_data(self.data_list, 'test_user_login_normal')
        if not case_data:  # 有可能为None
            print("用例数据不存在")
        case_name = case_data.get('case_name')
        url = IP + case_data.get('url')  # 从字典中取数据，excel中的标题也必须是小写url
        headers = case_data.get('headers')
        data = json.loads(case_data.get('data'))  # 注意字符串格式，需要用json.loads()转化为字典格式
        expect_res = case_data.get('expect_res')  # 期望数据
        res = requests.post(url=url, data=json.dumps(data), headers=json.loads(headers))   #data字典转json
        res_code = res.json()['code']  # 获取状态码
        token1 = res.json()['data']['token']
        token = token1.encode()
        with open(token_path,'wb') as f:
            f.write(token)
        log_case_info(case_name, url, data, expect_res, res.text)  # 输出用例log信息
        logging.info("=================================================================================================")
        self.assertEqual(expect_res, res_code)  # 改为assertEqual断言

    # def test_user_login_normal_password_wrong(self):  # 一条测试用例，必须test_开头
    #     case_data = get_test_data(self.data_list, 'test_user_login_password_wrong')  # 从数据列表中查找到该用例数据
    #     if not case_data:  # 有可能为None
    #         print("用例数据不存在")
    #     url = IP + case_data.get('url')  # 从字典中取数据，excel中的标题也必须是小写url
    #     print("url:", (url))
    #     data = case_data.get('data')  # 注意字符串格式，需要用json.loads()转化为字典格式
    #     print("data:", (data))
    #     expect_res = case_data.get('expect_res')  # 期望数据
    #     print("expext_res:", (expect_res))
    #     res = requests.post(url=url, data=json.loads(data))  # 表单请求，数据转为字典格式
    #     # result=res.text()  #请求结果返回
    #     logging.info("测试用例：{}".format('test_user_login_normal'))
    #     logging.info("url：{}".format(url))
    #     logging.info("请求参数：{}".format(data))
    #     logging.info("期望结果：{}".format(expect_res))
    #     logging.info("实际结果：{}".format(res.text))
    #     self.assertIn(expect_res, res.text)  # 改为assertEqual断言


if __name__ == '__main__':  # 如果是直接从当前模块执行（非别的模块调用本模块）
    unittest.main(verbosity=2)  # 运行本测试类所有用例,verbosity为结果显示级别