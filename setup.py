DESCRIPTION = "pymirai"

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development
Typing :: Typed
Operating System :: OS Independent
"""

INSTALL_REQUIREMENTS = """
py4j>=0.10
"""


def setup_pkg():
    import setuptools

    metadata = dict(
        name="myrai",
        version="0.0.2",
        author="Rebuild",
        author_email="admin@rebuild.moe",
        license="AGPLv3",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/Shimogawa/myrai",
        classifiers=[_f for _f in CLASSIFIERS.split("\n") if _f],
        python_requires=">=3.9",
        install_requires=[_f for _f in INSTALL_REQUIREMENTS.split("\n") if _f],
        package_dir={"": "py_src"},
        packages=setuptools.find_packages("py_src"),
        package_data={"myrai": ["resources/*.jar", "*.pyi", "py.typed"]},
        include_package_data=True,
    )

    setuptools.setup(**metadata)


if __name__ == "__main__":
    setup_pkg()
