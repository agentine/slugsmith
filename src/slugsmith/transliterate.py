"""Unicode to ASCII transliteration engine."""

from __future__ import annotations

import unicodedata

# Comprehensive Unicode → ASCII mapping.
# Covers Latin Extended, Cyrillic, Greek, Arabic, Hebrew, and symbols.
# Characters that decompose cleanly via NFKD are handled automatically;
# this map catches everything else.
CHAR_MAP: dict[str, str] = {
    # Latin Extended-A / Extended-B
    "\u0110": "D",  # Đ
    "\u0111": "d",  # đ
    "\u0126": "H",  # Ħ
    "\u0127": "h",  # ħ
    "\u0131": "i",  # ı (dotless i)
    "\u0138": "k",  # ĸ
    "\u0141": "L",  # Ł
    "\u0142": "l",  # ł
    "\u014a": "N",  # Ŋ
    "\u014b": "n",  # ŋ
    "\u0152": "OE",  # Œ
    "\u0153": "oe",  # œ
    "\u0166": "T",  # Ŧ
    "\u0167": "t",  # ŧ
    "\u00d8": "O",  # Ø
    "\u00f8": "o",  # ø
    "\u00c6": "AE",  # Æ
    "\u00e6": "ae",  # æ
    "\u00df": "ss",  # ß
    "\u00f0": "d",  # ð
    "\u00de": "Th",  # Þ
    "\u00fe": "th",  # þ

    # Cyrillic (Russian)
    "\u0410": "A", "\u0411": "B", "\u0412": "V", "\u0413": "G",
    "\u0414": "D", "\u0415": "E", "\u0416": "Zh", "\u0417": "Z",
    "\u0418": "I", "\u0419": "J", "\u041a": "K", "\u041b": "L",
    "\u041c": "M", "\u041d": "N", "\u041e": "O", "\u041f": "P",
    "\u0420": "R", "\u0421": "S", "\u0422": "T", "\u0423": "U",
    "\u0424": "F", "\u0425": "Kh", "\u0426": "Ts", "\u0427": "Ch",
    "\u0428": "Sh", "\u0429": "Shch", "\u042a": "", "\u042b": "Y",
    "\u042c": "", "\u042d": "E", "\u042e": "Yu", "\u042f": "Ya",
    "\u0430": "a", "\u0431": "b", "\u0432": "v", "\u0433": "g",
    "\u0434": "d", "\u0435": "e", "\u0436": "zh", "\u0437": "z",
    "\u0438": "i", "\u0439": "j", "\u043a": "k", "\u043b": "l",
    "\u043c": "m", "\u043d": "n", "\u043e": "o", "\u043f": "p",
    "\u0440": "r", "\u0441": "s", "\u0442": "t", "\u0443": "u",
    "\u0444": "f", "\u0445": "kh", "\u0446": "ts", "\u0447": "ch",
    "\u0448": "sh", "\u0449": "shch", "\u044a": "", "\u044b": "y",
    "\u044c": "", "\u044d": "e", "\u044e": "yu", "\u044f": "ya",
    # Ukrainian extras
    "\u0404": "Ye", "\u0454": "ye",
    "\u0406": "I", "\u0456": "i",
    "\u0407": "Yi", "\u0457": "yi",
    "\u0490": "G", "\u0491": "g",

    # Greek
    "\u0391": "A", "\u0392": "B", "\u0393": "G", "\u0394": "D",
    "\u0395": "E", "\u0396": "Z", "\u0397": "I", "\u0398": "Th",
    "\u0399": "I", "\u039a": "K", "\u039b": "L", "\u039c": "M",
    "\u039d": "N", "\u039e": "X", "\u039f": "O", "\u03a0": "P",
    "\u03a1": "R", "\u03a3": "S", "\u03a4": "T", "\u03a5": "Y",
    "\u03a6": "F", "\u03a7": "Ch", "\u03a8": "Ps", "\u03a9": "O",
    "\u03b1": "a", "\u03b2": "b", "\u03b3": "g", "\u03b4": "d",
    "\u03b5": "e", "\u03b6": "z", "\u03b7": "i", "\u03b8": "th",
    "\u03b9": "i", "\u03ba": "k", "\u03bb": "l", "\u03bc": "m",
    "\u03bd": "n", "\u03be": "x", "\u03bf": "o", "\u03c0": "p",
    "\u03c1": "r", "\u03c2": "s", "\u03c3": "s", "\u03c4": "t",
    "\u03c5": "y", "\u03c6": "f", "\u03c7": "ch", "\u03c8": "ps",
    "\u03c9": "o",

    # Arabic (basic)
    "\u0627": "a",  # ا alef
    "\u0628": "b",  # ب ba
    "\u062a": "t",  # ت ta
    "\u062b": "th",  # ث tha
    "\u062c": "j",  # ج jim
    "\u062d": "h",  # ح ha
    "\u062e": "kh",  # خ kha
    "\u062f": "d",  # د dal
    "\u0630": "dh",  # ذ dhal
    "\u0631": "r",  # ر ra
    "\u0632": "z",  # ز zay
    "\u0633": "s",  # س sin
    "\u0634": "sh",  # ش shin
    "\u0635": "s",  # ص sad
    "\u0636": "d",  # ض dad
    "\u0637": "t",  # ط ta
    "\u0638": "z",  # ظ za
    "\u0639": "a",  # ع ain
    "\u063a": "gh",  # غ ghain
    "\u0641": "f",  # ف fa
    "\u0642": "q",  # ق qaf
    "\u0643": "k",  # ك kaf
    "\u0644": "l",  # ل lam
    "\u0645": "m",  # م mim
    "\u0646": "n",  # ن nun
    "\u0647": "h",  # ه ha
    "\u0648": "w",  # و waw
    "\u064a": "y",  # ي ya

    # Hebrew (basic)
    "\u05d0": "a",  # א alef
    "\u05d1": "b",  # ב bet
    "\u05d2": "g",  # ג gimel
    "\u05d3": "d",  # ד dalet
    "\u05d4": "h",  # ה he
    "\u05d5": "v",  # ו vav
    "\u05d6": "z",  # ז zayin
    "\u05d7": "ch",  # ח het
    "\u05d8": "t",  # ט tet
    "\u05d9": "y",  # י yod
    "\u05da": "k",  # ך kaf final
    "\u05db": "k",  # כ kaf
    "\u05dc": "l",  # ל lamed
    "\u05dd": "m",  # ם mem final
    "\u05de": "m",  # מ mem
    "\u05df": "n",  # ן nun final
    "\u05e0": "n",  # נ nun
    "\u05e1": "s",  # ס samekh
    "\u05e2": "a",  # ע ayin
    "\u05e3": "p",  # ף pe final
    "\u05e4": "p",  # פ pe
    "\u05e5": "ts",  # ץ tsadi final
    "\u05e6": "ts",  # צ tsadi
    "\u05e7": "q",  # ק qof
    "\u05e8": "r",  # ר resh
    "\u05e9": "sh",  # ש shin
    "\u05ea": "t",  # ת tav

    # Special symbols
    "\u00a9": "c",  # ©
    "\u00ae": "r",  # ®
    "\u2122": "tm",  # ™
    "\u20ac": "euro",  # €
    "\u00a3": "pound",  # £
    "\u00a5": "yen",  # ¥
    "\u00a2": "cent",  # ¢
    "\u2026": "...",  # …
    "\u2013": "-",  # –
    "\u2014": "-",  # —
    "\u2018": "'",  # '
    "\u2019": "'",  # '
    "\u201c": '"',  # "
    "\u201d": '"',  # "
    "\u00ab": '"',  # «
    "\u00bb": '"',  # »
    "\u00b0": "deg",  # °
    "\u00b5": "u",  # µ
}


def transliterate(text: str) -> str:
    """Transliterate Unicode text to ASCII.

    Strategy:
    1. Apply CHAR_MAP for characters with explicit mappings.
    2. Apply NFKD normalization and strip combining marks.
    3. Encode to ASCII ignoring remaining non-ASCII characters.
    """
    # First pass: apply explicit char map
    result: list[str] = []
    for char in text:
        if char in CHAR_MAP:
            result.append(CHAR_MAP[char])
        elif ord(char) < 128:
            result.append(char)
        else:
            # NFKD decompose this character
            decomposed = unicodedata.normalize("NFKD", char)
            ascii_part = decomposed.encode("ascii", "ignore").decode("ascii")
            result.append(ascii_part)

    return "".join(result)
