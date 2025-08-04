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

        if '-' in version:
            base, prerelease = version.split('-', 1)
            full_prerelease_version = prerelease.split('.')
        else:
            base, full_prerelease_version = version, []

        base_version_split = base.split('.')  # [1, 0, 1]
        self.major = int(base_version_split[0])
        self.minor = int(base_version_split[1])
        self.patch = int(base_version_split[2])

        self.prerelease = full_prerelease_version
        
        for i in range(len(full_prerelease_version)):
            if self.prerelease[i].isdigit():
                self.prerelease[i] = int(self.prerelease[i])

        self.info = {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "prerelease": self.prerelease
        }

    
    def __eq__(self, value):
        pass
    
    def __gt__(self, value):
        pass
    
    def __lt__(self, value):
        pass
    
    


versions = [
    "1.2.0-alpha.1",
    "2.0.5",
    "3.1.4-beta",
    "0.1.0-rc.7+build567",
    "4.2.1",
    "1.0.0-alpha",
    "1.0.10-alpha.beta.2.3.4.beta.alpha",  # Custom case
]

for v in versions:
    try:
        ver = Version(v)
        print(f"{v} → {ver.info}")
    except Exception as e:
        print(f"{v} → ERROR: {e}")
