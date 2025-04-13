
import pathlib
import sys

script_dir = pathlib.Path(__file__).parent.absolute()
parent_dir = script_dir.parents[0]
sys.path.append(str(parent_dir))

from amocarray import readers, standardise


def test_standardise_samba():
    datasets = readers.load_dataset("samba")
    for ds in datasets:
        std_ds = standardise.standardise_samba(ds, ds.attrs["source_file"])
        assert "weblink" in std_ds.attrs
        assert any(var in std_ds.variables for var in ["MOC", "UPPER_TRANSPORT"])