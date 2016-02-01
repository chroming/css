#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import os
import re


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
def import_css(reallocal):
    global importcsstmp
    realdir = os.path.dirname(reallocal)+'/'
    cssfile = open(reallocal, 'r+')
    rcss = cssfile.read()
    importlist = re.findall(r'\@import \".*?\";', rcss)
    if importlist:
        for imone in importlist:
            import_local = re.findall(r'\"(.*?)\"', imone)[0]
            imreallocal = realdir+import_local
            csscontent = import_css(imreallocal)
            importcsstmp = rcss.replace(str(imone), str(csscontent))
            rcss = importcsstmp
    cssfile.close()
    return rcss


# 第一层CSS导入及替换内容
def root_css(reallocal):
    global rootcsstmp
    localdir, imname = os.path.split(reallocal)
    today = datetime.date.today()
    newcsslocal = localdir+'/'+today.strftime('%Y%m%d')+'/'+imname
    # 判断要生成的文件和目录是否存在
    if os.path.isfile(newcsslocal):
        raw_input("需生成文件已存在! 程序将重新生成并覆盖该文件! 按Enter确认……\n")
    elif not os.path.exists(localdir+'/'+today.strftime('%Y%m%d')):
        try:
            os.mkdir(localdir+'/'+today.strftime('%Y%m%d'))
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
    realdir = os.path.dirname(reallocal)+'/'
    cssfile = open(reallocal, 'r+')
    rcss = cssfile.read()
    importlist = re.findall(r'\@import \".*?\";', rcss)
    # 如果内容中有import 语句则调用import_css()
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
    csslocal = localdir+'/css-src/nt/'
    print("正在获取%s下css文件列表……\n"%csslocal)
    try:
        csslist = os.listdir(csslocal)
    except OSError as err:
        if err.args[0] == 3 or 2:
            raw_input("%s目录不存在!请检查后重新运行!按Enter关闭程序……"%csslocal)
            return

    for imname in csslist:
        ext = imname.split('.')[-1]
        if ext == 'css':
            reallocal = csslocal+imname
            root_css(reallocal)

if __name__ == '__main__':
    localdir = raw_input('请输入css-src目录所在路径，默认为当前路径: ')
    maincss(localdir)
