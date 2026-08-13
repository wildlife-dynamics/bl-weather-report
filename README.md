# BL Weather Report — User Guide

This guide walks you through configuring and running the Big Life Weather Report workflow, which ingests rainfall gauge observations from EarthRanger, derives NDVI vegetation condition from Google Earth Engine, and produces an automated weather report and dashboard for the Amboseli ecosystem.

---

## Overview

The workflow delivers, for each run:

- An **overall rainfall bar chart** — total millimetres per gauge station for the analysis period
- A **monthly stacked bar chart** — month-by-month rainfall breakdown per station, ordered by calendar month
- A **rainfall by station summary table** — sortable, filterable table of total readings per station
- An **interactive rainfall map** — Amboseli land use, ranch boundaries, and electric fence layers, with a clustered proportional-symbol layer of rainfall readings per station
- **Per-ranch NDVI time-series charts** — current NDVI overlaid against the historic min/max/mean range, one chart per ranch in the Amboseli conservancy boundaries
- A **data file** — aggregated station rainfall readings with point geometry (GeoParquet)
- A **Word document report** — all charts and the map embedded in the Big Life weather report template, downloaded automatically from Dropbox
- An **interactive dashboard** — widgets for the rainfall map, the overall rainfall chart, the monthly rainfall chart, and the rainfall-by-station table (NDVI charts are not included on the dashboard — they appear only in the Word report)

The three Amboseli geospatial layers (land use, ranch boundaries & electric fence, conservancy boundaries) and the Word report template are downloaded automatically from Dropbox at run time. No additional setup is required for these.

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with `rainfall_rep` events logged for the analysis period
- Access to a **Google Earth Engine** service account with a private key in JSON format

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/bl_weather_report.git
```

Then click **Add Template**.

![Add Workflow Template](data/screenshots/add_workflow.png)

---

### Step 2 — Configure Connection

Navigate to **Data Sources** and click **Connect**. A dialog will appear prompting you to **Select Data Source Type**. This workflow requires two connections:

| Data Source Type | Purpose |
|-----------------|---------|
| **EarthRanger** | Pull rainfall gauge events (`rainfall_rep`) |
| **Google Earth Engine** | Compute per-ranch NDVI time-series against historic baselines |

Select **EarthRanger** first and complete Step 3, then repeat and select **Google Earth Engine** for Step 4.

![Configure Connection](data/screenshots/configure_connection.png)

---

### Step 3 — Add an EarthRanger Connection

After selecting **EarthRanger** in Step 2, fill in the connection form:

- **Data Source Name** — a label to identify this connection
- **EarthRanger URL** — your instance URL (e.g. `your-site.pamdas.org`)
- **EarthRanger Username** and **EarthRanger Password**

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

Click **Connect** to save.

![EarthRanger Connection](data/screenshots/er_connection.png)

---

### Step 4 — Add a Google Earth Engine Connection

After selecting **Google Earth Engine** in Step 2, fill in the connection form:

- **Data Source Name** — a label to identify this connection
- **Private Key** — click **Browse** to select your GEE service account private key file (JSON format)

> To generate a private key, follow the instructions in the [Setup Guide](https://developers.google.com/earth-engine/guides/service_account). The key is stored encrypted and used only to authenticate with Google Earth Engine.

Click **Connect** to save.

![Google Earth Engine Connection](data/screenshots/gee_connection.png)

---

### Step 5 — Select the Workflow

After the template is added, it appears in the **Workflow Templates** list as **bl_weather_report**. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

![Select Workflow Template](data/screenshots/select_workflow.png)

---

### Step 6 — Set Workflow Details and Time Range

The configuration form opens with two sections at the top.

**Set Workflow Details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes (e.g. month, ranger station, or site name) |

**Time Range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time of the analysis period |
| Until | End date and time of the analysis period |

Rainfall events and NDVI data are both fetched for this window.

![Set Workflow Details and Time Range](data/screenshots/workflow_details_time_range.png)

---

### Step 7 — Set GEE Connection, Connect to ER, and NDVI Method

Scroll down to configure the next three sections.

**Set GEE connection**

Select the Google Earth Engine data source configured in Step 4 from the **Data Source** dropdown.

**Connect to ER**

Select the EarthRanger data source configured in Step 3 from the **Data Source** dropdown (e.g. `Amboseli Trust for Elephants`).

**NDVI Method**

Choose the MODIS satellite product to use for NDVI calculations:

| Option | Description |
|--------|-------------|
| **MODIS MYD13A1 16-Day Composite** *(default)* | Pre-calculated NDVI from 16-day composites. Quality-filtered best-pixel values at 500 m resolution with ~0.025 accuracy. Better for phenology studies but may saturate in dense canopies. |
| **MODIS MCD43A4 Daily NBAR** | Computes NDVI from NIR/Red bands with view-angle correction for consistent measurements. Higher temporal resolution but more susceptible to cloud gaps. |

![Set GEE Connection, Connect to ER, and NDVI Method](data/screenshots/set_gee_connection_er_ndvi_method.png)

---

### Step 8 — NDVI Trend

Configure how historical NDVI data is grouped when computing the baseline statistics (min, max, mean) that the current period is compared against:

| Grouping Unit | Behaviour |
|--------------|-----------|
| **month** *(default)* | Compare against the same calendar month (1–12) |
| **week** | Compare against the same ISO week number (1–53) |
| **day_of_year** | Compare against the same day of year (1–366) |
| **modis_16_day** | Compare against the same MODIS 16-day composite period (0–22) |

NDVI is calculated separately for each ranch in the Amboseli conservancy boundaries, grouped by the `R_NAME` field.

![NDVI Method and NDVI Trend](data/screenshots/ndvi_method_trend_persist.png)

---

## Running the Workflow

Once all parameters are configured, click **Submit**. The runner will:

1. Download the three Amboseli geospatial layers (land use, ranch boundaries & electric fence, conservancy boundaries) from Dropbox and reproject them to EPSG:4326.
2. Style the land-use layer by category and build the ranch-boundary and electric-fence map layers.
3. Fetch `rainfall_rep` events from EarthRanger for the specified time range, extract the digital and manual rain-gauge readings from each event's details, and combine them into a single reading per event (falling back to the manual gauge, then to zero).
4. Aggregate rainfall readings by gauge station (sum) and decompose event dates into year, month, and month name for later charting.
5. Render the overall rainfall bar chart, the calendar-ordered monthly stacked bar chart, and the sortable/filterable rainfall-by-station summary table.
6. Build a clustered rainfall reading layer and combine it with the land-use, boundary, and fence layers into an interactive map, automatically framed to the data extent.
7. Split the Amboseli conservancy boundaries by ranch name (`R_NAME`) and run NDVI analysis per ranch via Google Earth Engine, then render a historic NDVI time-series chart for each ranch.
8. Convert the rainfall charts, the monthly chart, the map, and each ranch's NDVI chart to PNG.
9. Download the Big Life weather report Word template from Dropbox and populate it with the charts, the map, and the per-ranch NDVI charts.
10. Assemble the dashboard with the rainfall map, overall rainfall chart, monthly rainfall chart, and rainfall-by-station table widgets.
11. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`:

| File | Description |
|------|-------------|
| `overall_rainfall_station_readings` (GeoParquet) | Total rainfall per station, with point geometry |
| `rainfall_readings_over_time.html` / `.png` | Overall rainfall bar chart by station |
| `monthly_rainfall_readings.html` / `.png` | Monthly stacked rainfall bar chart, ordered by calendar month |
| `rainfall_by_station_summary_table.html` | Sortable, filterable rainfall-by-station summary table |
| `rainfall_map.html` / `.png` | Interactive map: land use, ranch boundaries, electric fence, and rainfall readings |
| `<ranch>.html` / `.png` (one per ranch) | Historic NDVI time-series chart — current NDVI vs. historic min/max/mean |
| `overall_report.docx` | Final populated Big Life weather report Word document |
