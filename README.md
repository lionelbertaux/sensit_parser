# sensit_parser
This repository contains sample script to parse data coming from a Sigfox sensit version 1.

* sensit_parser.py can be used as a serverless function for scaleway to parse incoming MQTT data
* call_handle.py can be called with a '--data' to attempt parsing a payload sent by a device


## Deployment in Scaleway serverless function

* Create a function
* Select online editor / python3
* Paste the code in sensit_parser.py
* Wait for function to be ready


Check function status with API
```bash
curl -X GET --header "x-auth-token: $scw_token" https://api.scaleway.com/functions/v1alpha2/regions/fr-par/functions/
```

To test a public function:
```bash
curl -X POST -d "@body.json" -H "Content-Type: application/json"  FUNCTION_ENDPOINT

```
