from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render_to_response
from content.models import SMS
from django.http import HttpResponse
from contman.settings import LOG_FILE
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
