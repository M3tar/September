# -*- coding: utf-8 -*-
import unittest
import requests
import sys
sys.path.append("../..")  # 提升2级到项目根目录下
from config.config import *
from lib.read_excel import *  # 从项目路径下导入
from lib.case_log import log_case_info  # 导入日志方法
from lib.db import DB

db = DB()


class TestCompanyadmin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_list = excel_to_list("../../data/test_data.xls", "TestCompanyadmin")  # 读取TestCompanyadmin工作簿的所有数据

    def test_companyadmin_normal(self):
        case_data = get_test_data(self.data_list, 'test_companyadmin_normal')
        if not case_data:
            print("用例数据不存在")
        case_name = case_data.get("case_name")  # 获取名字
        url = IP + case_data.get('url')
        headers = headers1
        data = json.loads(case_data.get('data'))  # 转为字典，需要取里面的name进行数据库检查
        # expect_res = json.loads(case_data.get('expect_res'))  # 转为字典，断言时直接断言两个字典是否相等
        expect_res = case_data.get('expect_res')
        user_name = data.get('name')
        # 环境检查
        if db.check_user(user_name):
            db.del_user(user_name)
        # 发送请求
        res = requests.post(url=url, json=data, headers=headers)  # 用data=data 传字符串也可以
        res_code = res.json()['code']  # 获取状态码
        log_case_info(case_name, url, data, expect_res, res.text)  # 输出用例log信息
        logging.info("=================================================================================================")
        self.assertEqual(expect_res, res_code)  # 请求结果断言
        # self.assertTrue(db.check_user(user_name))  # 数据库断言
        db.del_user(user_name)    # 环境清理（删除已添加管理员）







    # def test_companyadmin_error(self):
    #     case_data = IP + get_test_data(self.data_list, 'test_companyadmin_error')
    #     if not case_data:
    #         print("用例数据不存在")
    #     url = case_data.get('url')
    #     data = json.loads(case_data.get('data'))  # 转为字典，需要取里面的name进行数据库检查
    #     expect_res = json.loads(case_data.get('expect_res'))  # 转为字典，断言时直接断言两个字典是否相等
    #     name = data.get("name")  # huyajie
    #     # 环境检查
    #     if not db.check_user(name):
    #         print("用户不存在")
    #     # 发送请求
    #     res = requests.post(url=url, json=data)  # 用data=data 传字符串也可以
    #     log_case_info('test_companyadmin_error', url, data, expect_res, res.text)  # 输出用例log信息
    #     # 响应断言（整体断言）
    #     # self.assertDictEqual(res.json(), expect_res)
    #     self.assertIn(expect_res, res.text)  # 改为assertEqual断言
    #     # 数据库断言
    #     self.assertTrue(db.check_user(name))

if __name__ == '__main__':
    unittest.main(verbosity=2)  # 运行所有用例