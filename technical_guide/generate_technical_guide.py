"""
Generate the BL Weather Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: bl_weather_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date

OUTPUT_FILE = "bl_weather_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
GREEN_LIGHT = colors.HexColor("#d8f3dc")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)

H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")

BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10,
                  bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)
def code(text):          return Paragraph(text, CODE)

def c(text):
    """Wrap text in a Paragraph for use inside Table cells."""
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


# ── Page template ──────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "BL Weather Report — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="BL Weather Report — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("BL Weather Report", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Rainfall Monitoring &amp; NDVI Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"),
        hr(),
        p(
            "The <b>BL Weather Report</b> workflow is a data-to-report pipeline built "
            "for Big Life Foundation's rainfall monitoring programme in the Amboseli "
            "ecosystem. It ingests rainfall gauge observations from <b>EarthRanger</b>, "
            "derives vegetation condition from <b>Google Earth Engine</b> NDVI time-series, "
            "and delivers a set of charts, an interactive rainfall map, per-ranch NDVI "
            "trend charts, and a print-ready Word report."
        ),
        p(
            "The workflow is implemented as an <b>Ecoscope Workflow</b> (YAML spec) "
            "and executes within the <code>ecoscope-workflows</code> runtime. "
            "NDVI analysis is fanned out per ranch using the <code>mapvalues</code> "
            "directive, grouping by the <code>R_NAME</code> column of the Amboseli "
            "conservancy boundaries GeoDataFrame."
        ),
        sp(4),
        p("The workflow delivers the following outputs per run:"),
        make_table(
            [
                ["Category",         "Outputs"],
                ["Rainfall charts",  "Overall rainfall bar chart (per station), monthly stacked bar chart (per station × month)"],
                ["Rainfall map",     "Interactive proportional-symbol map of readings per station"],
                ["NDVI charts",      "Per-ranch historic NDVI time-series with min/max/mean band (one chart per conservancy)"],
                ["Data files",       "Aggregated station readings (GeoPackage), monthly readings (GeoPackage), per-ranch NDVI CSV"],
                ["Report",           "Word document: Big Life weather report template populated with all charts and map images"],
                ["Dashboard",        "Metadata dashboard (run details, time range, groupers)"],
            ],
            [4*cm, 12.5*cm],
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "All rainfall data is sourced from an <b>EarthRanger</b> instance via "
            "<code>set_er_connection</code>. The workflow fetches events of type "
            "<code>rainfall_rep</code> using <code>get_events</code>. "
            "<code>raise_on_empty: true</code> is set, so the workflow will halt "
            "with an error if no rainfall events are found for the period — "
            "distinguishing a data-availability problem from a genuine zero-reading period."
        ),
        p(
            "The EarthRanger connection is also used to look up the current user's "
            "full name (<code>get_current_user</code> → <code>get_user_full_name</code>), "
            "which is inserted into the <i>Generated by</i> field of the Word report."
        ),

        sp(4), h2("2.2 Google Earth Engine Connection"),
        p(
            "A <b>Google Earth Engine (GEE)</b> service account is required for NDVI "
            "analysis. <code>set_gee_connection</code> stores the project handle, which "
            "is passed to <code>calculate_ndvi_range</code> for each ranch ROI. "
            "GEE credentials must be stored as a JSON private key; see the GEE "
            "Setup Guide for instructions."
        ),

        sp(4), h2("2.3 Static Geospatial Layers"),
        p(
            "Three GeoPackage files are downloaded automatically from Dropbox at "
            "run time. All three are reprojected to <b>EPSG:4326 (WGS 84)</b> "
            "before use."
        ),
        make_table(
            [
                ["File",                                                   "Layer used for",               "Key columns"],
                ["amboseli_ranch_conservancies_layers.gpkg",               "Land-use fill polygons on map", "land_use (5 categories)"],
                ["amboseli_group_ranch_boundaries_x_electric_fence.gpkg",  "Ranch boundaries + electric fence lines on map", "land_use (Ranch boundaries, Electric Fence)"],
                ["amboseli_group_ranch_boundaries.gpkg",                   "ROI polygons for per-ranch NDVI calculation", "R_NAME (ranch / conservancy name)"],
            ],
            [5.5*cm, 5.5*cm, 5.5*cm],
        ),

        sp(4), h2("2.4 Base Map Tile Layers"),
        p("Every map uses two stacked tile services:"),
        make_table(
            [
                ["Layer",                    "URL (abbreviated)",                              "Opacity", "Max zoom"],
                ["ESRI World Hillshade",      "arcgisonline.com/…/World_Hillshade/…",          "1.0",     "20"],
                ["ESRI World Street Map",     "arcgisonline.com/…/World_Street_Map/…",         "0.15",    "20"],
            ],
            [4.5*cm, 7*cm, 2*cm, 2.5*cm],
        ),

        sp(4), h2("2.5 Grouping Strategy"),
        p(
            "The grouper is fixed to <code>R_NAME</code> — the ranch / conservancy "
            "name field in the Amboseli boundaries GeoPackage. This column drives the "
            "<code>split_groups</code> fan-out that produces one NDVI chart per ranch. "
            "The temporal index added to rainfall events also uses this grouper."
        ),
    ]

    # ── 3. Rainfall Data Pipeline ─────────────────────────────────────────────
    story += [
        sp(4), h1("3. Rainfall Data Pipeline"), hr(),

        h2("3.1 Event Fetch — rainfall_rep"),
        p(
            "<code>get_events</code> queries EarthRanger for events of type "
            "<code>rainfall_rep</code> within the analysis time range. "
            "<code>include_details: true</code> ensures the <code>event_details</code> "
            "JSON blob is returned, which carries the actual gauge readings. "
            "Only events with a point geometry are included "
            "(<code>include_null_geometry: false</code>)."
        ),
        p("Columns retained per event:"),
        bullet("id, time, event_type, event_category, reported_by, serial_number, geometry, created_at, event_details"),

        sp(4), h2("3.2 JSON Normalisation"),
        p(
            "<code>normalize_json_column</code> flattens the nested "
            "<code>event_details</code> JSON object into individual columns. "
            "The resulting columns follow the pattern "
            "<code>event_details__&lt;key&gt;</code>. "
            "<code>skip_if_not_exists: true</code> makes this step a no-op if the "
            "column is already flat, ensuring robustness across EarthRanger versions. "
            "<code>sort_columns: true</code> reorders the output columns alphabetically "
            "for deterministic downstream access."
        ),

        sp(4), h2("3.3 Column Renaming"),
        p(
            "<code>transform_columns</code> renames the three key fields from their "
            "raw JSON-flattened names to shorter working names:"
        ),
        make_table(
            [
                ["Raw column name",                               "Working name",       "Description"],
                ["event_details__rainfallrep_raingauge_digital",  "digital_readings",   "Reading from the digital rain gauge"],
                ["event_details__rainfallrep_raingauge_manual",   "manual_readings",    "Reading from the manual rain gauge"],
                ["event_details__raingauge_stations",             "raingauge_stations", "Name of the gauge station"],
            ],
            [6*cm, 3.5*cm, 7*cm],
        ),
        p(
            "<code>skip_missing_rename: true</code> suppresses errors if any of these "
            "columns are absent in a given run (e.g. if the EarthRanger event form "
            "schema differs). <code>required_columns</code> is still declared, so the "
            "workflow will warn on missing fields without halting."
        ),

        sp(4), h2("3.4 Combined Readings — Digital / Manual Fallback"),
        p(
            "<code>create_combined_column</code> merges the digital and manual gauge "
            "readings into a single <code>overall_readings</code> column using a "
            "priority fallback strategy:"
        ),
        bullet("<b>Primary:</b> <code>digital_readings</code> — used when available and non-null"),
        bullet("<b>Fallback:</b> <code>manual_readings</code> — used when the digital reading is absent"),
        bullet("<b>fill_remaining: 0</b> — rows where both are null receive a zero reading"),
        p(
            "This design reflects field practice: digital gauges are preferred for "
            "accuracy, but rangers fall back to manual readings when the digital "
            "gauge malfunctions or has not yet been read."
        ),

        sp(4), h2("3.5 Data Cleaning"),
        p("Three sequential cleaning steps ensure numeric integrity:"),
        make_table(
            [
                ["Task",                    "What it does"],
                ["replace_empty_strings",   "Replaces blank raingauge_stations values with 'Unknown', preventing empty-string grouping keys downstream"],
                ["convert_to_float",        "Casts overall_readings to float; non-parseable values are coerced to NaN then filled with 0"],
                ["fill_numeric_nulls",      "Fills any remaining NaN in overall_readings with 0 — ensures the aggregation step receives no nulls"],
            ],
            [4.5*cm, 12*cm],
        ),

        sp(4), h2("3.6 Aggregation by Station"),
        p(
            "<code>groupby_aggregate</code> collapses all events to one row per "
            "gauge station:"
        ),
        make_table(
            [
                ["Column",             "Aggregation",   "Result"],
                ["overall_readings",   "sum",           "Total rainfall in mm recorded at each station for the period"],
                ["geometry",           "first",         "Station point geometry (all readings for a station share the same location)"],
            ],
            [4*cm, 3*cm, 9.5*cm],
        ),
        p(
            "A parallel monthly aggregation branch (<code>group_month_rain</code>) "
            "groups by <code>month_name × raingauge_stations</code> and is used "
            "exclusively for the monthly stacked bar chart."
        ),
    ]

    # ── 4. Chart Outputs ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Chart Outputs"), hr(),

        h2("4.1 Overall Rainfall Bar Chart"),
        p(
            "<code>draw_bar_chart</code> renders a simple bar chart of total "
            "rainfall (mm) per station for the full analysis period."
        ),
        make_table(
            [
                ["Property",      "Value"],
                ["X axis",        "raingauge_stations — one bar per station"],
                ["Y axis",        "overall_readings (sum) — total mm"],
                ["Bar colour",    "#6495ed  (cornflower blue)"],
                ["Plot background","#f5f5f5  (light grey)"],
                ["Legend",        "Hidden (showlegend: false)"],
                ["Bar gap",       "0.1"],
            ],
            [5*cm, 11.5*cm],
        ),

        sp(4), h2("4.2 Monthly Stacked Bar Chart"),
        p(
            "<code>draw_custom_stacked_bar_chart</code> renders a stacked bar chart "
            "showing month-by-month rainfall contributions at each station. "
            "Each stack segment represents one calendar month."
        ),
        h3("Month name derivation"),
        p(
            "<code>return_month_name</code> extracts the month name string "
            "(e.g. <code>'January'</code>) from the <code>time</code> column and "
            "appends it as <code>month_name</code>. "
            "<code>ordered_month_list</code> returns the canonical "
            "January–December ordering, which is passed to "
            "<code>stack_order</code> to ensure consistent month sequencing "
            "regardless of which months have data."
        ),
        h3("Month colour assignment"),
        p(
            "<code>apply_color_map</code> maps each <code>month_name</code> value "
            "to a shade from the <b>Blues_r</b> sequential colormap — earliest months "
            "are darker blue, later months lighter — providing an intuitive temporal "
            "gradient within each stacked bar."
        ),
        make_table(
            [
                ["Property",        "Value"],
                ["X axis",          "raingauge_stations — one grouped bar per station"],
                ["Y axis",          "overall_readings (sum per month per station)"],
                ["Stack column",    "month_name"],
                ["Stack order",     "January → December (canonical)"],
                ["Colour column",   "colors  (Blues_r colormap)"],
                ["Plot background", "#f5f5f5"],
                ["Legend",          "Visible"],
            ],
            [5*cm, 11.5*cm],
        ),
    ]

    # ── 5. Rainfall Map ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Rainfall Map"), hr(),
        p(
            "An interactive proportional-symbol map where each gauge station is "
            "represented by a circle whose radius scales with total rainfall, "
            "overlaid on land-use polygons and ranch boundaries."
        ),

        h2("5.1 Geometry Filtering"),
        p(
            "Before map layer creation, two cleaning steps remove problematic geometries "
            "from the aggregated station GeoDataFrame:"
        ),
        bullet(
            "<b>exclude_geom_outliers</b> — removes stations whose location is a "
            "statistical outlier (Z-score > 3 on coordinate values). This eliminates "
            "stray GPS artefacts that would skew the map extent."
        ),
        bullet(
            "<b>drop_null_geometry</b> — removes any remaining rows with null geometry "
            "before DeckGL layer creation, preventing rendering errors."
        ),

        h2("5.2 Proportional Symbol Layer"),
        p(
            "<code>create_scatterplot_layer</code> draws one circle per station. "
            "The radius is driven by the <code>overall_readings</code> column, "
            "making larger rainfall totals visually larger:"
        ),
        make_table(
            [
                ["Property",         "Value",          "Effect"],
                ["get_fill_color",   "[100, 149, 237]  #6495ed", "Cornflower blue fill — matches bar chart colour"],
                ["get_line_color",   "[70, 119, 207]",  "Slightly darker outline"],
                ["get_radius",       "overall_readings","Radius driven by the rainfall total"],
                ["radius_scale",     "0.044",           "Scales raw mm values to screen pixels"],
                ["radius_min_pixels","5",               "Minimum circle size — stations with zero rainfall remain visible"],
                ["radius_max_pixels","20",              "Caps circle size to prevent overlap at high values"],
                ["radius_units",     "pixels",          "Screen-space radius, zoom-independent"],
                ["opacity",          "85 %",            "Slightly transparent to show polygon layers beneath"],
                ["stroked",          "true",            "Outline drawn"],
            ],
            [4*cm, 4.5*cm, 8*cm],
        ),

        h2("5.3 Text Label Layer"),
        p(
            "A text layer renders each station's total rainfall value (in mm, "
            "rounded to the nearest integer) directly on the map:"
        ),
        bullet("<code>overall_readings</code> is converted to <code>int</code> then <code>str</code> before passing to the text layer"),
        bullet("Font: <b>Calibri Bold</b>, 65 px base size, 90–180 px screen clamp"),
        bullet("<code>get_pixel_offset: [-1, -5]</code> — nudges the label slightly above the circle centre"),
        bullet("Background padding: [-3, -20] — tight horizontal / loose vertical clearance"),
        bullet("Text colour: black (0, 0, 0, 255); billboard mode (always faces the viewer)"),
        bullet("<code>pickable: false</code> — labels do not trigger hover tooltips"),

        h2("5.4 Land-use Fill Layers"),
        p(
            "The Amboseli ranch conservancies layer is split by "
            "<code>land_use</code> column and styled independently:"
        ),
        make_table(
            [
                ["Land-use Category",            "Fill / Line Colour",              "Opacity"],
                ["Rangeland",                    "RGB(163, 156, 145)  —  #a39c91", "75 %"],
                ["Rangeland and settlement",     "RGB(255, 160, 122)  —  #ffa07a", "75 %"],
                ["Settlement and agriculture",   "RGB(47,  79,  79)   —  #2f4f4f", "75 %"],
                ["Conservancies",                "RGB(143, 188, 139)  —  #8fbc8b", "75 %"],
                ["National parks and reserves",  "RGB(77,  102,  0)   —  #4d6600", "75 %"],
            ],
            [5*cm, 6.5*cm, 4*cm],
        ),

        h2("5.5 Ranch Boundaries and Electric Fence"),
        p(
            "The boundaries layer is split by <code>land_use</code> and styled "
            "as line layers (no fill):"
        ),
        make_table(
            [
                ["Feature",          "Colour",                         "Width / Opacity", "Notes"],
                ["Ranch boundaries", "RGB(0, 0, 0)  —  black",         "0.95 / 55 %",     "Thin black outlines delineating each group ranch"],
                ["Electric Fence",   "RGB(45, 98, 177)  —  #2d62b1",  "5.5 px / 100 %",  "Bold blue lines marking the electric fence alignment"],
            ],
            [3.5*cm, 4.5*cm, 3*cm, 5.5*cm],
        ),
        p(
            "The map view state is set by <code>view_state_deck_gdf</code> using "
            "the rainfall station GeoDataFrame extent (pitch 0, bearing 0), "
            "constraining the initial view to the area of recorded measurements."
        ),
    ]

    # ── 6. NDVI Analysis ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. NDVI Analysis"), hr(),
        p(
            "Vegetation condition is assessed per ranch using the Normalised "
            "Difference Vegetation Index (NDVI) derived from MODIS satellite imagery. "
            "The analysis produces one historic time-series chart per conservancy, "
            "showing how current-period NDVI compares against the multi-year "
            "historic range."
        ),

        h2("6.1 ROI Split by Ranch"),
        p(
            "<code>split_groups</code> partitions the Amboseli conservancy "
            "boundaries GeoDataFrame by the <code>R_NAME</code> column, producing "
            "one GeoDataFrame per ranch. Each GeoDataFrame is used as the "
            "<code>roi</code> (region of interest) for a separate "
            "<code>calculate_ndvi_range</code> call via <code>mapvalues</code>."
        ),
        p(
            "<code>dataframe_column_first_unique_str</code> extracts the ranch name "
            "from each split GeoDataFrame. Ranch names are then zipped with the "
            "corresponding NDVI chart HTML via <code>zip_groupbykey</code>, so each "
            "persisted file is suffixed with the correct ranch name."
        ),

        h2("6.2 NDVI Method"),
        p(
            "The user selects one of two MODIS-based NDVI methods at run time "
            "via the <code>ndvi_method</code> string variable:"
        ),
        make_table(
            [
                ["Method",                          "Source",           "Resolution", "Temporal resolution", "Best for"],
                ["MODIS MYD13A1 16-Day Composite",  "Pre-calculated NDVI", "500 m",  "16-day composites",   "Phenology studies; quality-filtered best-pixel values; ~0.025 accuracy; may saturate in dense canopies"],
                ["MODIS MCD43A4 Daily NBAR",         "NIR/Red band ratio", "500 m",  "Daily (view-angle corrected)", "Higher temporal resolution; consistent measurements across acquisitions; more susceptible to cloud gaps"],
            ],
            [4.5*cm, 3.5*cm, 2*cm, 3*cm, 3.5*cm],
        ),
        p(
            "Default is <b>MODIS MYD13A1 16-Day Composite</b>. "
            "<code>baseline_time_range</code> is set to <code>null</code> and "
            "<code>image_size</code> to <code>1 000 000 000</code> "
            "(effectively unlimited), both pending support for a baseline time range "
            "parameter in the web form."
        ),
        note(
            "NDVI data is persisted per ranch as a CSV "
            "(<code>persist_df_wrapper</code> with <code>sanitize: true</code>, "
            "which replaces special characters in column names). "
            "The <code>skipif: never</code> condition on this task ensures the "
            "CSV is always written even when upstream tasks trigger skip conditions."
        ),

        h2("6.3 Historic Time-series Chart"),
        p(
            "<code>draw_historic_timeseries</code> renders the per-ranch NDVI chart "
            "with three visual layers:"
        ),
        make_table(
            [
                ["Visual element",   "Column",         "Style"],
                ["Current NDVI line","NDVI",            "Default plotly line style; labelled 'NDVI'"],
                ["Historic min-max band", "min / max", "Filled area between min and max; fill: rgba(144, 238, 144, 0.3) — light green; line: rgba(144, 238, 144, 0.8)"],
                ["Historic mean line","mean",           "Default plotly line style; labelled 'Historic Mean'"],
            ],
            [4*cm, 3*cm, 9.5*cm],
        ),
        p(
            "The time axis uses the <code>img_date</code> column. The min-max band "
            "is drawn as a filled area between two <code>mode: lines</code> traces, "
            "giving a visual envelope of multi-year NDVI variability. "
            "When the current NDVI line falls outside this envelope it indicates "
            "an anomalously wet or dry condition relative to the historical baseline."
        ),
    ]

    # ── 7. Word Report ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Word Report"), hr(),
        p(
            "The final deliverable is a <b>Word document</b> "
            "(<code>big_life_weather_report.docx</code>) assembled from a "
            "Dropbox-hosted template populated with all generated charts and the "
            "rainfall map."
        ),

        h2("7.1 Template Download"),
        p(
            "The template file (<code>big_life_weather_report_template.docx</code>) "
            "is downloaded automatically from Dropbox at run time "
            "(<code>fetch_and_persist_file</code>, up to 3 retries). "
            "<code>overwrite_existing: false</code> skips the download on subsequent "
            "runs if the file is already cached, saving bandwidth."
        ),

        h2("7.2 Author Attribution"),
        p(
            "The workflow looks up the currently authenticated EarthRanger user via "
            "<code>get_current_user</code> and resolves their display name with "
            "<code>get_user_full_name</code>. This name is passed as "
            "<code>generated_by</code> to <code>generate_weather_report</code>, "
            "so the report is automatically attributed to the ranger who ran it "
            "without requiring manual input."
        ),

        h2("7.3 Report Generation"),
        p(
            "<code>generate_weather_report</code> populates the template context "
            "and inserts all map and chart images into the document:"
        ),
        make_table(
            [
                ["Parameter",        "Value",                       "Description"],
                ["template_path",    "downloaded .docx",            "Big Life weather report template"],
                ["output_dir",       "ECOSCOPE_WORKFLOWS_RESULTS",  "Output directory"],
                ["generated_by",     "EarthRanger user full name",  "Author field in the report"],
                ["box_height",       "3.12 inches",                 "Image placeholder height"],
                ["box_width",        "5.34 inches",                 "Image placeholder width"],
                ["time_period",      "analysis time_range",         "Report period displayed in the header"],
                ["filename",         "big_life_weather_report.docx","Output filename"],
                ["validate_images",  "true",                        "Checks that all expected image files exist before populating placeholders"],
            ],
            [3.5*cm, 4.5*cm, 8.5*cm],
        ),
        p(
            "Images are sourced from the PNG screenshots produced by "
            "<code>html_to_png</code> tasks at 2× device scale factor. "
            "The rainfall map uses a 40 000 ms tile-load wait to ensure satellite "
            "tiles render fully before screenshotting; chart screenshots use a "
            "10 ms wait (charts render client-side without external tile requests)."
        ),
    ]

    # ── 8. Output Files ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("8. Output Files"), hr(),
        p(
            "All outputs are written to the directory defined by "
            "<code>ECOSCOPE_WORKFLOWS_RESULTS</code>."
        ),
        make_table(
            [
                ["File",                                   "Format",     "Content"],
                ["overall_rainfall_station_readings.gpkg", "GeoPackage", "Total rainfall per station, with point geometry"],
                ["monthly_rainfall_station_readings.gpkg", "GeoPackage", "Total rainfall per station per month, with point geometry"],
                ["ndvi_<ranch>.csv",                       "CSV",        "NDVI time-series with historic min/max/mean per ranch"],
                ["rainfall_readings_over_time.html",       "HTML",       "Interactive overall rainfall bar chart"],
                ["monthly_rainfall_readings.html",         "HTML",       "Interactive monthly stacked bar chart"],
                ["rainfall_map.html",                      "HTML",       "Interactive proportional-symbol rainfall map"],
                ["<ranch>_ndvi.html",                      "HTML",       "Interactive NDVI historic time-series per ranch"],
                ["rainfall_readings_over_time.png",        "PNG",        "Screenshot of overall bar chart (2× resolution)"],
                ["monthly_rainfall_readings.png",          "PNG",        "Screenshot of monthly stacked bar chart (2× resolution)"],
                ["rainfall_map.png",                       "PNG",        "Screenshot of rainfall map (2× resolution)"],
                ["<ranch>_ndvi.png",                       "PNG",        "Screenshot of NDVI chart per ranch (2× resolution)"],
                ["big_life_weather_report.docx",           "Word",       "Final populated weather report"],
            ],
            [6*cm, 2.5*cm, 8*cm],
        ),
    ]

    # ── 9. Workflow Execution Logic ───────────────────────────────────────────
    story += [
        sp(4), h1("9. Workflow Execution Logic"), hr(),

        h2("9.1 Skip Conditions"),
        p(
            "Every task carries two default skip conditions via "
            "<code>task-instance-defaults</code>:"
        ),
        bullet("<b>any_is_empty_df</b> — if any input DataFrame is empty the task and all its dependants are skipped rather than raising an error."),
        bullet("<b>any_dependency_skipped</b> — if an upstream task was skipped, all downstream tasks that depend on it are also skipped automatically."),
        p(
            "<code>get_events_data</code> carries an explicit "
            "<code>skipif</code> block with both conditions. Note, however, that "
            "<code>raise_on_empty: true</code> means EarthRanger will return an "
            "error (not an empty DataFrame) when no events are found — "
            "distinguishing a workflow skip from a genuine data-availability error."
        ),
        p(
            "<code>persist_ndvi_data</code> has <code>skipif: conditions: [never]</code>, "
            "ensuring NDVI CSVs are always written even if the NDVI DataFrame "
            "might otherwise trigger a skip."
        ),

        h2("9.2 mapvalues Fan-out (NDVI per Ranch)"),
        p(
            "The NDVI pipeline fans out per ranch via <code>mapvalues</code>. "
            "<code>split_groups</code> partitions the conservancy GeoDataFrame "
            "by <code>R_NAME</code>. Each subsequent task in the chain "
            "(<code>calculate_ndvi_range</code>, <code>persist_ndvi_data</code>, "
            "<code>draw_ndvi</code>, <code>get_ranch_name</code>, "
            "<code>persist_ndvi</code>, <code>convrt_ranch_png</code>) "
            "receives the <code>argvalues</code> list from its upstream task, "
            "processing one ranch per invocation."
        ),
        p(
            "<code>zip_groupbykey</code> aligns the per-ranch NDVI chart HTML "
            "with the corresponding ranch name string before <code>persist_text</code>, "
            "so each output file is named with the correct conservancy suffix."
        ),

        h2("9.3 Screenshot Configuration"),
        make_table(
            [
                ["Task",                    "wait_for_timeout", "max_concurrent_pages", "Reason"],
                ["convrt_ranch_png",        "10 ms",           "3",                    "NDVI charts are self-contained HTML; fast render, parallelised"],
                ["convrt_br_png",           "10 ms",           "1",                    "Bar chart is self-contained HTML"],
                ["convrt_monthly_png",      "10 ms",           "1",                    "Stacked bar chart is self-contained HTML"],
                ["convert_map_png",         "40 000 ms",       "1",                    "Rainfall map loads external tile layers — long wait ensures tiles render before screenshot"],
            ],
            [3.5*cm, 3*cm, 3.5*cm, 6.5*cm],
        ),
    ]

    # ── 10. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("10. Software Versions"), hr(),
        make_table(
            [
                ["Package",                         "Version",   "Role"],
                ["ecoscope-workflows-core",         "0.22.17.*", "Core task library and workflow engine"],
                ["ecoscope-workflows-ext-ecoscope", "0.22.17.*", "Ecoscope spatial analysis tasks (events, map layers, charts)"],
                ["ecoscope-workflows-ext-custom",   "0.0.39.*",  "Custom utility tasks (column transforms, geometry cleaning)"],
                ["ecoscope-workflows-ext-ste",      "0.0.17.*",  "STE-specific tasks (NDVI range, historic timeseries chart)"],
                ["ecoscope-workflows-ext-mnc",      "0.0.7.*",   "MNC domain tasks"],
                ["ecoscope-workflows-ext-mep",      "0.12.0.*",  "MEP tasks (weather report generation, stacked bar chart)"],
                ["ecoscope-workflows-ext-big-life",  "0.0.9.*",  "Big Life Foundation tasks (weather report template context)"],
            ],
            [5.5*cm, 2.8*cm, 8.2*cm],
        ),
        p(
            "Packages are distributed via the <code>prefix.dev</code> conda channel "
            "and pinned to patch-compatible versions (<code>.*</code> suffix). "
            "The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build PDF ──────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
