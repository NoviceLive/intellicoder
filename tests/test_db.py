import os

from intellicoder import Database
from intellicoder.database import Item


path = 'ignored/test.db'
os.makedirs(os.path.dirname(path), exist_ok=True)
try:
    os.remove(path)
except:
    pass
db = Database(path)
with open('tests/syscall_32.tbl') as tbl32, \
     open('tests/syscall_64.tbl') as tbl64, \
     open('tests/allsc.txt') as allsc:
    db.add_data([tbl32, tbl64, allsc])


def test_query_item():
        item = db.query_item('fork', abis=['i386'])[0]
        print(item)
        assert item.name == 'fork'
        assert item.abi == 'i386'
        assert item.number == 2

        item = db.query_item('fork', abis=['common'])[0]
        print(item)
        assert item.name == 'fork'
        assert item.abi == 'common'
        assert item.number == 57

        item = db.query_item('5', abis=['common'])[0]
        print(item)
        assert item.name == 'fstat'
        assert item.abi == 'common'
        assert item.number == 5

        item = db.query_item('100', abis=['i386'])[0]
        print(item)
        assert item.name == 'fstatfs'
        assert item.abi == 'i386'
        assert item.number == 100


def test_query_decl():
    decl = db.query_decl(name='fork')[0]
    print(decl)
    print(decl.decl())
    assert decl.decl() == 'long fork();'
    assert decl.filename == 'kernel/fork.c'

    decl = db.query_decl(name='brk')[0]
    print(decl)
    print(decl.decl())
    assert decl.decl() == 'long brk(unsigned long brk);'
    assert decl.filename == 'mm/nommu.c'

    decl = db.query_decl(name='execve')[0]
    print(decl)
    print(decl.decl())
    assert decl.decl() == 'long execve(const char * filename,  const char *const * argv,  const char *const * envp);'
    assert decl.filename == 'fs/exec.c'
