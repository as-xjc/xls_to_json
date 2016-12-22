# -*- coding: UTF-8 -*-

class Prototype:

    def __init__(self):
        self.args = {}
        self.types = {}
        self.data = {}

    def getArg(self, arg):
        return self.args[arg]

    def setArg(self, key, arg):
        self.args[key] = arg

    def printArgs(self):
        print('-- args ---')
        for k, v in self.args.items():
            print('%s: %s'%(k, v))

    def addType(self, index, name, type, content):
        self.types[index] = {'name':name, 'type':type, 'content':content}

    def getType(self, index):
        return self.types[index]

    def printTypes(self):
        print('-- types ---')
        for k, v in self.types.items():
            print("%d. %s:%s [%s]"%(k, v['name'], v['type'], v['content']))

    def setDataType(self, type):
        if type == 'array':
            self.data = []
        else:
            self.data = {}

    def addData(self, key, value):
        if isinstance(self.data, dict):
            self.data[key] = value
        elif isinstance(self.data, list):
            self.data.append(value)

    def getData(self):
        return self.data

    def printData(self):
        print('-- data ---')
        if isinstance(self.data, dict):
            for k, v in self.data.items():
                print("%s:%s"%(k, v))
        elif isinstance(self.data, list):
            for v in self.data:
                print("%s"%(v))
