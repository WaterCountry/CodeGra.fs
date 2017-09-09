import pytest

from helpers import isdir, isfile, join, ls, mkdir, rm, rm_rf, rmdir


@pytest.fixture(autouse=True)
def username():
    yield 'stupid1'


@pytest.fixture(autouse=True)
def password():
    yield 'Stupid1'


def test_list_courses(mount_dir):
    assert isdir(mount_dir)
    for course in ['Inleiding Programmeren', 'Programmeertalen']:
        assert isdir(mount_dir, course)


def test_list_assignments(mount_dir):
    course_dir = join(mount_dir, 'Programmeertalen')

    assert isdir(mount_dir)
    assert isdir(course_dir)

    for assig in ['Haskell', 'Go', 'Python', 'Shell']:
        assert isdir(course_dir, assig)


def test_list_submissions(mount_dir):
    course_dir = join(mount_dir, 'Programmeertalen')
    assert isdir(mount_dir)
    assert isdir(course_dir)

    for assig in ls(course_dir):
        for sub in ls(course_dir, assig):
            assert 'Stupid1' in sub


def test_create_files(mount_dir, sub_open, sub_done):
    with open(join(sub_open, 'file1'), 'w') as f:
        pass

    assert isfile(sub_open, 'file1')

    with open(join(sub_open, 'file2'), 'w') as f:
        f.write('abc\n')
    assert isfile(sub_open, 'file2')

    with pytest.raises(PermissionError):
        with open(join(sub_done, 'file1'), 'w') as f:
            pass
    assert not isfile(sub_done, 'file1')

    with pytest.raises(PermissionError):
        with open(join(sub_done, 'file1'), 'w') as f:
            f.write('abc\n')
    assert not isfile(sub_done, 'file1')


def test_write_and_read_files(mount_dir, sub_open, sub_done):
    with open(join(sub_open, 'file1'), 'a') as f:
        f.write('abc\n')
    assert isfile(sub_open, 'file1')

    with open(join(sub_open, 'file1'), 'r') as f:
        assert f.read() == 'abc\n'

    with open(join(sub_open, 'file1'), 'w') as f:
        f.write('def\n')
    with open(join(sub_open, 'file1'), 'r') as f:
        assert f.read() == 'def\n'

    with open(join(sub_open, 'file1'), 'a') as f:
        f.write('def\n')
    with open(join(sub_open, 'file1'), 'r') as f:
        assert f.read() == 'def\ndef\n'


def test_delete_files(mount_dir, sub_open, sub_done):
    with open(join(sub_open, 'file1'), 'w') as f:
        f.write('abc\n')
    assert isfile(sub_open, 'file1')

    with open(join(sub_open, 'file1'), 'r') as f:
        assert f.read() == 'abc\n'

    rm(sub_open, 'file1')
    assert not isfile(sub_open, 'file1')

    with pytest.raises(FileNotFoundError):
        rm(sub_open, 'nonexisting')


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
        mkdir(sub_done, 'dir')
    assert isdir(sub_done, 'dir')

    with pytest.raises(PermissionError):
        rm_rf(sub_done, 'dir')

    assert isdir(sub_done, 'dir')
    assert isfile(sub_done, 'dir', 'single_file_work')
    assert isfile(sub_done, 'dir', 'single_file_work_copy')

    with pytest.raises(IsADirectoryError):
        rm(sub_open, 'dir')
    with pytest.raises(OSError):
        rmdir(sub_open, 'dir')
    assert isdir(sub_open, 'dir')

    rm_rf(sub_open, 'dir')

    assert 'dir' not in ls(sub_open)

    mkdir(sub_open, 'dir')
    assert isdir(sub_open, 'dir')

    rmdir(sub_open, 'dir')
    assert 'dir' not in ls(sub_open)
