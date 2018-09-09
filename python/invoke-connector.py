import sys, json
import os
#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    # Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    #get our data as an array from read_in()
    jsondata = read_in()
    #print('From inovek-script '+jsondata["connectionId"])
    os.system('python3 /node-parser/python/connector_driver.py '+ jsondata["connectionId"])
# Start process
if __name__ == '__main__':
    main()
