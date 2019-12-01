import os,re
from AppAdbCom import AdbDebug
ad = AdbDebug()

class DeviceMsg(object):

    # 获取手机基本信息
    def GetDevModel(self, dev):
        '''
        返回字典
        release：Android版本
        phone_name：手机名
        phone_model：手机品牌
        :param dev:
        :return:
        '''
        result = {}
        result["release"] =  ad.adbGetAndroidVersion(dev)
        result["phone_name"] = ad.adbGetDeviceName(dev)
        result["phone_model"] = ad.adbGetDeviceBrand(dev)
        return result

    # 获取手机内存总数
    def GetDevMemTotal(self, dev):
        '''
        通过adb shell cat /proc/meminfo
        :param dev: 设备名
        :return: 手机内存总数
        '''
        list = ad.adbGetDevMem(dev).split()
        for k, v in enumerate(list):
            if str(v) == 'MemTotal:':
                return int(list[k+1])

    # 获取手机处理器核数量
    def GetDevCpuCore(self, dev):
        '''
        通过adb shell cat /proc/cpuinfo
        :param dev: 设备名
        :return: 手机处理器核数量
        '''
        resp = ad.adbGetDevCPU(dev)
        return str(len(re.findall("processor", resp)))

    # 获取手机屏幕分辨率
    def GetDevPix(self, dev):
        '''
        通过adb shell wm size
        :param dev: 设备名
        :return: 手机屏幕分辨率
        '''
        resp = ad.adbGetScreenSize(dev).split()[2]
        return resp

    # 同时返回以上四个方法的返回值
    def GetDevMsg(self, dev):
        '''
        返回Android系统版本，手机名，手机品牌字典
        返回手机分辨率
        返回手机内存总数
        返回手机处理器核心数
        :param dev:
        :return: 所有devinfo，
        '''
        pix = self.GetDevPix(dev)
        men_total = self.GetDevMemTotal(dev)
        phone_msg = self.GetDevModel(dev)
        cpu_sum = self.GetDevCpuCore(dev)
        print(dev + ":"+ pix, men_total, phone_msg, cpu_sum)
        return phone_msg, men_total, cpu_sum, pix


if __name__ == "__main__":
   pass


