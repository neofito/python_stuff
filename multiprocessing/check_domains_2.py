# -*- coding: utf-8 -*-
"""
Benchmarks (para 161 dominios):
23:13:41,52 | 7:34:29,07
23:15:22,16 | 7:36:45,57
"""
import multiprocessing
import requests
import csv
import sys
# To avoid SecurityWarning: Certificate has no `subjectAltName`, falling back to check for
# a `commonName` for now. This feature is being removed by major browsers and deprecated by
#  RFC 2818. See https://github.com/shazow/urllib3/issues/497 for details.
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


def check_url(url):

    try:
        req = requests.get(url, timeout=5, allow_redirects=False)
        return req.status_code
    except UnicodeDecodeError:
        return "ERROR_UNICODEDECODE"
    except requests.exceptions.InvalidURL:
        return "ERROR_INVALIDURL"
    except requests.ConnectionError:
        return "ERROR_CONNECTION"
    except requests.HTTPError:
        return "ERROR_HTTP"
    except requests.Timeout:
        return "ERROR_TIMEOUT"


def make_url(string_url):

    if 'http' in string_url:
        return string_url, "https://%s" % string_url

    if 'https' in string_url:
        return "http://%s" % string_url, string_url

    return "http://%s" % string_url, "https://%s" % string_url


def worker(in_data, out_data):
    for row in iter(in_data.get, 'STOP'):
        (url1, url2) = make_url(row[5])
        out_data.put(row + [check_url(url1), check_url(url2)])


def main(domains_file, results_file):

    in_queue = multiprocessing.Queue()
    out_queue = multiprocessing.Queue()

    rows = 0
    with open(domains_file, 'rb') as csv_input:
        reader = csv.reader(csv_input, dialect='excel', delimiter=';')
        next(reader, None)
        for row in reader:
            in_queue.put(row)
            rows += 1

    for process in range(multiprocessing.cpu_count()):
        multiprocessing.Process(target=worker, args=(in_queue, out_queue)).start()

    with open(results_file, 'wb') as csv_output:
        writer = csv.writer(csv_output, dialect='excel', delimiter=';')
        for writing in range(rows):
            writer.writerow(out_queue.get())

    for process in range(multiprocessing.cpu_count()):
        in_queue.put('STOP')


if __name__ == "__main__":

    main(sys.argv[1], sys.argv[2])
