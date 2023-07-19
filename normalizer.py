from transliterate import translit

def normal(s):
    ns = ''
    s = s.upper()
    if '"' in s:
        s = s.split('"')[1:]
    elif '(' in s:
        s = s.split('(')[:1]
    for item in s:
        ns += item
    to_replace = {" ": "", "!": "", ",": "", ".": "", "-": "", "CS": "КС", "CO": "КО", "WE": "ВЕ", "EW": "ЬЮ", "GE": "Ж", "X": "КС", "HI": "ХАЙ", 
                  "MI": "МАЙ", "LY": "ЛИ", "CC": "КЦ", "WA": "ВЭЙ", "CT": "КТ", "CH": "Х", "SIS": "ЗИС", "GIES": "ДЖИС", "EQ": "ЭК", "ILE": "АЙЛ", 
                  "W": "В", "CK": "К", "ER": "ЭР", "OO": "У", "HEA": "ХЭ", "AND": "ЭНД", "HA": "ХЭ", "OU": "У"}
    for item in to_replace.keys():
        ns = ns.replace(item, to_replace[item])
    return translit(ns, 'ru')