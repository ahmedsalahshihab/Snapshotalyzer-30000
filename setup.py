import setuptools

setuptools.setup(name="snapshotalyzer-30000",
                 version="0.1",
                 author="Ahmed Shihab",
                 author_email="ahmed.salah.shihab@gmail.com",
                 description="SnapshotAlyzer 30000 is a tool to manage AWS EC2 snapshots",
                 packages=["shotty"],
                 url="https://github.com/ahmedsalahshihab/Snapshotalyzer-30000.git",
                 install_requires=[
                     "click",
                     "boto3",
                     "botocore"],
                 entry_points='''
                    [console_scripts]
                    shotty=shotty.shotty:cli
                    ''',
                 )
