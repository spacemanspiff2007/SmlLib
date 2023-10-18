# SmlLib
[![Tests Status](https://github.com/spacemanspiff2007/SmlLib/workflows/Tests/badge.svg)](https://github.com/spacemanspiff2007/SmlLib/actions?query=workflow%3ATests)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/SmlLib)](https://pypi.org/project/smllib/)
[![PyPI](https://img.shields.io/pypi/v/SmlLib)](https://pypi.org/project/smllib/)
[![Downloads](https://pepy.tech/badge/SmlLib)](https://pepy.tech/project/SmlLib)


_A SML (Smart Message Language) library_

## About
This library can be used to parse SML byte streams.
It does not read from external devices.

## Usage
The [sml2mqtt](https://pypi.org/project/sml2mqtt/) program makes use of this library.


Example:
```python
from smllib import SmlStreamReader

stream = SmlStreamReader()
stream.add(b'BytesFromSerialPort')
sml_frame = stream.get_frame()
if sml_frame is None:
    print('Bytes missing')

# Add more bytes, once it's a complete frame the SmlStreamReader will
# return the frame instead of None
stream.add(b'BytesFromSerialPort')
sml_frame = stream.get_frame()

# A quick Shortcut to extract all values without parsing the whole frame
# In rare cases this might raise an InvalidBufferPos exception, then you have to use sml_frame.parse_frame()
obis_values = sml_frame.get_obis()

# return all values but slower
parsed_msgs = sml_frame.parse_frame()
for msg in parsed_msgs:
    # prints a nice overview over the received values
    print(msg.format_msg())

# In the parsed message the obis values are typically found like this
obis_values = parsed_msgs[1].message_body.val_list

# The obis attribute of the SmlListEntry carries different obis representations as attributes
list_entry = obis_values[0]
print(list_entry.obis)            # 0100010800ff
print(list_entry.obis.obis_code)  # 1-0:1.8.0*255
print(list_entry.obis.obis_short) # 1.8.0
```

```text
SmlMessage
    transaction_id: 17c77d6b
    group_no      : 0
    abort_on_error: 0
    message_body <SmlOpenResponse>
        codepage   : None
        client_id  : None
        req_file_id: 07ed29cd
        server_id  : 11111111111111111111
        ref_time   : None
        sml_version: None
    crc16         : 25375
SmlMessage
    transaction_id: 17c77d6c
    group_no      : 0
    abort_on_error: 0
    message_body <SmlGetListResponse>
        client_id       : None
        sever_id        : 11111111111111111111
        list_name       : 0100620affff
        act_sensor_time : 226361515
        val_list: list
            <SmlListEntry>
                obis           : 8181c78203ff (129-129:199.130.3*255)
                status         : None
                val_time       : None
                unit           : None
                scaler         : None
                value          : ISK
                value_signature: None
                -> (Hersteller-Identifikation)
            <SmlListEntry>
                obis           : 0100000009ff (1-0:0.0.9*255)
                status         : None
                val_time       : None
                unit           : None
                scaler         : None
                value          : 11111111111111111111
                value_signature: None
                -> (Geräteeinzelidentifikation)
            <SmlListEntry>
                obis           : 0100010800ff (1-0:1.8.0*255)
                status         : 386
                val_time       : None
                unit           : 30
                scaler         : -1
                value          : 123456789
                value_signature: None
                -> 12345678.9Wh (Zählerstand Total)
            <SmlListEntry>
                obis           : 0100010801ff (1-0:1.8.1*255)
                status         : None
                val_time       : None
                unit           : 30
                scaler         : -1
                value          : 123456789
                value_signature: None
                -> 12345678.9Wh (Zählerstand Tarif 1)
            <SmlListEntry>
                obis           : 0100010802ff (1-0:1.8.2*255)
                status         : None
                val_time       : None
                unit           : 30
                scaler         : -1
                value          : 0
                value_signature: None
                -> 0.0Wh (Zählerstand Tarif 2)
            <SmlListEntry>
                obis           : 0100100700ff (1-0:16.7.0*255)
                status         : None
                val_time       : None
                unit           : 27
                scaler         : 0
                value          : 555
                value_signature: None
                -> 555W (aktuelle Wirkleistung)
            <SmlListEntry>
                obis           : 8181c78205ff (129-129:199.130.5*255)
                status         : None
                val_time       : None
                unit           : None
                scaler         : None
                value          : XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                value_signature: None
                -> (Öffentlicher Schlüssel)
        list_signature  : None
        act_gateway_time: None
    crc16         : 22117
SmlMessage
    transaction_id: 17c77d6d
    group_no      : 0
    abort_on_error: 0
    message_body <SmlCloseResponse>
        global_signature: None
    crc16         : 56696
```
