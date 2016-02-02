#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import os
import re
import sys
import glob


class UnicodeStreamFilter:
    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = self.target.encoding
    def write(self, s):
        if type(s) == str:
            s = s.decode('utf-8')
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
        self.target.write(s)

if sys.stdout.encoding == 'cp936':
    sys.stdout = UnicodeStreamFilter(sys.stdout)


# 压缩CSS函数
def compress_css(newcsslocal):
    # 压缩css的正则规则
    reglis = {r'/\*.*?\*/': '', r'\n': '', r'\r': '', r'\v': '', r'\t': '', r' *; *': ';', r' *{ *': '{', r' *} *': '}'}
    for reg in reglis:
        newcssfile = open(newcsslocal, 'r')
        newcssread = newcssfile.read()
        repl = re.sub(reg, reglis[reg], newcssread, flags=re.S)  # 根据正则替换特定字符串
        newcssfile.close()
        os.remove(newcsslocal)
        newcssfile = open(newcsslocal, 'w')
        newcssfile.seek(0)
        newcssfile.write(repl)
        newcssfile.flush()
        os.fsync(newcssfile.fileno())
        newcssfile.close()
    print("文件压缩成功！\n")


# 循环导入其他层CSS文件并替换内容
def import_css(imlocal, filelist=[]):
    global importcsstmp
    realdir = os.path.dirname(imlocal)+'/'
    try:
        cssfile = open(imlocal, 'r')
    except:
        print("文件%s不存在,导入失败! \n"%imlocal)
        return
    rcss = cssfile.read()
    importlist = re.findall(r'\@import \".*?\";', rcss)
    if importlist:
        filelist.append(imlocal)
        for imone in importlist:
            import_local = re.search(r'\"(.*?)\"', imone).group(1)
            imreallocal = os.path.join(realdir, import_local)
            imreallocal = os.path.normpath(imreallocal)
            # 判断是否有循环调用现象
            if imreallocal in filelist:  #
                print("文件%s存在循环调用现象!放弃导入循环内容!\n"%imreallocal)
                return ''
            else:
                csscontent = import_css(imreallocal, filelist)
                importcsstmp = rcss.replace(str(imone), str(csscontent))
                rcss = importcsstmp
    cssfile.close()
    return rcss


# 第一层CSS导入及替换内容
def root_css(reallocal):
    filelist = [reallocal]  # 初始化调用文件的上层文件列表
    global rootcsstmp
    localdir, imname = os.path.split(reallocal)
    today = datetime.date.today()
    newcsslocal = os.path.join(localdir, today.strftime('%Y%m%d'), imname)
    # 判断要生成的文件和目录是否存在
    if os.path.isfile(newcsslocal):
        raw_input("需生成文件已存在! 程序将重新生成并覆盖该文件! 按Enter确认……\n")
    elif not os.path.exists(os.path.join(localdir, today.strftime('%Y%m%d'))):
        try:
            os.mkdir(os.path.join(localdir, today.strftime('%Y%m%d')))
        except OSError as err:
            if 'Permission denied' in err:
                raw_input("目录无写入权限! 请检查后重新运行! 按Enter关闭程序……")
                return
            else:
                raw_input("所需目录生成出错! 请检查后重新运行! 按Enter关闭程序……")
                return
        except:
            raw_input("所需目录生成出错! 请检查后重新运行! 按Enter关闭程序……")
            return

    print("正在创建新文件%s……\n"%newcsslocal)
    realdir = os.path.dirname(reallocal)
    cssfile = open(reallocal, 'r+')
    rcss = cssfile.read()
    importlist = re.findall(r'\@import \".*?\";', rcss)
    # 如果内容中有import 语句则调用import_css()
    if importlist:
        for imone in importlist:
            importlocal = re.search(r'\"(.*?)\"', imone).group(1)
            #imreallocal = os.path.normpath(realdir+importlocal)
            imreallocal = os.path.join(realdir, importlocal)
            csscontent = import_css(imreallocal, filelist)
            newfile = open(newcsslocal, 'w')
            rootcsstmp = rcss.replace(str(imone), str(csscontent))
            rcss = rootcsstmp
            newfile.write(rootcsstmp)
            newfile.close()
    # 没有import 语句则直接复制到新文件
    else:
        newfile = open(newcsslocal, 'w')
        newfile.seek(0)
        newfile.write(rcss)
        newfile.close()
    print("新文件%s创建成功！开始压缩……\n"%newcsslocal)
    compress_css(newcsslocal)  # 调用compress_css()压缩新文件
    cssfile.close()


# 读取目录下css文件并调用root_css()处理文件内容
def maincss(localdir=False):
    if not localdir:
        localdir = os.getcwd()
    print("正在获取%s下css文件列表……\n"%localdir)

    csslist = glob.glob(r'%s/*.css'%localdir)
    if csslist:
        for imname in csslist:
            print imname
            root_css(imname)
    else:
        print("目录%s内无css文件!请检查后重新运行！"%localdir)
        return

if __name__ == '__main__':
    localdir = raw_input("请输入需遍历文件所在目录，默认为当前目录： ")
    maincss(localdir)
