from crypto_tools import b64_hex, print_byte_as_hex, xor_fl

# challenge 1:
print('challenge 1: print base64 of a hex string')
hb = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
print(b64_hex(bytes.fromhex(hb)))

# challenge 2:
print('challenge 2: print xor of two strings in hex string')
s1 = '1c0111001f010100061a024b53535009181c'
s2 = '686974207468652062756c6c277320657965'
print_byte_as_hex((xor_fl(bytes.fromhex(s1), bytes.fromhex(s2))))

#challenge 3:
print('challenge 3: print xor of single character key')
s1 = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
iv = 0x61
for i in range (0,25):
    iv += 1
    s2 = str(hex(iv)).split('x')[1]*int((len(s1)/2))
    out = xor_fl(bytes.fromhex(s1), bytes.fromhex(s2))
    if iv == 0x78:
        print_byte_as_hex(out)
        print(out.decode('ascii'))

iv = 0x41
for i in range (0,25):
    iv += 1
    s2 = str(hex(iv)).split('x')[1]*int((len(s1)/2))
    out = xor_fl(bytes.fromhex(s1), bytes.fromhex(s2))
    if iv == 0x58:
        print_byte_as_hex(out)
        print(out.decode('ascii'))

