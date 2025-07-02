from datetime import datetime, timezone

def iso_to_formatted_time(iso_time: str) -> str:
    if iso_time.endswith('Z'):
        iso_time = iso_time[:-1] + '+00:00'

    dt = datetime.fromisoformat(iso_time)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    delta = dt - now

    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 and not parts:  # Only show seconds if nothing else
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    if parts:
        readable_time = "in " + " ".join(parts)
    else:
        readable_time = "soon"

    return readable_time
