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
        test_objs.append(_TestObjList(test_containers_name[num]))

    return test_objs


class _TestObjList():
    def __init__(self, test_container_name):
        self.state = "STOPPED"

    def start(self):
        if self.state == "STOPPED":
            self.state = "RUNNING"

        return True


    def stop(self):
        if self.state == "RUNNING":
            self.state = "STOPPED"

        return True


    def shutdown(self):
        if self.state == "RUNNING":
            self.state = "STOPPED"

        return True

