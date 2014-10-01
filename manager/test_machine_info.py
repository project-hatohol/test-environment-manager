#! /usr/bin/env python3

import machine_info
import unittest
import sys

def get_output(file_name, func_name, **kwargs):
    sys.stdout = open(file_name, "w")
    func_name(**kwargs)
    sys.stdout.close()
    sys.stdout = sys.__stdout__
 

def read_file(file_name):
    file = open(file_name)
    lines = file.readlines()
    file.close()

    return lines


test_dict = {"id":0, "host":"machine1_1", "group":"1", "ip":"10.0.3.11"}

class TestMachineInfo(unittest.TestCase):
    def test_get_info_dict(self):
        self.assertEqual(machine_info.get_info_dict(0), test_dict)


    def test_print_header(self):
        get_output("header_output", machine_info.print_header)
        lines = read_file("header_output")
        self.assertTrue("-" in lines[0])
        self.assertTrue("No" in lines[1])


    def test_print_container_info(self):
        get_output("output_container_info", machine_info.print_container_info, dict = test_dict)
        lines = read_file("output_container_info")
        self.assertTrue("machine1_1" in lines[0])


    def test_insert_header(self):
        for test_line in [0, 10, 20]:
            get_output("output_insert_header", machine_info.insert_header, line_number=test_line)
            lines = read_file("output_insert_header")
            if test_line % 20 == 0:
                self.assertTrue("-" in lines[0])
            else:
                self.assertFalse(lines)


    def test_read_file(self):
        self.assertTrue("1" in machine_info.read_file(0, "group")[0])


    def test_get_group_info(self):
        test_dict = {}
        machine_info.get_group_info(test_dict, 1)
        self.assertTrue(test_dict["group"] == "1")


if __name__ == '__main__':
    unittest.main()

