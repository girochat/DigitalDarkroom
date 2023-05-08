# Fixing pylint issues

## Initial pylint output for extract_metadata

************* Module extract_metadata\
extract_metadata.py:3:0: C0301: Line too long (128/100) (line-too-long)\
extract_metadata.py:5:0: C0301: Line too long (103/100) (line-too-long)\
extract_metadata.py:6:0: C0301: Line too long (140/100) (line-too-long)\
extract_metadata.py:50:80: C0303: Trailing whitespace (trailing-whitespace)\
extract_metadata.py:51:0: C0325: Unnecessary parens after '=' keyword (superfluous-parens)\
extract_metadata.py:55:0: C0301: Line too long (264/100) (line-too-long)\
extract_metadata.py:56:29: C0303: Trailing whitespace (trailing-whitespace)\
extract_metadata.py:68:147: C0303: Trailing whitespace (trailing-whitespace)\
extract_metadata.py:68:0: C0301: Line too long (147/100) (line-too-long)\
extract_metadata.py:70:0: C0303: Trailing whitespace (trailing-whitespace)\
extract_metadata.py:80:56: C0303: Trailing whitespace (trailing-whitespace)\
extract_metadata.py:81:0: C0325: Unnecessary parens after '=' keyword (superfluous-parens)\
extract_metadata.py:84:0: C0301: Line too long (116/100) (line-too-long)\
extract_metadata.py:85:0: C0301: Line too long (253/100) (line-too-long)\
extract_metadata.py:93:0: C0303: Trailing whitespace (trailing-whitespace)\
extract_metadata.py:111:0: C0301: Line too long (118/100) (line-too-long)\
extract_metadata.py:32:0: R0914: Too many local variables (17/15) (too-many-locals)\
extract_metadata.py:35:4: C0103: Variable name "df" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:37:45: C0103: Variable name "it" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:42:16: C0103: Variable name "im" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:52:16: C0103: Variable name "t" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:67:4: C0103: Variable name "image_DB" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:72:8: C0103: Variable name "im" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:73:19: W0212: Access to a protected member _getexif of a client class (protected-access)\
extract_metadata.py:82:8: C0103: Variable name "t" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:64:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)\
extract_metadata.py:95:0: C0103: Function name "sort_image_DB" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:112:4: C0103: Variable name "t" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:133:4: C0103: Variable name "p" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:134:4: C0103: Variable name "im" doesn't conform to snake_case naming style (invalid-name)\
extract_metadata.py:148:0: W0105: String statement has no effect (pointless-string-statement)\
extract_metadata.py:12:0: C0411: standard import "import os" should be placed before "import pandas as pd" (wrong-import-order)\
extract_metadata.py:14:0: C0411: standard import "from datetime import datetime" should be placed before "import pandas as pd" (wrong-import-order)\
extract_metadata.py:15:0: C0411: standard import "import shutil" should be placed before "import pandas as pd" (wrong-import-order)\


-----------------------------------
Your code has been rated at 6.00/10


### What still needs to be changed
extract_metadata.py:33:0: R0914: Too many local variables (18/15) (too-many-locals)\
- split up function, maybe define database separately

extract_metadata.py:77:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)\
- function will be updated for next release

Final score:
Your code has been rated at 9.77/10 (previous run: 9.65/10, +0.12)



## Initial pylint output for image_upload
************* Module image_upload\
image_upload.py:49:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:54:74: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:63:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:66:0: C0301: Line too long (122/100) (line-too-long)\
image_upload.py:67:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:70:72: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:74:80: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:75:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:82:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:87:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:89:36: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:96:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:98:96: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:105:0: C0301: Line too long (141/100) (line-too-long)\
image_upload.py:107:0: C0301: Line too long (166/100) (line-too-long)\
image_upload.py:115:0: C0301: Line too long (107/100) (line-too-long)\
image_upload.py:128:0: C0301: Line too long (187/100) (line-too-long)\
image_upload.py:138:63: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:139:68: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:140:0: C0301: Line too long (122/100) (line-too-long)\
image_upload.py:141:68: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:151:0: C0301: Line too long (119/100) (line-too-long)\
image_upload.py:154:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:164:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:167:0: C0301: Line too long (109/100) (line-too-long)\
image_upload.py:168:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:170:0: C0301: Line too long (129/100) (line-too-long)\
image_upload.py:172:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:174:0: W0311: Bad indentation. Found 12 spaces, expected 8 (bad-indentation)\
image_upload.py:175:0: W0311: Bad indentation. Found 12 spaces, expected 8 (bad-indentation)\
image_upload.py:177:43: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:180:0: C0303: Trailing whitespace (trailing-whitespace)\
image_upload.py:36:0: R0903: Too few public methods (0/2) (too-few-public-methods)\
image_upload.py:73:11: W0718: Catching too general exception Exception (broad-exception-caught)\
image_upload.py:117:7: R1714: Consider merging these comparisons with 'in' by using 'user_input in ('all', '1')'. Use a set instead if elements are hashable. (consider-using-in)\
image_upload.py:34:0: C0411: third party import "import pandas as pd" should be placed before "from extract_metadata import extract_metadata_upload" (wrong-import-order)\
image_upload.py:34:0: W0611: Unused pandas imported as pd (unused-import)\

-----------------------------------
Your code has been rated at 5.80/10


### What still needs to be changed

- image_upload.py:35:0: R0903: Too few public methods (0/2) (too-few-public-methods)\
- image_upload.py:73:11: W0718: Catching too general exception Exception (broad-exception-caught)

Final score:
Your code has been rated at 9.77/10 (previous run: 9.77/10, +0.00)