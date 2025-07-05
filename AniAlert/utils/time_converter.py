from datetime import datetime, timezone

def convert_unix(seconds: int) -> str:
    """Convert duration in seconds to 'Xd Yh Zm Ws' format."""
    if seconds is None:
        return "unknown"

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)


def convert_iso(iso_time: str) -> str:
    """Convert ISO time string to human-readable relative time (e.g., 'in 1 day 2 hours')."""
    if not iso_time:
        return "unknown"

    # Normalize 'Z' timezone notation
    if iso_time.endswith('Z'):
        iso_time = iso_time[:-1] + '+00:00'

    dt = datetime.fromisoformat(iso_time)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    delta = dt - now

    if delta.total_seconds() <= 0:
        return "soon"

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
    if seconds > 0 and not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return "in " + " ".join(parts) if parts else "soon"

example = convert_unix(424824)
print(example)