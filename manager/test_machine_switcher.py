#! /usr/bin/env python3

import machine_switcher
import test_stub
import unittest
import sys
import os

class TestMachineInfo(unittest.TestCase):
    _container_list = test_stub.test__container_list()
    _container_obj_list = test_stub.test_obj_list()
    test_container_dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"
    test_id = 0

    def _assert_container_state(self, container_id):
        previous_state = self._container_obj_list[container_id].state
        machine_switcher.toggle_state(self._container_obj_list[container_id],
                                      self._container_list[container_id])
        self.assertFalse(previous_state == self._container_obj_list[container_id].state)


    def _get_containers_state(self, container_ids):
        states = []
        for container_id in container_ids:
            states.append(self._container_obj_list[container_id].state)

        return states


    def test_toggle_state(self):
        self._assert_container_state(self.test_id)


    def test_change_state_to_start(self):
        machine_switcher.change_state_to_start(self._container_obj_list[self.test_id],
                                               self._container_list[self.test_id])
        self.assertEquals("RUNNING", self._container_obj_list[self.test_id].state)


    def test_change_state_to_stop(self):
        machine_switcher.change_state_to_stop(self._container_obj_list[self.test_id],
                                               self._container_list[self.test_id])
        self.assertEquals("STOPPED", self._container_obj_list[self.test_id].state)


    def test_toggle_state_for_group(self):
        test_ids = [0, 1, 2, 3, 4, 5]
        previous_states = self._get_containers_state(test_ids)
        machine_switcher.toggle_state_for_group([1, 2], self.test_container_dir_path,
                                                self._container_list, self._container_obj_list)
        current_states = self._get_containers_state(test_ids)

        for num in range(len(test_ids)):
            self.assertNotEquals(previous_states, current_states)


    def test_toggle_state_for_each_machine(self):
        test_ids = [0, 1, 3]
        previous_states = self._get_containers_state(test_ids)
        machine_switcher.toggle_state_for_each_machine(test_ids, self._container_obj_list,
                                                       self._container_list)
        current_states = self._get_containers_state(test_ids)

        for num in range(len(test_ids)):
            self.assertNotEquals(previous_states, current_states)


    def test_convert_machine_nums_to_ids(self):
        test_machine_nums = [1, 2, 3]
        current_convert = machine_switcher.convert_machine_nums_to_ids(test_machine_nums)
        self.assertEquals(current_convert, [0, 1, 2])


    def test_enum_id_list(self):
        test_argument = ["0-3",  "5"]
        enum_ids = machine_switcher.enum_id_list(test_argument)
        self.assertEquals([0, 1, 2, 3, 5], enum_ids)


    def test_create_group_dict(self):
        test_group_dict = machine_switcher.create_group_dict(self.test_container_dir_path,
                                                             self._container_list)
        self.assertEquals(test_group_dict, {1: [0, 1, 2], 2: [3, 4, 5]})


    def test_get_container_dir_path(self):
        container_dir_path = machine_switcher.get_container_dir_path()
        self.assertEquals("/var/lib/lxc/", container_dir_path)


if __name__ == '__main__':
    unittest.main()

