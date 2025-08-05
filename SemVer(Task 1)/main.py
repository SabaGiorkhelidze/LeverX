# class Version:
#     def __init__(self, version):
#         self.original = version
#         self.version = version.split("+")[0]

#         if '-' in version:
#             base, prerelease = version.split('-', 1)
#             prerelease_version = prerelease.split('.')
#         else:
#             base, prerelease_version = version, []

#         base_version_split = base.split('.')  # [1, 0, 1]

#         self.major = int(base_version_split[0])
#         self.minor = int(base_version_split[1])
#         self.patch = int(base_version_split[2])
#         self.prerelease = prerelease_version[0] if len(prerelease_version) > 0 else None 
        
        
#         # ['alpha', 'beta', '2', '3', '4', 'beta', 'alpha'] [alpha, 1] [beta, 1, 4] 
#         for i in range(len(prerelease_version)):
#             if self.prerelease[i].isdigit():
#                 self.prerelease[i] = int(self.prerelease[i])
                
#         self.info = {
#             "major": self.major,
#             "minor": self.minor,
#             "patch": self.patch,
#             "prerelease": self.prerelease
            
#         }
#     def match_version(self):
#         pass



# versions = [
#     "1.2.0-alpha.1",
#     "2.0.5",
#     "3.1.4-beta",
#     "0.1.0-rc.7+build567",
#     "4.2.1",
#     "1.0.0-alpha"
# ]

# for v in versions:
#     try:
#         ver = Version(v)
#         print(f"{v} → {ver.info}")
#     except Exception as e:
#         print(f"{v} → ERROR: {e}")


 
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
        
        
        if not self.prerelease and other.prelease:
            return True
        if not self.prerelease and not other.prerelease:
            return False
        if self.prerelease and not other.prelease:
            return False
        
        
        for s, o in zip(self.prerelease, other.prerelease):
            pass
        
        
        
        
        
    
    def __lt__(self, value):
        pass
    


def test_comparisons():
    print("🧪 Simple Version Comparison Tests\n")

    test_cases = [
        ("1.0.0", "2.0.0"),           # v1 < v2
        ("2.0.0", "1.0.0"),           # v1 > v2
        ("1.2.3", "1.2.3"),           # v1 == v2
        ("1.2.3", "1.2.4"),           # v1 < v2
        ("1.0.0-alpha", "1.0.0"),     # v1 < v2
        # ("1.0.0-beta.2", "1.0.0-beta.1"),  # v1 > v2
        # ("1.0.0-alpha.1", "1.0.0-alpha.beta"),  # v1 < v2
        # ("1.0.0-alpha", "1.0.0-alpha"),        # v1 == v2
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