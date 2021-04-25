# sensit_parser

This repository contains sample script to parse data coming from a Sigfox sensit version 1.

* **sensit_parser.py** can be used as a serverless function for scaleway to parse incoming MQTT data,
* **call_handle.py can** be called with a '--data' to attempt parsing a payload sent by a device,
* **callback_body.json** contains an example of body sent by Sigfox backend in a POST callback,
* **scw_data** contains exmaple of event.json and context.json dictionnaries.


## Usage as Scaleway serverless function

*The current version does not push the data once parsed, it could be added in the future.*

Deploying a serverless function is straigtforward.

1. Create a Namespace
2. Create a function and choose Public or Private
3. Select online editor / python3
4. Paste the code in sensit_parser.py
5. Wait for function to be ready

*API example below are all using the fr-par region*

### Check function availability

Status of the function can be assessed in the GUI or via the API. For the API, you need to created credentials for the Organization. The API Secret can then be used as token for the API.

```bash
# Check function status with API
curl -X GET --header "x-auth-token: $SCW_TOKEN" https://api.scaleway.com/functions/v1alpha2/regions/fr-par/functions/
```

### Call a public serverless function
A public function can simply be called via its endpoint.
```bash
# Test a public function
curl -X POST -d "@body.json" -H "Content-Type: application/json"  <endpoint>
```

### Call a private serverless function
Private function can be called when authentified with a dedicated token. This token can be generated with the API and the function id.
```bash
# Retrieve the function ID
curl --silent  -X GET --header "x-auth-token: $SCW_TOKEN"  "https://api.scaleway.com/functions/v1alpha2/regions/fr-par/functions" | jq ".functions[]"
# Generate a token using the 'id' field of the function we want to call
curl --silent  -X GET --header "x-auth-token: $SCW_TOKEN"  "https://api.scaleway.com/functions/v1alpha2/regions/fr-par/jwt/issue?function_id=<function_id>" | jq "."
# Call the function and pass the generated token
curl -X POST -d "@callback_body.json" -H "SCW_FUNCTIONS_TOKEN: $SCW_FUNCTION_TOKEN" <endpoint>

```

### Parse data sent to an IoT Hub MQTT broker

Using scaleway APIs or scaleway cli, you can retrieve your IoT Hub information and the name of the devices.
The secret for the devices is also required depending on the method used to publish
```bash
scw iot list
```

#### Subscribe to a topic with mosquitto

```bash
# Verbose option will display the topic name along with the message, -t # displays all topics
mosquitto_sub -h iot.fr-par.scw.cloud -i <device id> -t # -v
```

#### Publish a message with mosquitto
```bash
mosquitto_pub -i <device id> -h iot.fr-par.scw.cloud -t <topic/subtopic> -d <data>
```


### Publish a message with curl
```bash
curl -X POST -d <data> -H "x-secret:<device secret>" -H "x-topic:<topic/subtopic>" <url>
```
