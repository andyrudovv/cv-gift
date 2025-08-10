import json
import logging
import re

def convert_to_clean_json(s: str) -> str:
    """
    Convert AI response with markdown code blocks to clean JSON string
    """
    try:
        logging.debug(f"Original string: {s[:200]}")
        
        if "```" in s:
            start = s.find("{")
            end = s.rfind("}") + 1
            if start != -1 and end != -1:
                s = s[start:end]
        
        s = s.replace('\\n', '\n')
        s = s.replace('\\"', '"')
        s = s.replace('\\\\', '\\')
        
        s = re.sub(r'\n\s*', ' ', s)
        s = re.sub(r',\s*}', '}', s)
        s = re.sub(r'\s+', ' ', s)
        s = s.strip()
        
        try:
            parsed = json.loads(s)
        except json.JSONDecodeError:
            s = re.sub(r':\s*([^"\{\[\d][^,\}\]]*?)(\s*[,\}\]])', r': "\1"\2', s)
            parsed = json.loads(s)
        
        clean_json = json.dumps(parsed, ensure_ascii=False, indent=2)
        logging.debug(f"Cleaned JSON: {clean_json[:200]}")
        return clean_json
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON cleaning failed: {str(e)}")
        logging.error(f"Failed string: {s[:200]}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error while cleaning JSON: {str(e)}")
        raise