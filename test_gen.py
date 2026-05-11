import generator as gen
ps = gen.generate_batch(2, 'random', region=['Poland'])
for p in ps:
    print('---')
    print(gen.format_profile_text(p))
