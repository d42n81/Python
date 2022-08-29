from ensurepip import version
import json
import os
from operator import length_hint
import unittest
from pprint import pprint
from selenium import webdriver
from axe_devtools_selenium import AxeDriver
from axe_devtools_api import Axe, ReportConfiguration
from pyvirtualdisplay import Display


class TestStringMethods(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        display = Display(visible=0, size=(800, 800))  
        display.start()
        self.page = webdriver.Chrome()
    
    def takeScan(self):
        self.page.get("http://abcdcomputech.dequecloud.com/")
        report_config = ReportConfiguration().test_suite_name("homepage-no-flow").ui_state("Pre click")
        axe = Axe(AxeDriver(self.page), report_configuration=report_config)
        results = axe.analyze()
        # pprint(results.findings.length)
        home_dir = os.system("cd ~")
        print("`cd ~` ran with exit code %d" % home_dir)
        # os.system("axe --help")
        with open("homePage.json", "w") as f:
            f.write(results.to_json())
    
    def testA11y(self):
        self.takeScan()
        file = open("homePage.json", "r")
        jsonObject = json.load(file)
        violations = jsonObject.get("findings").get("violations")
        pprint(len(violations))
        file.close()
        # generate report:
        # os.system("axe reporter ./ ./results --format=html")
        os.system("npm run reporter")
        self.assertEqual(len(violations), 0)


if __name__ == '__main__':
    unittest.main()
    