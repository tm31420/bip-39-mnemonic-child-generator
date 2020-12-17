import pprint
import binascii
import mnemonic
import bip32utils

arq1 = open('WIFs.txt', 'w')
arq2 = open('addr.txt', 'w')
def bip39(mnemonic_words, children):
    '''
    mnemonic_words: 12 word mnemonic.
    children: positive integer for num of address desired.
    FUTURE IMPLEMENT...
    - choose coin
    - return main account information
    '''
    mobj = mnemonic.Mnemonic("english")
    seed = mobj.to_seed(mnemonic_words)
    holder = {}
    if children < 0:
        raise ValueError('Children must be positive.')
    for child in range(children):
        bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
        bip32_child_key_obj = bip32_root_key_obj.ChildKey(
            44 + bip32utils.BIP32_HARDEN
        ).ChildKey(
            0 + bip32utils.BIP32_HARDEN
        ).ChildKey(
            0 + bip32utils.BIP32_HARDEN
        ).ChildKey(0).ChildKey(child)
        template = {
            'mnemonic_words': mnemonic_words,
            'bip32_root_key': bip32_root_key_obj.ExtendedKey(),
            'bip32_extended_private_key': bip32_child_key_obj.ExtendedKey(),
            'path': f"m/44'/0'/0'/{child}",
            'address': bip32_child_key_obj.Address(),
            'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
            'privatekey': bip32_child_key_obj.WalletImportFormat(),
            'coin': 'BTC'
        }
        holder[f'Child_{child}'] = template
        arq1.write("%s \n" % bip32_child_key_obj.WalletImportFormat())
        arq2.write("%s \n" % bip32_child_key_obj.Address())
        print(bip32_child_key_obj.WalletImportFormat())
children = 100
with open("mnemonics.txt") as file:
    for line in file:
        mnemonic_words = str.strip(line)
		
        bip39(mnemonic_words, children)
