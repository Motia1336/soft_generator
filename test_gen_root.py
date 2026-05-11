# test_gen_root.py
from generator import generate_batch, format_profile_text

profiles = generate_batch(3)
for p in profiles:
    print("-" * 30)
    print(format_profile_text(p))
