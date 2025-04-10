## Usage

### Setup .env file

add a .env file to the root of the project with the following content:

```
# Environment variables for the IoT stack

# InfluxDB credentials
DOCKER_INFLUXDB_INIT_USERNAME=my-username
DOCKER_INFLUXDB_INIT_PASSWORD=my-secret-passowrd
DOCKER_INFLUXDB_INIT_ORG=home-iot
DOCKER_INFLUXDB_INIT_BUCKET=sensor-data

# InfluxDB token
INFLUXDB_TOKEN=infludb-generated-token
```

for the INFLUXDB_TOKEN, after first run of docker compose, login to serverip:8086 
with the username and password above, go to sources->api_token , clone the key 
already persent, then copy the token the influxdb prompts to copy
as value for INFLUXDB_TOKEN above. 
Delete the previous token just to be safe.

### Start docker containers

to start docker run `docker compose up` from the `iot-stack` directory or `docker compose up --detach` for background run

### Start sensor read and publish

in the sensor directory run 
- `source venv` this should create python venv and install dependencies
- execute the tmp102_read_publish.py, eg `python3 tmp102_read_publish.py --broker localhost --serial_number 1234abc` or as `python3 tmp102_read_publish.py --broker localhost --serial_number 1234abc > /dev/null &` for no logs background run