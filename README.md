- Usage

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
