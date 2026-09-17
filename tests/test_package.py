def test_package_import():
    """Verify that the topography_intel package can be imported."""

    # Importing the package is the minimum structural smoke test.
    # A failure here indicates a packaging, source-layout, or initialization
    # problem before any topographic calculation is executed.
    import topography_intel

    # Confirm that Python resolved and loaded the package successfully.
    assert topography_intel is not None
