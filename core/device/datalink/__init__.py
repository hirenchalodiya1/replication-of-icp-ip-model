import settings
from core.utils import load_class

klass = load_class(settings.ERROR_CHECKING)
print(klass("100", "1001").codeword())
