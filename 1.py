import subprocess
import re
import pandas as pd
import sys

def ping_host(hostname):
    completed_process = subprocess.run(['ping', '-c', '5', hostname], stdout=subprocess.PIPE, text=True)

    output = completed_process.stdout
    return output

def find_rtt(ping_out):
    str_with_rtt = ping_out.split('\n')[-2]
    match = re.search(r"(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)", str_with_rtt)

    res_dict = {
        'min': float(match.group(1)),
        'avg': float(match.group(2)),
        'max': float(match.group(3))
    }

    return res_dict

if __name__ == '__main__':
    sites = sys.argv[1:]
    list_of_dict_rtt = list()

    for site in sites:
        ping_out = ping_host(site)
        rtt = find_rtt(ping_out)
        rtt['name'] = site
        list_of_dict_rtt.append(rtt)
    
    data = pd.DataFrame(list_of_dict_rtt)
    data.to_csv('./data_of_rtt.csv')
    print(data)

