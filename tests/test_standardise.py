from amocarray import logger, readers, standardise, utilities

logger.disable_logging()


def test_standardise_samba():
    # Load datasets (could be one or two files)
    datasets = readers.load_dataset("samba")

    # Load metadata from the YAML to match expectations
    meta = utilities.load_array_metadata("samba")
    global_meta = meta["metadata"]
    file_metas = meta["files"]

    for ds in datasets:
        file_name = ds.attrs.get("source_file")
        assert file_name in file_metas, f"Missing metadata for file: {file_name}"

        # Standardise the dataset
        std_ds = standardise.standardise_samba(ds, file_name)

        # Global metadata keys expected
        for key in ["weblink", "summary"]:
            assert key in std_ds.attrs, f"Missing global attribute: {key}"

        # Check if data_product or acknowledgement were added if in the YAML
        for key in ["data_product", "acknowledgement"]:
            if key in file_metas[file_name]:
                assert key in std_ds.attrs

        # Variables renamed and enriched
        variable_mapping = file_metas[file_name].get("variable_mapping", {})
        expected_vars = list(variable_mapping.values())

        for var in expected_vars:
            assert var in std_ds.variables, f"Expected variable not found: {var}"
            attrs = std_ds[var].attrs
            for attr in ["units", "standard_name"]:
                assert attr in attrs, f"Missing {attr} for variable: {var}"
