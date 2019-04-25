import re


def check_url(url):
    c = re.compile(r"^(https?://)?(www.)?(youtube.com|youtu.?be)/.+$")
    m = re.match(c, url)
    if m:
        return True
    else:
        return False



