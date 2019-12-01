import os
from PerConfig import AppPerCon

class AdbDebug(object):

    # 调用adb
    def call_adb(self, command):
        '''调用adb'''
        result = ''
        command_text = 'adb %s' % (command)
        results = os.popen(command_text, 'r')
        while True:
            line = results.readline()
            if not line:
                break
            result += line
            results.close()
            return result

    # 返回device，devices未实现
    def checkDevices(self):
        res = self.call_adb('devices')
        devices = res.partition('\n')[2].replace('\n', '').split('\tdevice')
        # return [device for device in devices if len(device) > 2]
        return devices

    # adb kill-server
    def adbStop(self):
        return self.call_adb('kill-server')

    # adb start-server
    def adbStart(self):
        return self.call_adb('start-server')

    # adb version
    def adbVersion(self):
        return self.call_adb('version')

    #
    def adbTcp(self, target):
        return self.call_adb('-s %s tcpip 5555' % (target))

    # adb connect with wifi
    def adbNetConOpen(self, target, address):
        return self.call_adb('-s %s connect %s' % (target, address))

    # adb disconnect with wifi
    def adbNetConClose(self, target, address):
        return self.call_adb('-s %s disconnect %s' % (target, address))

    # adb push
    def push(self, target, local, remote):
        result = self.call_adb('-s %s push %s %s' % (target, local, remote))
        return result

    # adb pull
    def pull(self, target, remote, local):
        result = self.call_adb('-s %s pull %s %s' % (target, remote, local))
        return result

    # adb install apk
    def adbInstallApk(self, target, local):
        return self.call_adb('-s %s install %s' % (target, local))

    # adb uninstall packagename
    def adbUninstallApk(self, target, packName):
        return self.call_adb('-s %s uninstall %s' % (target, packName))

    # adb shell list packages packagename
    def adbGetPmList(self, target, var):
        return self.call_adb('-s %s shell pm list packages %s' % (target, var))

    # adb shell pm clear packagename
    # 清楚应用缓存
    def adbCacheClear(self, target, packName):
        result = self.call_adb('-s %s shell pm clear %s' % (target, packName))
        return result.rstrip()

    # adb shell dumpsys packages packagename
    # 查看应用详细信息
    def adbGetAppInfo(self, target, packName):
        result = self.call_adb("-s %s shell dumpsys package %s" % (target, packName))
        return result.strip()

    # adb shell am start activity
    # 启动Activity
    def adbStartActivity(self, target, activity):
        result = self.call_adb("-s %s shell am start %s" % (target, activity))
        return result.rstrip()

    # adb shell am force-stop packagename
    # 强制停止Activity
    def adbStopActivity(self, target, packName):
        result = self.call_adb("-s %s shell am force-stop %s" % (target, packName))
        return result

    # adb shell getprop ro.product.model
    # 获得设备型号
    def adbGetDeviceModel(self, target):
        result = self.call_adb("-s %s shell getprop ro.product.model" % (target))
        return result.rstrip()

    # adb shell getprop ro.product.brand
    # 获取设备品牌
    def adbGetDeviceBrand(self, target):
        result = self.call_adb("-s %s shell getprop ro.product.brand" % (target))
        return result.rstrip()

    # adb shell getprop ro.product.name
    # 获得设备名称
    def adbGetDeviceName(self, target):
        result = self.call_adb("-s %s shell getprop ro.product.name" % (target))
        return result.rstrip()

    # adb shell getprop ro.product.board
    # 获得设备处理器型号
    def adbGetDeviceBoard(self, target):
        result = self.call_adb("-s %s shell getprop ro.product.board" % (target))
        return result.rstrip()

    # adb reboot
    # 设备重启
    def adbDeviceReboot(self, target):
        result = self.call_adb("-s %s reboot" % (target))
        return result.rstrip()

    # adb shell dumpsys battery
    # 获取电池状况
    def adbGetBattery(self, target):
        result = self.call_adb("-s %s shell dumpsys battery" % (target))
        return result.rstrip()

    # adb shell wm size
    # 获取屏幕分辨率
    def adbGetScreenSize(self, target):
        result = self.call_adb("-s %s shell wm size" % (target))
        return result.rstrip()

    # adb shell wm density
    # 获取屏幕dpi
    def adbGetScreenDPI(self, target):
        result = self.call_adb("-s %s shell wm density" % (target))
        return result.rstrip()

    # adb shell dumpsys window displays
    # 获取屏幕参数
    def adbGetScreenInfo(self, target):
        result = self.call_adb("-s %s shell dumpsys window displays" % (target))
        return result.rstrip()

    # adb shell getprop ro.build.version.release
    # 获取Android系统版本
    def adbGetAndroidVersion(self, target):
        result = self.call_adb("-s %s shell getprop ro.build.version.release" % (target))
        return result.strip()

    # adb shell ifconfig wlan0
    # 获取IP地址
    def adbGetDevIP(self, target):
        result = self.call_adb("-s %s shell ifconfig wlan0" % (target))
        if int(self.adbGetAndroidVersion(target).split(".")[0]) > 4:
            if  result.rsplit(":")[1][19:23] == "inet":
                return result.rsplit(":")[2][:13]
            else:
                print("WIFI未开启，请打开WIFI开关")
                return
        else:
            return result.rsplit(":")[1][4:17]

    # adb shell cat /sys/class/net/wlan0/address
    # 获取MAC地址
    def adbGetDevMac(self, target):
        result = self.call_adb("-s %s shell cat /sys/class/net/wlan0/address" % (target))
        return result.strip()

    # adb shell cat /proc/cpuinfo
    # 获取CPU信息
    def adbGetDevCPU(self, target):
        result = self.call_adb("-s %s shell cat /proc/cpuinfo" % (target))
        return result.strip()

    # adb shell cat /proc/meminfo
    # 获取系统内存信息
    def adbGetDevMem(self, target):
        result = self.call_adb("-s %s shell cat /proc/meminfo" % (target))
        return result.strip()

    # adb shell dumpsys meminfo oackagename
    # 获取应用内存信息
    def adbGetDevPidMem(self, target, packname):
        result = self.call_adb("-s %s shell dumpsys meminfo %s | grep TOTAL" % (target, packname))
        print(type(result))
        print(target, packname)
        return result

    # adb shell cat /proc/stat
    # 获取总的CPU使用时间
    def adbGetCpuTime(self, target):
        result = self.call_adb("-s %s shell cat /proc/stat" % (target))
        return result.strip()

    # adb shell cat /proc/pid/stat
    # 获取进程CPU时间片
    def adbGetPidJiff(self, target, pid):
        result = self.call_adb("-s %s shell cat /proc/%s/stat" % (target, pid))
        return result.strip()

    # adb shell dumpsys gfxinfo packagename
    # 获取进程fps
    def adbGetPidfps(self, target, packname):
        result = self.call_adb("-s %s shell dumpsys gfxinfo %s" % (target, packname))
        return result.strip()

    #
    # 获取进程流量信息
    def adbGetPidflow(self, target, packname, flag):
        flow = 0
        if int(self.adbGetAndroidVersion(target).split('.')[0]) < 8:
            uid = AppPerCon.appuid['MATE8'][packname]
            rec = self.call_adb("-s %s shell cat /proc/uid_stat/%s/tcp_rcv" % (target, uid)).strip()
            sen = self.call_adb("-s %s shell cat /proc/uid_stat/%s/tcp_snd" % (target, uid)).strip()
            # print rec, sen
            flow = float(rec) + float(sen)
        else:
            if flag == 1:
             #   self.adbStartActivity(target, activity)
                pid = self.adbGetPid(target, packname)
                print(pid)
                lis = self.call_adb("-s %s shell cat /proc/%s/net/dev" % (target, pid)).strip().split()
                for k, v in enumerate(lis):
                    if v == 'wlan0:':
                        recindex = k + 1
                        tranindex = k + 9
                        flow = float(lis[recindex])+float(lis[tranindex])
                        self.adbStopActivity(target, packname)
                        break
            else:
                    lis = self.call_adb("-s %s shell cat /proc/net/dev" % (target)).strip().split()
                    for k, v in enumerate(lis):
                        if v == 'wlan0:':
                            recindex = k + 1
                            tranindex = k + 9
                            flow = float(lis[recindex]) + float(lis[tranindex])
                            break
        return flow


    # adb shell ps | grep packagename
    # 获取进程pid
    def adbGetPid(self, target, packname):
        if int(self.adbGetAndroidVersion(target).split('.')[0]) < 8:
            pid = self.call_adb("-s %s shell ps | grep %s"%(target, packname)).rstrip().split("\n")
            if pid == ['']:
                print("this process doesn't exist")
                return None
            else:
                for item in pid:
                    if item.split()[8] == packname:
                        return item.split()[1]
        else:
            pid = self.call_adb("-s %s shell top -n 1 | grep %s" % (target, packname)).strip().split()
            if pid == []:
                print("this process doesn't exist")
                return None
            else:
                return pid[0]

    # adb shell cat /proc/pid/status
    # 获取uid
    def adbGetUid(self, target, packname):
        pid = self.adbGetPid(target, packname)
        lis = self.call_adb('-s %s shell cat /proc/%s/status' % (target, pid)).split()
        uid = 0
        for k, v in enumerate(lis):
            if v == 'Uid:':
                index = k + 1
                uid = lis[index]
                break
        return uid

    # adb shell am start -W activity
    # 获取app启动时间
    def adbGetAPPstartTime(self, target, activity):
        lis = self.call_adb('-s %s shell am start -W %s' % (target, activity))
        time = 0
        for k, v in enumerate(lis):
            if v == 'TotalTime:':
                index = k + 1
                time = lis[index]
                break
        return time

if __name__ == '__main__':
    pass


























