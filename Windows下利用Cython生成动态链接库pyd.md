# Windows下利用Cython生成动态链接库pyd


pyd在Windows下其实就是dll。如果已经有C文件，可以使用微软开发的Visual Studio系列开发环境（IDE）来编译生成。不同的版本的设置位置可能不同，但所要设置的项目都是一样的：

 * 新建项目，项目类型选择C++的MFC DLL，注意项目名要全小写（其实只要最后生成的dll是全小写就可以了，这里为了方便起见）；
 * 菜单栏中工具->选项，项目与解决方案->VC++目录，右边选择“包含文件”，添加Python安装路径里面的include目录；选择“库文件”，添加Python安装路径里面的libs目录；
 * 右击项目->属性，配置属性->C/C++->预编译头，将“创建/使用预编译头”选项设为“不使用预编译头”
 * 继续在项目属性窗口，配置属性->链接器->输入，将“模块定义文件”的值删除；配置属性->链接器->常规，把“输出文件”的值中的"dll"替换为"pyd"

生成的过程中常常出现error link的情况，这多半是因为文件找不到的情况，解决方法有：

 1. 增加include的文件夹；
 2. 补充系统或python安装目录缺失的包。

当缺失python27_d.lib时，有三种办法：

 1. 将python安装目录下libs目录里的python27复制一份并命名为python27_d.lib，修改include目录下的pyconfig.h，将#define Py_DEBUG注释掉
 2. 上网搜索并下载python27_d.lib和python27.dll，分别放入libs目录和C:/windows/system32

如果只提供了pyx文件的话，就需要将pyx转换为c文件，再编译成pyd文件。我所需要处理的pyx文件是[word2vec_inner.pyx](https://github.com/piskvorky/gensim/blob/develop/gensim/models/word2vec_inner.pyx)，一开始，我查询了Cython的[官方文档](http://docs.cython.org/src/reference/compilation.html)使用如下代码文件进行c文件生成和编译，为不损坏原文件，我使用副本`word2vec_inner_t.pyx`。
```python
# setup_wv.py
from distutils.core import setup
from Cython.Build import cythonize

import numpy

setup(
    name = "My hello app",
    ext_modules = cythonize("word2vec_inner_t.pyx", include_path = [numpy.get_include()]),
)
```
```
python setup_wv.py build_ext --inplace
```
命令行给出的信息：
```
running build_ext
```
后来在Pycharm里运行一遍，才发现完整的信息：
```
running build_ext
error: Unable to find vcvarsall.bat
```
如果系统上已经安装了Visual Studio，这个问题可以通过事先在命令行中设置排除，听说这个选项写死在编译器，只能这么干。
```
SET VS90COMNTOOLS=%VS100COMNTOOLS%
```
到了这里，再次编译，报错说无法找到numpy的include文件：
```
Z:\CodeSpace\Python\testPython2\gensim\models>python setup_wv.py build_ext --inplace
running build_ext
building 'testPython2.gensim.models.word2vec_inner_t' extension
C:\Program Files\Microsoft Visual Studio 10.0\VC\BIN\cl.exe /c /nologo /Ox /MD /W3 /GS- /DNDEBUG -ID:\Python27\include -ID:\Python27\PC /Tcword2vec_inner_t.c /Fobuild\temp.win32-2.7\Release\word2vec_inner_t.obj
word2vec_inner_t.c
word2vec_inner_t.c(346) : fatal error C1083: 无法打开包括文件:“numpy/arrayobject.h”: No such file or directory
error: command '"C:\Program Files\Microsoft Visual Studio 10.0\VC\BIN\cl.exe"' failed with exit status 2
```
在谷歌半天之后，在`StackOverflow`我才发现能通过以下方式加入numpy的include文件夹：
```python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy

extensions = [
    Extension("word2vec_inner_t", ["word2vec_inner_t.pyx"],
              include_dirs=[numpy.get_include()])
]
setup(
    name="My Hello app",
    ext_modules=cythonize(extensions),
)
```
这样虽然没有生成pyd文件，但已经给出了c文件，我使用之前的方法试图利用Visual Studio生成pyd文件，但是遭遇失败，错误几乎无从下手：
```
1>d:\python27\lib\site-packages\numpy\core\include\numpy\npy_1_7_deprecated_api.h(12): warning Msg: Using deprecated NumPy API, disable it by #defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
1>z:\codespace\cplusplus\com4pyd2\com4pyd2\com4pyd2.cpp(6863): error C2440: “=”: 无法从“void (__cdecl *)(const __pyx_t_5numpy_uint32_t *,const __pyx_t_5numpy_uint8_t *,int *,__pyx_t_11testPython2_6gensim_6models_16word2vec_inner_t_REAL_t *,__pyx_t_11testPython2_6gensim_6models_16word2vec_inner_t_REAL_t *,__pyx_t_11testPython2_6gensim_6models_16word2vec_inner_t_REAL_t *,const int,const __pyx_t_5numpy_uint32_t *,const __pyx_t_11testPython2_6gensim_6models_16word2vec_inner_t_REAL_t,__pyx_t_11testPython2_6gensim_6models_16word2vec_inner_t_REAL_t *,int,int,int,int)”转换为“__pyx_t_11testPython2_6gensim_6models_16word2vec_inner_t_fast_sentence_cbow_hs_ptr”
1>          该转换要求 reinterpret_cast、C 样式转换或函数类型转换
...
1>
1>生成失败。
```

我想大概是C文件也有错误，还是得从pyx文件入手。偶然又在Overflow上发现文件名的问题，我又将`setup_wv.py`中的`word2vec_inner_t`改正：
```python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy

extensions = [
    Extension("word2vec_inner", ["word2vec_inner.pyx"],
              include_dirs=[numpy.get_include()])
]
setup(
    name="word2vec_inner",
    ext_modules=cythonize(extensions),
)
```
重敲命令：
```
python setup_wv.py build_ext --inplace
Compiling word2vec_inner.pyx because it changed.
Cythonizing word2vec_inner.pyx
running build_ext
building 'word2vec_inner' extension
C:\Program Files\Microsoft Visual Studio 10.0\VC\BIN\cl.exe /c /nologo /Ox /MD /W3 /GS- /DNDEBUG -ID:\Python27\lib\site-packages\numpy\core\include -ID:\Python27\include -ID:\Python27\PC /Tcword2vec_inner.c /Fobuild\temp.win32-2.7\Release\word2vec_inner.obj
word2vec_inner.c
d:\python27\lib\site-packages\numpy\core\include\numpy\npy_1_7_deprecated_api.h(12) : Warning Msg: Using deprecated NumPy API, disable it by #defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
C:\Program Files\Microsoft Visual Studio 10.0\VC\BIN\link.exe /DLL /nologo /INCREMENTAL:NO /LIBPATH:D:\Python27\libs /LIBPATH:D:\Python27\PCbuild /EXPORT:initword2vec_inner build\temp.win32-2.7\Release\word2vec_inner.obj /OUT:Z:\CodeSpace\Python\testPython2\gensim\models\word2vec_inner.pyd /IMPLIB:build\temp.win32-2.7\Release\word2vec_inner.lib /MANIFESTFILE:build\temp.win32-2.7\Release\word2vec_i
nner.pyd.manifest
   正在创建库 build\temp.win32-2.7\Release\word2vec_inner.lib 和对象 build\temp.
win32-2.7\Release\word2vec_inner.exp
```
我当时以为这就算大功告成了吗？但我在Pycharm中运行后，发现还是无法`import`，我不信，紧接在命令行敲`python`尝试：
```
Python 2.7.6 (default, Nov 10 2013, 19:24:18) [MSC v.1500 32 bit (Intel)] on win
32
Type "help", "copyright", "credits" or "license" for more information.
>>> import word2vec_inner
>>> word2vec_inner.train_sentence_sg
<built-in function train_sentence_sg>
>>> word2vec_inner.train_sentence_cbow
<built-in function train_sentence_cbow>
>>> word2vec_inner.FAST_VERSION
0
```
看来是Pycharm的问题了，重启之，顺利运行~
