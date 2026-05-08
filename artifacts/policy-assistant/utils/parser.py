def parse_response(raw_response: str, task_type: str) -> dict:
    formatted_output = {}
    
    if task_type == "summarize":
        formatted_output["summary"] = raw_response
    elif task_type == "explain":
        formatted_output["plain_language"] = raw_response
    elif task_type == "compare":
        formatted_output["comparison"] = raw_response
    elif task_type == "evaluate":
        formatted_output["critical_analysis"] = raw_response
    else:
        formatted_output["output"] = raw_response
    
    return formatted_output

def preprocess_input(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize("NFKC", text)
    text = " ".join(text.split())
    return text.strip()

def validate_input(text: str, min_length: int = 5, max_chars: int = 500000) -> tuple[bool, str]:
    if not text or len(text.strip()) < min_length:
        return False, f"Input is too short. Please provide at least {min_length} characters."
    if len(text) > max_chars:
        return False, f"Input is too long ({len(text)} characters). Please keep it under {max_chars:,} characters."
    return True, ""
