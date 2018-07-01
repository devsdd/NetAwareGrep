def pytest_addoption(parser):
    parser.addoption("--ip", action="store")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.ip
    if 'ip' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("ip", [option_value])
