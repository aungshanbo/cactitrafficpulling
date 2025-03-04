# Cacti Traffic Data Collector

This Python 2.7 script retrieves traffic data from Cacti graphs, processes it, and displays the inbound/outbound traffic usage. The script logs in to Cacti, fetches graph data based on user input, and calculates traffic usage.

## Prerequisites

- Python 2.7
- `curl` command-line tool installed on your system
- Access to the Cacti monitoring system

## Installation

1. Clone the repository or download the script:
   ```sh
  git@github.com:aungshanbo/cactitrafficpulling.git
   cd cactitrafficpulling
   ```
2. Ensure the script is executable:
   ```sh
   chmod +x traffic_collector.py
   ```

## Usage

Run the script with a CSV file containing Cacti graph IDs as an argument:

```sh
python2.7 lazyguy.py <graph_id_file.csv>
```

### Example CSV File Format
The CSV file should have the following format:

```
Description,eth3p1,eth3p2,trafficsource
Server1,123,456,inbound
Server2,789,1011,outbound
```

### Script Execution Example
```
$ python2.7 traffic_collector.py graph_ids.csv
Enter the cookie value for url1: <cookie1>
Enter the cookie value for url2: <cookie2>
Enter Your Username: admin
Enter Your Password: ****
Enter the graph time (YYYY-MM-DD HH:MM:SS): 2023-12-01 12:00:00

Description                   eth3p1    eth3p2
-------------------------------------------------
Server1                       2.5       3.7
Server2                       1.2       4.6
```

## How It Works
- The script prompts the user for authentication details.
- It retrieves CSRF tokens from the Cacti system and logs in.
- It modifies cookie files with user-provided cookie values.
- It reads graph IDs from the provided CSV file.
- It fetches graph data for a given time range.
- It calculates and displays traffic usage in gigabytes.

## Troubleshooting
- Ensure the Cacti URLs are correctly configured.
- Check if the credentials are valid.
- Verify the CSV file format is correct.
- Ensure Python 2.7 is installed and used to run the script.

