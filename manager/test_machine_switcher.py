#! /usr/bin/env python3

import machine_switcher
import test_stub
import unittest
import sys
import os

class TestMachineInfo(unittest.TestCase):
    def test_toggle_state(self):
        before_state = container_objs[0].state
        machine_switcher.toggle_state(0)
        self.assertFalse(before_state == container_objs[0].state)


if __name__ == '__main__':
    unittest.main()
