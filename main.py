from DrissionPage import ChromiumPage, ChromiumOptions
import getpass
import requests
import base64
import time
import wx
import threading
import sys
import random

co = ChromiumOptions().auto_port()
page1 = ChromiumPage(co)
page1.get('https://xk.nju.edu.cn/')
# login_name = input("你的学号：")
login_name = "1111"
# login_pwd = getpass.getpass("你的密码：")
login_pwd = "aaaa"
vcode     = ""
loop_flag  = True
pause_flag = False
pause_lowb = 5.0
pause_upb  = 20.0
loop_lock  = threading.Lock()
crt_flag   = False
batch_n    = 0
success_list = []


def load():
    print("正在加载网页")
    page1.refresh()
    time.sleep(1.5)
    # if page1.ele('.cv-btn cv-mb-8'):
    #     page1.ele('.cv-btn cv-mb-8').click()
    #     page1.ele('#courseBtn').click()
    #     page1.eles('.tab-first')[-1].click()
    #     return
    session = requests.Session()
    verifyCodeDiv = page1.ele('#verifyCodeDiv')
    pic = verifyCodeDiv.ele('tag:img')
    print(pic)
    pic_addr = pic.attr('src')
    pic = session.get(
        pic_addr
    ).content
    pic_res = requests.post(
        "https://captcha.994321.xyz/ocr/b64/json", data=base64.b64encode(pic)
    ).json()
    ocr_vcode = pic_res["result"]
    print(ocr_vcode)
    # vcode = input("输入你看到的验证码：")
    page1.ele('#loginName').input(login_name)
    page1.ele('#loginPwd').input(login_pwd)
    page1.ele('#verifyCode').input(ocr_vcode)
    page1.ele('#studentLoginBtn').click()

def reopen():
    print("重新打开浏览器")
    global page1
    page1.close()
    page1 = ChromiumPage(co)
    page1.get('https://xk.nju.edu.cn/')
    load()
    batch_select()

def reload():
    print("重新加载网页")
    global page1
    page1.get('https://xk.nju.edu.cn')
    page1.ele('.cv-btn cv-mb-8').click()
    page1.eles('.tab-first')[-1].click()



def batch_select():
    while True:
        global batch_n
        if page1.ele('.jqx-rc-all jqx-window jqx-popup jqx-widget jqx-widget-content'):
            page1.eles('.cv-electiveBatch-select')[batch_n-1].click()
            page1.ele("确认").click()
            page1.ele('#courseBtn').click()
            page1.eles('.tab-first')[-1].click()
            break
        else:
            print("验证码识别错误，请耐心等待")
            load()

#input("选择批次并回车")


def main_loop():
    global page1
    while True:
        try:
            page1.refresh()
            wanted_courses = page1.eles('.course-tr ')
            if not wanted_courses:
                print("未进入正确界面，或者收藏列表为空，正在重载")
                assert 0
            for wanted_course in wanted_courses:
                print(wanted_course('.kcmc course-cell').text, wanted_course('.jsmc course-cell').text, wanted_course('.yxrs course-cell').text)
                statue = wanted_course('.yxrs course-cell').text
                if '已满' in statue:
                    print("已满，尝试刷新")
                else:
                    while True:
                        wanted_course.child(8).ele('选择').click(by_js=True)
                        page1.ele('.cv-sure cvBtnFlag').wait.displayed()
                        page1.ele('.cv-sure cvBtnFlag').click()
                        dialog = page1.ele('#cvDialog').child(2).child(1)
                        if "失败" in dialog.texts():
                            dialog.next().click()
                            print("选课失败")
                            assert 0
                        else:
                            dialog.next().click()
                            print(f"{wanted_course.texts()}选课成功") 
                            assert 0
        except:
            try:
                reload()
            except:
                reopen()
    

def t_loop():
    global page1
    while True:
        with loop_lock:
            if not loop_flag: continue
        with loop_lock:
            if pause_flag:
                global pause_upb, pause_lowb
                if pause_upb < pause_lowb: pause_upb, pause_lowb = pause_lowb, pause_upb
                slf = random.uniform(pause_lowb, pause_upb)
                print(f"本轮随机时间{slf}")
                time.sleep(slf)
        try:
            page1.refresh()
            wanted_courses = page1.eles('.course-tr ')
            if not wanted_courses:
                print("未进入正确界面，或者收藏列表为空，正在重载")
                assert 0
            for wanted_course in wanted_courses:
                print(wanted_course('.kcmc course-cell').text, wanted_course('.jsmc course-cell').text, wanted_course('.yxrs course-cell').text)
                course_name = wanted_course('.kcmc course-cell').text
                statue = wanted_course('.yxrs course-cell').text
                if '已满' in statue:
                    print("已满，尝试刷新")
                else:
                    while True:
                        wanted_course.child(8).ele('选择').click(by_js=True)
                        page1.ele('.cv-sure cvBtnFlag').wait.displayed()
                        page1.ele('.cv-sure cvBtnFlag').click()
                        dialog = page1.ele('#cvDialog').child(2).child(1)
                        if "失败" in dialog.texts():
                            dialog.next().click()
                            print("选课失败")
                            assert 0
                        else:
                            dialog.next().click()
                            print(f"{wanted_course.texts()}选课成功") 
                            success_list.append(course_name)
                            assert 0
        except:
            try:
                reload()
            except:
                reopen()

def wx_wrapper():
    load()
    batch_select()
    t_loop()

class RedirectText:
    def __init__(self, wx_text_ctrl):
        self.out = wx_text_ctrl

    def write(self, string):
        wx.CallAfter(self.out.AppendText, string)

    def flush(self):
        pass  # 必须提供，但这里不需要实际实现
    
class MyApp(wx.App):
    def OnInit(self):
        # 创建一个窗口
        frame = wx.Frame(None, title="NJU抢课王", size=(400, 300))
        panel = wx.Panel(frame)
        self.id_lable = wx.StaticText(panel, label="学号", pos=(20, 20))
        self.id_text  = wx.TextCtrl(panel, pos=(20, 50), size=(150, -1))
        self.pwd_lable = wx.StaticText(panel, label="密码", pos=(20, 80))
        self.pwd_text  = wx.TextCtrl(panel, pos=(20, 110), size=(150, -1))
        self.label3 = wx.StaticText(panel, label="暗号", pos=(20, 140))
        self.text_ctrl3 = wx.TextCtrl(panel, pos=(20, 170), size=(150, -1))

        # 创建一个按钮
        button = wx.Button(panel, label="Submit", pos=(20, 200))
        button.Bind(wx.EVT_BUTTON, self.startMainLoop)


        # 显示窗口
        frame.Show()
        return True

    def startMainLoop(self, event):
        global login_name, login_pwd
        print(self.id_text.GetValue())
        print(self.pwd_text.GetValue())
        login_name = self.id_text.GetValue()
        login_pwd  = self.pwd_text.GetValue()
        qkw = threading.Thread(target=wx_wrapper)
        qkw.start()

    # 按钮点击事件处理函数
    def on_button_click(self, event):
        self.label.SetLabel("Button Clicked!")  # 更改标签文本

class LoginFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(LoginFrame, self).__init__(*args, **kw)
        
        panel = wx.Panel(self)
        
        self.qkw = threading.Thread(target=wx_wrapper)
        
        self.lable_id   = wx.StaticText(panel, label="学号", pos=(20, 25))
        self.input_id   = wx.TextCtrl(panel, pos=(20, 50), size=(150, -1))
        self.label_pwd  = wx.StaticText(panel, label="密码", pos=(20, 85))
        self.input_pwd  = wx.TextCtrl(panel, pos=(20, 110), size=(150, -1), style=wx.TE_PASSWORD)
        self.label3     = wx.StaticText(panel, label="帅哥", pos=(20, 145))
        self.text_ctrl3 = wx.TextCtrl(panel, pos=(20, 170), size=(150, -1))
        self.label_batch= wx.StaticText(panel, label="批次", pos=(200, 25))
        self.input_batch= wx.TextCtrl(panel, pos=(200, 50), size=(70, -1))
        self.label4     = wx.StaticText(panel, label="不要碰那个蹦出来的chrome浏览器", pos=(20, 210))
        
        submit_button = wx.Button(panel, label="Login", pos=(200, 110))
        submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        exit_button = wx.Button(panel, label="quit", pos = (200, 170))
        exit_button.Bind(wx.EVT_BUTTON, self.on_quit)
        self.SetSize((400, 300))
        self.SetTitle("NJU传奇抢课王 - Login")

    def on_quit(self, event):
        self.Close()
        global page1
        page1.close()
        exit(0)

    def on_submit(self, event):
        print("on submit")
        self.Hide()
        global login_name, login_pwd, loop_lock, loop_flag, crt_flag, batch_n
        login_name = self.input_id.GetValue()
        login_pwd  = self.input_pwd.GetValue()
        if self.input_batch.strip():
            batch_n    = int(self.input_batch.GetValue())
        else: 
            batch_n    = -1
        # if self.text_ctrl3.GetValue() != "cyh": exit(0)
        with loop_lock:
            loop_flag = True
        if not crt_flag:
            self.qkw.start()
            crt_flag = True
        print("跳转至控制台")
        second_frame = SecondFrame(None, title="NJU传奇抢课王 - 抢课控制台", parent=self)
        second_frame.Show()

class SecondFrame(wx.Frame):
    def __init__(self, *args, parent=None, **kw):
        super(SecondFrame, self).__init__(*args, **kw)
        
        panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        label = wx.StaticText(panel, label="控制台", pos=(30, 50))
        self.text_ctrl = wx.TextCtrl(panel, pos=(30, 70), size=(300, 250), style=wx.TE_MULTILINE | wx.TE_READONLY)
        redir = RedirectText(self.text_ctrl)
        sys.stdout = redir

        
        self.label_upb  = wx.StaticText(panel, label="随机时间分布(输入小数)(秒)", pos=(30, 23))
        self.input_lowb = wx.TextCtrl(panel, pos=(180, 20), size=(50, -1))
        self.input_upb  = wx.TextCtrl(panel, pos=(250, 20), size=(50, -1))

        global success_list

        # 创建 wx.ListBox 或 wx.TextCtrl 控件
        # self.list_box = wx.ListBox(panel, size=(100, 50), choices=success_list)
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(100, 50))

        # 布局
        # self.list_box.SetPosition((365, 20))  # 设置 ListBox 的位置
        # self.list_box.SetSize((100, 50))    # 设置 ListBox 的大小

        self.succ_info  = wx.StaticText(panel, label="当前抢课成果", pos=(365, 15))
        self.text_ctrl.SetPosition((365, 30))  # 设置 TextCtrl 的位置
        self.text_ctrl.SetSize((100, 130))     # 设置 TextCtrl 的大小

        # 绑定定时器用于实时更新
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_suc_display, self.timer)
        self.timer.Start(3000)  # 每秒钟更新一次

        self.pause_button = wx.Button(panel, label="暂停/继续", pos=(365, 190))
        self.pause_button.Bind(wx.EVT_BUTTON, self.on_pause)

        self.mode_button = wx.Button(panel, label="开启/关闭延时刷新", pos=(365, 230))
        self.mode_button.Bind(wx.EVT_BUTTON, self.on_switch_mode)
        
        self.back_button = wx.Button(panel, label="quit", pos=(365, 270))
        self.back_button.Bind(wx.EVT_BUTTON, self.on_quit)

        self.parent = parent
        
        self.SetSize((520, 400))
    
    def update_suc_display(self, event):
        global success_list
        if success_list:
            # 如果列表不为空，显示列表内容
            # self.list_box.Set(success_list)
            self.text_ctrl.SetValue("\n".join(success_list))
        else:
            # self.list_box.Set(["革命尚未成功,同志仍需努力"])
            self.text_ctrl.SetValue("革命尚未成功,同志仍需努力")

    def on_switch_mode(self, event):
        global loop_lock, pause_flag, pause_lowb, pause_upb
        print("等待时间方法切换")
        with loop_lock:
            print("获取锁")
            if pause_flag: print("切换到急速刷新模式，比较狂野ᕙ༼ຈ ͜ຈ༽ᕗ")
            else: 
                time.sleep(1)
                print("切换到随机时间刷新模式，比较温柔(*´▽`*)❀")
                pause_lowb = float(self.input_lowb.GetValue())
                pause_upb  = float(self.input_upb.GetValue())
                print(f"等待时间：{pause_lowb}秒-{pause_upb}秒")
            print("3秒后继续抢课~")
            pause_flag = not pause_flag
            time.sleep(3)


    def on_pause(self, event):
        global loop_lock, loop_flag
        with loop_lock:
            print("获取锁")
            loop_flag = not loop_flag

    def on_quit(self, event):
        global page1
        with loop_lock:
            self.Close()
            page1.close()
            exit(0)

    def on_close(self, event):
        global page1
        page1.close()
        self.Close()
        exit(0)

if __name__ == '__main__':
    app = wx.App(False)
    frame_login = LoginFrame(None)
    frame_login.Show()
    app.MainLoop()
    # load()
    # batch_select()
    # main_loop()