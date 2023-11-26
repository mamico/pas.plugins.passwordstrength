# -*- coding: utf-8 -*-
"""Installer for the pas.plugins.passwordstrength package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.md").read(),
        open("CONTRIBUTORS.md").read(),
        open("CHANGES.md").read(),
    ]
)


setup(
    name="pas.plugins.passwordstrength",
    version="1.0a1",
    description="Adds verification rules for user passwords in plone.",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Mauro Amico",
    author_email="mauro.amico@gmail.com",
    url="https://github.com/collective/pas.plugins.passwordstrength",
    project_urls={
        "PyPI": "https://pypi.org/project/pas.plugins.passwordstrength/",
        "Source": "https://github.com/collective/pas.plugins.passwordstrength",
        "Tracker": "https://github.com/collective/pas.plugins.passwordstrength/issues",
        # 'Documentation': 'https://pas.plugins.passwordstrength.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["pas", "pas.plugins"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "plone.api>=1.8.4",
        "plone.app.dexterity",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
         ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
