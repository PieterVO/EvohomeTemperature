# Script to monitor and read temperatures from Honeywell EvoHome Web API and send them to Plotly

# Load required libraries
import requests
import json
import datetime
import time
import plotly
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

# Sign in
py.sign_in("Username", "APIkey")

# Stream tokens from plotly
tls.set_credentials_file(stream_ids=[
    "token1",
    "token2",
    "token3",
    "token4",
    "token5",
    "token6",
])
stream_ids = tls.get_credentials_file()['stream_ids']

# Set your login details in the 2 fields below
USERNAME = 'Your Evohome connected username'
PASSWORD = 'Your Evohome password'

# Initial JSON POST to the website to return your userdata
url = 'https://rs.alarmnet.com/TotalConnectComfort/WebAPI/api/Session'
postdata = {'Username':USERNAME, 'Password':PASSWORD,'ApplicationId':'91db1612-73fd-4500-91b2-e63b069b185c'}
headers = {'content-type':'application/json'}
response = requests.post(url,data=json.dumps(postdata),headers =headers)
userinfo = json.loads(response.content)

# Extract the sessionId and your userid from the response
userid = userinfo['userInfo']['userID']
sessionId = userinfo['sessionId']

# Next, using your userid, get all the data back about your site
url = 'https://rs.alarmnet.com/TotalConnectComfort/WebAPI/api/locations?userId=%s&allData=True' % userid
headers['sessionId'] = sessionId
response = requests.get(url,data=json.dumps(postdata),headers =headers)
fullData = json.loads(response.content.decode('utf-8'))[0]

# We make a plot for every room
i=0
for device in fullData['devices']:
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
    # Next, using your userid, get all the data back about your site
    url = 'https://rs.alarmnet.com/TotalConnectComfort/WebAPI/api/locations?userId=%s&allData=True' % userid
    headers['sessionId'] = sessionId
    response = requests.get(url,data=json.dumps(postdata),headers =headers)
    fullData = json.loads(response.content.decode('utf-8'))[0]

# Get current time and then send all thermostat readings to plotly
    from datetime import datetime
    j=0
    for device in fullData['devices']:
        stream_id = stream_ids[j]
        j+=1
        s = py.Stream(stream_id)
        s.open()
        tijd = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        temperatuur = device['thermostat']['indoorTemperature']
        s.write(dict(x=tijd ,y=temperatuur))
        s.close()
    time.sleep(300)
