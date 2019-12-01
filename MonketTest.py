import os, threading, time, subprocess
from PerConfig import AppPerCon
from AppMonitor import AppMoni
from AppAdbCom import AdbDebug
from AppDevinfo import DeviceMsg
from AppOperateFile import OperateFile
from AppOperatePick import OperatePick
from AppReport import Report

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.realpath('__file__')), p))

ad = AdbDebug()
apm = AppMoni()
devMs = DeviceMsg()
pick = OperatePick()
Config = AppPerCon()

MemTestFlag = 0
monkey_log = ''
path_log = ''

def get_phone(dev):
    phone_info = devMs.GetDevMsg(dev)
    print(phone_info)
    app = {}
    app['phone_name'] = phone_info[0]['phone_name'] + '_' + phone_info[0]['phone_model'] + '_' + phone_info[0]['release']
    app['rom'] = phone_info[1]
    app['kel'] = phone_info[2]
    app['pix'] = phone_info[3]
    return app

def Create_pickle(dev, data):
    print('创建持久性文件.....')
    if apm.IsIp(dev) == True:
        devIP = dev.split(':')[0].replace('.', '')
        freemen = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Free_mem.pickle")  # 空闲状态
        medimen = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Medium_mem.pickle")  # 中等压力
        fullmen = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Full_mem.pickle")  # 满压力
        freecpu = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Free_cpu.pickle")  # 空闲状态
        medicpu = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Medium_cpu.pickle")  # 中等压力
        fullcpu = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Full_cpu.pickle")  # 满压力
        freejiff = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Free_jiff.pickle")  # 空闲状态
        medijiff = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Medium_jiff.pickle")  # 中等压力
        fulljiff = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Full_jiff.pickle")  # 满压力
        medifps = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Medium_fps.pickle")  # 中等压力
        fullfps = PATH(Config.info_path + devIP + "_" + Config.package_name + "_" + "Full_fps.pickle")  # 满压力
    else:
        freemen = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Free_mem.pickle")  # 空闲状态
        medimen = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Medium_mem.pickle")  # 中等压力
        fullmen = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Full_mem.pickle")  # 满压力
        freecpu = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Free_cpu.pickle")  # 空闲状态
        medicpu = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Medium_cpu.pickle")  # 中等压力
        fullcpu = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Full_cpu.pickle")  # 满压力
        freejiff = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Free_jiff.pickle")  # 空闲状态
        medijiff = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Medium_jiff.pickle")  # 中等压力
        fulljiff = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Full_jiff.pickle")  # 满压力
        medifps = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Medium_fps.pickle")  # 中等压力
        fullfps = PATH(Config.info_path + dev + "_" + Config.package_name + "_" + "Full_fps.pickle")  # 满压力

    OperateFile(freemen).mkdir_file()
    OperateFile(medimen).mkdir_file()
    OperateFile(fullmen).mkdir_file()
    OperateFile(freecpu).mkdir_file()
    OperateFile(medicpu).mkdir_file()
    OperateFile(fullcpu).mkdir_file()
    OperateFile(freejiff).mkdir_file()
    OperateFile(medijiff).mkdir_file()
    OperateFile(fulljiff).mkdir_file()
    OperateFile(medifps).mkdir_file()
    OperateFile(fullfps).mkdir_file()

    OperateFile(PATH(Config.info_path + "sumInfo.pickle")).mkdir_file()  # 用于记录是否已经测试完毕，里面存的是一个整数
    OperateFile(PATH(Config.info_path + "info.pickle")).mkdir_file()  # 用于记录统计结果的信息，是[{}]的形式
    pick.writeSum(0, data, PATH(Config.info_path + "sumInfo.pickle"))  # 初始化记录当前真实连接的设备数
    print('持久性文件创建完成')

def unlockScreen(dev):
    cmd_openScreen = '-s %s shell input keyevent 224' % (dev)
    cmd_slide = '-s %s shell input swipe 300 500 1000 500' % (dev)
    ad.call_adb(cmd_openScreen)
    time.sleep(0.5)
    ad.call_adb(cmd_slide)

def logProcess(dev, runtime):
    logcat_log = path_log + '//' + runtime + 'logcat.log'
    cmd_logcat = '-s ' + dev + ' logcat -d > %s' % (logcat_log)
    ad.call_adb(cmd_logcat)
    print('logcat 完成')

    traces_log = path_log + '//' + runtime + 'traces.log'
    cmd_traces = '-s ' + dev + ' shell cat /data/anr/traces.txt > %s' % (traces_log)
    ad.call_adb(cmd_traces)
    print('traces_log 完成')

def monkeyStart(dev, runtime, flag):
    global path_log
    adb_monkey = ''
    if apm.IsIp(dev):
        devIP = dev.split(':')[0].replace('.', '')
        path_log = Config.log_location + '_' + devIP
    else:
        path_log = Config.log_location + '-' + dev
    device_dir = os.path.exists(path_log)
    if device_dir:
        print("log已存在，继续执行测试!")
    else:
        os.mkdir(path_log)
    if flag == 2:
        adb_monkey = "shell monkey -p %s -s %s %s" % (Config.package_name, Config.monkey_seed, Config.monkey_parameters_full)
    elif flag == 1:
        adb_monkey = "shell monkey -p %s -s %s %s" % (Config.package_name, Config.monkey_seed, Config.monkey_parameters_medi)
    global monkey_log
    monkey_log = path_log + "//" + runtime + "monkey.log"
    cmd_monkey = "adb -s %s %s > %s" % (dev, adb_monkey, monkey_log)
    subprocess.Popen(cmd_monkey, shell=True)
    print('Monkey成功开始')

def mediMemTest(dev, app):
    print("--------------开始执行测试----------------")
    print("--------------设备：%s 场景2：中等压力下APP性能指标----------------" % dev)
    ad.adbStopActivity(dev, Config.package_name)
    run_time = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    print(run_time)

    print(Config.info_path)

    monkeyStart(dev, run_time, 1)
    logProcess(dev, run_time)
    while True:
        try:
            with open(monkey_log, 'rb') as monkeylog:
                time.sleep(2)
                print('睡眠结束')

                apm.pid_mem(dev, Config.package_name, 1)
                apm.pid_cpuRate(dev, Config.package_name, 1)
                apm.pid_fps(dev, Config.package_name, 1)

                print('apm结束')

                str1 = monkeylog.read()
                string1 = str(str1, 'utf-8')

                if string1.count('Monkey finished') > 0:
                    print('monkey脚本执行完毕')
                    app[dev] = {"header": get_phone(dev)}
                    app[dev]["header"]["net"] = Config.net
                    pick.writeInfo(app, PATH(Config.info_path + "info.pickle"))
                    print("--------------设备：%s 场景2：中等压力下测试完成----------------" % dev)
                    break
        except:
            print('异常')
            break

def fullMemTest(dev):
    print("--------------开始执行测试----------------")
    print("--------------设备：%s 场景3：满压力下APP性能指标----------------" % dev)
    ad.adbStopActivity(dev, Config.package_name)
    run_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time()))
    monkeyStart(dev, run_time, 2)
    logProcess(dev, run_time)
    while True:
        try:
            with open(monkey_log, 'rb') as monkeylog:
                time.sleep(2)  # 每2秒采集一次
                apm.pid_mem(dev, Config.package_name, 2)
                apm.pid_cpuRate(dev, Config.package_name, 2)
                #fps测试需要事先开启手机开发者模式里的GPU显示，否则运行出错
                apm.pid_fps(dev, Config.package_name, 2)

                str1 = monkeylog.read()
                string1 = str(str1, 'utf-8')

                if string1.count('Monkey finished') > 0:
                    print("--------------设备：%s 场景3：满压力下测试完成----------------" % dev)
                    break
        except:
            break

def start(dev):
    rt = os.popen('adb devices').readlines()  # os.popen()执行系统命令并返回执行后的结果
    print(rt)
    num = len(rt) - 2
    print(num)
    app = {}
    Create_pickle(dev, num)
    # unlockScreen(dev)
    # 中等压力下测试
    print('88888888888')
    mediMemTest(dev, app)
    print('生成测试报告......')
    rep = Report(dev, "Alink V2.6.17 性能测试报告", "Medium")
    print(rep)
    rep.createReport(dev)
    print("测试报告生成完毕")

#启动MONKEY多线程
class MonkeyTestThread(threading.Thread):
    def __init__(self, dev):
        threading.Thread.__init__(self)
        self.dev = dev
        self.thread_stop = False

    def run(self):
        time.sleep(2)
        start(self.dev)



def create_threads_monkey(device_list):
    Thread_instances = []
    if device_list != []:
        for id_instance in device_list:
            dev = id_instance
            MontestInstance = MonkeyTestThread(dev)
            Thread_instances.append(MontestInstance)
        for instance in Thread_instances:
            instance.start()



if __name__ == '__main__':
    device_dir = os.path.exists(AppPerCon.info_path)
    if device_dir:
        print("持久性目录info已存在，继续执行测试!")
    else:
        #os.mkdir(AppPerformanceConfig.info_path)  # 创建持久性目录,需要在文件存在的情况下创建二级目录
        os.makedirs(AppPerCon.info_path)   # 使用makedirs可以在文件夹不存在的情况下直接创建
    device_list = apm.get_device()
    if ad.checkDevices():
        print("设备存在")
        create_threads_monkey(device_list)
    else:
        print("设备不存在")



































