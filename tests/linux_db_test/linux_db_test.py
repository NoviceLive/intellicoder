import os

from intellicoder import Database


path = 'ignored'
name = os.path.join(path, 'test.db')
if os.path.exists(path):
    pass
else:
    try:
        os.makedirs(path)
    except:
        pass
try:
    os.remove(path)
except:
    pass
db = Database(name)
with open('tests/linux_db_test/syscall_32.tbl') as tbl32, \
     open('tests/linux_db_test/syscall_64.tbl') as tbl64, \
     open('tests/linux_db_test/allsc.txt') as allsc:
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

        item = db.query_item(0x32, abis=['common'])[0]
        print(item)
        assert item.name == 'listen'
        assert item.abi == 'common'
        assert item.number == 50

        item = db.query_item('0x64', abis=['i386'])[0]
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
