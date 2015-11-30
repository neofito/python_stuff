# -*- coding: utf-8 -*-
"""
http://www.ibm.com/developerworks/aix/library/au-multiprocessing/
http://stackoverflow.com/questions/2359253/solving-embarassingly-parallel-problems-using-python-multiprocessing
"""
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


def main(domains_file, results_file):

    with open(domains_file, 'rb') as csv_input, open(results_file, 'wb') as csv_output:
        reader = csv.reader(csv_input, dialect='excel', delimiter=';')
        next(reader, None)
        writer = csv.writer(csv_output, dialect='excel', delimiter=';')
        for row in reader:
            (url1, url2) = make_url(row[5])
            writer.writerow(row + [check_url(url1), check_url(url2)])


if __name__ == "__main__":

    # CSV con los datos, CSV para los resultados
    main(sys.argv[1], sys.argv[2])
