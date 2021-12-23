#!/usr/bin/python3

""" Displays CPU, Memory and Network information """

import psutil


def get_hr_size(b, suffix="b"):
    """ Scale bytes to human-readable format """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor


def cpu_info():
    """ Displays CPU Information."""
    print("=" * 40, "CPU Info", "=" * 40)
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))

    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")

    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"  Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")


def memory_info():
    """ Displays Memory Info """
    print("=" * 35, "Memory Information", "=" * 35)

    mem = psutil.virtual_memory()
    print(f"Total: {get_hr_size(mem.total)}")
    print(f"Available: {get_hr_size(mem.available)}")
    print(f"Used: {get_hr_size(mem.used)}")
    print(f"Percentage: {mem.percent}%")
    print("-" * 20, "SWAP", "-" * 20)

    swap = psutil.swap_memory()
    print(f"Total: {get_hr_size(swap.total)}")
    print(f"Free: {get_hr_size(swap.free)}")
    print(f"Used: {get_hr_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")
    

def network_info():
    """ Displays Networking Information """
    print("=" * 34, "Network Information", "=" * 35)
    # all network interfaces (virtual and physical)
    if_address = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_address.items():
        for address in interface_addresses:
            print(f"--- Interface: {interface_name} ---")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print("-" * 35)
    print(f"Total Bytes Sent: {get_hr_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_hr_size(net_io.bytes_recv)}")


if __name__ == '__main__':
    cpu_info()
    memory_info()
    network_info()
