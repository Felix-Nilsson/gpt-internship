import json

json_data = {"observation": [
    {
      "patient_id": 123123,
      "aktivitet_id": 12345678,
      "begrepp": "diagnos",
      "kod": "J189 Pneumoni, ospecificerad",
      "värde": "primär",
      "startdatum": "2020-03-28",
      "slutdatum": "2020-03-30"
    }
  ]}

json_string = json.dumps(json_data).replace('"', '\\"')

print(json_string)