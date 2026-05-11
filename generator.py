"""
generator.py - Mobile Device Profile Generator (updated)

Generates realistic Android/iOS profiles according to the
requirements described by the user:

* ОЗУ – для устройств с 12 GB или 16 GB всегда используется 8 GB. Значение 16 GB исключено.
* Android ОС: используются только версии 11–15. Устройства с макс. ОС 10 и ниже удалены.
* Гео – список всех стран Европы + стран СНГ/бывшего СССР.
* Язык системы и интерфейса – зависит от выбранного региона.
* Имя устройства – используется только модель без случайных суффиксов.
* Renderer в iOS – 60 % конкретный GPU‑модель, 40 % «Apple GPU».
* Удалены строки: «Група», «Cookie», «Платформа», «Вкладки», «MAC‑адрес»,
  а также пояснения к «Имя устройства» и «Геолокация».
"""

import random
import uuid
from datetime import datetime
import re
from pathlib import Path
from device_database import ANDROID_DEVICES, IOS_DEVICES
# ─────────────────────────────────────────────
#  DEVICE DATABASE
# ─────────────────────────────────────────────
# format: (manufacturer, model, os_version, screen_w, screen_h,
#          cores, rambase, mic, speaker, cameras, vendor, renderer)

ANDROID_MAX_OS = {
    # Samsung
    "Samsung Galaxy S10": 12, "Samsung Galaxy Note 10": 12,
    "Samsung Galaxy S20": 13, "Samsung Galaxy Note 20 Ultra": 13, "Samsung Galaxy A52": 14, "Samsung Galaxy S21": 15,
    "Samsung Galaxy Z Fold 3": 15, "Samsung Galaxy S22": 15, "Samsung Galaxy A53": 15, "Samsung Galaxy Z Flip 4": 15,
    "Samsung Galaxy S23": 15, "Samsung Galaxy A54": 15, "Samsung Galaxy Z Fold 5": 15, "Samsung Galaxy S24 Ultra": 15,
    "Samsung Galaxy A55": 15, "Samsung Galaxy Z Flip 6": 15, "Samsung Galaxy S25 Ultra": 15,
    # Pixel
    "Google Pixel 3": 12, "Google Pixel 3a": 12, "Google Pixel 4": 13, "Google Pixel 4a": 13, "Google Pixel 5": 14,
    "Google Pixel 5a": 14, "Google Pixel 6": 15, "Google Pixel 6 Pro": 15, "Google Pixel 6a": 15, "Google Pixel 7": 15,
    "Google Pixel 7 Pro": 15, "Google Pixel 7a": 15, "Google Pixel 8": 15, "Google Pixel 8 Pro": 15, "Google Pixel 8a": 15,
    "Google Pixel 9": 15, "Google Pixel 9 Pro": 15, "Google Pixel 9 Pro Fold": 15, "Google Pixel 9a": 15, "Google Pixel Fold": 15,
    # Xiaomi
    "Xiaomi Mi 9": 11, "Xiaomi Redmi Note 8 Pro": 11, "Xiaomi Mi 10": 13,
    "Xiaomi Redmi Note 10 Pro": 13, "Xiaomi Mi 11": 14, "Xiaomi 11T Pro": 14, "Xiaomi Redmi Note 11 Pro": 13,
    "Xiaomi 12": 15, "Xiaomi Redmi Note 12 Pro": 15, "Xiaomi 13": 15, "Xiaomi Redmi Note 13 Pro": 15,
    "Xiaomi 14": 15, "Xiaomi 14 Ultra": 15, "Xiaomi Redmi Note 14 Pro": 15, "Xiaomi 15": 15,
    "Xiaomi 15 Pro": 15, "Xiaomi Redmi Note 15 Pro": 15,
    # Poco
    "Poco F2 Pro": 12, "Poco X3 NFC": 12, "Poco M3": 12, "Poco F3": 13,
    "Poco X3 Pro": 13, "Poco M4 Pro": 13, "Poco F4": 14, "Poco X4 Pro 5G": 13,
    "Poco M5": 14, "Poco F5": 15, "Poco X5 Pro": 14, "Poco M6 Pro": 15, "Poco F6": 15,
    "Poco X6 Pro": 15, "Poco M7 Pro": 15, "Poco F7": 15, "Poco X7 Pro": 15,
    # Realme
    "Realme 3 Pro": 11, "Realme X2 Pro": 11, "Realme 6 Pro": 11,
    "Realme 7 Pro": 12, "Realme 8 Pro": 13, "Realme GT 5G": 13, "Realme 9 Pro+": 14,
    "Realme GT Neo 3": 14, "Realme 10 Pro+": 15, "Realme GT3": 15, "Realme 11 Pro+": 15,
    "Realme GT5": 15, "Realme 12 Pro+": 15, "Realme GT5 Pro": 15, "Realme 13 Pro+": 15,
    "Realme GT6": 15, "Realme 14 Pro+": 15,
    # Oppo
    "Oppo Reno 2": 11, "Oppo Find X2 Pro": 13, "Oppo Reno 4 Pro": 12, "Oppo Find X3 Pro": 14,
    "Oppo Reno 6 Pro": 13, "Oppo Find X5 Pro": 15, "Oppo Reno 8 Pro": 14, "Oppo Find N2 Flip": 15,
    "Oppo Find X6 Pro": 15, "Oppo Reno 10 Pro": 15, "Oppo Find N3": 15, "Oppo Find X7 Ultra": 15,
    "Oppo Reno 11 Pro": 15, "Oppo Find X8 Ultra": 15, "Oppo Reno 12 Pro": 15, "Oppo Find N4 Flip": 15,
    "Oppo Reno 13 Pro": 15,
    # Vivo
    "Vivo V15 Pro": 11, "Vivo X50 Pro": 12, "Vivo V20": 13, "Vivo X60 Pro": 13, "Vivo V21": 13,
    "Vivo X70 Pro": 14, "Vivo V23": 14, "Vivo X80 Pro": 15, "Vivo V25": 14, "Vivo X90 Pro": 15, "Vivo V27": 15,
    "Vivo X100 Pro": 15, "Vivo V29": 15, "Vivo X Fold 3": 15, "Vivo X200 Pro": 15, "Vivo V30": 15, "Vivo X Fold 4": 15,
    # OnePlus
    "OnePlus 6": 11, "OnePlus 6T": 11, "OnePlus 7 Pro": 12, "OnePlus 7T": 12,
    "OnePlus 8 Pro": 13, "OnePlus Nord": 12, "OnePlus 8T": 14, "OnePlus 9 Pro": 14,
    "OnePlus Nord 2": 13, "OnePlus 10 Pro": 15, "OnePlus 10T": 15, "OnePlus Nord 3": 15,
    "OnePlus 11": 15, "OnePlus Open": 15, "OnePlus 12": 15, "OnePlus Nord 4": 15,
    "OnePlus Open 2": 15, "OnePlus 13": 15, "OnePlus Nord 5": 15,
    # Tecno
    "Tecno Camon 15": 11, "Tecno Pouvoir 4": 11, "Tecno Camon 17 Pro": 12,
    "Tecno Phantom X": 12, "Tecno Spark 8 Pro": 12, "Tecno Camon 18 Premier": 12, "Tecno Pova 3": 13,
    "Tecno Camon 19 Pro": 13, "Tecno Phantom X2 Pro": 14, "Tecno Spark 10 Pro": 14, "Tecno Camon 20 Premier": 15,
    "Tecno Phantom V Fold": 15, "Tecno Pova 5 Pro": 14, "Tecno Camon 30 Premier": 15, "Tecno Phantom V Flip": 15,
    "Tecno Spark 20 Pro": 15,
    # Infinix
    "Infinix Note 7": 11, "Infinix Zero 8": 11, "Infinix Note 10 Pro": 12,
    "Infinix Zero X Pro": 12, "Infinix Hot 11": 12, "Infinix Note 12 VIP": 13, "Infinix Zero Ultra": 13, "Infinix Hot 20": 13,
    "Infinix Note 30 VIP": 15, "Infinix Zero 30 5G": 15, "Infinix GT 10 Pro": 14, "Infinix Hot 40 Pro": 14,
    "Infinix Note 40 Pro+": 15, "Infinix GT 20 Pro": 15, "Infinix Zero 40": 15, "Infinix Note 50 Pro+": 15,
    "Infinix GT 30 Pro": 15,
    # Honor
    "Honor 30 Pro": 11, "Honor 50": 13,
    "Honor 60 Pro": 13, "Honor Magic 4 Pro": 14, "Honor 70": 14, "Honor 80 Pro": 14,
    "Honor Magic 5 Pro": 15, "Honor 90": 15, "Honor Magic V2": 15, "Honor 100 Pro": 15,
    "Honor Magic 6 Pro": 15, "Honor 200 Pro": 15, "Honor Magic V3": 15, "Honor Magic 7 Pro": 15,
    "Honor 300 Pro": 15,
    # Motorola
    "Motorola Razr (2019)": 11, "Motorola Edge+ (2020)": 12,
    "Motorola Moto G100": 12, "Motorola Edge 20 Pro": 13, "Motorola Edge 30 Pro": 14, "Motorola Razr 2022": 14,
    "Motorola Edge 40 Pro": 15, "Motorola Razr 40 Ultra": 15, "Motorola Moto G84": 14, "Motorola Edge 50 Pro": 15,
    "Motorola Razr 50 Ultra": 15, "Motorola ThinkPhone": 15, "Motorola Moto G Stylus 5G (2024)": 15,
    "Motorola Moto G Power 5G (2024)": 15, "Motorola Edge 60 Pro": 15, "Motorola Razr 60 Ultra": 15,
    "Motorola Moto G85": 15,
    # Asus
    "Asus Zenfone 6": 11, "Asus ROG Phone II": 11,
    "Asus Zenfone 7 Pro": 12, "Asus ROG Phone 3": 12, "Asus Zenfone 8": 13, "Asus ROG Phone 5": 13,
    "Asus Zenfone 9": 14, "Asus ROG Phone 6": 14, "Asus Zenfone 10": 15, "Asus ROG Phone 7": 15,
    "Asus Zenfone 11 Ultra": 14, "Asus ROG Phone 8 Pro": 14, "Asus ROG Phone 8": 14,
    "Asus Zenfone 12 Ultra": 15, "Asus ROG Phone 9": 15, "Asus ROG Phone 9 Pro": 15,
    # Sony
    "Sony Xperia 1": 11, "Sony Xperia 5": 11,
    "Sony Xperia 1 II": 12, "Sony Xperia 5 II": 12, "Sony Xperia 10 II": 12, "Sony Xperia 1 III": 13,
    "Sony Xperia 5 III": 13, "Sony Xperia 10 III": 13, "Sony Xperia PRO-I": 13, "Sony Xperia 1 IV": 14,
    "Sony Xperia 5 IV": 14, "Sony Xperia 10 IV": 14, "Sony Xperia 1 V": 15, "Sony Xperia 5 V": 15,
    "Sony Xperia 10 V": 15, "Sony Xperia 1 VI": 15, "Sony Xperia 5 VI": 15, "Sony Xperia 1 VII": 15,
}

from device_database import ANDROID_DEVICES, IOS_DEVICES

# Filter ANDROID_DEVICES to only include those that support Android 11 or higher
ANDROID_DEVICES = [dev for dev in ANDROID_DEVICES if ANDROID_MAX_OS.get(dev[1], 0) >= 11]

def _get_random_os_version(launch_os: str, platform: str, model_name: str = None) -> str:
    """Выбирает версию ОС не ниже версии выхода устройства.
    """
    l_os = int(float(launch_os))
    if platform == "Android":
        max_os = ANDROID_MAX_OS.get(model_name, 15) if model_name else 15
        # Актуальные версии Android: 11, 12, 13, 14, 15
        android_versions = [v for v in [11, 12, 13, 14, 15] if l_os <= v <= max_os]
        if android_versions:
            return str(random.choice(android_versions))
        else:
            # If no version in range, but device supports 11 or more (checked by filter), 
            # we must return 11 at least.
            return "11"
    else:  # iOS
        # handled by _get_random_ios_version
        return str(l_os)


def _random_android_ua(os_ver: str, sb_version: int) -> str:
    """Создает UA для Android (маскированный под Android 10 и устройство K)."""
    if random.choice([True, False]):
        chrome_ver = f"{sb_version}.0.0.0"
    else:
        v2 = random.randint(0, 9999)
        v3 = random.randint(0, 200)
        chrome_ver = f"{sb_version}.0.{v2}.{v3}"
    # Гугл начал скрывать реальные данные: в UA всегда Android 10 и модель K
    return (f"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
            f"(KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36")





# ─────────────────────────────────────────────
#  FONTS DATABASE
# ─────────────────────────────────────────────
_POOL_IOS = [
    "SF Pro", "SF Pro Text", "SF Mono", "Apple Color Emoji", "Academy Engraved LET", "American Typewriter", 
    "Apple SD Gothic Neo", "Arial", "Avenir", "Baskerville", "Bodoni 72", "Charter", "Copperplate", "Courier New", 
    "Georgia", "Helvetica", "Helvetica Neue", "Menlo", "Palatino", "Times New Roman", "Avenir Next", "Bradley Hand", 
    "Chalkboard SE", "Cochin", "Didot", "Futura", "Gill Sans", "Hoefler Text", "Iowan Old Style", "Marker Felt", 
    "Noteworthy", "Optima", "Papyrus", "Savoye LET", "Snell Roundhand", "Trebuchet MS", "Verdana", "Zapfino", 
    "PingFang SC", "Hiragino Kaku Gothic ProN", "Geeza Pro", "Thonburi", "Kohinoor Bangla", "Kohinoor Devanagari"
]

_POOL_SAMSUNG = [
    "SamsungOne", "One UI Sans", "Samsung Sans", "Rosemary", "Choco Cooky", "Cool Jazz", "Roboto", "Noto Sans", 
    "Noto Serif", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Samsung Korean", "Samsung Chinese", "Samsung Arabic", 
    "Samsung Thai", "Samsung Hebrew", "Samsung Greek", "Samsung Cyrillic", "Samsung Latin", "Harmonious Sans", 
    "Noto Color Emoji", "Roboto Mono", "Roboto Flex", "Roboto Serif", "Samsung Sharp Sans", "Samsung Inter", 
    "Samsung Neo", "Samsung SimHei", "Samsung Meiryo", "Arial", "Helvetica", "Verdana", "Georgia", "Times New Roman",
    "Noto Sans CJK", "Noto Sans Arabic", "Noto Sans Thai", "Noto Sans Devanagari", "Noto Sans Georgian", 
    "Noto Sans Armenian", "Noto Sans Ethiopic", "Noto Sans Khmer", "Noto Sans Lao"
]

_POOL_XIAOMI = [
    "Mi Sans", "MiLan Pro", "Mi Lanting", "Roboto", "Noto Sans", "Noto Serif", "Droid Sans", "Droid Serif", 
    "Droid Sans Mono", "Mi Sans Latin", "Mi Sans Arabic", "Mi Sans Hebrew", "Mi Sans Thai", "Mi Sans Cyrillic", 
    "Mi Sans Indic", "Xiaomi Sans", "Lantinghei", "Noto Color Emoji", "Roboto Mono", "Roboto Flex", "Xiaomi Inter", 
    "Mi Pro", "Mi Thai", "Mi Arabic", "Arial", "Helvetica", "Verdana", "Georgia", "Times New Roman", "Mi Lanting Pro",
    "Noto Sans CJK", "Noto Sans Armenian", "Noto Sans Georgian", "Noto Sans Devanagari", "Noto Sans Ethiopic",
    "Mi Sans Chinese", "Mi Sans Japanese", "Mi Sans Korean", "Mi Sans Global", "Mi Sans VF"
]

_POOL_PIXEL = [
    "Google Sans", "Google Sans Text", "Google Sans Medium", "Google Sans Bold", "Roboto", "Roboto Mono", 
    "Roboto Flex", "Roboto Serif", "Noto Sans", "Noto Serif", "Droid Sans", "Droid Serif", "Droid Sans Mono", 
    "Noto Color Emoji", "Noto Sans Symbols", "Google Sans Mono", "Google Sans Display", "Noto Sans CJK", 
    "Noto Sans Armenian", "Noto Sans Georgian", "Google Sans Serif", "Google Sans Narrow", "Arial", "Helvetica", 
    "Verdana", "Georgia", "Times New Roman", "Noto Sans Arabic", "Noto Sans Hebrew", "Noto Sans Thai", 
    "Noto Sans Devanagari", "Noto Sans Ethiopic", "Noto Sans Khmer", "Noto Sans Lao", "Noto Sans Myanmar",
    "Noto Sans Sinhala", "Noto Sans Tamil", "Noto Sans Telugu", "Noto Sans Malayalam", "Noto Sans Kannada"
]

_POOL_ANDROID_GENERIC = [
    "Roboto", "Noto Sans", "Noto Serif", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Noto Color Emoji", 
    "Roboto Mono", "Roboto Flex", "Noto Sans Symbols", "Noto Sans Arabic", "Noto Sans Hebrew", "Noto Sans Thai", 
    "Noto Sans Cyrillic", "Noto Sans Indic", "Noto Sans CJK", "Noto Sans Armenian", "Noto Sans Georgian", 
    "Noto Sans Devanagari", "Noto Sans Ethiopic", "Arial", "Helvetica", "Verdana", "Georgia", "Times New Roman",
    "Noto Sans Khmer", "Noto Sans Lao", "Noto Sans Myanmar", "Noto Sans Sinhala", "Noto Sans Tamil", "Noto Sans Telugu",
    "Noto Sans Malayalam", "Noto Sans Kannada", "Noto Sans Bengali", "Noto Sans Gujarati", "Noto Sans Gurmukhi",
    "Noto Sans Oriya", "Noto Sans Tibetan", "Noto Sans Thaana", "Noto Sans Tifinagh"
]

def _get_device_fonts(platform: str, model_name: str) -> str:
    """Return a randomized comma-separated list of fonts (20-40) based on device brand."""
    if platform == "iOS":
        pool = _POOL_IOS
    else:
        model_lower = model_name.lower()
        if "samsung" in model_lower:
            pool = _POOL_SAMSUNG
        elif "xiaomi" in model_lower or "redmi" in model_lower:
            pool = _POOL_XIAOMI
        elif "pixel" in model_lower:
            pool = _POOL_PIXEL
        else:
            pool = _POOL_ANDROID_GENERIC
    
    # Pick random count between 20 and 40 (clamped to pool size)
    count = random.randint(20, 40)
    count = min(count, len(pool))
    
    # Sample unique fonts from the pool
    selected = random.sample(pool, count)
    return ", ".join(selected)

# ─────────────────────────────────────────────
#  LANGUAGE & LOCALES
# ─────────────────────────────────────────────
UA_LANGS = [("uk", "Українська"), ("ru", "Русский")]
EXTRA_LANGS = ["en-GB", "pl", "fr"]

# Minimal mapping country -> primary language code + display name
COUNTRY_LANG = {
    # CIS / former USSR
    "Armenia": ("hy", "Հայերեն"),
    "Azerbaijan": ("az", "Azərbaycanca"),
    "Belarus": ("ru", "Русский"),
    "Kazakhstan": ("kk", "Қазақша"),
    "Kyrgyzstan": ("ky", "Кыргызча"),
    "Moldova": ("ro", "Română"),
    "Russia": ("ru", "Русский"),
    "Tajikistan": ("tg", "Тоҷикӣ"),
    "Turkmenistan": ("tk", "Türkmen"),
    "Uzbekistan": ("uz", "Oʻzbekcha"),
    "Ukraine": ("uk", "Українська"),

    # Common European
    "Poland": ("pl", "Polski"),
    "Germany": ("de", "Deutsch"),
    "France": ("fr", "Français"),
    "Spain": ("es", "Español"),
    "Italy": ("it", "Italiano"),
    "Netherlands": ("nl", "Nederlands"),
    "Portugal": ("pt", "Português"),
    "Romania": ("ro", "Română"),
    "Czech Republic": ("cs", "Čeština"),
    "Sweden": ("sv", "Svenska"),
    "Belgium": ("nl", "Nederlands"),
    "Ireland": ("en-GB", "English (UK)"),
    "United Kingdom": ("en-GB", "English (UK)"),
}

# ─────────────────────────────────────────────
#  GEO‑LIST (Europe + СНГ/Бывший СССР)
# ─────────────────────────────────────────────
EUROPE_COUNTRIES = [
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina",
    "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia",
    "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland",
    "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg",
    "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia",
    "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia",
    "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine",
    "United Kingdom", "Vatican City"
]

CIS_COUNTRIES = [
    "Armenia", "Azerbaijan", "Belarus", "Kazakhstan", "Kyrgyzstan",
    "Moldova", "Russia", "Tajikistan", "Turkmenistan", "Uzbekistan", "Ukraine"
]

ALL_GEO = list(sorted(set(EUROPE_COUNTRIES + CIS_COUNTRIES)))

def pick_geo(allowed: list | None = None) -> str:
    """Return a random country.

    If `allowed` is None, pick from ALL_GEO.
    If `allowed` is a list, pick from that list.
    If `allowed` is a single-string list with one country, return it.
    """
    if allowed is None:
        pool = ALL_GEO
    else:
        pool = allowed if isinstance(allowed, list) else [allowed]
    return random.choice(pool)

# ─────────────────────────────────────────────
#  RAM ADJUSTMENT (12 GB special case)
# ─────────────────────────────────────────────
def _fix_ram(actual_ram: int) -> int:
    """
    Adjust RAM to a value supported by AdsPower.

    * Supported sizes: 2, 4, 6, 8, 32 GB.
    * If the device reports 12 GB or 16 GB, we always use 8 GB.
    * Values < 2 GB are clamped to 2 GB; > 32 GB to 32 GB.
    * For any other unsupported size we pick the nearest supported step.
    """
    valid = [2, 4, 6, 8, 32]
    if actual_ram in valid:
        return actual_ram
    if actual_ram == 12 or actual_ram == 16:
        return 8
    if actual_ram < 2:
        return 2
    if actual_ram > 32:
        return 32
    return min(valid, key=lambda x: abs(x - actual_ram))

# ─────────────────────────────────────────────
#  LANGUAGES LOGIC
# ─────────────────────────────────────────────
def _rand_lang(country: str, allowed: list | None = None) -> tuple[str, str]:
    """Return tuple (langs_csv, interface_language_name) for given country.

    Rules implemented:
    - `en-GB` is present in 100% of profiles.
    - Country primary language is always present.
    - CIS (except Ukraine): `ru` is always present and is system language in ~90%.
    - Kazakhstan: include `kk` + `ru` + `en-GB`; system: 60% ru, 35% kk, 5% en-GB.
    - Ukraine: `uk` always present; `ru` present in 60% profiles; system: if ru present -> 50% ru,45% uk,5% en; if ru absent -> uk primary.
    - For Europe/other countries: system language probabilities: 60% country_lang, 35% ru, 5% en-GB.
    - When country_lang == 'ru' we may produce 2 languages (ru + en-GB).
    - System/interface language is the first language in the returned CSV.
    """
    # determine country primary language
    country_lang_code, country_lang_name = COUNTRY_LANG.get(country, ("en-GB", "English (UK)"))

    # classify country
    if country == "Kazakhstan":
        group = "KZ"
    elif country == "Ukraine":
        group = "UA"
    elif country in CIS_COUNTRIES:
        group = "CIS"
    else:
        group = "EU"

    def pick_system(prob_map: list[tuple[str, float]]) -> str:
        r = random.random()
        acc = 0.0
        for code, p in prob_map:
            acc += p
            if r < acc:
                return code
        return prob_map[-1][0]

    # Determine whether ru appears (special UA rule)
    ru_present = False
    if allowed is not None:
        # If allowed explicitly provided, control ru presence by allowed set
        ru_present = "ru" in allowed
    else:
        if group == "CIS":
            ru_present = True
        elif group == "KZ":
            ru_present = True
        elif group == "UA":
            ru_present = random.random() < 0.60
        else:
            # Europe: ru may appear as additional language with some chance
            ru_present = random.random() < 0.35

    # Determine system language (primary)
    if group == "CIS":
        sys_code = pick_system([("ru", 0.90), (country_lang_code, 0.09), ("en-GB", 0.01)])
    elif group == "KZ":
        sys_code = pick_system([("ru", 0.60), ("kk", 0.35), ("en-GB", 0.05)])
    elif group == "UA":
        if ru_present:
            sys_code = pick_system([("ru", 0.50), ("uk", 0.45), ("en-GB", 0.05)])
        else:
            sys_code = pick_system([("uk", 0.95), ("en-GB", 0.05)])
    else:  # EU / others
        sys_code = pick_system([(country_lang_code, 0.60), ("ru", 0.35), ("en-GB", 0.05)])

    # Build languages list ensuring en-GB and country_lang presence
    langs = []
    # If user provided allowed languages, start from that set but ensure country/en presence
    if allowed is not None:
        # preserve order: system first if in allowed
        if sys_code in allowed:
            langs.append(sys_code)
        # ensure country language included if allowed contains it (or if allowed uses literal country code)
        if country_lang_code in allowed and country_lang_code not in langs:
            langs.append(country_lang_code)
        # include ru if allowed
        if "ru" in allowed and "ru" not in langs:
            langs.append("ru")
        # include en-GB if allowed
        if "en-GB" in allowed and "en-GB" not in langs:
            langs.append("en-GB")
        # include any other allowed languages
        for a in allowed:
            if a not in langs:
                langs.append(a)
    else:
        # primary first
        langs.append(sys_code)
        # ensure country language present
        if country_lang_code not in langs:
            langs.append(country_lang_code)
        # ensure ru present when needed
        if ru_present and "ru" not in langs:
            langs.append("ru")
        # always include en-GB
        if "en-GB" not in langs:
            langs.append("en-GB")

    # normalize order: primary already first; truncate or fill to desired size
    # desired: 3 languages generally, but if country_lang == 'ru' allow 2
    desired = 3
    if country_lang_code == "ru":
        desired = 2

    # fill extras if needed (only when allowed not provided)
    if allowed is None:
        extras_pool = [c for c in EXTRA_LANGS if c not in langs]
        while len(langs) < desired and extras_pool:
            langs.append(extras_pool.pop(0))

    # if longer than desired, keep first `desired` and ensure en-GB remains present
    if len(langs) > desired:
        # keep primary and en-GB and then the next ones up to desired
        primary = langs[0]
        rest = [x for x in langs[1:] if x != primary]
        # ensure en-GB in rest
        if "en-GB" in rest:
            rest.remove("en-GB")
            rest.insert(0, "en-GB")
        langs = [primary] + rest[: max(0, desired - 1)]

    # interface language display name
    lang_name_map = {"ru": "Русский", "uk": "Українська", "kk": "Қазақша", "en-GB": "English (UK)",
                     "pl": "Polski", "fr": "Français", "de": "Deutsch", "es": "Español", "it": "Italiano"}
    intf_name = lang_name_map.get(langs[0], COUNTRY_LANG.get(country, (None, country_lang_name))[1])

    return ", ".join(langs), intf_name

# ─────────────────────────────────────────────
#  USER‑AGENT BUILDERS
# ─────────────────────────────────────────────
SUNBROWSER_VERSIONS = [144, 145, 146, 147]


def _random_ios_ua(ios_base_version: str, sb_version: int) -> tuple[str, str]:
    """Create a random iOS UA string and the sub‑version part."""
    safari_ver = f"{random.randint(604, 605)}.{random.randint(1, 2)}"
    wk_ver = "605.1.15"
    ua_type = random.choice(["Safari", "CriOS", "GSA"])
    sub_ver = f"{ios_base_version}_{random.randint(1, 7)}"
    if ua_type == "Safari":
        dot_ver = sub_ver.replace("_", ".")
        ua = (f"Mozilla/5.0 (iPhone; CPU iPhone OS {sub_ver} like Mac OS X) "
              f"AppleWebKit/{wk_ver} (KHTML, like Gecko) "
              f"Version/{dot_ver} Mobile/15E148 Safari/{safari_ver}")
    elif ua_type == "CriOS":
        if random.choice([True, False]):
            chrome_ver = f"{sb_version}.0.0.0"
        else:
            v2 = random.randint(0, 9999)
            v3 = random.randint(0, 200)
            chrome_ver = f"{sb_version}.0.{v2}.{v3}"
        ua = (f"Mozilla/5.0 (iPhone; CPU iPhone OS {sub_ver} like Mac OS X) "
              f"AppleWebKit/{wk_ver} (KHTML, like Gecko) "
              f"CriOS/{chrome_ver} Mobile/15E148 Safari/{safari_ver}")
    else:  # GSA
        sub_ver = f"{ios_base_version}_{random.randint(1, 4)}_{random.randint(0, 5)}"
        gsa_major = random.randint(380, 420)
        gsa_minor = random.randint(1, 9)
        gsa_patch = random.randint(100_000_000, 999_999_999)
        gsa_ver = f"{gsa_major}.{gsa_minor}.{gsa_patch}"
        ua = (f"Mozilla/5.0 (iPhone; CPU iPhone OS {sub_ver} like Mac OS X) "
              f"AppleWebKit/{wk_ver} (KHTML, like Gecko) "
              f"GSA/{gsa_ver} Mobile/15E148 Safari/{safari_ver}")
    return ua, sub_ver


# -------------------------------------------------------------------
# iOS version handling – realistic max OS per model
# -------------------------------------------------------------------
# Mapping of iPhone model name -> maximum iOS version that ever received.
# Values are based on real‑world update history up to 2026.
# For models that never received updates beyond launch, we keep the launch version.
IOS_MAX_OS = {
    "iPhone XR": 18,
    "iPhone XS": 18,
    "iPhone XS Max": 18,
    "iPhone 11": 26,
    "iPhone 11 Pro": 26,
    "iPhone 11 Pro Max": 26,
    "iPhone SE (2nd gen)": 26,
    "iPhone 12 mini": 26,
    "iPhone 12": 26,
    "iPhone 12 Pro": 26,
    "iPhone 12 Pro Max": 26,
    "iPhone 13 mini": 26,
    "iPhone 13": 26,
    "iPhone 13 Pro": 26,
    "iPhone 13 Pro Max": 26,
    "iPhone SE (3rd gen)": 26,
    "iPhone 14": 26,
    "iPhone 14 Plus": 26,
    "iPhone 14 Pro": 26,
    "iPhone 14 Pro Max": 26,
    "iPhone 15": 26,
    "iPhone 15 Plus": 26,
    "iPhone 15 Pro": 26,
    "iPhone 15 Pro Max": 26,
    "iPhone 16": 26,
    "iPhone 16 Plus": 26,
    "iPhone 16 Pro": 26,
    "iPhone 16 Pro Max": 26,
    "iPhone 17": 26,
    "iPhone 17 Air": 26,
    "iPhone 17 Pro": 26,
    "iPhone 17 Pro Max": 26,
}

def _get_random_ios_version(model_name: str, launch_os: str) -> str:
    """Return a random iOS version for *model_name*.
    - Cannot be lower than the launch OS.
    - Cannot exceed the maximum OS the device ever received (IOS_MAX_OS).
    - Skip non-existent versions 19-25 (Apple skipped them).
    - Occasionally a sub‑version like ``26_2`` is added for realism.
    """
    launch = int(launch_os)
    max_os = IOS_MAX_OS.get(model_name, launch)
    if max_os < launch:
        max_os = launch
    
    # Собираем список всех версий от launch до max_os
    all_possible = list(range(launch, max_os + 1))
    
    # Фильтруем: исключаем 19, 20, 21, 22, 23, 24, 25
    # Оставляем только те, что <= 18 или >= 26
    valid_versions = [v for v in all_possible if v <= 18 or v >= 26]
    
    if not valid_versions:
        return str(launch)
        
    chosen = random.choice(valid_versions)
    
    # Добавляем суб-версию для 26 (например, 26_3) для реализма
    if chosen == 26 and random.random() < 0.3:
        return f"{chosen}_{random.randint(1,5)}"
    return str(chosen)

# -------------------------------------------------------------------
def generate_profile(platform: str = "random", custom_ua: str = None, region: list | None = None, languages_allowed: list | None = None) -> dict:
    """Generate a single device profile."""
    if platform == "random":
        platform = random.choice(["Android", "iOS"])
    sb_version = random.choice(SUNBROWSER_VERSIONS)
    font_range = random.randint(20, 400)
    # region can be None, a single country string, or a list of allowed countries
    region = pick_geo(region)
    # if languages_allowed provided, pass to _rand_lang
    lang_str, intf_lang = _rand_lang(region, allowed=languages_allowed)
    profile = {
        "id":           str(uuid.uuid4()),
        "platform":     platform,
        "browser_ver":  str(sb_version),
        "timezone":     "на основе IP",
        "geo":          region,
        "lang":         lang_str,
        "intf_lang":    intf_lang,
        "created_at":   datetime.now().isoformat(timespec='seconds'),
    }
    if platform == "Android":
        dev = random.choice(ANDROID_DEVICES)
        launch_os = dev[2]
        actual_os = _get_random_os_version(launch_os, "Android", model_name=dev[1])
        
        profile["model"]       = dev[1]
        profile["os_version"] = actual_os
        profile["screen"]     = f"{dev[3]}x{dev[4]}"
        # 30% – «на основе User-Agent», 70% – реальное разрешение экрана
        profile["screen_extension"] = f"{dev[3]}x{dev[4]}" if random.random() < 0.7 else "на основе User-Agent"
        profile["cpu"]        = dev[5]
        profile["ram"]        = _fix_ram(dev[6])
        profile["fonts"]      = _get_device_fonts("Android", dev[1])
        profile["mic"]        = dev[7]
        profile["speaker"]    = dev[8]
        profile["cams"]       = dev[9]
        profile["vendor"]     = dev[10]
        profile["renderer"]   = dev[11]
        profile["device_name"] = dev[1]
        profile["user_agent"] = custom_ua if custom_ua else _random_android_ua(actual_os, sb_version)
        profile["os_display"] = f"Android {actual_os}"
        profile["hw_accel"]   = "Включить"
    else:  # iOS
        dev = random.choice(IOS_DEVICES)
        launch_os = dev[2]
        actual_os = _get_random_ios_version(dev[1], launch_os)
        
        profile["model"]       = dev[1]
        profile["os_version"] = actual_os
        profile["screen_extension"] = f"{dev[3]}x{dev[4]}" if random.random() < 0.7 else "на основе User-Agent"
        profile["cpu"]        = dev[5]
        profile["ram"]        = _fix_ram(dev[6])
        profile["fonts"]      = _get_device_fonts("iOS", dev[1])
        profile["mic"]        = dev[7]
        profile["speaker"]    = dev[8]
        profile["cams"]       = dev[9]
        profile["vendor"]     = dev[10]
        profile["renderer"]   = dev[11] if random.random() < 0.60 else "Apple GPU"
        profile["device_name"] = dev[1]
        if custom_ua:
            profile["user_agent"] = custom_ua
        else:
            ua, _ = _random_ios_ua(actual_os, sb_version)
            profile["user_agent"] = ua
        profile["os_display"] = f"Ios {actual_os}"
        profile["hw_accel"]   = "Включить"
    return profile

def generate_batch(count: int, platform: str = "random", region: list | None = None, languages_allowed: list | None = None) -> list[dict]:
    """Generate `count` unique profiles."""
    names_used = set()
    results = []
    for _ in range(count):
        max_retries = 10
        for _ in range(max_retries):
            p = generate_profile(platform, region=region, languages_allowed=languages_allowed)
            if p["device_name"] not in names_used:
                names_used.add(p["device_name"])
                results.append(p)
                break
        else:
            p = generate_profile(platform, region=region, languages_allowed=languages_allowed)
            p["device_name"] += f"_{random.randint(1000, 9999)}"
            results.append(p)
    return results

# ─────────────────────────────────────────────
#  TEXT FORMATTER
# ─────────────────────────────────────────────
def format_profile_text(p: dict) -> str:
    """Render a profile to the exact text format required by SunBrowser.
    All previously‑mentioned “do not touch” sections are removed.
    """
    return f"""Имя: {p['model']} (указать марку телефона, если профиль для клика‑ничего дальше не указывать, если профиль для регистрации или депозита указать регион который выбивается в прокси, почту на которую регистрировался аккаунт и пароль, также указать дату и время создания профиля.)
Браузер: SunBrowser {p['browser_ver']}
Система: {p['os_display']}
User-Agent: {p['user_agent']}
WebRTC: подмена
Часовой пояс: {p['timezone']}
Геолокация: на основе IP
Язык: {p['lang']} (интерфейс {p['intf_lang']})
Язык интерфейса: {p['intf_lang']}
Разрешение экрана: {p['screen_extension']}
Шрифты: {p['fonts']}
Canvas: вкл
WebGL Image: вкл
Audiocontext: вкл
Медиа‑Устройства: Микрофон: {p['mic']}, Динамик: {p['speaker']}, Камеры: {p['cams']} (нажать изменить, убрать галочку автоматически и написать нужное количество)
ClientRects: вкл
SpeechVoices: вкл
WebGL метаданные: настроить, вендор: {p['vendor']}, рендер: {p['renderer']}
WebGPU: На основе WebGL
CPU: {p['cpu']}
RAM: {p['ram']} GB
Имя устройства: {p['device_name']}
Do Not Track: Выключить
Защита от сканирования портов: Включить
Аппаратное ускорение: {p['hw_accel']}
Отключить функции TLS: Выключить

"""
if __name__ == "__main__":
    ios = generate_profile("iOS")
    android = generate_profile("Android")
    print("=== iOS PROFILE ===")
    print(format_profile_text(ios))
    print("\n=== Android PROFILE ===")
    print(format_profile_text(android))
