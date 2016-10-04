from __future__ import print_function
import csv
import numpy as np
import sys

# hard code the max duration of the movie stimulus
maxmovietime = 7085.28


def time2sec(text, event_nmbr, allow_empty=False):
    # fix formating error
    if text.count(".") > 1 and max([len(i) for i in text.split(".")]) > 2:
        text = text.replace(".", "", 1)
    # convert text time specification to a float for the number of seconds
    if text.count('.') > 1 or ':'.join(text.split(':')[:-1]).count('.'):
        # not just a comma
        text = text.replace('.', ':')
    if not len(text.strip()) or text.strip() == '#NV':
        if allow_empty:
            pass
            #report("WARN: empty timestamp", '', event_nmbr)
        else:
            pass
            #report("ERR: empty timestamp", '', event_nmbr)
        return 0
    val = text.split(':')
    if len(val) == 4:
        # including frames
        h, m, s, frames = val
        frames = int(frames)
        if frames > 24:
            report("ERR: strange time stamps '%s'" % text, '', event_nmbr)
        try:
            s = float(s) + frames / 25.
        except:
            report("ERR: failed to convert time stamp '{0}'".format(text), '', event_nmbr)
    elif len(val) == 3:
        # standard
        h, m, s = val
    elif len(val) == 2:
        # assume seconds are zero
        h, m = val
        s = 0
    elif len(val) == 1:
        # assume only seconds given
        h = 0
        m = 0
        s = val[0]
    else:
        report("ERR: cannot understand time stamp '%s'" % text, '', event_nmbr)
        return 0
    try:
        h = int(h)
        m = int(m)
        s = float(s)
    except:
        report("ERR: cannot understand time stamp '%s'" % text, '', event_nmbr)
        return 0
    return 3600 * h + 60 * m + s


def safeopen_table(fname):
    csvfile = open(fname, 'r')
    try:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
    except:
        dialect = 'excel'
    csvfile.seek(0)
    return csv.reader(csvfile, dialect)


def report(msg, event, event_nmbr):
    print("# %i: %s  --  %s" % (event_nmbr + 2, msg, event), file=sys.stderr)


def get_nsecond_segments(n=1):
    return np.array((np.arange(0, maxmovietime - n, n), np.arange(n, maxmovietime, n))).T
