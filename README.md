# 基于Django2.2.4开发的简单的在线考试系统

## 技术汇总

+ 项目使用的框架或者插件
  + 后端方向：Django，PyMySQL
  + 数据库方向：MySQL
  + 前端方向：Bootstrap4，Ajax，Bootstrap Table，SweetAlert2
  + css模块：main.css,  test.css, my-login.css,  cssfamily=Varela+Round.css, Nunito.css, styles.css
  + js模块：jquery.downCount.js， jquery.js,  echarts.min.js ,  my-login.js,  popper.min.js,  jquery.easing.min.js, scripts.js
+ 具体技术
  + Django作为服务端进行逻辑处理、客户端和服务端交互连线（通过Ajax和自身模板语言实现）、与数据库交互、异常全局处理
  + PyMySQL作为连接数据库和Django交互连线
  + Bootstrap4作为前端框架给与网页前端基本样式和动态效果
  + Bootstrap Table作为Bootstrap插件，为前端提供更加智能和使用的表格
  + SweetAlert2作为弹窗插件，使网页更加具有动感，使交互更加人性化
  + 利用main.css,  test.css, my-login.css,  cssfamily=Varela+Round.css, Nunito.css, styles.css进行前端样式设计
  + jquery.downCount.js， jquery.js,  echarts.min.js ,  my-login.js,  popper.min.js,  jquery.easing.min.js, scripts.js进行动态效果设计

## 启动配置

+ 推荐使用Intellij IDEA调试该项目(IDEA可以去官网通过学生邮箱注册学生账号，免费使用旗舰版，不要下载社区版）
+ Python版本推荐3.7，MySQL 推荐5.7版本 ，可以去官网下载 MySQL(GPL)Python3.7（Python和PyCharm的连接以及MySQL的配置请自己百度执行）
+ 后台启动MySQL5.7(注意记录一下MySQL账号密码）
+ 在Github项目页面点击code，复制HTTPS的链接，在IDEA中点击File->New->Project from Version Control,在URL中输入复制的链接，点击clone
+ 等待Github代码Pull完成，点击PyCharm左上角的File->Settings，之后,在弹出的界面中点击Project：onlineexam之后，再点击Project Interpreter，随后在点击界面中的加号。在搜索框中输入django，回车，之后，点击Specify version，随后选择版本2.2.4，之后再点击Install Package按钮即可配置Django。PyMySQL的下载同理，注意版本为1.0.2。
+ 在Django，PyMySQL配置好后，先删除onlineexam->student->migrations中除了、__ init __.py之外的其他.py文件。随后在onlineexam->onlineexam->setting.py中的DATABASE中更改数据库配置（各个部分代表什么，文件有注释）
+ 在配置更改完后点击右侧的Database，点击左上角的+，选择Data Source->MySQL数据库 输入数据库user和password点击OK连接
+ 随后点击下方的Terminal，随后在其中输入 ‘mysql -u 你的数据库用户名 -p’，回车。之后输入你的密码，回车，即可进入MySQL管理界面。
+ 在MySQL管理界面中输入‘CREATE DATABASE IF NOT EXISTS 你在setting.py中的配置的使用数据库的名称 DEFAULT CHARSET utf8;’随后输出‘exit();’即可退出MySQL管理界面
+ 退出MySQL管理界面后，随即依次输入和执行 ‘python manage.py makemigrations’，‘ python3 manage.py migrate’ 和 ‘ python manage.py loaddata data.json’即可完成数据库的迁移和数据的导入
+ 在数据导入后，输入‘python manage.py createsuperuser’ 按照提示即可创建超级管理员账号和密码，同时也是进入项目管理员模块的账号和密码，随后点击Terminal栏的右上角的 - 隐藏Terminal栏
+ 点击pycharm右上角的绿色三角即可运行该项目，之后在下方点击连接即可进入界面进行操作

## 项目代码分块

- 建议在二次开发项目之前系统学习Django的基础知识！！！前端看看Jquery语法和Bootstrap、Bootstap Table和sweetalert2的用法！！（参考学习网址：Bootstap Table：http://www.itxst.com/bootstrap-table-methods/tutorial.html SweetAlert2：http://mishengqiang.com/sweetalert2/#ajax-request） 【一个免费的Bootstrap模板的网址：https://startbootstrap.com/】
- onlineexam->templates存放项目中的所有html文件
- onlineexam->static中存放项目中所有html需要引入的模块
- onlineexam->onlineexam：
  - setting.py为项目的配置文件
  - urls.py中存放了客户端（前端）所需的所有url索引
- onlineexam->student:
  - admin.py里为注册到admin模块展现和可以编辑的数据
  - model.py里为数据库各表的描述文件
  - view.py里为本项目所需的所有逻辑处理函数
