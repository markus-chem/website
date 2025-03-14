r"""
Utilities to work with remote data packages.
"""
# ********************************************************************
#  This file is part of echemdb.
#
#        Copyright (C) 2021 Albert Engstfeld
#        Copyright (C) 2021 Johannes Hermann
#        Copyright (C) 2021 Julian Rüth
#        Copyright (C) 2021 Nicolas Hörmann
#
#  echemdb is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  echemdb is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with echemdb. If not, see <https://www.gnu.org/licenses/>.
# ********************************************************************

from functools import cache

@cache
def collect_datapackages(data=".", url="https://github.com/echemdb/website/archive/refs/heads/gh-pages.zip", outdir=None):
    r"""
    Return a list of data packages defined in a remote location.

    The default is to download the packages currently available on echemdb and
    extract them to a temporary directory.

    EXAMPLES::

        >>> packages = collect_datapackages()

    """
    if outdir is None:
        import tempfile
        import atexit
        import shutil

        outdir = tempfile.mkdtemp()
        atexit.register(lambda dirname: shutil.rmtree(dirname), outdir)

    from urllib.request import urlopen
    response = urlopen(url)

    from zipfile import ZipFile
    from io import BytesIO
    compressed = ZipFile(BytesIO(response.read()))

    compressed.extractall(outdir, members=[name for name in compressed.namelist() if name.endswith('.json') or name.endswith('.csv')])

    import os.path
    import echemdb.data.local
    return echemdb.data.local.collect_datapackages(os.path.join(outdir, data))
