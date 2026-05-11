# test_fonts_brands.py
import sys
import io
from generator import generate_profile, format_profile_text

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

brands = ["Samsung Galaxy S24 Ultra", "Xiaomi 14", "Google Pixel 8 Pro", "iPhone 15 Pro Max"]
for brand in brands:
    # We can't force generate_profile to pick a specific model easily without modifying it,
    # but we can mock the model data if we wanted. 
    # Let's just generate a batch and find them, or just call _get_device_fonts directly for demonstration.
    from generator import _get_device_fonts
    platform = "iOS" if "iPhone" in brand else "Android"
    fonts = _get_device_fonts(platform, brand)
    print(f"--- {brand} ---")
    print(f"Fonts: {fonts}\n")
