# in built modules
import json
import os
from typing import Dict, Optional


def read_json(file_path: str) -> Optional[Dict]:
    """
    Args:
        file_path:

    Returns:

    """
    if os.path.exists(file_path) is False:
        return None

    with open(file_path, 'r') as file:
        return json.load(file)
