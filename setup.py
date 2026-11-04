"""Setup for pdf XBlock."""

import os
import re
from pathlib import Path

from setuptools import setup

ROOT = Path(__file__).resolve().parent


def get_version():
    """Read the version without importing Django or the XBlock runtime."""
    source = (ROOT / 'pdf' / '__init__.py').read_text(encoding='utf-8')
    match = re.search(r"^__version__ = ['\"]([^'\"]+)['\"]", source, re.MULTILINE)
    if match is None:
        raise RuntimeError('Unable to find the PDF XBlock version.')
    return match.group(1)


def runtime_requirements():
    """Load unpinned runtime requirements, independently of test constraints."""
    return [
        line.strip() for line in (ROOT / 'requirements' / 'base.in').read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.lstrip().startswith('#')
    ]


def package_data(pkg, root_list):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for root in root_list:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock-pdf',
    version=get_version(),
    description='Course component (Open edX XBlock) that provides an easy way to embed a PDF',
    packages=[
        'pdf',
    ],
    install_requires=runtime_requirements(),
    entry_points={
        'xblock.v1': [
            'pdf = pdf.pdf:PdfBlock',
        ]
    },
    package_data=package_data('pdf', ['static', 'templates', 'translations']),
)
