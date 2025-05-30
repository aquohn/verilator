#!/usr/bin/env python3
# DESCRIPTION: Verilator: Verilog Test driver/expect definition
#
# Copyright 2024 by Wilson Snyder. This program is free software; you
# can redistribute it and/or modify it under the terms of either the GNU
# Lesser General Public License Version 3 or the Perl Artistic License
# Version 2.0.
# SPDX-License-Identifier: LGPL-3.0-only OR Artistic-2.0

import vltest_bootstrap

test.scenarios('vlt_all')
test.pli_filename = "t/t_trace_public_sig.cpp"
test.top_filename = "t/t_trace_public.v"
test.golden_filename = "t/t_trace_public.out"

out_filename = test.obj_dir + "/V" + test.name + ".tree.json"

test.compile(make_top_shell=False,
             make_main=False,
             v_flags2=[
                 "--trace-vcd --exe", test.pli_filename,
                 test.t_dir + "/t_trace_public_sig.vlt --no-json-edit-nums"
             ])

if test.vlt_all:
    test.file_grep(
        out_filename,
        r'{"type":"VAR","name":"GSR",.*"loc":"\w,47:[^"]*",.*"origName":"GSR",.*"isSigPublic":true,.*"dtypeName":"logic",.*"isSigUserRdPublic":true.*"isSigUserRWPublic":true'
    )

test.execute()

test.vcd_identical(test.trace_filename, test.golden_filename)

# vcd_identical doesn't detect "$var a.b;" vs "$scope module a; $var b;"
test.file_grep(test.trace_filename, r'module glbl')

test.passes()
