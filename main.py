#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2018/4/11 0011 13:36
# @author  : zza
# @Email   : 740713651@qq.com
"""整个系统的主入库"""
from kivy.app import App
from kivy.uix.label import Label

from bin.server import Server


class MyApp(App):
    def __init__(self, **kwargs):
        self.server = Server()
        super().__init__(**kwargs)

    def build(self):
        return Label(text='Hello world')


def main():
    MyApp().run()


if __name__ == '__main__':
    main()
