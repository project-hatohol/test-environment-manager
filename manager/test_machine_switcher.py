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


    def test_toggle_state(self):
        self._compare_container_state(0)


    def test_change_state_to_start(self):
        machine_switcher.change_state_to_start(self.container_obj_list[0],
                                               self.container_list[0])
        self.assertEquals("RUNNING", self.container_obj_list[0].state)


    def test_change_state_to_stop(self):
        machine_switcher.change_state_to_stop(self.container_obj_list[0],
                                               self.container_list[0])
        self.assertEquals("STOPPED", self.container_obj_list[0].state)


    def test_toggle_state_for_group(self):
        test_ids = [0, 1, 2, 3, 4, 5]
        before_states = self._get_containers_state(test_ids)
        machine_switcher.toggle_state_for_group([1, 2], self.test_container_dir_path,
                                                self.container_list, self.container_obj_list)
        after_states = self._get_containers_state(test_ids)

        for num in range(len(test_ids)):
            self.assertNotEquals(before_states, after_states)


    def test_toggle_state_for_each_machine(self):
        test_ids = [0, 1, 3]
        before_states = self._get_containers_state(test_ids)
        machine_switcher.toggle_state_for_each_machine(test_ids, self.container_obj_list,
                                                       self.container_list)
        after_states = self._get_containers_state(test_ids)

        for num in range(len(test_ids)):
            self.assertNotEquals(before_states, after_states)


if __name__ == '__main__':
    unittest.main()

