from smllib.builder import SmlCloseResponseBuilder, SmlGetListResponseBuilder, \
    SmlListEntryBuilder, SmlMessageBuilder, SmlObjBuilder
from smllib.sml import EndOfSmlMsg, SmlCloseResponse, SmlListEntry
from tests.helper import in_snip


def test_build_entry():
    builder = SmlListEntryBuilder()
    obj = builder.build(in_snip(['0100010800ff', None, None, None, None, '76616c', None]), {SmlListEntry: builder})
    assert obj.obis == '0100010800ff'
    assert obj.value == 'val'


def test_build_entry_list():
    data = in_snip([
        None, 'server', None, None,
        [['0100010800ff', None, None, None, None, '76616c31', None],
         ['0100010801ff', None, None, None, None, '76616c32', None]],
        None, None
    ])

    builder = SmlGetListResponseBuilder()

    obj = builder.build(data, {SmlListEntry: SmlListEntryBuilder()})
    assert obj.server_id == 'server'
    assert obj.val_list[0].obis == '0100010800ff'
    assert obj.val_list[0].value == 'val1'
    assert obj.val_list[1].obis == '0100010801ff'
    assert obj.val_list[1].value == 'val2'

    class PatchedBuilder(SmlListEntryBuilder):
        BUILDS = SmlListEntry

        def build(self, obj: list, classes):
            ret = super().build(obj, classes)
            ret.obis += '_patched'
            return ret

    obj = builder.build(data, {SmlListEntry: PatchedBuilder()})
    assert obj.server_id == 'server'
    assert obj.val_list[0].obis == '0100010800ff_patched'
    assert obj.val_list[0].value == 'val1'
    assert obj.val_list[1].obis == '0100010801ff_patched'
    assert obj.val_list[1].value == 'val2'


def test_build_choice():
    data = in_snip(['t1', 1, 0, [0x0201, ['sig']], 1111, EndOfSmlMsg])
    builder = SmlMessageBuilder()
    obj = builder.build(data, {SmlCloseResponse: SmlCloseResponseBuilder()})
    assert obj.transaction_id == 't1'
    assert obj.group_no == 1
    assert obj.abort_on_error == 0
    assert isinstance(obj.message_body, SmlCloseResponse)
    assert obj.message_body.global_signature == 'sig'
    assert obj.crc16 == 1111

    class PatchedBuilder(SmlObjBuilder):
        BUILDS = SmlCloseResponse

        def build(self, obj: list, classes):
            ret = super().build(obj, classes)
            ret.global_signature += '_patched'
            return ret

    data = in_snip(['t1', 1, 0, [0x0201, ['sig']], 1111, EndOfSmlMsg])
    obj = builder.build(data, {SmlCloseResponse: PatchedBuilder()})
    assert obj.transaction_id == 't1'
    assert obj.group_no == 1
    assert obj.abort_on_error == 0
    assert isinstance(obj.message_body, SmlCloseResponse)
    assert obj.message_body.global_signature == 'sig_patched'
    assert obj.crc16 == 1111
