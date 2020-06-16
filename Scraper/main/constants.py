NOT_DEFINED = '-'
PENDING = 'Pending'
RUNNING = 'Running'
FINISHED = 'Finished'
FAILED = 'Failed'

TIPO = 1
DIRECCION = 2
MUNICIPIO = 3
PROVINCIA = 4
SUPERFICIE = 5
PARKING = 6
ASCENSOR = 7


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
