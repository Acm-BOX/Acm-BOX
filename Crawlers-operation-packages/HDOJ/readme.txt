自认为规范的 中文：
本函数包是一个包含了大部分HDOJ操作的爬虫工具库，由Reskip 于 2016/4/12 实现
其中：
函数分为接口函数和核心（core）函数，外部接入时请使用接口函数，以避免由于网络原因导致的程序崩溃。
网络错误统一返回 -1 

simple and crude English:
This package is a library that include almost operation in HD online judge. Powered by Reskip in 2016/4/12
There in:
these methods(functions) is classified of API methods and core methods. Plz use API methods to avoid Bugs that caused by network failure.


API METHODS:

get_cookie(username,password)

 input just as its name implies.
 return a name-value pair that can be used as cookie later.


submit_code(problem_id,code_lang,code,cookie)

 language nubmer:
 G++   0       C       3       C#      6
 gcc   1       Pascal  4
 C++   2       Java    5

 cookie should be get (get_cookie) before use.
 code is a string that want to be submit.


get_code(address,cookie,username,problem_id)

 you can only get your own code that submited before.(must login before download)
 cookie should be get before.
 
 address is an string where the information will be saved
 
 this method will download all Ac submission in a document and named from 0_code.inf/0_record.inf to i_code.inf/i_record.inf .


get_history_inf(address = '',cookie = '',username = '')

 can only get your own code that submited before.(must login before download)
 cookie should be get before.
 
 address is an string where the information will be saved
 
 this method will download all Ac submission in a document and named from 0_code.inf/0_record.inf to i_code.inf/i_record.inf .
 like this : address\username\problem_id\(i_code.inf/i_record.inf)


get_user_inf(address = '',username='')

 this methods will save a .inf file nemed of username , and some data information (like submission number/Accepted number etc.) will stored in it.
 NO cookie needed
