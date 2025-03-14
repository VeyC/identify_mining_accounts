
from datetime import datetime

date_string = '2018/09/12'
date_object = datetime.strptime(date_string, '%Y/%m/%d')
print(date_object)
print(type(date_object))