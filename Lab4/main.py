import time
from utils import *
from config import *

mydb = MyDB(db_config)


def show_interface():
    go_on = True
    while go_on:
        op = '7'
        while op < '0' or op > '6':
            clear_cmd()
            print('\t学生管理系统')
            print('1 学生信息维护')
            print('2 课程信息维护')
            print('3 学生成绩维护')
            print('4 学生成绩统计')
            print('5 学生成绩排名')
            print('6 学生信息查询')
            print('0 退出')
            op = input(op_tip)
        if op == '1':
            show_mt_stu()
        elif op == '2':
            show_mt_course()
        elif op == '3':
            show_mt_sc()
        elif op == '4':
            show_sc_grade()
        elif op == '5':
            show_sc_rank()
        elif op == '6':
            select_stu()
        else:
            go_on = False


def select_stu():
    clear_cmd()
    print('\t学生信息查询')
    sno = inputing('请输入学号:')
    condition = f'Sno="{sno}"'
    if not sno:
        print('学号为空,查询失败')
        time.sleep(sleep_time)
        return
    ret = mydb.select_sql('student', '*', condition)
    if not ret[1]:
        print('查询学生信息不存在')
        time.sleep(sleep_time)
        return
    print('基本信息:')
    print_list(stu_title, stu_format)
    print_sql(ret[1][0], stu_format)
    col = ['Cno', 'Grade']
    col_format = [8, 8]
    c = ''
    for s in col:
        c += s + ','
    ret = mydb.select_sql('sc', c.rstrip(','), condition)
    print('选课信息:')
    if ret[1]:
        print_list(col, col_format)
        for info in ret[1]:
            print_sql(info, course_format)
    else:
        print('无选课信息')
    op = input('\n按任意键返回\n')


def show_sc_rank():
    clear_cmd()
    print('\t学生成绩排名')
    sdepts = mydb.select_sql('student', 'distinct Sdept')
    # print(sdepts)
    for sdept in sdepts[1]:
        ret = mydb.select_sql('sc,student', 'sc.Sno,Cno,Grade',
                              'Sdept="{}" and sc.Sno=student.Sno order by Grade desc'
                              .format(sdept['Sdept']))
        if ret[1]:
            print(sdept['Sdept'] + ':')
            print_list(sc_title, sc_format)
            for info in ret[1]:
                print_sql(info, sc_format)
    op = input('\n按任意键返回\n')


def show_sc_grade():
    clear_cmd()
    print('\t学生成绩统计')
    titles = ['平均成绩', '最好成绩', '最差成绩']
    sdept_str = 'Sdept'
    grade_format = [8, 12]
    table_name = 'student,sc'
    where_str = 'student.Sno=sc.Sno group by Sdept'
    grade_str = ['AVG(Grade)', 'MAX(Grade)', 'MIN(Grade)']
    for i in range(len(grade_str)):
        col_str = sdept_str + ',' + grade_str[i]
        ret = mydb.select_sql(table_name, col_str, where_str)
        print(titles[i] + ':')
        if ret[0] == 1 and ret[1]:
            grade_title = [sdept_str, grade_str[i]]
            print_list(grade_title, grade_format)
            for info in ret[1]:
                print_sql(info, grade_format)
    title = '优秀率'
    cnt_str = 'COUNT(*)'
    print(title + ':')
    col_str = sdept_str + ',' + cnt_str
    total = mydb.select_sql(table_name, col_str, where_str)
    # print(total)
    if total[1]:
        good = mydb.select_sql(table_name, col_str,
                               'student.Sno=sc.Sno and Grade>=90 group by Sdept')
        # print(good)
        t = [sdept_str, title]
        print_list(t, grade_format)
        for a, b in zip(good[1], total[1]):
            if b[cnt_str] != 0:
                print_list([a[sdept_str], str(a[cnt_str] / b[cnt_str] * 100) + '%'],
                           grade_format)
    title = '不及格人数'
    print(title + ':')
    bad = mydb.select_sql(table_name, col_str,
                          'student.Sno=sc.Sno and Grade<60 group by Sdept')
    # print(bad)
    t = [sdept_str, title]
    print_list(t, grade_format)
    for info in bad[1]:
        print_sql(info, grade_format)
    op = input('\n按任意键返回\n')


def show_mt_sc():
    go_on = True
    while go_on:
        op = '6'
        while op < '0' or op > '2':
            clear_cmd()
            print('\t学生成绩信息维护')
            print('1 添加学生成绩')
            print('2 修改学生成绩')
            print('0 返回')
            op = input(op_tip)
        if op == '1':
            add_sc()
        elif op == '2':
            update_sc()
        else:
            go_on = False


def add_sc():
    clear_cmd()
    print('\t添加学生成绩')
    print('请输入学生成绩:')
    sno = inputing('学生学号:')
    cno = inputing('课程号:')
    grade = inputing('成绩:')
    sc = [sno, cno, grade]
    print('请确认添加信息:')
    print_list(sc_title, sc_format)
    print_list(sc, sc_format)
    op = input('1 确认\nElse 取消\n')
    if op == '1':
        if mydb.insert_sql('sc', sc) == 1:
            print('添加成功')
        else:
            print('添加失败')
        time.sleep(sleep_time)


def update_sc():
    clear_cmd()
    print('\t修改学生成绩')
    sno = input('请输入待修改学生学号:')
    # sno = '20001010'
    cno = input('请输入待修改学生的课程号:')
    condition = f'Sno="{sno}"and Cno="{cno}"'
    ret = mydb.select_sql('sc', '*', condition)
    if ret[0] == 0:
        print('待修改学生成绩查询失败')
        time.sleep(sleep_time)
        return
    elif ret[1]:
        print('请确认待修改信息:')
        print_list(sc_title, sc_format)
        print_sql(ret[1][0], sc_format)
    else:
        print('待修改学生成绩不存在')
        time.sleep(sleep_time)
        return
    col = []
    col_format = []
    sc = []
    print('请输入以下信息:')
    for i in range(len(sc_title)):
        info = input(sc_title[i] + ':')
        if info:
            col.append(sc_title[i])
            col_format.append(sc_format[i])
            sc.append(info)
    print('请确认修改后的信息:')
    print_list(col, sc_format)
    print_list(sc, sc_format)
    op = input('1 确认\nElse 取消\n')
    if op == '1':
        if mydb.update_sql('sc', col, sc, condition) == 1:
            print('修改成功')
        else:
            print('修改失败')
        time.sleep(sleep_time)


def show_mt_course():
    go_on = True
    while go_on:
        op = '6'
        while op < '0' or op > '3':
            clear_cmd()
            print('\t课程信息维护')
            print('1 添加课程信息')
            print('2 修改课程信息')
            print('3 删除无选课的课程信息')
            print('0 返回')
            op = input(op_tip)
        if op == '1':
            add_course()
        elif op == '2':
            update_course()
        elif op == '3':
            delete_ept_course()
        else:
            go_on = False


def add_course():
    clear_cmd()
    print('\t添加课程信息')
    print('请输入课程信息:')
    cno = inputing('课程号:')
    cname = inputing('课程名:')
    cpno = inputing('先修课程号:')
    ccredit = inputing('学分:')
    # sno, sname, ssex, sage, sdept = '20001010', 'hhy', '男', 20, 'IS'
    course = [cno, cname, cpno, ccredit]
    print('请确认添加信息:')
    print_list(course_title, course_format)
    print_list(course, course_format)
    op = input('1 确认\nElse 取消\n')
    if op == '1':
        if mydb.insert_sql('course', course) == 1:
            print('添加成功')
        else:
            print('添加失败')
        time.sleep(sleep_time)


def update_course():
    clear_cmd()
    print('\t修改课程信息')
    cno = input('请输入待修改的课程号:')
    condition = f'Cno="{cno}"'
    ret = mydb.select_sql('course', '*', condition)
    if ret[0] == 0:
        print('待修改课程信息查询失败')
        time.sleep(sleep_time)
        return
    elif ret[1]:
        print('请确认待修改信息:')
        print_list(course_title, course_format)
        print_sql(ret[1][0], course_format)
    else:
        print('待修改课程信息不存在')
        time.sleep(sleep_time)
        return
    col = []
    col_format = []
    course = []
    print('请输入以下信息:')
    for i in range(len(course_title)):
        info = input(course_title[i] + ':')
        if info:
            col.append(course_title[i])
            col_format.append(course_format[i])
            course.append(info)
    print('请确认修改后的信息:')
    print_list(col, col_format)
    print_list(course, col_format)
    op = input('1 确认\nElse 取消\n')
    if op == '1':
        if mydb.update_sql('course', col, course, condition) == 1:
            print('修改成功')
        else:
            print('修改失败')
        time.sleep(sleep_time)


def delete_ept_course():
    clear_cmd()
    print('\t删除未选课课程信息')
    condition = 'Cno not in (select distinct Cno from sc )'
    ret = mydb.select_sql('course', '*', condition)
    if ret[0] == 0:
        print('查询失败')
        return
    elif ret[1]:
        print('未选课课程信息:')
        print_list(course_title, course_format)
        for info in ret[1]:
            print_sql(info, course_format)
    else:
        print('无未选课课程')
        time.sleep(sleep_time)
        return
    op = input('1 删除\nElse 取消\n')
    if op == '1':
        if mydb.delete_sql('course', condition) == 1:
            print('删除成功')
        else:
            print('删除失败')
        time.sleep(sleep_time)


def show_mt_stu():
    go_on = True
    while go_on:
        op = '6'
        while op < '0' or op > '3':
            clear_cmd()
            print('\t维护学生信息')
            print('1 添加学生信息')
            print('2 修改学生信息')
            print('3 删除学生信息')
            print('0 返回')
            op = input(op_tip)
        if op == '1':
            add_stu()
        elif op == '2':
            update_stu()
        elif op == '3':
            delete_stu()
        else:
            go_on = False


def add_stu():
    clear_cmd()
    print('\t增加学生信息')
    print('请输入学生信息:')
    sno = inputing('学号:')
    sname = inputing('姓名:')
    ssex = inputing('性别:')
    sage = inputing('年龄:')
    sdept = inputing('系别:')
    # sno, sname, ssex, sage, sdept = '20001010', 'hhy', '男', 20, 'IS'
    stu = [sno, sname, ssex, sage, sdept, '否']
    print('请确认添加信息:')
    print_list(stu_title, stu_format)
    print_list(stu, stu_format)
    op = input('1 确认\nElse 取消\n')
    if op == '1':
        if mydb.insert_sql('student', stu) == 1:
            print('增加成功')
        else:
            print('增加失败')
        time.sleep(sleep_time)


def update_stu():
    clear_cmd()
    print('\t修改学生信息')
    sno = input('请输入待修改学生的学号:')
    # sno = '20001010'
    condition = f'Sno="{sno}"'
    ret = mydb.select_sql('student', '*', condition)
    if ret[0] == 0:
        print('待修改学生信息查询失败')
        time.sleep(sleep_time)
        return
    elif ret[1]:
        print('请确认待修改信息:')
        print_list(stu_title, stu_format)
        print_sql(ret[1][0], stu_format)
    else:
        print('待修改学生信息不存在')
        time.sleep(sleep_time)
        return
    col = []
    col_format = []
    stu = []
    print('请输入以下信息:')
    for i in range(len(stu_title)):
        info = input(stu_title[i] + ':')
        if info:
            col.append(stu_title[i])
            col_format.append(stu_format[i])
            stu.append(info)
    print('请确认修改后的信息:')
    print_list(col, stu_format)
    print_list(stu, stu_format)
    op = input('1 确认\nElse 取消\n')
    if op == '1':
        if mydb.update_sql('student', col, stu, condition) == 1:
            print('修改成功')
        else:
            print('修改失败')
        time.sleep(sleep_time)


def delete_stu():
    clear_cmd()
    print('\t删除学生信息')
    sno = input('请输入待修改学生的学号:')
    # sno = '20001010'
    ret = mydb.select_sql('student', '*', f'Sno="{sno}"')
    if ret[0] == 0:
        print('待修改学生信息查询失败')
        time.sleep(sleep_time)
        return
    elif ret[1]:
        print('请确认待修改信息:')
        print_list(stu_title, stu_format)
        print_sql(ret[1][0], stu_format)
    else:
        print('待修改学生的信息不存在!')
        return
    op = input('1 删除\nElse 取消\n')
    if op == '1':
        if mydb.delete_sql('student', f'Sno="{sno}"') == 1:
            print('删除成功')
        else:
            print('删除失败')
        time.sleep(sleep_time)


def main():
    try:
        show_interface()
        print('\t已退出')
    except RuntimeError:
        print('\t无法连接数据库')
    finally:
        mydb.db.close()


if __name__ == '__main__':
    main()
    # add_course()
    # update_course()
    # add_stu()
    # update_stu()
    # delete_ept_course()
    # add_sc()
    # update_sc()
    # show_sc_stat()
    # show_sc_rank()
    # select_stu()
    pass
