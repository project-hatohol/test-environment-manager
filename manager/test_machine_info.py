#! /usr/bin/env python3

import machine_info
import unittest
import sys
import lxc
import os

def _get_output(file_name, func_name, **kwargs):
    sys.stdout = open(file_name, "w")
    func_name(**kwargs)
    sys.stdout.close()
    sys.stdout = sys.__stdout__
 

def _read_file(file_name):
    file = open(file_name)
    lines = file.readlines()
    file.close()

    return lines


class TestMachineInfo(unittest.TestCase):
    test_dict = {"id":0, "host":"machine1_1", "group":"1", "ip":"10.0.3.11"}
    test_path = os.path.dirname(os.path.abspath(__file__)) + "/test_stub1_1/"

    def _judge_printing_header(self, test_line):
        _get_output("output_insert_header", machine_info.insert_header, container_id = test_line)
        lines = _read_file("output_insert_header")
        os.remove("output_insert_header")

		delimit_output = 20
        if test_line % delimit_output == 0:
            self.assertIn("-----", lines[0])
        else:
            self.assertFalse(lines)


    def test_get_info_dict(self):
        self.assertEqual(machine_info.get_info_dict(0, self.test_path), self.test_dict)


    def test_print_header(self):
        _get_output("header_output", machine_info.print_header)
        lines = _read_file("header_output")
        os.remove("header_output")
        self.assertIn("------", lines[0])
        self.assertIn("No", lines[1])
        self.assertIn("HostName", lines[1])


    def test_print_container_info(self):
        test_container_list = lxc.list_containers()
        test_container_obj_list = lxc.list_containers(as_object = True)

        _get_output("output_container_info", machine_info.print_container_info, 
                   dict = self.test_dict, container_list = test_container_list,
                   container_obj_list = test_container_obj_list)
        lines = _read_file("output_container_info")
        os.remove("output_container_info")
        self.assertIn("machine1_1", lines[0])


    def test_insert_header(self):
        self._judge_printing_header(0)
        self._judge_printing_header(10)
        self._judge_printing_header(20)


    def test_read_file(self):
        self.assertIn("1", machine_info.read_file(self.test_path, "group")[0])
        self.assertIn("test", machine_info.read_file(self.test_path, "config")[0])


    def test_get_group_info(self):
        self.test_dict = {}
        machine_info.get_group_info(self.test_dict, self.test_path)
        self.assertEqual(self.test_dict["group"], "1")


    def test_get_config_info(self):
        machine_info.get_config_info(self.test_dict, self.test_path)
        self.assertEqual(self.test_dict["ip"], "10.0.3.11")
        self.assertEqual(self.test_dict["host"], "machine1_1")

    
if __name__ == '__main__':
    unittest.main()

