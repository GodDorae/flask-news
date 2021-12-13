from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xb2\xf0\xe3Hs\x80\xca\xe2\xc7\x14\xdb\x81\xe4\xf9\x1e\xcc'