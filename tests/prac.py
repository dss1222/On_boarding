try:
    from unittest import mock
except ImportError:
    import mock

m = mock.Mock()
m.some_attribute = "hello world"
print(m.some_attribue)
