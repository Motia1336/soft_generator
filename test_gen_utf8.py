# test_gen_utf8.py
import sys
import io
from generator import generate_batch, format_profile_text

# Force stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

profiles = generate_batch(3)
for p in profiles:
    print("-" * 30)
    print(format_profile_text(p))
