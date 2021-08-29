## Specification of form manipulation


Specification of the value-to-form processing in Lexibank datasets:

The value-to-form processing is divided into two steps, implemented as methods:
- `FormSpec.split`: Splits a string into individual form chunks.
- `FormSpec.clean`: Normalizes a form chunk.

These methods use the attributes of a `FormSpec` instance to configure their behaviour.

- `brackets`: `{'(': ')'}`
  Pairs of strings that should be recognized as brackets, specified as `dict` mapping opening string to closing string
- `separators`: `~;,/`
  Iterable of single character tokens that should be recognized as word separator
- `missing_data`: `['∅', '#', 'NA', 'XX']`
  Iterable of strings that are used to mark missing data
- `strip_inside_brackets`: `True`
  Flag signaling whether to strip content in brackets (**and** strip leading and trailing whitespace)
- `replacements`: `[('1', '¹'), ('2', '²'), ('3', '³'), ('4', '⁴'), ('5', '⁵'), ('6', '⁶'), ('7', '⁷'), ('8', '⁸'), ('9', '⁹'), ('0', '⁰'), ('-', ''), (' "mountain"', ''), (' "hill"', ''), (' [<Lao]', ''), ('[', ''), (']', ''), (' < Lao', ''), (' ', '_'), ('ʔək__̄', 'ʔək'), ('anaŋ__᷅ ', 'anaŋ'), ("_'abdomen'", ''), ('d\uf1f6ŋ.³³', 'dəŋ³³'), ('_', ''), ('m̀', 'm'), ('ŋ᷄', 'ŋ'), ('᷄', ''), ('᷅', '')]`
  List of pairs (`source`, `target`) used to replace occurrences of `source` in formswith `target` (before stripping content in brackets)
- `first_form_only`: `True`
  Flag signaling whether at most one form should be returned from `split` - effectively ignoring any spelling variants, etc.
- `normalize_whitespace`: `True`
  Flag signaling whether to normalize whitespace - stripping leading and trailing whitespace and collapsing multi-character whitespace to single spaces
- `normalize_unicode`: `None`
  UNICODE normalization form to use for input of `split` (`None`, 'NFD' or 'NFC')