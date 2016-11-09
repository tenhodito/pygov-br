from .__meta__ import __author__, __version__  # noqa: F401
from .lazy_datasource import DataSourceNode as _mk_lazy_data_source

data = _mk_lazy_data_source()
