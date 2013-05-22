from ethel.client import submit_report, next_job, close_job
import sys


def submit():
    return submit_report(sys.argv[1], sys.argv[2])


def next():
    return next_job(sys.argv[1])


def close():
    return close(sys.argv[1])
