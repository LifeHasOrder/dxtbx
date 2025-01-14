from __future__ import annotations

import procrunner


def test_print_header(dials_data):
    screen = dials_data("thaumatin_eiger_screen", pathlib=True)
    master = screen / "Therm_6_1_master.h5"
    result = procrunner.run(["dxtbx.print_header", master])
    assert not result.returncode and not result.stderr

    expected_output = [
        f"=== {master} ===",
        "Using header reader: FormatNXmxDLS16M",
    ]

    for record in expected_output:
        assert record.strip().encode("latin-1") in result.stdout, record
