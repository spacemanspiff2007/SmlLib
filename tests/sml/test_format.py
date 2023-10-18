from smllib.builder import SmlCloseResponseBuilder, \
    SmlGetListResponseBuilder, SmlListEntryBuilder, SmlOpenResponseBuilder
from smllib.sml import SmlListEntry
from tests.helper import in_snip


def test_open_response():
    r = SmlOpenResponseBuilder().build(in_snip([None, None, 'ab', 'cd', None, 1]), {})
    assert r.format_msg() == '<SmlOpenResponse>\n' \
                             '  codepage   : None\n' \
                             '  client_id  : None\n' \
                             '  req_file_id: ab\n' \
                             '  server_id  : cd\n' \
                             '  ref_time   : None\n' \
                             '  sml_version: 1\n'


def test_close_response():
    r = SmlCloseResponseBuilder().build(in_snip(['my_sig']), {})
    assert r.format_msg() == '<SmlCloseResponse>\n' \
                             '  global_signature: my_sig\n'


def test_list_entry():
    data = in_snip([
        None, 'server', None, None,
        [['0100010800ff', None, None, None, None, '76616c31', None],
         ['0100010801ff', None, None, None, None, '76616c32', None]],
        None, None
    ])

    builder = SmlGetListResponseBuilder()
    obj = builder.build(data, {SmlListEntry: SmlListEntryBuilder()})

    assert obj.format_msg() == '<SmlGetListResponse>\n' \
                               '  client_id       : None\n' \
                               '  server_id       : server\n' \
                               '  list_name       : None\n' \
                               '  act_sensor_time : None\n' \
                               '  val_list:\n' \
                               '    <SmlListEntry>\n' \
                               '      obis           : 0100010800ff (1-0:1.8.0*255)\n' \
                               '      status         : None\n' \
                               '      val_time       : None\n' \
                               '      unit           : None\n' \
                               '      scaler         : None\n' \
                               '      value          : val1\n' \
                               '      value_signature: None\n' \
                               '      -> (Zählerstand Bezug Total)\n' \
                               '    <SmlListEntry>\n' \
                               '      obis           : 0100010801ff (1-0:1.8.1*255)\n' \
                               '      status         : None\n' \
                               '      val_time       : None\n' \
                               '      unit           : None\n' \
                               '      scaler         : None\n' \
                               '      value          : val2\n' \
                               '      value_signature: None\n' \
                               '      -> (Zählerstand Bezug Tarif 1)\n' \
                               '  list_signature  : None\n' \
                               '  act_gateway_time: None\n'
