#!/usr/bin/python2.7
import subprocess
import re
import datetime
import csv
import sys
import getpass

printformat = "%-30s%-10s%-25s"
txt_file = sys.argv[1]

# Command to execute shell commands and capture output
def execute_command(command):
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, _ = result.communicate()
    return output.strip()

# Retrieve CSRF token from Cacti webpage
def get_csrf_token(url):
    output = execute_command('curl -L -s {}'.format(url))
    match = re.search(r'__csrf_magic.*?value="([^"]+)', output)
    if match:
        return match.group(1)
    else:
        return None


def datareform(graph_data):
    lines = graph_data.split('\n')
    inbound_line = [line for line in lines if line.startswith('"2023')]
    if inbound_line:
         inbound = int(float(inbound_line[0].split(',')[1].strip().strip('"')))
         outbound = int(float(inbound_line[0].split(',')[2].strip().strip('"')))
    else:
         outbound = 0
         inbound = 0
    return inbound, outbound

# Login to Cacti system and store cookies
def login_cacti1(url, csrf_token, username, password):
    command = 'curl -L -s -c /home/nocreport/cookies1.txt -b /home/nocreport/cookies1.txt -d "__csrf_magic={}&action=login&login_username={}&login_password={}&realm=ldap" "{}/index.php"'.format(csrf_token, username, password, url)
    execute_command(command)

def login_cacti2(url, csrf_token, username, password):
    command = 'curl -L -s -c /home/nocreport/cookies2.txt -b /home/nocreport/cookies2.txt -d "__csrf_magic={}&action=login&login_username={}&login_password={}&realm=ldap" "{}/index.php"'.format(csrf_token, username, password, url)
    execute_command(command)

# Modify cookies file with specific value
def modify_cookies1(cookie):
    sed_command = r's/^(([^[:space:]]+[[:space:]]+){6})[^[:space:]]+/\1%s/' % cookie
    command = "sed -i -E '{}' {}".format(sed_command, "/home/nocreport/cookies1.txt")
    execute_command(command)
    
def modify_cookies2(cookie):
    sed_command = r's/^(([^[:space:]]+[[:space:]]+){6})[^[:space:]]+/\1%s/' % cookie
    command = "sed -i -E '{}' {}".format(sed_command, "/home/nocreport/cookies2.txt")
    execute_command(command)

# Retrieve graph data for a given graph ID, start date, and end date
def get_graph_data1(url, graph_id, start_date, end_date):
    command = 'curl -L -s -b /home/nocreport/cookies1.txt "{}/graph_xport.php?local_graph_id={}&rra_id=0&graph_start={}&graph_end={}"'.format(url, graph_id, start_date, end_date)
    output = execute_command(command)
    return output

def get_graph_data2(url, graph_id, start_date, end_date):
    command = 'curl -L -s -b /home/nocreport/cookies2.txt "{}/graph_xport.php?local_graph_id={}&rra_id=0&graph_start={}&graph_end={}"'.format(url, graph_id, start_date, end_date)
    output = execute_command(command)
    return output

# Calculate usage based on graph data
def calculate_usage(dataa):
    trafficusage1 = float(dataa) / 1000000000
    trafficusage = round (trafficusage1, 2)
    return trafficusage

# Main function
def main():
    
    cookie1 = raw_input("Enter the cookie value for url1: ")
    cookie2 = raw_input("Enter the cookie value for url2: ")
    cacti_url1 = "your cacti url1"
    cacti_url2 = "your cacti url2"
    username = raw_input("Enter Your Username: ")  # Enter your username
    password = getpass.getpass("Enter Your Password: ")  # Enter your password

    # Set the timezone
    subprocess.call('export TZ="Asia/Rangoon"', shell=True)

    # Specify the date and time in the timezone
    graph_data = raw_input("Enter the graph time (YYYY-MM-DD HH:MM:SS): ")
    print(printformat % ("Description","eth3p1","eth3p2"))
    # Convert the dates to Unix epoch time
    graph_start = int(datetime.datetime.strptime(graph_data, "%Y-%m-%d %H:%M:%S").strftime('%s'))
    graph_end = int(datetime.datetime.strptime(graph_data, "%Y-%m-%d %H:%M:%S").strftime('%s'))

    # Retrieve CSRF token
    csrf_token1 = get_csrf_token(cacti_url1)
    #print(csrf_token1)
    csrf_token2 = get_csrf_token(cacti_url2)
    #print(csrf_token2)
    
    # Login to Cacti system
    login_cacti1(cacti_url1, csrf_token1, username, password)
    login_cacti2(cacti_url2, csrf_token2, username, password)
    
    # Modify cookies file with specific value
    modify_cookies1(cookie1)
    modify_cookies2(cookie2)

    # Read host IDs from input source (e.g., file, user input)
    with open(txt_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            description = row[0]
            trafficsource = row[3]
            eth3p1 = row[1]
            eth3p2 = row[2]
            if trafficsource == "inbound":
                eth3p1data = get_graph_data1(cacti_url1, eth3p1, graph_start, graph_end)
                inbound, outbound = datareform(eth3p1data)
                eth3p1traffic = calculate_usage(inbound)
                eth3p2data = get_graph_data1(cacti_url1, eth3p2, graph_start, graph_end)
                inbound, outbound = datareform(eth3p2data)
                eth3p2traffic = calculate_usage(outbound)
            elif trafficsource == "outbound":
                eth3p1data = get_graph_data2(cacti_url2, eth3p1, graph_start, graph_end)
                inbound, outbound = datareform(eth3p1data)
                eth3p1traffic = calculate_usage(outbound)
                eth3p2data = get_graph_data2(cacti_url2, eth3p2, graph_start, graph_end)
                inbound, outbound = datareform(eth3p2data)
                eth3p2traffic = calculate_usage(inbound)
            print(printformat % (description,eth3p1traffic,eth3p2traffic))
if __name__ == "__main__":
    main()
