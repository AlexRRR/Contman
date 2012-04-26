from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404,render_to_response
from content.models import SMS
from django.http import HttpResponse
from contman.settings import LOG_FILE
from datetime import datetime,date
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

def report_by_date():
    '''Fetches the results from a specific set of dates, and groups
    results by day, also filling the gaps in and days with no results'''
    stored_results = SMS.objects.filter().extra({'date_created' : "date(received)"}).values('date_created').annotate(created_count=Count('id'))
    no_gap_results = []
    for entry in stored_results:
        if len(no_gap_results) == 0:
            no_gap_results.append(entry)
            continue
        else:
            if to_georgian(entry['date_created']) - to_georgian(no_gap_results[-1]['date_created']) == 1:
                no_gap_results.append(entry)
            else:
                while (to_georgian(entry['date_created']) - to_georgian(no_gap_results[-1]['date_created']) != 1):
                    next_date = date.fromordinal(to_georgian(no_gap_results[-1]['date_created']) + 1).strftime('%Y-%m-%d')
                    next_empty_entry = {'date_created': next_date, 'created_count': 0}
                    no_gap_results.append(next_empty_entry)
                no_gap_results.append(entry)
                continue
    return no_gap_results





    
