# gobye
#### 分析统计需要选修的课程
---
### 下载源码
```
git clone https://github.com/PencilCl/gobye.git
```
### 安装依赖
```
pip install -r requirements.txt
```
### 配置数据库信息
##### 进入项目的gobye目录
##### 参照该目录下的`databaseSettings.ex.py`文件
##### 设置数据库相关信息,并把文件另存为`databaseSettings.py`
### 爬取培养方案
##### 进入项目的`trainingProgram`文件夹下
##### 运行`TP.py`文件
```
python TP.py
```
##### 等待爬完全部培养方案
### 开启服务器
##### 运行
```
python manage.py runserver
```
##### 打开服务器输入`127.0.0.1:8000`
##### 使用学号密码登录即可查询