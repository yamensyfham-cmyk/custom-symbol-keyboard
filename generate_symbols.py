#!/usr/bin/env python3
import os
import unicodedata

BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "app", "src", "main", "res", "xml")
KEYS_PER_PAGE = 60
KEYS_PER_ROW = 10
TOTAL_KEYS_TARGET = 5000

UNICODE_BLOCKS = [
    (0x2100, 0x214F, "Letterlike"),
    (0x2190, 0x21FF, "Arrows"),
    (0x2200, 0x22FF, "Math Operators"),
    (0x2300, 0x23FF, "Misc Technical"),
    (0x2460, 0x24FF, "Enclosed Alphanumerics"),
    (0x2500, 0x257F, "Box Drawing"),
    (0x2580, 0x259F, "Block Elements"),
    (0x25A0, 0x25FF, "Geometric Shapes"),
    (0x2600, 0x26FF, "Miscellaneous Symbols"),
    (0x2700, 0x27BF, "Dingbats"),
    (0x27C0, 0x27EF, "Misc Math A"),
    (0x27F0, 0x27FF, "Supplemental Arrows A"),
    (0x2800, 0x28FF, "Braille Patterns"),
    (0x2900, 0x297F, "Supplemental Arrows B"),
    (0x2980, 0x29FF, "Misc Math B"),
    (0x2A00, 0x2AFF, "Supplemental Math Operators"),
    (0x2B00, 0x2BFF, "Misc Symbols and Arrows"),
    (0x3000, 0x303F, "CJK Symbols"),
    (0x3200, 0x32FF, "Enclosed CJK"),
    (0x3300, 0x33FF, "CJK Compatibility"),
    (0xA700, 0xA71F, "Modifier Tone"),
    (0xFE30, 0xFE4F, "CJK Compat Forms"),
    (0xFE50, 0xFE6F, "Small Form Variants"),
    (0xFF00, 0xFFEF, "Halfwidth/Fullwidth"),
    (0x1D000, 0x1D0FF, "Byzantine Music"),
    (0x1D100, 0x1D1FF, "Musical Symbols"),
    (0x1D300, 0x1D35F, "Tai Xuan Jing"),
    (0x1D400, 0x1D7FF, "Math Alphanumeric"),
    (0x1F000, 0x1F02F, "Mahjong"),
    (0x1F030, 0x1F09F, "Domino Tiles"),
    (0x1F0A0, 0x1F0FF, "Playing Cards"),
    (0x1F100, 0x1F1FF, "Enclosed Alphanumeric Suppl"),
    (0x1F300, 0x1F5FF, "Misc Pictographs"),
    (0x1F600, 0x1F64F, "Emoticons"),
    (0x1F650, 0x1F67F, "Ornamental Dingbats"),
    (0x1F680, 0x1F6FF, "Transport Symbols"),
    (0x1F700, 0x1F77F, "Alchemical Symbols"),
    (0x1F780, 0x1F7FF, "Geometric Shapes Extended"),
    (0x1F800, 0x1F8FF, "Supplemental Arrows C"),
    (0x1F900, 0x1F9FF, "Suppl Symbols Pictographs"),
    (0x1FA00, 0x1FA6F, "Chess Symbols"),
    (0x1FA70, 0x1FAFF, "Symbols Pictographs Ext A"),
    (0x2000, 0x206F, "General Punctuation"),
    (0x2070, 0x209F, "Superscripts/Subscripts"),
    (0x20A0, 0x20CF, "Currency Symbols"),
    (0x2150, 0x218F, "Number Forms"),
    (0x2E80, 0x2EFF, "CJK Radicals"),
]

BAD_CATEGORIES = {'Cc', 'Cf', 'Cn', 'Co', 'Cs', 'Zl', 'Zp', 'Mn', 'Mc', 'Me'}
BAD_CODEPOINTS = set([
    0x00A0, 0x00AD, 0x034F, 0x061C, 0x115F, 0x1160,
    0x17B4, 0x17B5, 0x180B, 0x180C, 0x180D, 0x180E,
    0x200B, 0x200C, 0x200D, 0x200E, 0x200F,
    0x2028, 0x2029, 0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
    0x2060, 0x2061, 0x2062, 0x2063, 0x2064,
    0xFE00, 0xFE01, 0xFE02, 0xFE03, 0xFE04, 0xFE05,
    0xFE06, 0xFE07, 0xFE08, 0xFE09, 0xFE0A, 0xFE0B,
    0xFE0C, 0xFE0D, 0xFE0E, 0xFE0F,
    0xFEFF, 0xFFF0, 0xFFF1, 0xFFF2, 0xFFF3, 0xFFF4,
    0xFFF5, 0xFFF6, 0xFFF7, 0xFFF8,
    0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005,
    0x2006, 0x2007, 0x2008, 0x2009, 0x200A,
    0x202F, 0x205F, 0x3000,
])

def is_valid_symbol(codepoint):
    try:
        if codepoint <= 0x20:
            return False
        if codepoint in BAD_CODEPOINTS:
            return False
        ch = chr(codepoint)
        cat = unicodedata.category(ch)
        if cat in BAD_CATEGORIES:
            return False
        name = unicodedata.name(ch, '')
        if not name:
            return False
        return True
    except (ValueError, TypeError):
        return False

def collect_symbols():
    symbols = []
    seen = set()
    for start, end, block_name in UNICODE_BLOCKS:
        for cp in range(start, end + 1):
            if cp in seen:
                continue
            if is_valid_symbol(cp):
                symbols.append(cp)
                seen.add(cp)
    return symbols

def xml_entity(codepoint):
    return f"&#x{codepoint:04X};"

def generate_page_xml(symbols_page, page_num, total_pages):
    lines = []
    lines.append('<?xml version="1.0" encoding="utf-8"?>')
    lines.append(f'<!-- sym_page_{page_num:04d}.xml - Page {page_num+1}/{total_pages} -->')
    lines.append('<merge xmlns:latin="http://schemas.android.com/apk/res-auto">')
    lines.append('    <include latin:keyboardLayout="@xml/key_styles_common" />')
    lines.append('    <include latin:keyboardLayout="@xml/key_styles_currency" />')

    KEY_W = int(100 / KEYS_PER_ROW)

    lines.append(f'    <Row latin:keyWidth="{KEY_W}%p" latin:backgroundType="functional">')
    lines.append(f'        <Key latin:keySpec="&#x2261; Thorfin {page_num+1}/{total_pages}|!code/key_symbol_page" latin:keyWidth="fillRight" latin:keyLabelFlags="autoXScale" />')
    lines.append('    </Row>')

    for row_idx in range(KEYS_PER_PAGE // KEYS_PER_ROW):
        start_idx = row_idx * KEYS_PER_ROW
        end_idx = start_idx + KEYS_PER_ROW
        row_symbols = symbols_page[start_idx:end_idx]
        if not row_symbols:
            break
        lines.append(f'    <Row latin:keyWidth="{KEY_W}%p">')
        for cp in row_symbols:
            label = xml_entity(cp)
            code_hex = f"0x{cp:X}"
            lines.append(f'        <Key latin:keySpec="{label}|{code_hex}" latin:keyLabelFlags="autoScale" />')
        remaining = KEYS_PER_ROW - len(row_symbols)
        if remaining > 0:
            lines.append(f'        <Spacer latin:keyWidth="{remaining * KEY_W}%p" />')
        lines.append('    </Row>')

    lines.append(f'    <Row latin:keyWidth="{KEY_W}%p" latin:backgroundType="functional">')
    prev_enabled = page_num > 0
    next_enabled = page_num < total_pages - 1
    if prev_enabled:
        lines.append(f'        <Key latin:keySpec="&#x25C0;|!code/key_symbol_prev" latin:keyWidth="{KEY_W * 2}%p" />')
    else:
        lines.append(f'        <Key latin:keyWidth="{KEY_W * 2}%p" />')
    lines.append(f'        <Key latin:keySpec="{page_num+1}/{total_pages}|!code/key_symbol_page_info" latin:keyWidth="fillRight" latin:keyLabelFlags="autoXScale" />')
    lines.append(f'        <Key latin:keyStyle="deleteKeyStyle"')
    lines.append(f'            latin:keyXPos="{100 - KEY_W * 3}%p"')
    lines.append(f'            latin:keyWidth="{KEY_W}%p" />')
    if next_enabled:
        lines.append(f'        <Key latin:keySpec="&#x25B6;|!code/key_symbol_next" latin:keyWidth="{KEY_W * 2}%p" />')
    else:
        lines.append(f'        <Key latin:keyWidth="{KEY_W * 2}%p" />')
    lines.append('    </Row>')

    lines.append('</merge>')
    return '\n'.join(lines)

def main():
    print("[*] Collecting valid Unicode symbols...")
    symbols = collect_symbols()
    print(f"[*] Found {len(symbols)} valid symbols")

    if len(symbols) < TOTAL_KEYS_TARGET:
        print(f"[!] Only {len(symbols)} found, targeting all available")
    symbols = symbols[:TOTAL_KEYS_TARGET]

    total_pages = (len(symbols) + KEYS_PER_PAGE - 1) // KEYS_PER_PAGE
    print(f"[*] Generating {total_pages} pages ({KEYS_PER_PAGE} keys/page, {KEYS_PER_ROW} keys/row)")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for page in range(total_pages):
        start = page * KEYS_PER_PAGE
        end = start + KEYS_PER_PAGE
        page_symbols = symbols[start:end]
        xml = generate_page_xml(page_symbols, page, total_pages)
        filename = f"sym_page_{page:04d}.xml"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml)

    print(f"[*] Wrote {total_pages} page XML files to {OUTPUT_DIR}")
    print(f"[✓] Total: {len(symbols)} symbols across {total_pages} pages")

if __name__ == "__main__":
    main()
