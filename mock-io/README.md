# Mock-IO data

Synthetic example returns for the IO tasks, used by the `mock_io` test cases in
`test-cases.yaml` (see `.github/workflows/test.yml`, which points the
`WT_TASK_MOCK_IO__…` environment variables at these files).

They have the same columns and types as the real EarthRanger rainfall events and
Earth Engine NDVI table, but the station names, readings and dates are made up.
Locations are points inside the public Amboseli group-ranch polygons.

| File | Mocks |
|---|---|
| `get-events.example-return.parquet` | `ecoscope.platform.tasks.io.get_events` |
| `process-events-details.example-return.parquet` | `ecoscope.platform.tasks.io.process_events_details` |
| `calculate-ndvi-range.example-return.parquet` | `ecoscope.platform.tasks.io.calculate_ndvi_range` |
