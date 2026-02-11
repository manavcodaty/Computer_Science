
from typing import List, Tuple, Dict

# -------------------------------
# 1) INITIALS EXTRACTOR
# -------------------------------

def extract_initials(full_name: str, *, add_dots: bool = False, to_upper: bool = True) -> str:
    """
    Take a full name (e.g., 'Samir Ahmed Patel') and return initials.
    - add_dots=True  -> 'S.A.P'
    - add_dots=False -> 'SAP'
    - to_upper toggles case
    Ignores empty parts (multiple spaces / hyphen handling below).
    """
    if not isinstance(full_name, str):
        raise TypeError("full_name must be a string")

    # Treat hyphenated names as a single word but keep only first letter (e.g., 'Mary-Jane' -> 'M')
    parts = [p for p in full_name.strip().split() if p]

    initials = []
    for p in parts:
        ch = p[0]
        initials.append(ch)

    out = "".join(initials) if not add_dots else ".".join(initials)
    return out.upper() if to_upper else out


# -------------------------------
# 2) SENTENCE WORD REVERSER
# -------------------------------

def reverse_each_word(sentence: str) -> Tuple[str, int]:
    """
    Reverse each word in the sentence but keep word order.
    Returns (reversed_sentence, palindrome_count).
    Word = sequence of non-space chars; preserves spacing exactly.
    Palindrome check is case-insensitive and ignores non-alphanumeric characters.
    """
    import re

    def rev(word: str) -> str:
        return word[::-1]

    # Split on groups of spaces to preserve original spacing
    tokens = re.split(r"(\s+)", sentence)
    reversed_tokens = []
    palindrome_count = 0

    for t in tokens:
        if t.isspace() or t == "":
            reversed_tokens.append(t)
            continue

        r = rev(t)
        reversed_tokens.append(r)

        norm = re.sub(r"[^A-Za-z0-9]", "", t).lower()
        if norm and norm == norm[::-1]:
            palindrome_count += 1

    return "".join(reversed_tokens), palindrome_count


# -------------------------------
# 3) EMAIL ADDRESS VALIDATOR
# -------------------------------

def validate_email(addr: str, *, school_domain: str = "school.com") -> Dict[str, object]:
    """
    Validate simple email rules:
      - must contain exactly one '@'
      - must contain at least one '.' after '@'
      - '@' must come before last '.'
      - must not contain spaces
    Also returns extracted domain and 'School email' / 'Other email'.
    NOTE: This is a simple classroom validator, not RFC 5322 complete.
    """
    result = {
        "email": addr,
        "is_valid": False,
        "reason": "",
        "local": None,
        "domain": None,
        "type": None,  # 'School email' or 'Other email'
    }

    if " " in addr:
        result["reason"] = "Contains spaces"
        return result

    if addr.count("@") != 1:
        result["reason"] = "Must contain exactly one @"
        return result

    local, domain = addr.split("@", 1)
    if not local or not domain:
        result["reason"] = "Missing local or domain part"
        return result

    if "." not in domain:
        result["reason"] = "Domain must contain at least one '.'"
        return result

    # Last '.' position must be after '@' (already true if '.' is in domain)
    # Also ensure no empty labels like 'example..com'
    if ".." in domain or domain.startswith(".") or domain.endswith("."):
        result["reason"] = "Invalid dot placement in domain"
        return result

    # Basic character scan (letters, digits, allowed specials in a simple set)
    allowed_local = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._+-")
    if any(ch not in allowed_local for ch in local):
        result["reason"] = "Illegal character in local part"
        return result

    result["is_valid"] = True
    result["reason"] = "OK"
    result["local"] = local
    result["domain"] = domain
    result["type"] = "School email" if domain.lower() == school_domain.lower() else "Other email"
    return result


class EmailBucket:
    """
    Stores valid emails for later use.
    """
    def __init__(self, school_domain: str = "school.com"):
        self.school_domain = school_domain
        self.valid_emails: List[str] = []

    def add(self, addr: str) -> Dict[str, object]:
        v = validate_email(addr, school_domain=self.school_domain)
        if v["is_valid"]:
            self.valid_emails.append(addr)
        return v


# -------------------------------
# DEMO / SIMPLE TESTS
# -------------------------------
if __name__ == "__main__":
    # 1) Initials
    print("== Initials Extractor ==")
    for name in [
        "Samir Patel",
        "Samir Ahmed Patel",
        "  maya   el   saad  ",
        "Mary-Jane Watson",
        "a b c",
    ]:
        print(name, "->", extract_initials(name, add_dots=False),
              "| dotted:", extract_initials(name, add_dots=True))

    # 2) Sentence word reverser
    print("\n== Sentence Word Reverser ==")
    s = "The cat sat level on noon"
    rev, count = reverse_each_word(s)
    print("Original:", s)
    print("Reversed:", rev)
    print("Palindromic words count:", count)

    # 3) Email validator + storing valid emails
    print("\n== Email Validator ==")
    bucket = EmailBucket(school_domain="school.com")
    emails = [
        "alice@school.com",
        "bob.smith@dept.school.com",
        "charlie@@school.com",
        "dana@school..com",
        "eve school@com",
        "frank@company.org",
        "@nouser.com",
        "nouser@",
    ]
    for e in emails:
        res = bucket.add(e)
        print(f"{e:30} -> valid={res['is_valid']}, reason={res['reason']}, domain={res['domain']}, type={res['type']}")

    print("Stored valid emails:", bucket.valid_emails)
