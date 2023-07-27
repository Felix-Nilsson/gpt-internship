import json
import sys
import os
import yaml

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.chroma import query_db


def preprocess():
    json_data = query_db(
        query="Vad är orsaken bakom hjärtinfarkten som patienten upplevde?",
        id="789012",
        name='patientrecords'
    )

    #todo: currently selects only best, maybe add functionality for top n
    return json_data["documents"][0][0]


    """json_string = json.dumps(json_data).replace('"', '\\"')

    with open("promptfoo/promptfooconfig.yaml","r") as f:
        doc = yaml.safe_load(f)
    
    doc["tests"][0]["vars"]["background"] = json_string
    
    with open("promptfoo/promptfooconfig.yaml", 'w') as f:
        yaml.dump(doc, f)"""


print(preprocess())