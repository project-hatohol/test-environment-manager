#! /usr/bin/env python3

import machine_info
import test_stub
import unittest
import sys
import os

def _get_output(func_name, **kwargs):
    (read_fd, write_fd) = os.pipe()

    sys.stdout = os.fdopen(write_fd, 'w')
    # A print function is blocked when it outputs many characters
    # more than the size of the pipe.
    func_name(**kwargs)
    sys.stdout.close()
    sys.stdout = sys.__stdout__

    return os.fdopen(read_fd).readlines()


class _TestMachineInfo(unittest.TestCase):
    test_dict = {'id':0, 'host':'machine1_1', 'group':'1', 'ip':'10.0.3.11'}
    test_path = os.path.dirname(os.path.abspath(__file__)) + '/test_stub1_1/'

    def test_get_info_dict(self):
        self.assertEqual(machine_info.get_info_dict(0, self.test_path), self.test_dict)


    def test_print_header(self):
        lines = _get_output(machine_info.print_header)
        self.assertIn('------', lines[0])
        self.assertIn('No', lines[1])
        self.assertIn('HostName', lines[1])


    def test_print_container_info(self):
        test_container_list = test_stub.test_container_list()
        test_container_obj_list = test_stub.test_obj_list()

        lines = _get_output(machine_info.print_container_info, dict = self.test_dict,
                            container_list = test_container_list,
                            container_obj_list = test_container_obj_list)
        self.assertIn('machine1_1', lines[0])


    def test_read_file(self):
        self.assertIn('1', machine_info.read_file(self.test_path, 'group')[0])
        self.assertIn('test', machine_info.read_file(self.test_path, 'config')[0])


    def test_get_group_info(self):
        self.test_dict = {}
        machine_info.get_group_info(self.test_dict, self.test_path)
        self.assertEqual(self.test_dict['group'], '1')


    def test_get_config_info(self):
        machine_info.get_config_info(self.test_dict, self.test_path)
        self.assertEqual(self.test_dict['ip'], '10.0.3.11')
        self.assertEqual(self.test_dict['host'], 'machine1_1')

    
if __name__ == '__main__':
    unittest.main()

