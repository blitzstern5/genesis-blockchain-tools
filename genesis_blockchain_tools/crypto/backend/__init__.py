import os
import sys

def load_module_by_path(module_name, path): 
    if sys.version_info[0] == 2:
        import imp
        foo = imp.load_source(module_name, path)
    elif sys.version_info[0] == 3:
        if sys.version_info[1] < 5:
            from importlib.machinery import SourceFileLoader
            foo = SourceFileLoader(module_name, path).load_module()
        else:
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, path)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
    return foo        

__BACKEND_NAMES = ('fastecdsa', 'cryptography', 'ecdsa', 'ecpy', 'rubenesque')
__EXPORTED_NAMES = ('gen_private_key', 'get_public_key', 'gen_keypair', 'sign',
                    'backend_name')

def import_crypto_by_backend(name):
    basedir = os.path.abspath(os.path.dirname(__file__))
    if not name in __BACKEND_NAMES:
        raise ImportError("%s crypto backend isn't available" % name)
    path = basedir
    l = []
    for i in range(0, 3):
        path, part = os.path.split(path)
        l.insert(0, part)
    l.append(name)
    return load_module_by_path('.'.join(l), os.path.join(basedir, name + '.py'))

def get_backend_names():
    return __BACKEND_NAMES

def get_available_backend_names():
    l = []
    for name in __BACKEND_NAMES:
        try:
            __import__(name)
            l.append(name)
        except ImportError as e:
            pass
    return tuple(l)

def get_first_available_backend_name():
    for name in __BACKEND_NAMES:
        try:
            __import__(name)
            return name
        except ImportError as e:
            pass

def get_first_available_backend_module():
    name = get_first_available_backend_name()
    if not name:
        raise ImportError("None of %s ECDSA modules found" % ', '.join(__BACKEND_NAMES))
    return import_crypto_by_backend(name)

def import_backend_namespace(mod, names=tuple()):
    for name in names:
        globals()[name] = getattr(mod, name)

def import_first_available_backend_namespace():
    mod =  get_first_available_backend_module()
    import_backend_namespace(mod, __EXPORTED_NAMES)

if __name__ == '__main__':
    pass
else:
    backend_name = get_first_available_backend_name()
    import_first_available_backend_namespace()
