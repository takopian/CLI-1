import sys
from typing import Callable

sys.path.insert(0, '..')

from CLI import CliTransformer, cli_parser, Exit, Cat
from CLI import Echo, Wc, Pwd, LS, CD


def parse_test(input_text, verify: Callable) -> None:
    tfm = CliTransformer()
    res = cli_parser.parse(
        input_text
    )
    cmd = tfm.transform(res)
    result, err = verify(cmd)
    assert result, err


def verify_cmd(cmd, ethalon_cmd):
    if len(cmd) != len(cmd):
        return False, f"Expected single command got pipe of len {len(cmd)} instead"

    for i, (c, ethalon_c) in enumerate(zip(cmd, ethalon_cmd)):
        if not isinstance(c, type(ethalon_c)):
            return False, f"Parsed cmd number {i} in pipe, should be {type(ethalon_c)}, got {type(c)} instead"
        if c.name != ethalon_c.name:
            return False, f"Parsed cmd number {i} have unexpected name \"{c.name}\", expected \"{ethalon_c.name}\""
        for idx, (parsed_arg, arg) in enumerate(zip(c.args, ethalon_c.args)):
            if parsed_arg != arg:
                return False, f"Parsed error in argument {idx}: {parsed_arg} != {arg}"

    return True, ""


def test_simple_echo_cmd():
    parse_test("echo 1 2 3",
               lambda cmd: verify_cmd(cmd, [Echo("echo", *("1", "2", "3"))]))


def test_simple_wc_cmd():
    parse_test("wc parse_test.py",
               lambda cmd: verify_cmd(cmd, [Wc("wc", *("parse_test.py",))]))


def test_simple_exit_cmd():
    parse_test("exit",
               lambda cmd: verify_cmd(cmd, [Exit("exit")]))


def test_simple_pwd_cmd():
    parse_test("pwd",
               lambda cmd: verify_cmd(cmd, [Pwd("pwd")]))


def test_simple_cat_cmd():
    parse_test("cat parse_test.py",
               lambda cmd: verify_cmd(cmd, [Cat("cat", *("parse_test.py",))]))


def test_simple_ls_cmd():
    parse_test("ls",
               lambda cmd: verify_cmd(cmd, [LS("ls")]))


def test_simple_ls_cmd_2():
    parse_test("ls ..",
               lambda cmd: verify_cmd(cmd, [LS("ls", *("..",))]))


def test_simple_ls_cmd_3():
    parse_test("pwd | ls",
               lambda cmd: verify_cmd(cmd, [Pwd("pwd"), LS("ls")]))


def test_simple_cd_cmd():
    parse_test("cd ..",
               lambda cmd: verify_cmd(cmd, [CD("cd", *("..",))]))

# parse_test("echo 1 2 3",
#            lambda cmd: (isinstance(cmd, calls.Echo),
#                         "parse error here in \"echo 1 2 3\""))
#
# res = CLI.cli_parser.parse(
#     "echo 1 2 3 | wc"
# )
# print(res.pretty())
# print(tfm.transform(res))
#
# res = CLI.cli_parser.parse(
#     "echo 1 2 ${var} | wc"
# )
# print(res.pretty())
# print(tfm.transform(res))
#
# res = CLI.cli_parser.parse(
#     "echo 1 2 ${var} \"echo 1 2 ${var} | wc\" | wc"
# )
# print(res.pretty())
# print(tfm.transform(res))
