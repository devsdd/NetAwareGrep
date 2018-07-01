import argparse
from netaddr import *
import yaml


def parse_command_line():
    """
    Ensures proper command-line usage
    :return: ip/mask (string)
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=True, help="IP or CIDR address")
    args = parser.parse_args()
    cidr = args.ip

    # sample value for testing
    # cidr = "180.76.15.32/23"
    return cidr

def get_settings():
    with open("settings.yaml") as f:
        settings = yaml.safe_load(f)

    return settings


def validate_CIDR(cidr):
    """
    Ensures cidr is a legitimate IPv4 or IPv6
    host or network address
    :param cidr: "net"|"host"|False
    :return:
    """
    '''
    if "/" in cidr and ipaddress.ip_network(cidr):
        return "net"
    elif ipaddress.ip_address(cidr):
        return "host"
    else:
        return False
    '''

    try:
        if(IPAddress(cidr)):
            return "host"
    except: # we passed a network address, not IP

        try:
            if (IPNetwork(cidr)):
                return "net"
        except:
            return False

def queryString_for_common_netmasks(cidr, netmask):

    if netmask == '8':
        ip_parts = cidr.split('.')[0]
    elif netmask == '16':
        ip_parts = cidr.split('.')[0:2]
    elif netmask == '24':
        ip_parts = cidr.split('.')[0:3]

    queryString = ""
    for octet in ip_parts:
        # /8 addresses will have a single string
        if type(ip_parts) == str:
            queryString = ip_parts + '.'
        # /16 and /24 will turn into a list split on the dots
        elif type(ip_parts) == list:
            queryString += octet + '.'

    return queryString

def expand_subnet(cidr):

    ips = []
    for ip in IPNetwork(cidr):
        ips.append(str(ip) + " ")    # needed to distinguish .1, .12 and .123 and not triple count such lines

    return ips


def grep_in_log(queryObj, logfile):

    result = []
    with open(logfile) as f:
        if type(queryObj) == list:
            for line in f:
                for ip in queryObj:
                    if str(ip) in line:
                        result.append(line.rstrip())
        elif type(queryObj) == str:  # searching for single IP
            for line in f:
                if queryObj in line:
                    result.append(line.rstrip())

    return result

if __name__ == "__main__":

    cidr = parse_command_line()
    var = validate_CIDR(cidr)
    if not var:
        raise Exception("%s does not seem to be a valid IP or network address" % var)

    if var == "net":
        '''
        For common netmasks like /8, /16 and /24,
        ranges of IP's in them align neatly with 
        octet boundaries in the dotted-decimal 
        notation of an IPv4 IP, so we don't need to  
        go the computationally heavy route of 
        grepping every IP in the network against 
        every line in the file; we can just snip out 
        the network part and grep with it.
        '''
        ip = cidr.split('/')[0]
        netmask = cidr.split('/')[1]

        if netmask in ('8', '16', '24'):
            iplist = queryString_for_common_netmasks(ip, netmask)
        else:
            iplist = expand_subnet(cidr)

    elif var == "host":
        iplist = cidr

    logfile = get_settings()['logfile']
    res = grep_in_log(iplist, logfile)
    print(type(res))
    for line in res:
        print(line)

