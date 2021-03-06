import subprocess
import re, time, os, sys, msvcrt
import bencode
import codecs
import psutil
from Misc import processArguments


def check_interface(interface_name):
    output = subprocess.check_output("ipconfig /all")

    lines = output.splitlines()
    lines = filter(lambda x: x, lines)

    # print('output: ', output)
    # print('lines: ', lines)

    ip_address = ''
    # mac_address = ''
    name = ''

    for line in lines:
        # -------------
        # Interface Name

        is_interface_name = re.match(r'^[a-zA-Z0-9].*:$', line)
        # is_interface_name = 1
        if is_interface_name:

            # Check if there's previews values, if so - yield them
            if name and ip_address:
                if name == interface_name:
                    return ip_address

            ip_address = ''
            # mac_address = ''
            name = line.rstrip(':')

            # print('line: ', line)
            # print('name: ', name)

        line = line.strip().lower()

        if ':' not in line:
            continue

        value = line.split(':')[-1]
        value = value.strip()

        # -------------
        # IP Address

        is_ip_address = not ip_address and re.match(r'ipv4 address|autoconfiguration ipv4 address|ip address', line)

        if is_ip_address:
            ip_address = value
            ip_address = ip_address.replace('(preferred)', '')
            ip_address = ip_address.strip()

            # print('line: ', line)
            # print('ip_address: ', ip_address)

        # -------------
        # MAC Address

        # is_mac_address = not ip_address and re.match(r'physical address', line)
        #
        # if is_mac_address:
        #     mac_address = value
        #     mac_address = mac_address.replace('-', ':')
        #     mac_address = mac_address.strip()

    if name and ip_address:
        if name == interface_name:
            return ip_address
    return None


if __name__ == '__main__':

    params = {
        'interface_name': 'PPP adapter PureVPN',
        'restart_time': 86400,
        'wait_time': 10800,
        'post_wait_time': 10,
        'check_vpn_gap': 30,
        'vpn_path': 'C:\Users\Tommy\Desktop\purevpn.lnk',
        'tor_path': 'C:\Users\Tommy\Desktop\uTorrent.lnk',
        'settings_path': 'C:\Users\Tommy\AppData\Roaming\uTorrent\settings.dat',
        'vpn_proc': 'purevpn.exe',
        'tor_proc': 'uTorrent.exe',
    }

    processArguments(sys.argv[1:], params)
    interface_name = params['interface_name']
    restart_time = params['restart_time']
    wait_time = params['wait_time']
    post_wait_time = params['post_wait_time']
    check_vpn_gap = params['check_vpn_gap']
    vpn_path = params['vpn_path']
    tor_path = params['tor_path']
    settings_path = params['settings_path']
    vpn_proc = params['vpn_proc']
    tor_proc = params['tor_proc']

    global_start_t = time.time()

    restart_now = 0

    while True:

        os.startfile(vpn_path)
        ip_address = None

        print 'waiting for vpn to start'

        while True:
            ip_address = check_interface(interface_name)
            if time.time() - global_start_t > restart_time:
                restart_now = 1
                break
            if ip_address is not None:
                break

        if restart_now:
            break

        print 'vpn started with ip_address: {}'.format(ip_address)

        f = codecs.open(settings_path, "rb").read()
        d = bencode.bdecode(f)
        d['net.bind_ip'] = ip_address
        d['net.outgoing_ip'] = ip_address
        f_out = bencode.bencode(d)
        codecs.open(settings_path, "wb").write(f_out)

        os.startfile(tor_path)

        print 'Waiting for {} seconds. Press any key to continue'.format(wait_time)

        for i in xrange(wait_time):
            if (i + 1) % check_vpn_gap == 0:
                ip_address = check_interface(interface_name)
                if ip_address is None:
                    print '\nvpn disconnection detected'
                    break

            if msvcrt.kbhit():
                inp = msvcrt.getch()
                print '\ncontinuing'
                break

            time.sleep(1)
            sys.stdout.write('\r{}'.format(i + 1))
            sys.stdout.flush()

        sys.stdout.write('\n')
        sys.stdout.flush()

        tor_killed = 0
        for proc in psutil.process_iter():
            if proc.name() == tor_proc:
                proc.terminate()
                tor_killed = 1
                break

        if not tor_killed:
            raise IOError('Tor process {} not found'.format(tor_proc))

        vpn_killed = 0
        for proc in psutil.process_iter():
            if proc.name() == vpn_proc:
                proc.kill()
                vpn_killed = 1
                break

        if not vpn_killed:
            raise IOError('VPN process {} not found'.format(vpn_proc))

        if time.time() - global_start_t > restart_time:
            restart_now = 1
            break

        if restart_now:
            break

        print 'Waiting for {} seconds. Press any key to continue'.format(post_wait_time)
        for i in xrange(post_wait_time):
            if msvcrt.kbhit():
                inp = msvcrt.getch()
                print '\ncontinuing'
                break

            time.sleep(1)
            sys.stdout.write('\r{}'.format(i + 1))
            sys.stdout.flush()

        sys.stdout.write('\n')
        sys.stdout.flush()

    if restart_now:
        print "Restarting..."
        os.system("shutdown -t 0 -r -f")
