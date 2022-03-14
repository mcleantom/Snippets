from typing import Any
import json
from fastapi.responses import Response

class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")


"""
Usage:

@app.get("/", response_class=PrettyJSONResponse)
def get_pretty_json_response():
  some_json = {"name": "Tom", groups=["group 1", "group 2", "group 3"]}
  return some_json
"""
