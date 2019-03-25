import unicodecsv
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

# 将daily_engagement中学号的列表示acct替换为account_key
for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    del[engagement_record['acct']]

# 获取去重后的学员数
def get_unique_students(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students


unique_daily_engagement = get_unique_students(daily_engagement)
unique_enrollments = get_unique_students(enrollments)
unique_project_submissions = get_unique_students(project_submissions)


print('daily_engagement总行数：', len(daily_engagement), '去重后总行数：', len(unique_daily_engagement))
print('enrollments总行数：', len(enrollments), '去重后总行数：', len(unique_enrollments))
print('project_submissions总行数：', len(project_submissions), '去重后总行数：', len(unique_project_submissions))

