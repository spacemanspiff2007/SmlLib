from smllib.sml import SmlObjFieldInfo


def test_copy():
    def func(a):
        pass

    a = SmlObjFieldInfo(func)
    b = a.copy()
    assert b.func == a.func
    assert a == b
