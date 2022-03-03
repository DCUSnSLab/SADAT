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
            print('========import Failed=============')
            libp = _library
            if _library is None:
                libp = ""
            #print('There is no library -> %s : %s'%(_from, libp))
            raise Exception('There is no library -> %s : %s'%(_from, libp))

        return lib


    @classmethod
    def checkVispy(cls):
        try:
            import vispy
            from vispy.gloo import gl
            vispy.sys_info()
            version = gl.glGetParameter(gl.GL_VERSION)
            #print('GL version:  %r\n' % (gl.glGetParameter(gl.GL_VERSION),))
            return True
        except:
            return False