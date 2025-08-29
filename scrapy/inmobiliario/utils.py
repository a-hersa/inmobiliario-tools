import re

def extract_location_from_title(self, raw_title):
    """
    Extract location using prioritized strategies:
    1. Last part after the last comma
    2. Last part after "en"
    3. Last part after "de"
    """
    if not raw_title:
        return "", ""
    
    title = raw_title.strip()
    
    # Strategy 1: Last part after the last comma (existing logic - highest priority)
    if ',' in title:
        title_parts = title.split(',')
        if len(title_parts) > 1:
            location = title_parts[-1].strip()
            clean_title = ','.join(title_parts[:-1]).strip()
            return clean_title, location
    
    # Strategy 2: Last part after "en" 
    en_match = re.search(r'\ben\s+(.+?)$', title, re.IGNORECASE)
    if en_match:
        location = en_match.group(1).strip()
        clean_title = title[:en_match.start()].strip()
        return clean_title, location
    
    # Strategy 3: Last part after "de"
    de_match = re.search(r'\bde\s+(.+?)$', title, re.IGNORECASE)
    if de_match:
        location = de_match.group(1).strip()
        clean_title = title[:de_match.start()].strip()
        return clean_title, location
    
    # No location found, return original title
    return title, ""