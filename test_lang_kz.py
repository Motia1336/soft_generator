import generator as gen
ps = gen.generate_batch(5, 'random', region=['Kazakhstan'], languages_allowed=['en-GB','ru','kk'])
for p in ps:
    print('---')
    print('Langs:', p['lang'], 'Interface:', p['intf_lang'])
    print(p['user_agent'])
