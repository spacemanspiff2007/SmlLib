from smllib.sml import SmlOpenResponse, SmlCloseResponse, SmlGetListResponse, SmlListEntry, SmlMessage
from smllib.builder import SmlOpenResponseBuilder, SmlCloseResponseBuilder, SmlGetListResponseBuilder, SmlListEntryBuilder, SmlMessageBuilder


def test_open_response():
    r = SmlOpenResponseBuilder().build([None, None, 'ab', 'cd', None, 1], {})
    assert r.format_msg() == '<SmlOpenResponse>\n' \
                             '  codepage   : None\n' \
                             '  client_id  : None\n' \
                             '  req_file_id: ab\n' \
                             '  server_id  : cd\n' \
                             '  ref_time   : None\n' \
                             '  sml_version: 1\n'


def test_close_response():
    r = SmlCloseResponseBuilder().build(['my_sig'], {})
    assert r.format_msg() == '<SmlCloseResponse>\n' \
                             '  global_signature: my_sig\n'


def test_list_entry():
    data = [
        None, 'server', None, None,
        [['obis1', None, None, None, None, '76616c31', None], ['obis2', None, None, None, None, '76616c32', None]],
        None, None
    ]
    
    builder = SmlGetListResponseBuilder()
    obj = builder.build(data, {SmlListEntry: SmlListEntryBuilder()})
    
    assert obj.format_msg() == '<SmlGetListResponse>\n' \
                               '  client_id       : None\n' \
                               '  sever_id        : server\n' \
                               '  list_name       : None\n' \
                               '  act_sensor_time : None\n' \
                               '  val_list:\n' \
                               '    <SmlListEntry>\n' \
                               '      obis           : obis1\n' \
                               '      status         : None\n' \
                               '      val_time       : None\n' \
                               '      unit           : None\n' \
                               '      scaler         : None\n' \
                               '      value          : val1\n' \
                               '      value_signature: None\n' \
                               '    <SmlListEntry>\n' \
                               '      obis           : obis2\n' \
                               '      status         : None\n' \
                               '      val_time       : None\n' \
                               '      unit           : None\n' \
                               '      scaler         : None\n' \
                               '      value          : val2\n' \
                               '      value_signature: None\n' \
                               '  list_signature  : None\n' \
                               '  act_gateway_time: None\n'
