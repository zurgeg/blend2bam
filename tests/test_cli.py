import os
import sys

import pytest

import blend2bam
import blend2bam.cli
from blend2bam import blenderutils


TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')
TESTBLEND = os.path.join(SRCDIR, 'test.blend')


def run_cli_test(tmpdir, src=TESTBLEND, extra_args=None):
    dst = os.path.join(tmpdir, 'output.bam')
    args = [
        'python'
    ]
    if extra_args:
        args += extra_args
    args += [
        src, dst
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'output.bam'))


def test_cli_single(tmpdir):
    run_cli_test(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))


def test_cli_relative(tmpdir):
    args = [
        'python',
        os.path.relpath(os.path.join(SRCDIR, 'test.blend')),
        os.path.relpath(os.path.join(tmpdir, 'output.bam')),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'output.bam'))


def test_cli_single_to_dir(tmpdir):
    args = [
        'python',
        os.path.relpath(os.path.join(SRCDIR, 'test.blend')),
        str(tmpdir),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'test.bam'))


def test_cli_dir_to_dir(tmpdir):
    args = [
        'python',
        SRCDIR,
        str(tmpdir),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'test.bam'))

def test_cli_many_to_dir(tmpdir):
    args = [
        'python',
        os.path.join(SRCDIR, 'test.blend'),
        os.path.join(SRCDIR, 'test2.blend'),
        str(tmpdir),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert not os.path.exists(os.path.join(tmpdir, 'test2gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'test.bam'))
    assert os.path.exists(os.path.join(tmpdir, 'test2.bam'))

def test_cli_physics_builtin(tmpdir):
    run_cli_test(tmpdir, src=os.path.join(SRCDIR, 'physics.blend'), extra_args=[
        '--physics-engine', 'builtin'
    ])

def test_cli_physics_bullet(tmpdir):
    run_cli_test(tmpdir, src=os.path.join(SRCDIR, 'physics.blend'), extra_args=[
        '--physics-engine', 'bullet'
    ])

def test_cli_pipeline_egg(tmpdir):
    if blenderutils.is_blender_28():
        pytest.skip('EGG pipeline not supported with blender 2.8')
    run_cli_test(tmpdir, extra_args=[
        '--pipeline', 'egg'
    ])
    assert not os.path.exists(os.path.join(tmpdir, 'test.egg'))

def test_cli_blender_dir(tmpdir):
    with pytest.raises(SystemExit):
        run_cli_test(tmpdir, extra_args=[
            '--blender-dir', 'tests',
        ])

def test_cli_no_srgb(tmpdir):
    run_cli_test(tmpdir, extra_args=[
        '--no-srgb',
    ])

def test_cli_textures_ref(tmpdir):
    run_cli_test(tmpdir, extra_args=[
        '--textures=ref',
    ])

def test_cli_textures_copy(tmpdir):
    run_cli_test(tmpdir, extra_args=[
        '--textures=copy',
    ])

def test_cli_textures_embed(tmpdir):
    run_cli_test(tmpdir, extra_args=[
        '--textures=embed',
    ])
