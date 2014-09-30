#! /usr/bin/env python3

import machine_info
import unittest

test_dict = {"id":0, "host":"machine1_1", "group":"1", "ip":"10.0.3.11"}

class TestMachineInfo(unittest.TestCase):
    def test_get_info_dict(self):
        self.assertEqual(machine_info.get_info_dict(0), test_dict)


if __name__ == '__main__':
    unittest.main()

