import json
import sys
import os
import yaml

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.chroma import query_db_with_id


def preprocess():
    """Function that returns the relevant text chunks that should be used when answering the prompt. Used for evaluating prompt with promptfoo."""

    json_data = query_db_with_id(
        query="Vad är orsaken bakom hjärtinfarkten som patienten upplevde?",
        id="789012",
        name='patientrecords'
    )

    #todo: currently selects only best, maybe add functionality for top n
    return json_data["documents"][0][0]


print(preprocess())