from django.http import HttpResponse
from django.db.models import Count
from django.db import connections
from django.shortcuts import get_object_or_404,render_to_response
from content.models import SMS
from django.http import HttpResponse
from contman.settings import LOG_FILE
from datetime import datetime,date
import pdb
# Create your views here.

def show_log(request,rtype):
	log_data = tail(LOG_FILE)

	return render_to_response('log_report.html', {'log_entries':log_data}) 

def tail(file_name,window=20):
	f = open(file_name)
	BUFSIZE = 1024
	f.seek(0, 2)
	bytes = f.tell()
	size = window
	block = -1
	data = []
	while size > 0 and bytes > 0:
		if (bytes - BUFSIZE > 0):
			f.seek(block*BUFSIZE, 2)
			data.append(f.read(BUFSIZE))
		else:
			f.seek(0,0)
			data.append(f.read(bytes))
		linesFound = data[-1].count('\n')
		size -= linesFound
		bytes -= BUFSIZE
		block -= 1

        log_lines = ''.join(data).splitlines()[-window-1:]
        if log_lines[-1][-1] == "\n":
            return log_lines
        return log_lines[:-1]


def to_georgian(datestring):
    '''converts a date string into a georgian integeer'''
    georgian = datetime.strptime(datestring,'%Y-%m-%d').date().toordinal()
    return georgian

def to_month_number(datestring):
    '''converts a date string into a month number'''
    pdb.set_trace()
    month = datetime.strptime(datestring,'%Y-%m-%d').date().month
    pdb.set_trace()
    return month

def extract_week_no(ds):
        d = datetime.strptime(ds,'%Y-%m-%d').isocalendar()[1]
        return d

def next_month(last_result):
    last_date = date.strptime(last_result,'%Y-%m-%d').date()
    m = last_date.month
    y = last_result.year
    m += 1
    if m == 13:
        m = 1
        y += 1
    first_of_next_month = date(y, m, 1)
    return first_of_next_month.strftime('%Y-%m-%d')

def next_day(last_result):
    return date.fromordinal(to_georgian(last_result()) + 1).strftime('%Y-%m-%d')

def fill_gaps(results,qtype,end_d):
    '''adds entries to list for periods where not data was found'''
    dispatch={'by_day':to_georgian,'by_month':to_month_number}
    next_date={'by_day':next_day,'by_month':next_month} 
    stored_results = list(results)
    end_date = datetime.strptime(end_d,'%Y-%m-%d').date()

    end_date_found = False
    for result in stored_results:
        if end_date in result:
            end_date_found = True
    if not end_date_found:
        stored_results.append({'date_created': end_d, 'created_count': 0})

    no_gap_results = []
    last_result = lambda:no_gap_results[-1]['date_created']
    for entry in stored_results:
        if len(no_gap_results) == 0:
            no_gap_results.append(entry)
            continue
        else:
            if dispatch[qtype](entry['date_created']) - dispatch[qtype](last_result()) == 1:
                no_gap_results.append(entry)
            else:
                while (dispatch[qtype](entry['date_created']) - dispatch[qtype](last_result()) != 1):
                    next_date = next_date[qtype]
                    next_empty_entry = {'date_created': next_date, 'created_count': 0}
                    no_gap_results.append(next_empty_entry)
                no_gap_results.append(entry)
                continue
    return no_gap_results



def report_by_date(start_d,end_d):
    '''Fetches the results from a specific set of dates, and groups
    results by day, also filling the gaps in and days with no results'''
    start_date = datetime.strptime(start_d,'%Y-%m-%d').date()
    end_date = datetime.strptime(end_d,'%Y-%m-%d').date()
    query_results = SMS.objects.filter(received__gt=start_date).exclude(received__gt=end_date).extra({'date_created' : "date(received)"}).values('date_created').annotate(created_count=Count('id'))
    stored_results = list(query_results)

    end_date_found = False
    for result in stored_results:
        if end_date in result:
            end_date_found = True
    if not end_date_found:
        stored_results.append({'date_created': end_d, 'created_count': 0})

    no_gap_results = []
    last_result = lambda:no_gap_results[-1]['date_created']
    for entry in stored_results:
        if len(no_gap_results) == 0:
            no_gap_results.append(entry)
            continue
        else:
            if to_georgian(entry['date_created']) - to_georgian(last_result()) == 1:
                no_gap_results.append(entry)
            else:
                while (to_georgian(entry['date_created']) - to_georgian(last_result()) != 1):
                    next_date = date.fromordinal(to_georgian(last_result()) + 1).strftime('%Y-%m-%d')
                    next_empty_entry = {'date_created': next_date, 'created_count': 0}
                    no_gap_results.append(next_empty_entry)
                no_gap_results.append(entry)
                continue
    return no_gap_results



def report_by_month():
    a = SMS.objects.extra(select={'date_created': connections[SMS.objects.db].ops.date_trunc_sql('month', 'received')}).values('date_created').annotate(created_count=Count('received'))
    return fill_gaps(list(a),'by_month','2012-05-10')

    
