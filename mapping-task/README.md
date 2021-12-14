# Simple data mapping
Usage:
simple_data_mapping.py "Param_1" "Param_2"

Param_1  = Minutes to schedule
Param_2 = This is to tell to process old articles are not. value are **False or True**.

**Example**: In our case
simple_data_mapping.py "5" "False"


If we True in param_2, it will only process which is modified or published less than given time period in param_1.
