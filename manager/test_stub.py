#! /usr/bin/env python3

import sys
import os

def test_container_list():
     test_list = ["test_stub1_1", "test_stub1_2", "test_stub1_3",
                  "test_stub2_1", "test_stub2_2", "test_stub2_3"]

     return test_list


def test_obj_list():
    test_containers_name = test_container_list()
    test_objs = []
    for num in range(len(test_containers_name)):
        test_objs.append(TestObjList(test_containers_name[num]))

    return test_objs


def read_file(test_state_path):
    file = open(test_state_path)
    lines = file.readlines()
    file.close()

    return lines


def write_state(test_state_path, test_container_state):
    file = open(test_state_path, "w")
    file.write(test_container_state)
    file.close()


def get_test_container_state(test_container_name, test_state_path):
    container_state = read_file(test_state_path)[0].strip("\n")
        
    return container_state


class TestObjList():
    def __init__(self, test_container_name):
        self.test_state_path = os.path.dirname(os.path.abspath(__file__)) + "/" + test_container_name + "/state"
        self.state = get_test_container_state(test_container_name, self.test_state_path)


    def start(self):
        if self.state == "STOPPED":
            self.state = "RUNNING"
            write_state(self.test_state_path, self.state)

        return True


    def stop(self): 
        if self.state == "RUNNING":
            self.state = "STOPPED"
            write_state(self.test_state_path, self.state)

        return True


    def shutdown(self):
        if self.state == "RUNNING":
            self.state = "STOPPED"
            write_state(self.test_state_path, self.state)

        return True

