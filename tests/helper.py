from smllib.sml_frame import SmlFrameSnippet


def in_snip(obj, pack_top=True) -> SmlFrameSnippet:
    if not isinstance(obj, (list, tuple)):
        return SmlFrameSnippet(obj, 'from in_snip')

    for i, k in enumerate(obj):
        obj[i] = in_snip(k)

    if pack_top:
        return SmlFrameSnippet(obj, 'from in_snip')
    return obj
