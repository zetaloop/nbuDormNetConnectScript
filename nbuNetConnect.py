import requests
import json
import re
import traceback
import time
import subprocess
import threading

lock = threading.Lock()


def disConnect():
    with open("./ui.l") as f:
        userId = f.readline()
        if len(userId) == 0:
            print("您还未使用本工具连接过，请先连接。")
            return 0
    url = "http://10.36.100.2:8181/eportal/InterFace.do?method=logout"
    params = {"userIndex": userId}
    res = requests.post(url, params=params, verify=False)
    res.encoding = "utf-8"
    print(json.loads(res.text)["message"])


def connect():
    with open("./usrs.txt", "r", encoding="utf-8") as f:
        usrsInfo = f.readline()
        if len(usrsInfo) < 26:
            print("请先设定账号和密码")
            return 0
    usrsInfo = json.loads(usrsInfo)
    res = requests.get("http://www.gstatic.com/generate_204").text
    try:
        url_toPost = re.findall("href='(.*?)'</script>", res)[0]
    except Exception as e:
        print(
            "获取设备信息失败。1:您可能已经是连接状态。2:检查网线并暂时关闭wlan功能，再重试。"
        )
        print(traceback.format_exc())
        return 0
    sess = requests.session()
    url = url_toPost
    headers = {"Content-Type": "text/html;charset=UTF-8"}
    sess.get(url=url, headers=headers, verify=False)
    print("====发送连接请求")
    url = "http://10.36.100.2:8181/eportal/InterFace.do?method=login"
    params = {
        "userId": usrsInfo["ID"],
        "password": usrsInfo["Password"],
        "service": "",
        "queryString": re.findall("jsp\\?(.*)", url_toPost)[0],
        "operatorPwd": "",
        "operatorUserId": "",
        "validcode": "",
        "passwordEncrypt": "false",
    }
    res = sess.post(url, params=params, verify=False)
    res.encoding = "utf-8"
    res = json.loads(res.text)
    if res["result"] == "success":
        print("连接成功！")
        with open("./ui.l", "w") as f:
            f.write(res["userIndex"])
    else:
        print("连接失败！有可能是：")
        print("1、", res["message"])
        print("2、服务器出现问题。")


def netDetiction():
    while True:
        try:
            net_code = subprocess.run(
                ["ping", "www.baidu.com"], stdout=subprocess.DEVNULL
            )
            if net_code.returncode:
                print("==网络似乎断了")
                print("开始disconnect并reconnect")
                disConnect()
                connect()
        except Exception as e:
            print("请检查网线连接是否正常！")
            print(traceback.format_exc())
        time.sleep(30)


if __name__ == "__main__":
    net_de = threading.Thread(target=netDetiction)
    net_de.start()
    print("==========", "PRODUCED BY LEE jb", "==========")
    print("==========", "宁大only", "==========")
    print(
        "你好！若您现在已联网并是第一次使用本工具，请线前往http://10.36.100.2:8181/eportal/gologout.jsp登出，再使用本工具登录。"
    )
    while True:
        print("1:Connect;0:DisConnect")
        res = input(">>")
        try:
            if str(res) == "1":
                connect()
            elif str(res) == "0":
                disConnect()
        except Exception as e:
            print("未知错误，请联系开发者QQ：731908970")
            print(traceback.format_exc())
