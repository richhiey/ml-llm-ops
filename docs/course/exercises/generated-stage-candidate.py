"""INTENTIONALLY UNSAFE assistant-style proposal for review; not installed helper code."""
def proposed_guard(frame):
    if len(frame) == 0:
        raise ValueError("empty batch")
    frame["hour"] = frame["hour"].clip(upper=23)
    return frame
