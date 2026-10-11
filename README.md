# 基于Django2.2.4开发的简单的在线考试系统

## 技术汇总

+ 项目使用的框架或者插件
  + 后端方向：Django，PyMySQL
  + 数据库方向：MySQL
  + 前端方向：Bootstrap4，Ajax，Bootstrap Table，SweetAlert2
  + css模块：main.css, test.css, my-login.css, cssfamily=Varela+Round.css, Nunito.css, styles.css
  + js模块：jquery.downCount.js，jquery.js, echarts.min.js, my-login.js, popper.min.js, jquery.easing.min.js, scripts.js

+ 具体技术
  + Django作为服务端进行逻辑处理、客户端和服务端交互连线（通过Ajax和自身模板语言实现）、与数据库交互、异常全局处理
  + PyMySQL作为连接数据库和Django交互连线
  + Bootstrap4作为前端框架给予网页前端基本样式和动态效果
  + Bootstrap Table作为Bootstrap插件，为前端提供更加智能和实用的表格
  + SweetAlert2作为弹窗插件，使网页更加具有动感，使交互更加人性化
  + 利用main.css, test.css, my-login.css, cssfamily=Varela+Round.css, Nunito.css, styles.css进行前端样式设计
  + jquery.downCount.js，jquery.js, echarts.min.js, my-login.js, popper.min.js, jquery.easing.min.js, scripts.js进行动态效果设计

## 启动配置

+ 推荐使用IntelliJ IDEA或PyCharm调试该项目。
+ 原项目推荐使用Python 3.7、Django 2.2.4、PyMySQL 1.0.2及MySQL 5.7。
+ 后台启动MySQL 5.7（注意记录MySQL账号密码）。
+ 在GitHub项目页面点击Code，复制HTTPS链接，在IDE中通过版本控制功能Clone项目。
+ 配置Python解释器，并安装Django 2.2.4和PyMySQL 1.0.2。
+ 在`onlineexam/settings.py`中的`DATABASES`配置数据库连接信息。
+ 在MySQL中创建数据库：

  ```sql
  CREATE DATABASE IF NOT EXISTS exam
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;
  ```

+ 本仓库已保留原有的`student/migrations`迁移文件，无需删除或重新生成。
+ 在项目根目录依次执行：

  ```bash
  python manage.py migrate
  python manage.py loaddata data.json
  ```

+ 数据导入后，可执行以下命令创建Django管理员：

  ```bash
  python manage.py createsuperuser
  ```

+ 启动项目：

  ```bash
  python manage.py runserver
  ```

+ 浏览器访问：

  ```
  http://127.0.0.1:8000/
  ```

### 2026年Legacy环境兼容说明

2026年10月重新恢复本项目，已验证以下运行环境：

| 组件 | 版本 |
|---|---|
| Python | 3.9.25 |
| Django | 2.2.4 |
| PyMySQL | 1.0.2 |
| MySQL | 5.7.44（Docker） |

在Apple Silicon设备上，MySQL 5.7通过Docker的`linux/amd64`兼容模式运行。

由于Django 2.2.4与PyMySQL 1.0.2存在SQL字符串类型兼容问题，在`onlineexam/__init__.py`中增加了Legacy Compatibility Shim：

```python
import pymysql

pymysql.install_as_MySQLdb()

# Legacy compatibility:
# Django 2.2's MySQL backend expects cursor.mogrify() to return bytes,
# while PyMySQL 1.0.2 returns str.
from django.db.backends.mysql.operations import DatabaseOperations


def _legacy_last_executed_query(self, cursor, sql, params):
    query = cursor.mogrify(sql, params)

    if isinstance(query, bytes):
        query = query.decode(errors="replace")

    return query


DatabaseOperations.last_executed_query = _legacy_last_executed_query
```

该补丁通过Monkey Patch解决旧版本兼容问题，不需要修改Django安装包源码，仅用于Legacy环境恢复。

**注意：**

+ MySQL数据库需要显式指定UTF-8字符集，以避免中文数据写入错误。
+ 保留原有`student/migrations`迁移文件，不需要重新执行`makemigrations`。
+ 数据库账号密码需根据本地环境配置，不要将真实密码提交到公开仓库。
+ 本次已验证数据库迁移、历史数据导入及项目首页正常运行，完整业务流程尚未逐一验证。
+ 后续现代化重构将在独立分支进行，本次更新不涉及业务逻辑和项目架构调整。

## 项目代码分块

- 建议在二次开发项目之前系统学习Django的基础知识！前端可以学习jQuery语法，以及Bootstrap、Bootstrap Table和SweetAlert2的用法。

  参考学习网址：

  + Bootstrap Table：http://www.itxst.com/bootstrap-table-methods/tutorial.html
  + SweetAlert2：http://mishengqiang.com/sweetalert2/#ajax-request
  + Bootstrap免费模板：https://startbootstrap.com/

- `onlineexam/templates`存放项目中的所有HTML文件。
- `onlineexam/static`存放项目中HTML需要引入的静态资源。

- `onlineexam/onlineexam`：
  - `settings.py`为项目的配置文件。
  - `urls.py`中存放了客户端（前端）所需的URL路由配置。
  - `__init__.py`包含PyMySQL适配及Legacy兼容补丁。

- `onlineexam/student`：
  - `admin.py`中为注册到Django Admin模块、可以展示和编辑的数据。
  - `models.py`中为数据库各表的模型定义。
  - `views.py`中为本项目所需的业务逻辑处理函数。
  - `migrations/`中保留项目历史数据库迁移文件。

## LICENSE

MIT LICENSE
