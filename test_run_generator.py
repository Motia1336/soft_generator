import importlib.util
import sys
from pathlib import Path
p = Path(__file__).parent / 'generator.py'
try:
    spec = importlib.util.spec_from_file_location('genmod', str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    ad = getattr(m, 'ANDROID_DEVICES', None)
    io = getattr(m, 'IOS_DEVICES', None)
    print('OK')
    print('ANDROID_DEVICES:', len(ad) if ad is not None else 'missing')
    print('IOS_DEVICES:', len(io) if io is not None else 'missing')
    # list first 10 models
    if ad:
        print('Android sample:', [x[1] for x in ad[:10]])
    if io:
        print('iOS sample:', [x[1] for x in io[:10]])
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
