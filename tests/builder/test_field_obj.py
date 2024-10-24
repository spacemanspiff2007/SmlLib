from smllib.sml import SmlObjFieldInfo


def test_copy() -> None:
    def func(a) -> None:
        pass

    a = SmlObjFieldInfo(func)
    b = a.copy()
    assert b.func == a.func
    assert a == b
