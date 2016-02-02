此程序使用Python 2.7开发，用于提取css文件内容并合并压缩。兼容*nix系统和windows系统。

## 功能

**此程序实现了以下功能：**

1. 根据当前日期在此目录下新建一个名称为YYYYMMDD格式的目录
   
2. 提取输入的指定目录下的所有css文件，不输入目录默认为当前路径；
   
3. 依次读取文件内容，并根据其中的@import 语句导入css文件内容并替换此行；
   
4. 若替换后的内容仍有@import 语句则继续使用相应的css文件内容替换此行，直至没有任何@import语句；
   
5. 对最终的内容进行压缩处理。具体压缩要求为：
   
   + 删掉css源码中的注释 ( /*...*/ )
   
   
   + 删除css源码中的以下字符
     + 换行，回车，制表符
     + (半角分号)前后的1个或者多个空格
     + { (左大括号)前后的1个或者多个空格
     + } (右大括号)前后的1个或者多个空格
     + `此压缩规则定义在源码中的reglis变量中，用户可自行修改源码以满足要求。`
   
6. 将压缩后的内容保存到YYYYMMDD目录下的同名文件中。

**以下特殊情况程序也可以正常使用：**

1. 跨平台使用（*nix平台，windows平台）；
2. 存在多层@import 调用的情况；
3. 若内容中有调用自身的语句，即a.css中有@import "a.css"这种自身循环调用的语句，程序会输出提示并删除该条调用语句
4. 若不同文件中有相互调用的语句，即相互调用形成死循环，程序会输出提示并删除该条调用
5. 若YYYYMMDD目录下已有同名文件，重新生成时会提示覆盖文件



## 运行方式：

#### 直接在终端运行

`python comcss.py`

会等待输入需遍历的目录路径。

#### 在其他程序或终端中导入该程序作为模块：

`import comcss`

该模块有三个函数可供使用，分别是：

+ `comcss.maincss(path)`
  
  该函数参数为需遍历的目录路径。实现的功能与直接运行实现的功能相同。
  
+ `comcss.root_css(cssfilepath)`
  
  该函数参数为css文件的路径。实现对单文件读取及内容导入及压缩后保存到YYYYMMDD同名文件下的功能。
  
+ `comcss.compress_css(cssfilepath)`
  
  该函数参数为css文件的路径。实现对单css文件根据已定义在reglis中的压缩规则进行压缩的功能。

*注意：windows下输入路径请使用正斜线`/`代替默认的反斜线`\`*

​