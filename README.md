# sensit_parser

This repository contains sample script to parse data coming from a Sigfox sensit version 1.

* **sensit_parser.py** can be used as a serverless function for scaleway to parse incoming MQTT data,
* **call_handle.py can** be called with a '--data' to attempt parsing a payload sent by a device,
* **callback_body.json** contains an example of body sent by Sigfox backend in a POST callback,
* **scw_data** contains exmaple of event.json and context.json dictionnaries.


## Usage as Scaleway serverless function

1. Create a Namespace
2. Create a function and choose Public or Private
3. Select online editor / python3
4. Paste the code in sensit_parser.py
5. Wait for function to be ready

### Check function availability

Status of the function can be assessed in the GUI or via the API. For the API, you need to created credentials for the Organization. The API Secret can then be used as token for the API.

```bash
# Check function status with API
curl -X GET --header "x-auth-token: $SCW_TOKEN" https://api.scaleway.com/functions/v1alpha2/regions/fr-par/functions/
```
### Call the serverless function via its endpoint


```bash
# Test a public function
curl -X POST -d "@body.json" -H "Content-Type: application/json"  FUNCTION_ENDPOINT

```
