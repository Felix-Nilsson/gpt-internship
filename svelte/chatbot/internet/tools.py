from langchain.tools import BaseTool
from duckduckgo_search import DDGS


def get_functions():
    # This is used as a parameter to the functions and asks gpt to provide reasoning for the choice of function and search term.
    explanation_param = {
        'type': 'string',
        'description': 'Detaljerad beskrivning av tankegången från användarens fråga till varför funktionen bör kallas.'
    }

    functions = [
        {
            'name': '1177',
            'description': 'Använd detta verktyg när du behöver svara på frågor om sjukdomar eller skador.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'search_query': {
                    'type': 'string',
                    'description': 'Sökord för att hitta information om, till exempel, en sjukdom eller en skada.'
                    },
                    'explanation': explanation_param
                },
                'required': ['search_query', 'explanation']
            }
        },
        {
            'name': 'FASS',
            'description': 'Använd detta verktyg när du behöver svara på frågor om läkermedel, till exempel biverkningar, dosering eller tillgång.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'search_query': {
                        'type': 'string',
                        'description': 'Sökord för att hitta information om, till exempel, läkemedel.'
                    },
                    'explanation': explanation_param
                },
                'required': ['search_query', 'explanation']
            }
        },
        {
            'name': 'internetmedicin',
            'description': 'Använd detta verktyg när du behöver information om ICD-koder för skador eller sjukdomar.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'search_query': {
                        'type': 'string',
                        'description': 'ICD-kod.'
                    },
                    'explanation': explanation_param
                },
                'required': ['search_query', 'explanation']
            }
        }
    ]

    return functions



def search_1177(query):
    query += " site:1177.se"
    return _ddg_search(search_query=query)
    
def search_FASS(query):
    query += " site:fass.se"
    return _ddg_search(search_query=query)

def search_internetmedicin(query):
    query += " site:internetmedicin.se"
    return _ddg_search(search_query=query)


def _ddg_search(search_query: str, num_results=3) -> list[dict[str, str]]:
    """Run query through DuckDuckGo and return metadata.

    Args:
        query: The query to search for.
        num_results: The number of results to return.

    Returns:
        A list of dictionaries with the following keys:
            snippet - The description of the result.
            title - The title of the result.
            link - The link to the result.
    """

    with DDGS() as ddgs:
        results = ddgs.text(
            search_query,
            region="se-sv",
            #safesearch=self.safesearch,
            #timelimit=self.time,
        )
        if results is None:
            return [{"Result": "No good DuckDuckGo Search Result was found"}]

        def to_metadata(result: dict) -> dict[str, str]:
            return {
                "snippet": result["body"],
                "title": result["title"],
                "link": result["href"],
            }

        formatted_results = []
        for i, res in enumerate(results, 1):
            if res is not None:
                formatted_results.append(to_metadata(res))
            if len(formatted_results) == num_results:
                break
    return formatted_results





'''class Tool1177(BaseTool):
    name = "1177.se"
    description = "Använd detta verktyg när du behöver svara på frågor om sjukdomar eller skador"

    def _run(self, query):
        query += " site:1177.se"
        return _ddg_search(search_query=query)

    def _arun(self, query):
        return NotImplementedError("This tool does not support async")


class ToolFASS(BaseTool):
    name = "FASS.se"
    description = "Använd detta verktyg när du behöver svara på frågor om läkermedel, till exempel biverkningar, dosering eller tillgång"

    def _run(self, query):
        query += " site:fass.se"
        return _ddg_search(search_query=query)

    def _arun(self, query):
        return NotImplementedError("This tool does not support async")


class ToolInternetmedicin(BaseTool):
    name = "internetmedicin.se"
    description = "Använd detta verktyg när du behöver information om ICD-koder för skador eller sjukdomar"

    def _run(self, query):
        query += " site:internetmedicin.se"
        return _ddg_search(search_query=query)

    def _arun(self, query):
        return NotImplementedError("This tool does not support async")'''