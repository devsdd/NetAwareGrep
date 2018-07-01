
from weblogHelper import *
import pytest
import os

@pytest.fixture(scope="module", autouse=True)
def setup():
    global cidr
    cidr = parse_command_line()

@pytest.mark.unit
def test_parse_command_line():
    """
    Test whether parse_command_line function is
    able to extract an IP
    :return: string
    """
    if not isinstance(cidr, basestring):
        assert False

def test_validate_CIDR():
    good_inputs =   ("192.168.1.1",
                     "10.0.0.255",
                     "172.16.1.0/24",
                     "255.255.255.255",
                     "192.0.2.0/16"
                    )
    bad_inputs =    ("172.16.1.300",
                     "172.16.1.",
                     "172.16",
                     "172.16.1.0/16",
                     "172.16.1.0/33",
                     "172.16.1.0/0",
                     "172.16.1.0/"
                     "172.16.1.0/1"
                     )

    for i in good_inputs:
        assert validate_CIDR(i)

    for j in bad_inputs:
        if not validate_CIDR(j):
            assert True


def test_host_or_net():
    var = validate_CIDR(cidr)
    assert var == "host" or var == "net"


def test_expand_subnet():
    assert isinstance(expand_subnet(cidr), list)

def test_config_file_present():
    assert os.path.isfile("settings.yaml")

def test_get_settings():
    global logfile
    logfile = get_settings()['logfile']
    assert logfile

def test_queryString_for_slash24():
    slash24 = "172.16.1.0/24"
    queryString = queryString_for_common_netmasks("172.16.1.0", "24")
    print(queryString)
    assert queryString == "172.16.1."

def test_queryString_for_slash16():
    slash16 = "172.16.1.0/16"
    queryString = queryString_for_common_netmasks("172.16.1.0", "16")
    print(queryString)
    assert queryString == "172.16."

def test_queryString_for_slash8():
    slash8 = "172.16.1.0/8"
    queryString = queryString_for_common_netmasks("172.16.1.0", "8")
    print(queryString)
    assert queryString == "172."

def test_grep_in_log():
    ''' The actual function has been designed
    to only operate on a single IP at a time,
    (multiple IPs passed as a list are handled
    one-at-a-time), so we test with only a single IP
    '''

    singleIP = cidr.split('/')[0]
    res = grep_in_log(singleIP, logfile)
    assert type(res) == list
