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

class TestConditionAdd(unittest.TestCase):  # 类必须Test开头，继承TestCase才能识别为用例类
    @classmethod
    def setUpClass(cls):  # 整个测试类只执行一次
        cls.data_list = excel_to_list(os.path.join(data_path, "test_data.xls"), "TestCondition")  # 增加data路径

    def test_add_condition(self):
        case_data = get_test_data(self.data_list, 'test_condition_add')  # 从数据列表中查找到该用例数据
        if not case_data:  # 有可能为None
            print("用例数据不存在")
        case_name = case_data.get('case_name')
        url = IP + case_data.get('url')  # 从字典中取数据，excel中的标题也必须是小写url
        headers = headers1
        data = json.loads(case_data.get('data'))  # 注意字符串格式，需要用json.loads()转化为字典格式
        expect_res = case_data.get('expect_res')  # 期望数据
        condition_name = data.get('name')
        #检查环境
        if db.check_condition(condition_name):
            db.del_condition(condition_name)
        res = requests.post(url=url, data=json.dumps(data),headers=headers)  #data字典转json
        res_code = res.json()['code']  # 获取状态码
        log_case_info(case_name, url, data, expect_res, res.text)  # 输出用例log信息
        self.assertEqual(expect_res, res_code)  # 改为assertEqual断言
        # self.assertTrue()  # 数据库断言
        #恢复环境
        db.del_condition(condition_name)

if __name__ == '__main__':  # 如果是直接从当前模块执行（非别的模块调用本模块）
    unittest.main(verbosity=2)  # 运行本测试类所有用例,verbosity为结果显示级别