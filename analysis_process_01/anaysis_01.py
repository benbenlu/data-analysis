import unicodecsv
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

def read_csv(file):
    with open(file, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        # print('reader', reader)
        # for row in reader:
        #     print(row['acct'], row['utc_date'])
        return list(reader)

# test_csv = read_csv('./csv/test.csv')
daily_engagement = read_csv('./csv/daily-engagement.csv')
enrollments = read_csv('./csv/enrollments.csv')
project_submissions = read_csv('./csv/project-submissions.csv')

# 定义将字符串转为整形的方法
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

# 定义将字符串转为日期的方法
def parse_maybe_date(date):
    if date == '':
        return None
    else:
        return datetime.strptime(date, '%Y-%m-%d')


# enrollments中数据的部分处理
for enrollment in enrollments:
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['join_date'] = parse_maybe_date(enrollment['join_date'])
    enrollment['cancel_date'] = parse_maybe_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])

# 将daily_engagement中学号的列表示acct替换为account_key
for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    engagement_record['utc_date'] = parse_maybe_date(engagement_record['utc_date'])
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    del[engagement_record['acct']]
print('daily_engagement~~~~~~~~~~', daily_engagement[0])

# 获取去重后的学员数
def get_unique_students(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students

unique_daily_engagement = get_unique_students(daily_engagement)
unique_enrollments = get_unique_students(enrollments)
unique_project_submissions = get_unique_students(project_submissions)

# 打印出注册至少一天，且在unique_daily_engagement缺失的学员 -》找到了这些数据是优达的测试账号
num_problem_students = 0
for enrollment in enrollments:
    student = enrollment['account_key']
    if (student not in unique_daily_engagement and
            enrollment['join_date'] != enrollment['cancel_date']):
        print('enrollment', enrollment)
        num_problem_students += 1
        # break
print('num_problem_students', num_problem_students)

# 建立测试账号数据集，并在后边的分析中排除掉他们
udacity_test_accounts = set()
# print('enrollments,', type(enrollments[0]['is_udacity']))
for enrollment1 in enrollments:
    if enrollment1['is_udacity']: # 这里注意源数据文件中的值TRUE和在python中读出的数据是不一样的
        udacity_test_accounts.add(enrollment1['account_key'])
print('udacity_test_accounts', udacity_test_accounts)

# 删除测试账号
def remove_test_accounts(data):
    result = []
    for el in data:
        if el['account_key'] not in udacity_test_accounts:
            result.append(el)
    return result

no_udacity_engagement = remove_test_accounts(daily_engagement)
no_udacity_enrollments = remove_test_accounts(enrollments)
no_udacity_submissions = remove_test_accounts(project_submissions)

print('daily_engagement总行数：', len(daily_engagement), '去重后总行数：', len(unique_daily_engagement), '去掉测试账号', len(no_udacity_engagement))
print('enrollments总行数：', len(enrollments), '去重后总行数：', len(unique_enrollments), '去掉测试账号', len(no_udacity_enrollments))
print('project_submissions总行数：', len(project_submissions), '去重后总行数：', len(unique_project_submissions), '去掉测试账号', len(no_udacity_submissions))

# 计算未注销的和超过七天注销的学员的字典
# def no_cancel_students():
paid_students = {}
for enrollment in no_udacity_enrollments:
    if not enrollment['is_canceled'] or enrollment['days_to_cancel'] > 7:
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        # 学生存在多次注册情况，当前学生不在字典中，且注册日期比当前注册日期更近时，才写进字典
        if account_key not in paid_students or enrollment_date > paid_students[account_key]:
            paid_students[account_key] = enrollment_date
print('paid_students', len(paid_students))

# 获取第一周的数据
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return  time_delta.days >= 0 and time_delta.days < 7

# 删除免费试学的同学
def remove_free_trail_cancel(data):
    result = []
    for el in data:
        if el['account_key'] in paid_students:
            result.append(el)
    return result

paid_engagements = remove_free_trail_cancel(no_udacity_engagement)
paid_enrollments = remove_free_trail_cancel(no_udacity_enrollments)
paid_submissions = remove_free_trail_cancel(no_udacity_submissions)

paid_engagement_in_first_week = []
for student in paid_engagements:
    account_key = student['account_key']
    join_date = paid_students[account_key]
    if within_one_week(join_date, student['utc_date']):
        paid_engagement_in_first_week.append(student)

print('len(paid_engagement)', len(paid_engagements))
print('len(paid_enrollments)', len(paid_enrollments))
print('len(paid_submissions)', len(paid_submissions))
print('len(paid_engagement_in_first_week)', len(paid_engagement_in_first_week))

# 分组数据 
def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for point_data in data:
        key = point_data[key_name]
        grouped_data[key].append(point_data)
    return grouped_data

# 分组数据按某维度汇总
def sum_grouped_items(grouped_data, field_name):
    sum_data = {}
    for key, data_points  in grouped_data.items():
        total = 0
        for data_point in data_points:
            total += data_point[field_name]
        sum_data[key] = total
    return sum_data

# 输出分组数据的描述
def describe_data(data):
    print('Mean:', np.mean(data))
    print('Standard deviation:', np.std(data))
    print('Minimum:', np.min(data))
    print('Maximum:', np.max(data))

# 针对提交记录表，计算学生第一周的平均学习时间、最大值、最小值、标准差
engagement_by_account = group_data(paid_engagement_in_first_week, 'account_key')
total_minutes_by_account = sum_grouped_items(engagement_by_account, 'total_minutes_visited')

total_minutes = list(total_minutes_by_account.values())
describe_data(total_minutes)

# 完成课程数
lessons_completed_by_account = sum_grouped_items(engagement_by_account, 'lessons_completed')
describe_data(list(lessons_completed_by_account.values()))



# engagement_by_account = defaultdict(list)
# for engagement_record in paid_engagement_in_first_week:
#     account_key = engagement_record['account_key']
#     engagement_by_account[account_key].append(engagement_record)
# # print('engagement_by_account', len(engagement_by_account))

# total_minutes_by_account = {}
# for account_key, engagement_for_student in engagement_by_account.items():
#     minutes = 0
#     for engagement_record in engagement_for_student:
#         minutes += engagement_record['total_minutes_visited']
#     total_minutes_by_account[account_key] = minutes

# # print('total_minutes_by_account', total_minutes_by_account)

# total_minutes = list(total_minutes_by_account.values())
# X = np.array([1.222,2.222,3,4,5])

# print('学习平均分钟数', np.mean(total_minutes))
# print('学习最多分钟数', np.max(total_minutes))
# print('学习最小分钟数', np.min(total_minutes))
# print('标准差', np.std(total_minutes))

# 获取每个学生学习的课程数
# total_courses_by_account = {}
# for account_key, engagement_for_student in engagement_by_account.items():
#     course = 0
#     for engagement_record in engagement_for_student:
#         course = len(set(engagement_record['num_courses_visited']))
#     total_courses_by_account[account_key] = course

# total_courses = list(total_courses_by_account.values())
# # print('学习平total_courses均课程数', total_courses)
# print('学习平均课程数', np.mean(total_courses))
# print('学习最多课程数', np.max(total_courses))
# print('学习最少', np.min(total_courses))
# print('标准差', np.std(total_courses))
