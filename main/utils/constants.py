NOT_DEFINED = '-'
PENDING = 'Pending'
RUNNING = 'Running'
FINISHED = 'Finished'
FAILED = 'Failed'

TYPE = 1
ADDRESS = 2
CITY = 3
PROVINCE = 4
AREA = 5
PARKING = 6
LIFT = 7
LATITUDE = 8
LONGITUDE = 9

MAX_FILE_SIZE = 524288


def filesize(size):
    y = 512000
    step = 1024
    if size < y:
        value = round(size/step, 2)
        ext = ' kb'
    elif size < y*1000:
        value = round(size/(step**2), 2)
        ext = ' Mb'
    else:
        value = round(size/(step**3), 2)
        ext = ' Gb'
    return str(value)+ext


BASE_LINK = 'idealista.com'
