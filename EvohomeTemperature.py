# Script to monitor and read temperatures from Honeywell EvoHome Web API and send them to Plotly

# Load required libraries
import requests
import json
import datetime
import time
import plotly
import plotly.plotly as py
import plotly.tools as tls
import ConfigParser
from plotly.graph_objs import *
from evohomeclient2 import EvohomeClient

#config
Config = ConfigParser.ConfigParser()
Config.read("config.ini")
Username = Config.get('Plotly', 'Username')
APIkey = Config.get('Plotly', 'APIkey')

# Sign in
py.sign_in(Username, APIkey)

stream_ids_array = []
for name, value in Config.items('Rooms'):
    stream_ids_array.append(value)

# Stream tokens from plotly
tls.set_credentials_file(stream_ids=stream_ids_array)
stream_ids = tls.get_credentials_file()['stream_ids']

# Set your login details in the 2 fields below
USERNAME = Config.get('Evohome', 'Username')
PASSWORD = Config.get('Evohome', 'Password')

try:
    client = EvohomeClient(USERNAME, PASSWORD)
except ValueError:
    try:
        client = EvohomeClient(USERNAME, PASSWORD)
    except ValueError:
        print "Error when connecting to internet, please try again"

# We make a plot for every room
i=0
for device in client.temperatures():
    stream_id = stream_ids[i]
    i=i+1
    stream = Stream(
        token=stream_id,
        maxpoints=288
    )
    trace1 = Scatter(
           x=[],
           y=[],
           mode='lines+markers',
           line=Line(
               shape='spline'
               ),
           stream = stream
           )

    data = Data([trace1])
    layout = Layout(title=device['name'])
    fig = Figure(data=data, layout=layout)
    py.plot(fig, filename=device['name'], fileopt='extend')

# Infinite loop every 5 minutes, send temperatures to plotly
while True:

# Get current time and then send all thermostat readings to plotly
    try:
        client = EvohomeClient(USERNAME, PASSWORD)
        from datetime import datetime
        j=0
        for device in client.temperatures():
            stream_id = Config.get('Rooms', device['name'])
            j+=1
            s = py.Stream(stream_id)
            s.open()
            tijd = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            temperatuur = float(device['temp'])
            print tijd + " : " + device['name'] + " " + str(temperatuur)
            s.write(dict(x=tijd ,y=temperatuur))
            s.close()
        print "Going to sleep for 5 minutes"
        time.sleep(300)
    except Exception, e:
        print "An error occured! Trying again in 15 seconds"
        print str(e)
        time.sleep(15)
    
