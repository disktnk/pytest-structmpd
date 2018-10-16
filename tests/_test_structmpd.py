def test_tmpsessiondir(tmpsessiondir):
    assert 'abcdefg' in tmpsessiondir


def test_tmpfuncdir(tmpfuncdir):
    assert 'abcdefg' in tmpfuncdir
    assert 'test_tmpfuncdir' in tmpfuncdir
