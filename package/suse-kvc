#!/usr/bin/python3
#
# Note:
#   uname -r (as being found in the basic-environment.txt)
#   returns a kernel version like 4.12.14-197.78-default,
#   in the TID page however, it's specified as 4.12.14-197.78.1.
#   Hence, in order to match such versions, we have to remove
#   a flavor like '-default' or '-preempt' from the provided kernel
#   version and compare it with the versions found in the TID,
#   as well as with the last number (in this case '.1') removed.
#

import re
import sys
import lxml.html
import requests

tid_url = 'https://www.suse.com/support/kb/doc/?id=000019587'

def rows(html):
    """
    Return all text items from a html table row object
    """
    doc = lxml.html.fromstring(html.content)
    for row in doc.xpath('//body//table//tr'):
        if (row.text_content().strip()):
            yield row

def fields(row):
    """
    Return row values as array of [field1, field2]
    """
    data = row.xpath('td')
    return [ d.text_content().strip() for d in data ]

def clean_uname(kernel):
    """
    Remove kernel flavor (eg. -default, -preempt) from `uname -r` output
    """
    return re.sub('-\w+$', '', kernel)

def match_kernel_version(current, tidver):
    """
    Return True, if current kernel version matches the tid version
    while ignoring any build revision from the tid version (trailing '<dot><single digit> pattern)
    current is either the cleaned `uname -r` output, or the full build (tid) version
    tidver the kernel version, as recorded on the tid page
    """
    # exact match including build revision
    if current == tidver:
        return True
    # crude heuristic: do we have a single trailing digit?
    m = re.match('(.*)\.\d$', tidver)
    if m:
        return current == m[1]

def create_dict(html):
    """
    Create a dictionary of {os_version: [(date, kernel) .. ]}

    Arguments:
        html: html page test content as returned by requests.get(url)

    Return:
        dictionary: key is a specific OS version
                    value is a list of (release date, kernel) tuples
    """
    os_dict = {}
    os_ver = ""
    for row in rows(html):
        rel, ver = fields(row)[:2]
        if 'SLE' in ver:
            # unify SLES version labels
            ver = ver.replace("SLE12", "SLES12")
            os_ver = ver
            os_dict[os_ver] = []
        else:
            if os_ver:
                #print("'%s', '%s', %s" % (os_ver, rel, repr(ver)))
                for val in ver.split('\t'):
                    val = val.strip()
                    if not val:
                        continue
                    if val[0] + val[-1] == '<>':
                        val = val[1:-1]
                    if not re.match("\(.*\)|.*release.*|.*rebuild.*", val):
                        #print("add: %s, %s, %s" % (os_ver, rel, repr(val)))
                        os_dict[os_ver].append((rel, val))
                    #else:
                        #print("ignored: %s" % repr(val))
    return os_dict

def search_os(kernel, os_dict):
    """
    Return the OS version for a given kernel version
    """
    kernel_uname = clean_uname(kernel)

    for os_version, releases in os_dict.items():
        for rel, ver in releases:
            if match_kernel_version(kernel_uname, ver):
                return os_version
    return ""

def search_kr(kernel, os_dict):
    """
    Return a (kernel, release) tuple for a given kernel version
    """
    kernel_uname = clean_uname(kernel)

    for os_version, releases in os_dict.items():
        for rel, ver in releases:
            if match_kernel_version(kernel_uname, ver):
                return (kernel_uname, rel)

def is_pre_ltss(os_version, os_dict):
    ltss_version = os_version + " - LTSS"
    if ltss_version in os_dict:
        return True
    return False

def missing_kernels(kernel, os_dict):
    """
    Arguments:
        kernel  - kernel that is being searched tid
        os_dict - dictionary result of parsing tid html, returned by create_dict()

    Return:
        [missing_kernels][missing_ltss_kernels]
    """
    # find in which OS release <kernel> is shipped
    os_version = search_os(kernel, os_dict)

    kernel_uname = clean_uname(kernel)

    # find the position of this kernel in os_dict[os_version] array
    temp = ()
    for release in os_dict[os_version]:
        temp = release
        if match_kernel_version(kernel_uname, release[1]):
            break
    kernel_index = os_dict[os_version].index(temp)

    # get list of missing kernels, ie. [kernel_index+1:]
    missing_kernels = os_dict[os_version][kernel_index+1:]
    missing_ltss_kernels = []
    # add all kernels shipped in LTSS version
    if is_pre_ltss(os_version, os_dict):
        ltss_version = os_version + " - LTSS"
        missing_ltss_kernels = os_dict[ltss_version]
    return missing_kernels, missing_ltss_kernels

def print_sep():
    print("-----------------------")

def print_missing(lst, ltss = False):
    if lst:
        print()
        if ltss:
            print("{:d} missing LTSS updates: ".format(len(lst)))
        else:
            print("{:d} missing updates: ".format(len(lst)))
        print_sep()
        for rel, ver in lst:
            print ("Date: {}, Kernel: {}".format(rel, ver))

def kernel_check(kernel, tid_url):
    html = requests.get(tid_url)
    reld = create_dict(html)
    #from pprint import pp
    #pp(reld)
    os_release = search_os(kernel, reld)
    if os_release:
        if is_pre_ltss(os_release, reld):
            print ("Pre-LTSS OS: {}".format(os_release))
        else:
            print ("OS: %s" % os_release)

        missing, missing_ltss = missing_kernels(kernel, reld)
        ver, rel = search_kr(kernel, reld)
        msg = 'is up-to-date'
        if any((missing, missing_ltss)):
            msg = 'missed {} releases'.format(len(missing + missing_ltss))
            print_missing(missing)
            print_missing(missing_ltss, True)
        print_sep()
        print('Kernel {}, released {}, {}'.format(ver, rel, msg))
    else:
        print ("Kernel {} not found".format(kernel))
        exit(1)

if len(sys.argv) != 2:
    print("Usage: kernel_check <kernel from 'uname -r'>")
    exit(1)

kernel_check(sys.argv[1], tid_url)

# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
