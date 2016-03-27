from intellicoder import Converter


def test_elf():
    with open('tests/converter_test/elf64', 'rb') as stream:
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


def test_pe():
    # Not so bad: pefile sucks.
    expected_bytes = b'3\xc9d\x8bI0\x8bI\x0c\x8bI\x1c\x8bY\x08\x8bA \x8b\t\x80x\x0c3u\xf2\x8b\xeb\x03m<\x8bmx\x03\xeb\x8bE \x03\xc33\xd2\x8b4\x90\x03\xf3B\x81>GetPu\xf2\x81~\x04rocAu\xe9\x8bu$\x03\xf3f\x8b\x14V\x8bu\x1c\x03\xf3\x8bt\x96\xfc\x03\xf33\xffWharyAhLibrhLoadTS\xff\xd63\xc9Wf\xb932QhuserT\xff\xd0WhoxA\x01\xfeL$\x03hageBhMessTP\xff\xd6Whrld!ho WohHell\x8b\xccWWQW\xff\xd0Whess\x01\xfeL$\x03hProchExitTS\xff\xd6W\xff\xd0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    with open('tests/converter_test/pe32.exe', 'rb') as stream:
        conv = Converter.uni_from('sec', stream, section_name=b'.text')
        assert conv.to_bytes() == expected_bytes