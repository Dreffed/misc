import re
from collections import Counter
import logging
from logging.config import fileConfig
from sqlite3.dbapi2 import paramstyle

logger = logging.getLogger(__name__)

def get_regexes():    
    return {
        "^": re.compile("[A-Z]{2,}"),
        "|": re.compile("[A-Z][a-z]+"),
        "U": re.compile("[A-Z]+"),
        "L": re.compile("[a-z]+"),
        "*": re.compile(r"[\u4e00-\u9fff]+"),
        "N": re.compile(r"\d+"),
        "B": re.compile(r"[()\[\]{}']+"),
        "P": re.compile(r"[,!@#$%&+=?]+"),
        ".": re.compile(r"[\. _\-]+")
    }

def profile(input, regexes):
    positions = {}
    p = {}
    for k,v in regexes.items():
        for m in v.finditer(input):
            l = len(m.group())
            s = m.start()
            e = m.end()
            if s not in p:
                p[s] = {
                    "start": s,
                    "end": e,
                    "type": k.replace("^", "U").replace("|", "W"),
                    "value": m.group()
                }
                input = "{}{}{}".format(input[:s], k*l, input[e:])
                if l == 1:
                    positions[s] = k
                else:
                    positions[s] = "{}{}".format(k,l)

    output = []
    parts = []
    for k,v in sorted(positions.items()):
        output.append(v)
        parts.append(p.get(k))

    return {
        "parts": parts,
        "profile": "".join(output).replace("^","U").replace("|", "W"),
        "expand": input.replace("^", "U").replace("|", "W")
    }

def expand_profile(s):
    stack = []
    cc = None
    for c in s:
        if c.isdigit():
            if cc:
                stack.append(cc*int(c))
            cc = None
        else:
            if cc:
                stack.append(cc)
            cc = c
    return "".join(stack)

def consolidate_profile(s):
    p = re.sub(r"\.\.+", "-", s).replace('.','')
    p = re.sub("WW+", "w", p)
    p = re.sub("NN+", "n", p)
    p = re.sub("UU+", "u", p)
    p = re.sub("PP+", "p", p).replace('J','-')
    return p

def frequency(s):
    """
    :type s: str
    :rtype: str
    """
    d = Counter(s)
    return d


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    strings = [
        '1.4 Protection of Privacy - Information Incidents (Privacy Breaches)',
        'Accept Amendment to Disclosure Statement_02112019_0328',
        'DS1 29560',
        'RBC-20080401-ABCPmarket',
        'Accept Form V_05222018_1043',
        'Accept Disclosure_06202018_0915',
        'Deficiency (Discl)_06072018_0908',
        '29563 - Undertaking - Hillcrest Place',
        'BCFSA Application for Consent Application Section #2 - Sub-Section #2 - November 30 2019 MERGER AGREEMENTS',
        'Bulkley Valley - X020317'
    ]

    regexes = get_regexes()

    for s in strings:
        pr = profile(s, regexes=regexes)

        np = pr.get("profile")
        ep = expand_profile(np)
        cp = consolidate_profile(ep)
        hs = frequency(s)

        logger.info(s)
        for k,v in pr.items():
            logger.info("\t:{}: {}".format(k,v))
            
        logger.info("""\t{}
        \t{}
        \t{}""".format(hs, ep, cp))
