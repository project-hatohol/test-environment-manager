#! /usr/bin/env python3

import machine_switcher
import test_stub
import unittest
import sys
import os

class TestMachineInfo(unittest.TestCase):
    container_list = test_stub.test_container_list()
    container_obj_list = test_stub.test_obj_list()
    test_container_dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

    def _compare_container_state(self, container_id):
        before_state = self.container_obj_list[container_id].state
        machine_switcher.toggle_state(self.container_obj_list[container_id],
                                      self.container_list[container_id])
        self.assertFalse(before_state == self.container_obj_list[container_id].state)


    def _get_containers_state(self, container_ids):
        states = []
        for container_id in container_ids:
            print(container_id)
            states.append(self.container_obj_list[container_id].state)

        return states


if __name__ == '__main__':
    unittest.main()

