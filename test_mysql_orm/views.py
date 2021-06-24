# _*_coding:utf-8_*_
# @Time    :2021/6/2415:00
# @Author  :ErvinChiu
# @Email   :ErvinChiu@outlook.com
# @File    :views.py
# @Sofeware:PyCharm
from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
"""
1.展示学生列表信息， 执行sql原生语句，必须用到execute()函数
2.在excute里面写入sql原生语句
"""


def index(request):
    with connection.cursor() as c:
        c.execute("select * from student")
        raw = c.fetchall()
        for row in raw:
            print(row)
    return render(request, 'index.html', {"lists": raw})


"""
新增学生信息
1.录入学生学号、学生姓名，通过get()方法获取前端页面录入信息
2.f-string: formatted string literals, 格式化字符串常量
3.执行insert 语句，重定向至列表页，展示最新信息
格式化 {} 内容，不在 {} 内的照常展示输出，如果你想输出 {}，那就用双层 {{}} 将想输出的内容包起来
"""


def add(request):
    if request.method == "POST":
        snum = request.POST.get("sid")
        sname = request.POST.get("sname")
        # 校验提交数据是否为空
        if not sname:
            return render(request, 'add.html', {'error': '输入不能为空'})
        with connection.cursor() as c:
            c.execute(f'insert into student values({snum},"{sname}")')
        return redirect('/index/')
    return render(request, 'add.html')


"""
删除学生信息
1.获取前端<a>标签传入sid,执行delete 语句，删除当前语句
2.删除结束，重定向至列表页，展示最数据
"""


def stu_del(request, sid):
    with connection.cursor() as c:
        c.execute(f'delete from student where snum={sid}')
    return redirect("/index/")


"""
修改学生信息
1.render 方法渲染edit.html 模板，携带当前编辑信息于当前页面，
2.get() 方法获取当前编辑页面学号（sid）|姓名（sname）,
3.执行update语句，f 格式化字符串，sql语句传入变量【sid&sname】，
4.重定向至列表页，展示最新信息
"""


def stu_edit(request, sid):
    with connection.cursor() as c:
        c.execute(f'select * from student where snum={sid}')
        persons = c.fetchone()
        print(persons)
    if request.method == "POST":
        snum = request.POST.get("sid")
        sname = request.POST.get("sname")
        with connection.cursor() as c:
            c.execute(f'update student set name ="{sname}" where snum={snum}'),
        return redirect('/index/')
    return render(request, 'edit.html', {"lists": persons})
