import pytest

from helpers import ls, rm, join, isdir, mkdir, rm_rf, rmdir, isfile


@pytest.fixture(autouse=True)
def username():
    yield 'thomas'


@pytest.fixture(autouse=True)
def password():
    yield 'Thomas Schaper'


def test_list_courses(mount_dir):
    assert isdir(mount_dir)
    for course in [
        'Besturingssystemen', 'Programmeertalen',
        'Project Software Engineering'
    ]:
        assert isdir(mount_dir, course)

    assert set(ls(mount_dir)) == set(
        [
            'Besturingssystemen', 'Programmeertalen',
            'Project Software Engineering'
        ]
    )


def test_list_assignments(mount_dir):
    assert isdir(mount_dir)

    for assig in ['Security assignment', 'Shell']:
        assert isdir(mount_dir, 'Besturingssystemen', assig)

    for assig in ['Final deadline']:
        assert isdir(mount_dir, 'Project Software Engineering', assig)

    for assig in ['Haskell', 'Go', 'Python', 'Shell']:
        assert isdir(mount_dir, 'Programmeertalen', assig)


def test_list_submissions(mount_dir):
    for course in ['Besturingssystemen', 'Programmeertalen']:
        for assig in ls(mount_dir, course):
            for sub in ls(mount_dir, course, assig):
                assert any(f'Stupid{i}' in sub for i in range(1, 5))

    for assig in ls(mount_dir, 'Project Software Engineering'):
        for sub in ls(mount_dir, 'Project Software Engineering', assig):
            assert 'Thomas Schaper' in sub


def test_create_files(mount_dir, sub_open, sub_done):
    with pytest.raises(PermissionError):
        with open(join(sub_open, 'file1'), 'w') as f:
            pass
    assert not isfile(sub_open, 'file1')

    with pytest.raises(PermissionError):
        with open(join(sub_open, 'file1'), 'w') as f:
            f.write('abc\n')
    assert not isfile(sub_open, 'file1')

    with open(join(sub_done, 'file1'), 'w') as f:
        pass

    assert isfile(sub_done, 'file1')

    with open(join(sub_done, 'file2'), 'w') as f:
        f.write('abc\n')
    assert isfile(sub_done, 'file2')


def test_write_and_read_files(mount_dir, sub_open, sub_done):
    assert isfile(sub_done, 'dir', 'single_file_work')
    with open(join(sub_done, 'dir', 'single_file_work'), 'w') as f:
        f.write('abc\n')
    assert isfile(sub_done, 'dir', 'single_file_work')
    with open(join(sub_done, 'dir', 'single_file_work'), 'r') as f:
        assert f.read() == 'abc\n'

    with open(join(sub_done, 'file1'), 'a') as f:
        f.write('abc\n')
    assert isfile(sub_done, 'file1')

    with open(join(sub_done, 'file1'), 'r') as f:
        assert f.read() == 'abc\n'

    with open(join(sub_done, 'file1'), 'w') as f:
        f.write('def\n')
    with open(join(sub_done, 'file1'), 'r') as f:
        assert f.read() == 'def\n'

    with open(join(sub_done, 'file1'), 'a') as f:
        f.write('def\n')
    with open(join(sub_done, 'file1'), 'r') as f:
        assert f.read() == 'def\ndef\n'

    with pytest.raises(PermissionError):
        with open(join(sub_open, 'file1'), 'a') as f:
            f.write('def\n')
    assert not isfile(sub_open, 'file1')

    assert isfile(sub_open, 'dir', 'single_file_work')
    with open(join(sub_open, 'dir', 'single_file_work'), 'r') as f:
        old = f.read()
    with pytest.raises(PermissionError):
        with open(join(sub_open, 'dir', 'single_file_work'), 'a') as f:
            f.write('abc\n')
    assert isfile(sub_open, 'dir', 'single_file_work')
    with open(join(sub_open, 'dir', 'single_file_work'), 'r') as f:
        assert f.read() == old


def test_delete_files(mount_dir, sub_open, sub_done):
    assert not isfile(sub_done, 'file1')
    with open(join(sub_done, 'file1'), 'w') as f:
        f.write('abc\n')
    assert isfile(sub_done, 'file1')

    with open(join(sub_done, 'file1'), 'r') as f:
        assert f.read() == 'abc\n'

    rm(sub_done, 'file1')
    assert not isfile(sub_done, 'file1')

    with pytest.raises(FileNotFoundError):
        rm(sub_done, 'nonexisting')


def test_read_directories(mount_dir, sub_done, sub_open):
    for sub in [sub_done, sub_open]:
        assert 'dir' in ls(sub)
        assert 'dir2' in ls(sub)
        assert 'dir1' not in ls(sub)

        assert 'single_file_work' in ls(sub, 'dir')
        assert 'single_file_work_copy' in ls(sub, 'dir')
        assert 'single_file_work_copy2' not in ls(sub, 'dir')

        assert 'single_file_work' in ls(sub, 'dir2')
        assert 'single_file_work_copy' in ls(sub, 'dir2')
        assert 'single_file_work_copy2' not in ls(sub, 'dir2')

        with pytest.raises(FileNotFoundError):
            ls(sub, 'dir3')


def test_make_directories(mount_dir, sub_done, sub_open):
    with pytest.raises(FileExistsError):
        mkdir(sub_open, 'dir')
    assert isdir(sub_open, 'dir')

    with pytest.raises(PermissionError):
        rm_rf(sub_open, 'dir')

    assert isdir(sub_open, 'dir')
    assert isfile(sub_open, 'dir', 'single_file_work')
    assert isfile(sub_open, 'dir', 'single_file_work_copy')

    with pytest.raises(IsADirectoryError):
        rm(sub_done, 'dir')
    with pytest.raises(OSError):
        rmdir(sub_done, 'dir')
    assert isdir(sub_done, 'dir')

    rm_rf(sub_done, 'dir')

    assert 'dir' not in ls(sub_done)

    mkdir(sub_done, 'dir')
    assert isdir(sub_done, 'dir')

    rmdir(sub_done, 'dir')
    assert 'dir' not in ls(sub_done)
