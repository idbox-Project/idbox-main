# idbEnvlib.py - an API for idb Plugs
import os, re

from settings import define

language=__import__(define.languageSelect)



class errors:
    class InstallError(Exception):
        def __init__(self, arg):
            self.args = arg

    class UninstallError(Exception):
        def __init__(self, arg):
            self.args = arg

    class InputError(Exception):
        def __init__(self, arg):
            self.args = arg
    class SelectDeviceError(Exception):
        def __init__(self, arg):
            self.args = arg


class ADB:
    def __init__(self,adb=define.ADBPath):
        self.adb = adb
        self.selectDevice = None
        os.system(self.adb + ' start-server')

    def adbServer(self,status):
        if status=='start':
            os.system(self.adb + ' start-server')
        elif status=='kill':
            os.system(self.adb + ' kill-server')
        elif status=='restart':
            os.system(self.adb + ' kill-server')
            os.system(self.adb + ' start-server')

    @property
    def devices(self):
        output = list(os.popen(self.adb + ' devices'))
        output.pop(0)
        output.pop(-1)
        outputList = []
        for line in output:
            Process = re.split('\t|\n', line)
            Process.pop(-1)
            outputList.append(Process)
        return outputList

    def select(self, device):
        self.selectDevice = device

    def connect(self, ip, port=5555):
        status = os.system(self.adb + f" connect {ip}:{str(port)}")
        return status

    def disconnect(self, deviceName):
        status = os.system(self.adb + f" disconnect {deviceName}")
        return status

    def install(self, path, args='-r'):
        if self.selectDevice == None:
            raise errors.SelectDeviceError('The device was not set')
        status = list(os.popen(self.adb + " install -s " + self.selectDevice + " install " + args + " " + path))
        if ['Success\n'] not in status:
            raise errors.InstallError(str(status))
        else:
            return 'Success'

    def uninstall(self, packageName):
        if self.selectDevice == None:
            raise errors.SelectDeviceError('The device was not set')
        status = list(os.popen(self.adb + " -s " + self.selectDevice + " uninstall " + packageName))
        if ['Success\n'] not in status:
            raise errors.UninstallError(str(status))
        else:
            return 'Success'

    def push(self, source=None, destination='/sdcard'):
        if self.selectDevice == None:
            raise errors.SelectDeviceError('The device was not set')
        if source == None:
            raise errors.InputError
        else:
            status = list(os.popen(self.adb + " -s " + self.selectDevice + " push " + source + " " + destination))
            return status

    def pull(self, source=None, destination=None):
        if self.selectDevice == None:
            raise errors.SelectDeviceError('The device was not set')
        if source == None or destination == None:
            raise errors.InputError
        else:
            status = list(os.popen(self.adb + " -s " + self.selectDevice + " pull " + source + " " + destination))
            return status

    def shell(self, commands):
        if self.selectDevice == None:
            raise errors.SelectDeviceError('The device was not set')
        status = list(os.popen(self.adb + " -s " + self.selectDevice + " shell " + commands))
        return status

    def adbCommands(self, commands):
        if self.selectDevice == None:
            raise errors.SelectDeviceError('The device was not set')
        status = list(os.popen(self.adb + " -s " + self.selectDevice + " " + commands))
        return status


class Interface:
    def __init__(self, ExtName):
        self.ExtName = ExtName

    def DialogBox_double(self, title, info, continueText='y'):
        centerTitle = self.ExtName + ":" + title.ljust(20, '=')
        print('=' * len(centerTitle))
        print(centerTitle)
        print('=' * len(centerTitle))
        print(info)
        print('=' * len(centerTitle))
        if input() == continueText:
            return True
        else:
            return False

    def selectFile(self, title=language.CustomTitle_SelectFile):
        DisplayTitle = self.ExtName + ':' + title
        if define.LibPlatform == 'desktop':
            try:
                if define.selectGUI:
                    from PyQt5.QtWidgets import QFileDialog
                    fileName, fileType = QFileDialog.getOpenFileName(self, DisplayTitle, os.getcwd(), "All Files(*)")
            except ImportError:
                centerTitle = DisplayTitle.ljust(20, '=')
                print('=' * len(centerTitle))
                print(centerTitle)
                print('=' * len(centerTitle))
                print(language.DragFileToInputBox)
                print('=' * len(centerTitle))
                fileName = input(language.InputBox)

        elif define.LibPlatform == 'apple':
            centerTitle = DisplayTitle.ljust(20, '=')
            print('=' * len(centerTitle))
            print(centerTitle)
            print('=' * len(centerTitle))
            print(language.AppleSelectFile.format(define.HomePath + str("/idbShare")))
            print('=' * len(centerTitle))
            for root, dirs, files in os.walk(define.HomePath + '/idbShare', topdown=False):
                for name in files:
                    print(os.path.join(root, name))
            print('=' * len(centerTitle))
            fileName = input(language.InputBox)
        elif define.LibPlatform == 'android':
            centerTitle = DisplayTitle.ljust(20, '=')
            print('=' * len(centerTitle))
            print(centerTitle)
            print('=' * len(centerTitle))
            print(language.AndroidSelectFile.format(define.HomePath + str("/idbShare")))
            print('=' * len(centerTitle))
            for root, dirs, files in os.walk(define.HomePath + '/idbShare', topdown=False):
                for name in files:
                    print(os.path.join(root, name))
            print('=' * len(centerTitle))
            fileName = input(language.InputBox)
        return fileName
