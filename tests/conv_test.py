from intellicoder import Converter


def test_conv():
    with open('tests/lin64', 'rb') as stream:
        conv = Converter.uni_from(
            'sec', stream, section_name=b'.text')
        assert conv.to_esc() == r'\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05'
        assert conv.to_hex() == '31f648bb2f62696e2f2f73685653545f6a3b5831d20f05'

        c = r"""
char shellcode[] = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f"
    "\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31"
    "\xd2\x0f\x05";
""".strip()
        assert conv.to_c() == c
        assert conv.to_bytes() == b'1\xf6H\xbb/bin//shVST_j;X1\xd2\x0f\x05'
