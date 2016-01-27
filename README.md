EvohomeTemperature
==================

Log Evohome temperature using Plotly

Alternative with own webserver and MySQL database: https://github.com/PieterVO/EvohomeTemperatureSite


Requirements
-------------
- Python
- Plotly
    Installation: https://plot.ly/python/getting-started/


Installation
-------------
- Make a duplicate of instructions.ini and name it config.ini
- In config.ini you need to fill in your stream ids, plotly username and api key, evohome username and password
-   Go on the website to settings->api settings
-   There you find your api key en stream ids (you can easily generate them there)
- Then just run the Python script. It will update the temperature every 5 minutes.
