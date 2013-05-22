from ethel.chroot import schroot, copy, scmd, get_tarball
import os


def piuparts(chroot, package):
    tarball = get_tarball(chroot)

    name = os.path.basename(tarball)
    internal_path = "/tmp/%s" % (name)

    package_name = os.path.basename(package)
    internal_package = "/tmp/%s" % (package_name)

    with schroot(chroot) as session:

        copy(session, tarball, internal_path)
        copy(session, package, internal_package)

        print("Installing...")
        scmd(session, [
            'apt-get', 'install', '-y', 'piuparts'
        ], user='root')

        print("Piuparts installed.")
        out, ret = scmd(session, [
            'piuparts', '-b', internal_path, internal_package
        ], user='root')
        print(out)


def main():
    import sys
    piuparts(*sys.argv[1:])
