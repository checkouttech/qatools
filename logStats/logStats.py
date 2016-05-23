from jsonpath_rw import jsonpath, parse
import json
from collections import OrderedDict
from termcolor import colored

count =0 

print colored('\n***************** Log Validator *****************', 'red')
required_fields = {
                  'Requests with id in it': [parse('$.id'), count],
                  'Requests with tagid in it': [parse('$.imp[0].tagid'), count],
                  'Requests with appstoreid in it': [parse('$.app.ext.appstoreid'), count],
                  'Requests with regs.coppa in it': [parse('$.regs.coppa'), count],
                  'Requests with regs.ext.s22580 in it': [parse('$.regs.ext.s22580'), count],
                  'Requests with private_auction in it': [parse('$.imp[0].pmp.private_auction'), count],
                  'Requests with video mimes in it': [parse('$.imp[0].video.mimes'), count],
                  'Requests with device ip in it': [parse('$.device.ip'), count],
                  'Requests with rubicon user id in it': [parse('$.user.id'), count],
                  'Requests with imp banner height in it': [parse('$.imp[0].banner.h'), count],
                  'Requests with app publisher id in it': [parse('$.site.publisher.id'), count]
                  }


      
total_count = 0
total_valid_count = 0 
not_sent = 0

fileHandle = open('log_to_parse.log', 'r') 

for line  in fileHandle:
   
    if 'KEYWORD' in line :
        total_count += 1 
        recordDict = {} 
        try : 
            recordDict  = json.loads(line.split('KEYWORD :', 1)[1]) 
            total_valid_count += 1 

            for k,v in required_fields.iteritems() : 
                for match in v[0].find(recordDict) : 
                    v[1] += 1 

        except  : 
            print "issue with loading "


print '\n'
print 'Total number of Records : '     + colored(str(total_count), 'yellow' )  
print 'Total number of valid records : ' + colored(str(total_valid_count), 'yellow' ) + ', ' +  colored(str(total_valid_count*100/total_count), "red" ) + colored("%","red") +' of total records'   
print 'Total number of invalid records : ' + colored(str(total_count-total_valid_count), 'yellow' ) + ', ' +  colored(str((total_count - total_valid_count)*100/total_count), "red" ) + colored("%","red") +' of total records'   

print colored('***************** Stats *****************\n','blue')

# print by count sorted
for k,v in  OrderedDict( sorted(required_fields.items(), key=lambda kv: kv[1][1], reverse=True  )).iteritems() :
#for k,v in required_fields.iteritems():
    print str(k) + ' = ' + str(v[1]) + ', ' + colored(str((float(v[1])*100)/float(total_count)),'red') + colored('% ','red') + 'of total Requests\n'




 
