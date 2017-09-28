from packaging.specifiers import SpecifierSet
from packaging.version import Version


class PackageReleases(object):
    '''
    Represents released versions of a package, like: six-1.0, six-1.1.
    '''

    def __init__(self, name, versions):
        self.name = name
        self.versions = set(versions)

    def __repr__(self):
        return '<%s name=%r, versions=%r>' % (
            self.__class__.__name__,
            self.name,
            self.versions,
        )

    def __eq__(self, other):
        if not type(other) == self.__class__:
            return False

        return all((
            self.name == other.name,
            self.versions == other.versions,
        ))

    def __ne__(self, other):
        return not self.__eq__(other)

    def as_display_name_single(self):
        if len(self.versions) != 1:
            raise ValueError("Cannot display - need single version")

        return '%s-%s' % (self.name, list(self.versions)[0])

    def get_more_recent_than_requirement(self, package_requirement):
        released_versions = [Version(ver) for ver in self.versions]
        requirement_version = Version(package_requirement.version)

        released_versions.sort()
        newer_versions = [ver for ver in released_versions
                          if ver > requirement_version]

        if newer_versions:
            newest_version = newer_versions[-1].base_version
            return self.__class__(
                name=self.name,
                versions=set((newest_version,)),
            )
