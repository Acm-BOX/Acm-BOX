#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Author   : Reskip      #
# Date     : 16/4/11     #
# Tel  : +86 18603530068 #

import urllib2, urllib
import Cookie, cookielib
import re
import HTMLParser
import os, sys


def ini_header(cookie='0=0',referer='http://acm.hdu.edu.cn'):
    header={
        "Host": "acm.hdu.edu.cn",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        "Accept-Encoding": "default",
        'Referer':referer,
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cookie":cookie,
       }
    return header

class problemfile:

    run_id = ''     #Run ID in HDOJ
    time = ''       #submit time
    status = ''
    pro_id = ''     #problem ID
    exe_time = -1       #execute time /ms
    exe_memory = -1     #execute memory /Kb
    len = -1        #Code lenth /b
    lang = ''       #Code language
    code = ''
    submit_num = 0     #A series of submit information
    username = ''

    def save(self,address=os.getcwd()+'\\'):        #Two documents code.inf to save code and record to store others
        address += self.username + '\\'
        if not os.path.exists(address+self.pro_id):
            os.makedirs(address+self.pro_id)

        file = open(address+self.pro_id +'\\'+str(self.submit_num)+'_record.inf','w')
        file.write(self.run_id+'\n')
        file.write(self.status+'\n')
        file.write(self.pro_id+'\n')
        file.write(str(self.exe_time)+'\n')
        file.write(str(self.exe_memory)+'\n')
        file.write(str(self.len)+'\n')
        file.write(self.lang+'\n')

        file.close()

        codefile=open(address+self.pro_id+'\\'+str(self.submit_num)+'_code.inf','w')
        codefile.write(self.code)

        codefile.close()


class user_inf:

    username = ''
    problem_sub = 0
    problem_sol = 0
    submit_num = 0
    ac_num = 0

    def save(self,address=os.getcwd()+'\\'):
        address += self.username + '\\'
        if not os.path.exists(address):
            os.makedirs(address)

        file = open(address+self.username+'.inf','w')

        file.write(self.username+'\n')
        file.write(str(self.problem_sub)+'\n')
        file.write(str(self.problem_sol)+'\n')
        file.write(str(self.submit_num)+'\n')
        file.write(str(self.ac_num)+'\n')

        file.close()


# of course - username,password
def get_cookie_core(username,password):
    
    header=ini_header()     #initialize an opener object
    path = "http://acm.hdu.edu.cn"
    request = urllib2.Request(path,headers=header)
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)

    opener.open(request)    #get phpsessid cookie

    path = 'http://acm.hdu.edu.cn/userloginex.php?action=login'     #php action path of login

    data = urllib.urlencode({'username': username, 'userpass': password, 'login': 'Sign In'})       #submit form (based on local computer)

    for item in cookie:
        name=item.name
        value=item.value

    header=ini_header(name+'='+value,'http://acm.hdu.edu.cn/userloginex.php')       #use the cookie that just get before

    req = urllib2.Request(path,headers=header)
    test=opener.open(req,data)      #login submiton

    #file=open('123.txt','w')
    #file.write(test.read())    #test

    return name+'='+value

def get_cookie(username,password):

    try :
        return get_cookie_core(username,password)
    except :
        return -1

# problem_id - The problem's id in HDOJ
# code_lang - The language of submition
# code - A string to submit
# cookie - identity attestation


# language nubmer:
# G++   0       C       3       C#      6
# gcc   1       Pascal  4
# C++   2       Java    5
def submit_code_core(problem_id,code_lang,code,cookie):
    header=ini_header(cookie,'http://acm.hdu.edu.cn/submit.php')

    path = "http://acm.hdu.edu.cn/submit.php?action=submit"
    request = urllib2.Request(path,headers=header)
    opener = urllib2.build_opener()

    data = urllib.urlencode({'problemid': problem_id, 'language': code_lang, 'usercode': code , 'check': '0'})
    opener.open(request,data)

    return 0

def submit_code(problem_id,code_lang,code,cookie):
    try :
        return submit_code_core(problem_id,code_lang,code,cookie)
    except :
        return -1


def get_code_core(address,cookie,username,problem_id):      # a function to get and save a submission's information
    header=ini_header(cookie,'http://acm.hdu.edu.cn/status.php')
    path = 'http://acm.hdu.edu.cn/status.php?user='+username+'&pid='+problem_id+'&status=5'

    pro_req = urllib2.Request(path,headers=header)
    pro_opener = urllib2.build_opener()
    status = pro_opener.open(pro_req).read()

    submit_comp=('(\d+)</td><td>(.*?)</td><td><font color=.*?>(.*?)</font></td><td><a href="/showproblem\.php\?pid=\d+">\d+</a></td><td>(\d+)MS</td><td>(\d+)K</td><td><a href="(/viewcode\.php\?rid=\d+)"  target=_blank>(\d+) B</td><td>(.*?)</td><td class=fixedsize>')
    submit_list = re.findall(submit_comp,status)

    num = 0
    for submit in submit_list:      #create a submission object and ini it
        submission = problemfile()
        submission.username=username

        submission.run_id = submit[0]
        submission.time = submit[1]
        submission.status = submit[2]
        submission.exe_time = submit[3]
        submission.exe_memory = submit[4]
        submission.len = submit[6]
        submission.lang = submit[7]

        submission.pro_id = problem_id
        submission.submit_num = num

        header=ini_header(cookie,'http://acm.hdu.edu.cn/viewcode.php')
        path = 'http://acm.hdu.edu.cn'+submit[5]

        submit_req = urllib2.Request(path,headers=header)
        submit_opener = urllib2.build_opener()
        statuss = submit_opener.open(submit_req).read()

        status_comp = ('left;">([\s\S]*?)</textarea>')

        codes = re.findall(status_comp,statuss)
            
        for code in codes:
            code = code.decode('utf-8','ignore').encode('ascii','ignore')
            html_parser = HTMLParser.HTMLParser()
            submission.code = html_parser.unescape(code)

        if address=='':     #default path
            submission.save()
        else :
            submission.save(address)     #aimed path

        num += 1

    return 0

def get_code(address,cookie,username,problem_id):
    try :
        return get_code_core(address,cookie,username,problem_id)
    except :
        return -1
        


# address - A string where the information will be save
def get_history_inf_core(address = '',cookie = '',username = ''):   #get all history information and save as a ducument
    header=ini_header(cookie,'http://acm.hdu.edu.cn/userstatus.php')    #address will be formal automatic

    address_lenth = len(address)
    if address[address_lenth - 1] != '\\' :
        address += '\\'

    path = "http://acm.hdu.edu.cn/userstatus.php?user="+username

    request = urllib2.Request(path,headers=header)
    opener = urllib2.build_opener()
    userstatus = opener.open(request).read()

    pro_comp = ('p\((\d+),(\d+),(\d+)\);')
    pro_list = re.findall(pro_comp,userstatus)

    for pro in pro_list:
        get_code(address,cookie,username,pro[0])

    return 0


def get_history_inf(address = '',cookie = '',username = ''):
    try :
        return get_history_inf_core(address,cookie,username)
    except :
        return -1

def get_user_inf_core(address,username):
    cookie=''

    user_info = user_inf()

    header=ini_header(cookie,'http://acm.hdu.edu.cn/userstatus.php')    #address will be formal automatic

    address_lenth = len(address)
    if address[address_lenth - 1] != '\\' :
        address += '\\'

    path = "http://acm.hdu.edu.cn/userstatus.php?user="+username

    request = urllib2.Request(path,headers=header)
    opener = urllib2.build_opener()
    userstatus = opener.open(request).read()

    user_info.username = username
    pro_comp = ('<td>Problems Submitted</td><td align=center>(\d+)</td>')
    inf_list = re.findall(pro_comp,userstatus)
    for inf in inf_list:
        user_info.problem_sub = inf

    pro_comp = ('<td>Problems Solved</td><td align=center>(\d+)</td>')
    inf_list = re.findall(pro_comp,userstatus)
    for inf in inf_list:
        user_info.problem_sol = inf

    pro_comp = ('<td>Submissions</td><td align=center>(\d+)</td>')
    inf_list = re.findall(pro_comp,userstatus)
    for inf in inf_list:
        user_info.submit_num = inf

    pro_comp = ('<td>Accepted</td><td align=center>(\d+)</td>')
    inf_list = re.findall(pro_comp,userstatus)
    for inf in inf_list:
        user_info.ac_num = inf

    if address != '':
        user_info.save(address)
    else :
        user_info.save()

    return 0

def get_user_inf(address = '',username=''):
    try :
        return get_user_inf_core(address,username)
    except :
        return -1


if __name__=='__main__':
    #cookie = get_cookie('username','password')

    #str = ''
    #file = open('input.inf','r')
    #for line in file:
    #    str += line

    #submit_code('1000',0,str,cookie)
    #get_history_inf('addresss',cookie,'username')
    print 'The package "HDOJmethods" is powered by Reskip , if you want to use it in your open source project or other non-commercial occasion , please give references clearily . If business using , contact us to get permission .'
