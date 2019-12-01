import os

class AppPerCon(object):

    # 包名
    package_name = 'com.tencent.news'

    # activity
    alink_Activity = ''

    # 设备字典
    device_dict = {}

    # uid
    appuid = {'MATE8':{'news.activity.SplashActivity'}}

    # 网络
    net = 'wifi'

    # monkey种子数
    monkey_seed = 200

    # monkey指令
    monkey_parameters_full = "--throttle 50 --ignore-crashes --ignore-timeouts --pct-touch 80 --pct-trackball 5 --pct-appswitch 9 --pct-syskeys 1 --pct-motion 5 -v -v -v 10000"
    monkey_parameters_medi = "--throttle 150 --ignore-crashes --ignore-timeouts --pct-touch 80 --pct-trackball 5 --pct-appswitch 9 --pct-syskeys 1 --pct-motion 5 -v -v -v 2500"

    # log存放地址
    log_location = os.path.dirname(os.path.realpath(__file__)) + '/log'

    # info存放位置
    info_path = os.path.dirname(os.path.realpath(__file__)) + '/info' + '/'

    # report存放位置
    report_path = os.path.dirname(os.path.realpath(__file__)) + '/report/'