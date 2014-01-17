VERSION = (1, 3, 4, 'mmf', 0)
from datetime import datetime
import os
import subprocess


def get_version_file():
    directory = os.path.dirname(os.path.abspath(__file__))
    return directory + os.sep + "RELEASE_VERSION"


def get_version(release=False):
    if not release:
        try:
            f = open(get_version_file(), "r")

            try:
                version = f.readlines()[0]
                return version.strip()

            finally:
                f.close()
        except:
            pass
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            now = datetime.now()
            version = ' '.join((version, VERSION[3], now.strftime('%Y%m%d %H%M%S'), get_git_changeset()))
    if release:
        write_release_version(version)
    return version


def write_release_version(version):
    f = open(get_version_file(), "w")
    f.write("%s\n" % version)
    f.close()


def get_git_changeset():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen('git log --pretty=format:%H --quiet -1 HEAD',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=repo_dir, universal_newlines=True)
    return git_log.communicate()[0]
