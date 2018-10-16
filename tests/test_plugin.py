import os
import shutil

import pytest


def test_plugin_module(testdir):
    testdir.makeconftest("pytest_plugins = ['structmpd']")

    # 'testdir.copy_example' is useful method on this purpose, but the API is
    # experimental and outputs warning log, not use on this module.
    current = os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(current, '_test_structmpd.py')
    with open(script_path, 'r') as f:
        script = f.read()
    testdir.makepyfile(script)

    result = testdir.runpytest_subprocess(
        '--structmpd-root', testdir.tmpdir, '--structmpd-name', 'abcdefg',
        '--structmpd-leave')

    temp_path = os.path.join(testdir.tmpdir, 'abcdefg')
    assert os.path.exists(temp_path)
    shutil.rmtree(temp_path)

    result.assert_outcomes(passed=2)


def test_tmpsessiondir(request, tmpsessiondir):
    dir_name = request.config.getoption('structmpd-name')
    if dir_name is None:
        dir_name = 'pytest-structmpd'
    assert dir_name in tmpsessiondir


def test_tmpsessiondir_tmpfuncdir(tmpsessiondir, tmpfuncdir):
    expected_path = os.path.join(tmpsessiondir, tmpfuncdir)
    assert expected_path in tmpfuncdir


def test_tmpfuncdir(request, tmpfuncdir):
    dir_name = request.config.getoption('structmpd-name')
    if dir_name is None:
        dir_name = 'pytest-structmpd'
    assert dir_name in tmpfuncdir
    assert 'test_tmpfuncdir' in tmpfuncdir


@pytest.mark.parametrize('id', [-1, 0, 1])
def test_tmpfuncdir_param(id, tmpfuncdir):
    if id < 0:
        assert 'test_tmpfuncdir_param' in tmpfuncdir
        return

    dir_name = 'test_tmpfuncdir_param_{:d}'.format(id)
    assert dir_name in tmpfuncdir


class TestCustomClass(object):

    def test_cls_method(self, tmpfuncdir):
        dir_name = os.path.join('TestCustomClass', 'test_cls_method')
        assert dir_name in tmpfuncdir

    @pytest.mark.parametrize('id', [-1, 0, 1])
    def test_cls_method_param(self, id, tmpfuncdir):
        dir_name = os.path.join('TestCustomClass', 'test_cls_method_param')
        if id < 0:
            assert dir_name in tmpfuncdir
            return

        dir_name += '_{:d}'.format(id)
        assert dir_name in tmpfuncdir
