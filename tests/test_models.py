from zosmfrestapi.models import DataSet
from zosmfrestapi._utils import to_dict


def test_to_dict_converts_dictionary_values():
    data = {"dataset": DataSet(dsname="TEST.DATA", volume="VOL001")}

    assert to_dict(data) == {"dataset": {"dsname": "TEST.DATA", "volume": "VOL001"}}
