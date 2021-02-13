import os.path
import operator
import datetime


from googleapiclient.discovery import build
from google.auth.transport.requests import Request


from Credentials import authorization
from test import test

def get_courses(service, state="ACTIVE"):
    results = service.courses().list(courseStates=state).execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')

    return courses

def announcements_course(service, id_course, max_announcements=0):
    result = service.courses().announcements().list(courseId=id_course, pageSize=max_announcements).execute()
    announcements = result.get('announcements', [])

    return announcements

def announcements_account(service):
    courses = get_courses(service)

    announcements_account = []
    for course in courses:
        announcements = announcements_course(service, course['id'], 1)
        announcements_account.extend(announcements)

    return announcements_account

def new_announcements_account(service, last_update_time):
    courses = get_courses(service)

    announcements_account = []
    for course in courses:
        announcement = announcements_course(service, course['id'], 1)

        if(len(announcement) != 0):
            date_time_str = announcement[0]['updateTime']
            announcement_date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        
            if(last_update_time < announcement_date_time):
                announcements_account.append(announcement)
        
    return announcements_account

def works_course(service, id_course, max_works=0):
    result = service.courses().courseWork().list(courseId=id_course).execute()

    return result

def new_works_account(service, last_update_time):
    courses = get_courses(service)

    announcements_account = []
    for course in courses:
        announcement = works_course(service, course['id'], 1)

        if(len(announcement) != 0):
            date_time_str = announcement[0]['creationTime']
            announcement_date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        
            if(last_update_time < announcement_date_time):
                announcements_account.append(announcement)
        
    return announcements_account


def main():
    
    auth = authorization() 
    service = build('classroom', 'v1', credentials=auth.credentials)

    # result = service.courses().courseWork().list(courseId='254194885185').execute()
    # print("Tarefas: ", result)

    # print(announcements_account(service))
    quinta = yesterday = datetime.datetime.today() - datetime.timedelta(days=3)
    print(new_announcements_account(service, quinta))

    

if __name__ == '__main__':
    main()