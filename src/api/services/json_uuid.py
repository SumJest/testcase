import datetime
import json
from typing import Any
from uuid import UUID


class UUIDJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, UUID):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder().default(o)

