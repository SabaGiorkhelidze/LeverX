class Version:
    def __init__(self, version):
        self.original = version
        self.version = version.split("+")[0]
        prerelease = ''
        
        if '-' in version:
            base, prerelease = version.split('-', 1)
            full_prerelease_version = prerelease.split('.')
        else:
            base, full_prerelease_version = version, []

        base_version_split = base.split('.')  # [1, 0, 1]
        self.major = int(base_version_split[0])
        self.minor = int(base_version_split[1])
        self.patch = int(base_version_split[2])

        self.prerelease = [int(p) if p.isdigit() else p for p in prerelease.split(".")] if prerelease else []
        
        

        self.info = {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "prerelease": self.prerelease
        }

    
    def __eq__(self, other):
        return (self.major, self.minor, self.patch, self.prerelease) == (other.major, other.minor, other.patch, other.prerelease)
    
    def __gt__(self, other):
        
        if self.major != other.major:
            return self.major > other.major
        if self.minor != other.minor:
            return self.minor > other.minor
        if self.patch != other.patch:
            return self.patch > other.patch
        
        
        if not self.prerelease and other.prerelease:
            return True
        if not self.prerelease and not other.prerelease:
            return False
        if self.prerelease and not other.prerelease:
            return False
        
        
        for s, o in zip(self.prerelease, other.prerelease):
            if s == o:
                continue
            if (isinstance(s, int) and isinstance(o, int)) or (isinstance(s, str) and isinstance(o, str)):
                return s > o
            return isinstance(s, int) 
        
        return len(self.prerelease) > len(other.prerelease)
        
        
    
    def __lt__(self, other):
        return not (self > other or self == other)
    


def test_comparisons():
    print("🧪 Simple Version Comparison Tests\n")

    test_cases = [
        ("1.0.0", "2.0.0"),           # v1 < v2
        ("2.0.0", "1.0.0"),           # v1 > v2
        ("1.2.3", "1.2.3"),           # v1 == v2
        ("1.2.3", "1.2.4"),           # v1 < v2
        ("1.0.0-alpha", "1.0.0"),     # v1 < v2
        ("1.0.0-beta.2", "1.0.0-beta.1"),  # v1 > v2
        ("1.0.0-alpha.1", "1.0.0-alpha.beta"),  # v1 < v2
        ("1.0.0-alpha", "1.0.0-alpha"),        # v1 == v2
    ]

    for left, right in test_cases:
        v1 = Version(left)
        v2 = Version(right)

        print(f"Comparing: {left}  vs  {right}")
        print("  v1 < v2 :", v1 < v2)
        print("  v1 > v2 :", v1 > v2)
        print("  v1 == v2:", v1 == v2)
        print()

test_comparisons()