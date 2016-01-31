#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import os
import re


# 循环导入CSS文件内容
def import_css(reallocal):
    global importcsstmp
    realdir = os.path.dirname(reallocal)+'/'
    cssfile = open(reallocal, 'r+')
    rcss = cssfile.read()
    importlist = re.findall(r'\@import \".*?\";', rcss)
    if importlist != []:
        for imone in importlist:
            import_local = re.findall(r'\"(.*?)\"', imone)[0]
            imreallocal = realdir+import_local
            csscontent = import_css(imreallocal)
            importcsstmp = rcss.replace(str(imone), str(csscontent))
            rcss = importcsstmp
    cssfile.close()
    return rcss


# 第一层CSS导入及复制文件函数
def root_css(reallocal):
    global rootcsstmp
    print("正在创建新文件%s"%newcsslocal)
    realdir = os.path.dirname(reallocal)+'/'
    cssfile = open(reallocal,'r+')
    rcss = cssfile.read()
    importlist = re.findall(r'\@import \".*?\";', rcss)
    if importlist:
        for imone in importlist:
            importlocal = re.findall(r'\"(.*?)\"', imone)[0]
            imreallocal = realdir+importlocal
            csscontent = import_css(imreallocal)
            newfile = open(newcsslocal, 'w')
            rootcsstmp=rcss.replace(str(imone), str(csscontent))
            rcss = rootcsstmp
            newfile.write(rootcsstmp)
            newfile.close()
    else:
        newfile = open(newcsslocal, 'w')
        newfile.seek(0)
        newfile.write(rcss)
        newfile.close()
    print("新文件%s创建成功！开始压缩……"%newcsslocal)
    cssfile.close()


# 压缩CSS函数
def compress_css():

    for reg in reglis:
        newcssfile = open(newcsslocal, 'r')
        newcssread = newcssfile.read()
        repl = re.sub(reg, reglis[reg], newcssread, flags=re.S)
        newcssfile.close()
        os.remove(newcsslocal)
        newcssfile = open(newcsslocal, 'w')
        newcssfile.seek(0)
        newcssfile.write(repl)
        newcssfile.flush()
        os.fsync(newcssfile.fileno())
        newcssfile.close()
    print("文件压缩成功！")


def maincss():
    global reglis, newcsslocal
    localdir = raw_input('请输入css-src目录所在路径，默认为当前路径: ')
    if not localdir:
        localdir = os.getcwd()
    # 压缩函数的正则及需替换成的内容
    reglis = {r'/\*.*?\*/': '', r'\n': '', r'\r': '', r'\v': '', r'\t': '', r' *; *': ';', r' *{ *': '{', r' *} *': '}'}

    today = datetime.date.today()



    csslocal = localdir+'/css-src/nt/'

    print("正在获取%s下css文件列表……"%csslocal)
    try:
        csslist = os.listdir(csslocal)
    except OSError as err:
        print err
        if err.args[0] == 3 or 2:
            raw_input("css-src目录不存在!请检查后重新运行!按Enter关闭程序……")
            return

    try:
        os.mkdir(localdir+'/'+today.strftime('%Y%m%d'))
    except OSError as err:
        if 'File exists' in err:
            raw_input("需生成目录已存在! 程序将重新生成并覆盖该文件! 按Enter确认…….")
        elif 'Permission denied' in err:
            raw_input("目录无写入权限! 请检查后重新运行! 按Enter关闭程序……")
            return
        elif 183 in err.args : #Windows下目录已存在返回代码检测
            raw_input("需生成目录已存在! 程序将重新生成并覆盖该文件! 按Enter确认……")
        else:
            raw_input("所需目录生成出错! 请检查后重新运行! 按Enter关闭程序......")
            return
    except:
        raw_input("所需目录生成出错! 请检查后重新运行! 按Enter关闭程序......")
        return

    for imname in csslist:
        ext = imname.split('.')[-1]
        if ext == 'css':
            reallocal = csslocal+imname
            newcsslocal = localdir+'/'+today.strftime('%Y%m%d')+'/'+imname
            root_css(reallocal)
            compress_css()

if __name__ == '__main__':
    maincss()
