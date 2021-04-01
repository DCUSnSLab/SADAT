class Importer:
    @classmethod
    def importerLibrary(cls, _from, _library=None):
        lib = None
        try:
            if _library is None:
                lib = __import__(_from)
            else:
                _tmp = __import__(_from, fromlist=[_library])
                lib = getattr(_tmp, _library)
        except Exception as e:
            print('import Failed')

        return lib