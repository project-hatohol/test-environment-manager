#! /usr/bin/env python3

import machine_switcher
import unittest
import sys
import lxc 

container_objs = lxc.list_containers(as_object = True)

class TestMachineInfo(unittest.TestCase):
    def test_toggle_state(self):
        before_state = container_objs[0].state
        machine_switcher.toggle_state(0)
        self.assertFalse(before_state == container_objs[0].state)


if __name__ == '__main__':
    unittest.main()
