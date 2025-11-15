import re


def render_markdown(md: str) -> str:
    if not md:
        return ""

    lines = md.splitlines()
    html_lines = []
    in_ul = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False

    for raw in lines:
        line = raw.rstrip()

        if re.match(r"^#{1,6} ", line):
            close_ul()
            level = len(line.split(" ")[0])
            text = line[level+1:]
            html_lines.append(f"<h{level}>{text}</h{level}>")
            continue

        if re.match(r"^\- ", line):
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            text = line[2:]
            html_lines.append(f"<li>{text}</li>")
            continue

        if line.strip() == "":
            close_ul()
            html_lines.append("<br/>")
            continue

        close_ul()
        html_lines.append(f"<p>{line}</p>")

    close_ul()
    return "\n".join(html_lines)