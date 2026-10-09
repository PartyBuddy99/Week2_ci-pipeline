from backup import build_key, upload_files

class FakeS3:
    def __init__(self):
        self.calls = []
    def upload_file(self, local_path, bucket, key):
        self.calls.append((local_path, bucket, key))

def test_upload_files():
    fake = FakeS3()
    result = upload_files(fake, "backup_test", "my-bucket", "backup", "20261003")
    assert sorted(result) == ["backup/20261003/a.txt", "backup/20261003/b.txt", "backup/20261003/c.txt"]
    assert len(fake.calls) == 3

test_upload_files()
print("upload test passed")