from typing import Literal, Union

t_node = Literal["plus", "minus", "times", "lt", "ite", "par", "int", "bool", "error"]

t_int = int
t_bool = Literal["true", "false"]
t_error = Literal["error"]
t_val = Union[t_int, t_bool, t_error]