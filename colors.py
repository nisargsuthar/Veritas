def is_visible_color(hex_color, min_brightness=0.35):
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    brightness = (0.299 * r + 0.587 * g + 0.114 * b)
    return brightness >= min_brightness

distinct_colors = [
    "FF0000",  # Red
    "00FF00",  # Lime
    "0000FF",  # Blue
    "FFFF00",  # Yellow
    "FF00FF",  # Magenta
    "00FFFF",  # Cyan
    "FF8800",  # Orange
    "00FF88",  # Aqua Green
    "8800FF",  # Purple
    "FF0088",  # Hot Pink
    "00AAFF",  # Sky Blue
    "88FF00",  # Lime-Yellow
    "FF4444",  # Soft Red
    "44FF44",  # Soft Green
    "4444FF",  # Soft Blue
    "FFAA00",  # Amber
    "AA00FF",  # Violet
    "00FFAA",  # Mint
    "FF66CC",  # Pink
    "66CCFF",  # Light Blue
]

all_colors = {
    f"color{i}": f"[color={code.strip('#').upper()}]"
    for i, code in enumerate(distinct_colors)
}

color_dict = {
    name: value for name, value in all_colors.items()
    if is_visible_color(value.strip('[color=]'))
}
