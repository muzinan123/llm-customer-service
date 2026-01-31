"""
Tool definition file
"""

SEARCH_TOOL = {
    "function": {
        "name": "search",
        "description": "Perform an internet search and return relevant results",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keywords"
                }
            },
            "required": ["query"]
        }
    }
}

TOOL_DEFINITIONS = [SEARCH_TOOL]
