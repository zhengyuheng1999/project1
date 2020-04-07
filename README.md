# Project 1

此程序为太平洋书网程序，用户可注册，登陆后可以到搜索界面通过isbn、作者和标题进行查书，并进入某一本书界面评价。
注册时如果和已有用户重名，提示错误。
评价后自动跳转搜索界面，并且评价完某本书后不会在此书界面内再出现评价功能
同时具有api访问功能，若isbn不存在返回404错误
用户还可退出登录，在每个html界面（除error.html）都可退出

templates文件夹中包含html文件。
application.py为主程序，包括数据库连接、函数的实现和网页之间的逻辑。
books.csv为书信息文件。
import.py为将csv文件导入数据库的代码。
classes.py和models.py为类的定义和实现。

数据库BookList有三个表 books reviews users
表books有四列：
isbn(VARCHAR)主键，表reviews外键
title(VARCHAR)
author(VARCHAR)
year(VARCHAR)

表reviews有五列：
id(INTEGER)主键
username（VARCHAR)
isbn(VARCHAR)
mark(INTEGER)
text(VARCHAR)

表users有两列：
name(VARCHAR)主键，表reviews外键
password(VARCHAR)

数据库URL为postgresql://postgres:zyh@localhost:5432/BookList