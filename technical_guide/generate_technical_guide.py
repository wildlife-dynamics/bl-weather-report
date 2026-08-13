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
        p("Rainfall Monitoring, Mapping &amp; NDVI Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 2.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
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
            "ecosystem. It ingests rainfall-gauge observations from <b>EarthRanger</b>, "
            "derives vegetation condition per ranch from <b>Google Earth Engine</b> NDVI "
            "time-series, and delivers rainfall charts, an interactive map, a summary "
            "table, per-ranch NDVI trend charts, a Word report, and a dashboard."
        ),
        p(
            "The workflow is implemented as an <b>Ecoscope Workflow</b> (<code>spec.yaml</code>) "
            "and executes within the <code>ecoscope-workflows</code> runtime. NDVI analysis "
            "is fanned out per ranch using the <code>mapvalues</code> directive, grouping by "
            "the <code>R_NAME</code> column of the Amboseli conservancy boundaries GeoDataFrame."
        ),
        sp(4),
        note(
            "This version of the guide (2.0) reflects a substantially expanded "
            "<code>spec.yaml</code> compared to the original release: an interactive rainfall "
            "map (land use, ranch boundaries, electric fence, clustered rainfall readings), "
            "a rainfall-by-station summary table, and a 4-widget dashboard have all been added. "
            "The previously documented per-ranch NDVI CSV export and dynamic "
            "&ldquo;generated by&rdquo; author lookup are no longer part of the pipeline."
        ),
        sp(4),
        p("The workflow delivers the following outputs per run:"),
        make_table(
            [
                ["Category",         "Outputs"],
                ["Rainfall charts",  "Overall rainfall bar chart (per station), monthly stacked bar chart (per station × calendar month)"],
                ["Summary table",    "Sortable, filterable rainfall-by-station table"],
                ["Rainfall map",     "Interactive map: Amboseli land use, ranch boundaries, electric fence, and a clustered proportional-symbol layer of station readings"],
                ["NDVI charts",      "One historic NDVI time-series chart per ranch, with a min/max/mean band"],
                ["Data file",        "Aggregated station rainfall readings, with point geometry (GeoParquet)"],
                ["Report",           "Word document (overall_report.docx): Big Life weather report template populated with every chart, the map, and all NDVI charts"],
                ["Dashboard",        "4 widgets: rainfall map, overall rainfall chart, monthly rainfall chart, rainfall-by-station table"],
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
            "<code>rainfall_rep</code> using <code>get_events</code>, with "
            "<code>include_details: true</code> so the <code>event_details</code> "
            "JSON blob carrying the actual gauge readings is returned. "
            "<code>raise_on_empty: true</code> is set, so the workflow raises an error "
            "rather than silently skipping if no rainfall events are found for the period — "
            "distinguishing a data-availability problem from a genuine zero-reading period."
        ),

        sp(4), h2("2.2 Google Earth Engine Connection"),
        p(
            "A <b>Google Earth Engine (GEE)</b> service account is required for NDVI "
            "analysis. <code>set_gee_connection</code> stores the connection, which "
            "is passed to <code>calculate_ndvi_range</code> for each ranch ROI. "
            "GEE credentials must be stored as a JSON private key; see the GEE "
            "Setup Guide for instructions."
        ),

        sp(4), h2("2.3 Static Geospatial Layers"),
        p(
            "Three GeoPackage files are downloaded automatically from Dropbox at "
            "run time via <code>fetch_and_persist_file</code> (3 retries, "
            "<code>overwrite_existing: false</code> so a cached copy is reused on "
            "subsequent runs). All three are reprojected to <b>EPSG:4326 (WGS 84)</b> "
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
        p("Every map uses two stacked tile services, configured via <code>set_base_maps_pydeck</code>:"),
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
            "<code>split_groups</code> fan-out that produces one NDVI chart per ranch, "
            "and is also carried through to the temporal index added to rainfall events "
            "and to the final dashboard metadata."
        ),
    ]

    # ── 3. Rainfall Data Pipeline ─────────────────────────────────────────────
    story += [
        sp(4), h1("3. Rainfall Data Pipeline"), hr(),

        h2("3.1 Event Fetch — rainfall_rep"),
        p(
            "<code>get_events</code> queries EarthRanger for events of type "
            "<code>rainfall_rep</code> within the analysis time range, with "
            "<code>force_point_geometry: true</code> and null-geometry events excluded. "
            "Updates and related events are not fetched (<code>include_updates: false</code>, "
            "<code>include_related_events: false</code>)."
        ),
        p("Columns retained per event:"),
        bullet("id, time, event_type, event_category, reported_by, serial_number, geometry, created_at, event_details"),

        sp(4), h2("3.2 Detail Titles &amp; JSON Normalisation"),
        p(
            "<code>process_events_details</code> (a Big Life-specific task) maps the raw "
            "event-detail keys to their human-readable question titles "
            "(<code>map_to_titles: true</code>) and preserves field order "
            "(<code>ordered: true</code>) before the JSON is flattened. "
            "<code>normalize_json_column</code> then flattens the <code>event_details</code> "
            "object into individual <code>event_details__&lt;title&gt;</code> columns "
            "(<code>sort_columns: true</code>); <code>skip_if_not_exists: true</code> makes "
            "the step a no-op if the column is already flat."
        ),

        sp(4), h2("3.3 Column Renaming"),
        p(
            "<code>map_columns</code> renames the flattened detail columns to short "
            "working names and drops columns that are no longer needed:"
        ),
        make_table(
            [
                ["Raw column name",                                         "Working name",     "Description"],
                ["event_details__Digital rain gauge (mm)",                  "digital_raingauge","Reading from the digital rain gauge"],
                ["event_details__Manual rain gauge (mm)",                   "manual_raingauge", "Reading from the manual rain gauge"],
                ["event_details__Rain gauge station",                       "raingauge_station","Name of the gauge station"],
                ["event_details__Rain gauge station zone",                  "zone",             "Zone associated with the station"],
            ],
            [7*cm, 4*cm, 5.5*cm],
        ),
        p(
            "Dropped columns: <code>event_type</code>, <code>event_category</code>, "
            "<code>reported_by</code>, <code>serial_number</code>, <code>patrols</code>, "
            "<code>event_type_display</code>. <code>raise_if_not_found: false</code> "
            "means a missing source column is skipped rather than raising an error."
        ),

        sp(4), h2("3.4 Combined Readings — Digital / Manual Fallback"),
        p(
            "<code>combine_columns_with_fallback</code> merges the digital and manual "
            "gauge readings into a single <code>overall_readings</code> column, in place:"
        ),
        bullet("<b>Primary:</b> <code>digital_raingauge</code> — used when available and non-null"),
        bullet("<b>Fallback:</b> <code>manual_raingauge</code> — used when the digital reading is absent"),
        bullet("<b>fill_remaining: 0</b> — rows where both are null receive a zero reading"),
        p(
            "This design reflects field practice: digital gauges are preferred for "
            "accuracy, but rangers fall back to manual readings when the digital "
            "gauge malfunctions or has not yet been read."
        ),

        sp(4), h2("3.5 Data Cleaning"),
        p(
            "<code>convert_columns_to_float</code> casts <code>overall_readings</code> "
            "to a float column; values that fail to parse are coerced to <code>NaN</code> "
            "(<code>errors: coerce</code>) and then filled with <code>0</code> "
            "(<code>fill_value: 0</code>), so the aggregation step below receives no nulls."
        ),

        sp(4), h2("3.6 Aggregation by Station"),
        p(
            "<code>spatial_summarize_df</code> collapses all events to one row per "
            "gauge station (<code>groupby_cols: [raingauge_station]</code>):"
        ),
        make_table(
            [
                ["Column",             "Aggregation",   "Result"],
                ["geometry",           "first",         "Station point geometry (all readings for a station share the same location)"],
                ["raingauge_readings", "sum",           "Total rainfall in mm at each station for the period (1 decimal place); source column: overall_readings"],
            ],
            [4*cm, 3*cm, 9.5*cm],
        ),
        p(
            "This aggregated table (<code>group_and_aggregate</code>) is the source for "
            "the overall rainfall bar chart, the summary table, the persisted data file, "
            "and the rainfall map layer. The monthly chart, by contrast, works from the "
            "row-level (per-event) data — see &sect;4.2."
        ),
    ]

    # ── 4. Chart Outputs ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Chart Outputs"), hr(),

        h2("4.1 Overall Rainfall Bar Chart"),
        p(
            "<code>draw_bar_chart</code> (grouped mode) renders total rainfall (mm) "
            "per station from the station-aggregated table."
        ),
        make_table(
            [
                ["Property",       "Value"],
                ["X axis",         "raingauge_station — one bar per station"],
                ["Y axis",         "raingauge_readings (sum) — total mm"],
                ["Bar colour",     "#6495ed  (cornflower blue)"],
                ["Plot background","#f5f5f5  (light grey)"],
                ["Legend",         "Hidden (showlegend: false)"],
                ["Bar / group gap","0.05 / 0.05"],
            ],
            [5*cm, 11.5*cm],
        ),

        sp(4), h2("4.2 Monthly Stacked Bar Chart"),
        p(
            "<code>draw_bar_chart</code> (stacked mode) renders month-by-month rainfall "
            "contributions at each station, using the row-level events data with date "
            "components decomposed via <code>decompose_datetime</code> "
            "(year, month, month_name)."
        ),
        h3("Calendar ordering"),
        p(
            "<code>ecoscope_workflows_ext_big_life.tasks.localization.month_names</code> "
            "(<code>abbreviated: true</code>) returns the canonical Jan–Dec month-name "
            "ordering, passed to <code>stack_order</code> so stacks are sequenced by "
            "calendar month regardless of which months have data."
        ),
        h3("Month colour assignment"),
        p(
            "<code>apply_color_map</code> maps each <code>time_month_name</code> value "
            "to a shade from the <b>Blues_r</b> sequential colormap — earlier months are "
            "darker blue, later months lighter — giving an intuitive temporal gradient "
            "within each stacked bar."
        ),
        make_table(
            [
                ["Property",        "Value"],
                ["X axis",          "raingauge_station — one stacked bar per station"],
                ["Y axis",          "overall_readings (sum, per month per station)"],
                ["Stack column",    "time_month_name"],
                ["Stack order",     "Jan → Dec (from month_names task)"],
                ["Colour column",   "colors  (Blues_r colormap)"],
                ["Plot background", "#f5f5f5"],
                ["Legend",          "Visible"],
            ],
            [5*cm, 11.5*cm],
        ),

        sp(4), h2("4.3 Rainfall-by-Station Summary Table"),
        p(
            "<code>draw_table</code> renders the station-aggregated table "
            "(<code>raingauge_station</code>, <code>raingauge_readings</code>) with "
            "sorting and filtering enabled and downloads disabled "
            "(<code>enable_download: false</code>). It is persisted as HTML and wired "
            "into both the dashboard and the Word report is not applicable here — this "
            "widget appears on the dashboard only."
        ),
    ]

    # ── 5. Rainfall Map ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Rainfall Map"), hr(),
        p(
            "An interactive DeckGL map combining three static context layers with a "
            "clustered layer of rainfall readings, framed automatically to the data extent."
        ),

        h2("5.1 Land-use Fill Layer"),
        p(
            "<code>apply_color_map</code> assigns a fill colour to each polygon by its "
            "<code>land_use</code> value; <code>create_geojson_layer</code> then renders "
            "the filled/stroked polygons at 75% opacity:"
        ),
        make_table(
            [
                ["Land-use Category",            "Fill / Line Colour",              "Opacity"],
                ["Rangeland",                    "#a39c91", "75 %"],
                ["Rangeland and settlement",     "#ffa07a", "75 %"],
                ["Settlement and agriculture",   "#2f4f4f", "75 %"],
                ["Conservancies",                "#8fbc8b", "75 %"],
                ["National parks and reserves",  "#4d6600", "75 %"],
            ],
            [5*cm, 6.5*cm, 4*cm],
        ),

        h2("5.2 Ranch Boundaries and Electric Fence"),
        p(
            "The boundaries + fence GeoPackage is filtered on <code>land_use</code> into "
            "two separate line layers (no fill):"
        ),
        make_table(
            [
                ["Feature",          "Colour",                         "Width / Opacity", "Notes"],
                ["Ranch boundaries", "#000000  (black)",                "0.95 / 55 %",     "Thin outlines delineating each group ranch"],
                ["Electric Fence",   "#2d62b1",                         "5.5 px / 100 %",  "Bold line marking the electric-fence alignment"],
            ],
            [3.5*cm, 4.5*cm, 3*cm, 5.5*cm],
        ),

        h2("5.3 Clustered Rainfall Layer"),
        p(
            "<code>create_clustered_labeled_scatterplot_layer</code> draws the station "
            "readings as clustered circles, sized and labelled by "
            "<code>raingauge_readings</code>:"
        ),
        make_table(
            [
                ["Property",           "Value",           "Effect"],
                ["get_fill_color / get_line_color", "[100, 149, 237]  #6495ed", "Cornflower blue — matches the bar chart colour"],
                ["get_radius",          "raingauge_readings", "Circle radius scales with the station's total rainfall"],
                ["radius_units / scale","pixels / 1",       "Screen-space radius, zoom-independent"],
                ["cluster_padding",     "1.0",              "Spacing applied between clustered points"],
                ["cluster_max_radius",  "40 px",            "Maximum pixel radius used to group nearby stations into a cluster"],
                ["Text label",         "raingauge_readings value, monospace, size 15, scaled to the circle radius", "Reading is shown directly on each circle"],
                ["stroked / filled",   "true / true",      "Outline and fill both drawn"],
            ],
            [4.5*cm, 5*cm, 7*cm],
        ),

        h2("5.4 View Framing &amp; Layer Composition"),
        p(
            "<code>envelope_gdf</code> (expansion factor 1.05) computes a bounding "
            "envelope around the aggregated station points, and "
            "<code>compute_view_state_from_gdf</code> derives an initial camera view "
            "(pitch 0, bearing 0, max zoom 15) from that envelope — framing the map to "
            "the stations that actually reported data. "
            "<code>combine_deckgl_map_layers</code> then composes the land-use, boundary, "
            "and fence layers as static base layers with the clustered rainfall layer as "
            "a grouped layer, before <code>draw_map</code> renders the final map "
            "(max zoom 10, legend placed bottom-right)."
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
            "one GeoDataFrame per ranch. Each is used as the <code>roi</code> "
            "(region of interest) for a separate <code>calculate_ndvi_range</code> "
            "call via <code>mapvalues</code>."
        ),
        p(
            "<code>column_first_unique_value</code> extracts the ranch name from each "
            "split GeoDataFrame; <code>groupbykey</code> then zips the ranch names with "
            "the corresponding NDVI chart HTML so each persisted file is suffixed with "
            "the correct ranch name."
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
            "<code>baseline_time_range</code> is currently fixed to <code>null</code> and "
            "<code>image_size</code> to a very large fixed value — both marked in "
            "<code>spec.yaml</code> as pending support for a user-configurable baseline "
            "time range in the web form."
        ),
        note(
            "This version of the workflow does not persist a per-ranch NDVI data file "
            "(CSV or otherwise) — only the rendered chart (HTML/PNG) is written per ranch."
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
                ["Historic min-max band", "min / max", "Filled area between min and max; fill: rgba(144, 238, 144, 0.3) — light green; line: rgba(144, 238, 144, 0.8); labelled 'Historic Min-Max'"],
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
            "(<code>overall_report.docx</code>) assembled from a Dropbox-hosted "
            "template populated with every generated chart, the rainfall map, and "
            "every per-ranch NDVI chart."
        ),

        h2("7.1 Template Download"),
        p(
            "The template file (<code>big_life_weather_report_template.docx</code>) "
            "is downloaded automatically from Dropbox at run time "
            "(<code>fetch_and_persist_file</code>, up to 3 retries). "
            "<code>overwrite_existing: false</code> skips the download on subsequent "
            "runs if the file is already cached, saving bandwidth."
        ),

        h2("7.2 Report Generation"),
        p(
            "<code>generate_weather_report</code> populates the template context "
            "and inserts all map and chart images into the document:"
        ),
        make_table(
            [
                ["Parameter",        "Value",                       "Description"],
                ["template_path",    "downloaded .docx",            "Big Life weather report template"],
                ["output_dir",       "ECOSCOPE_WORKFLOWS_RESULTS",  "Output directory"],
                ["generated_by",     "\"Ecoscope\" (fixed string)", "Author field in the report — not resolved from the EarthRanger user"],
                ["box_height / box_width", "3.12 in / 5.34 in",     "Image placeholder dimensions"],
                ["time_period",      "analysis time_range",         "Report period displayed in the header"],
                ["filename",         "overall_report.docx",         "Output filename"],
                ["validate_images",  "true",                        "Checks that all expected image files exist before populating placeholders"],
            ],
            [3.5*cm, 4.5*cm, 8.5*cm],
        ),
        p(
            "Images are sourced from the PNG screenshots produced by "
            "<code>html_to_png</code> tasks at 2× device scale factor — see &sect;9.3 "
            "for the per-task wait-time configuration."
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
                ["File",                                       "Format",     "Content"],
                ["overall_rainfall_station_readings",          "GeoParquet", "Total rainfall per station, with point geometry"],
                ["rainfall_readings_over_time.html / .png",    "HTML / PNG", "Overall rainfall bar chart by station"],
                ["monthly_rainfall_readings.html / .png",      "HTML / PNG", "Monthly stacked rainfall bar chart, calendar-ordered"],
                ["rainfall_by_station_summary_table.html",     "HTML",       "Sortable, filterable rainfall-by-station table"],
                ["rainfall_map.html / .png",                   "HTML / PNG", "Interactive map: land use, boundaries, fence, rainfall readings"],
                ["&lt;ranch&gt;.html / .png (one per ranch)",  "HTML / PNG", "Historic NDVI time-series chart per ranch"],
                ["overall_report.docx",                        "Word",       "Final populated Big Life weather report"],
            ],
            [6*cm, 2.5*cm, 8*cm],
        ),
        p("PNGs are rendered at 2× device scale factor for all charts and the map."),
    ]

    # ── 9. Workflow Execution Logic ───────────────────────────────────────────
    story += [
        sp(4), h1("9. Workflow Execution Logic"), hr(),

        h2("9.1 Skip Conditions"),
        p(
            "Every task carries two default skip conditions via "
            "<code>task-instance-defaults</code>:"
        ),
        bullet("<b>any_is_empty_df</b> — if any input DataFrame is empty, the task and its dependants are skipped rather than raising an error."),
        bullet("<b>any_dependency_skipped</b> — if an upstream task was skipped, all downstream tasks that depend on it are also skipped automatically."),
        p(
            "The rainfall-event fetch (<code>get_events_data</code>) sets "
            "<code>raise_on_empty: true</code>, so EarthRanger returning zero "
            "<code>rainfall_rep</code> events for the period produces an explicit error "
            "rather than a silent, empty-output run — distinguishing a workflow skip "
            "from a genuine data-availability problem."
        ),

        h2("9.2 mapvalues Fan-out (NDVI per Ranch)"),
        p(
            "The NDVI pipeline fans out per ranch via <code>mapvalues</code>. "
            "<code>split_roi_groups</code> (<code>split_groups</code>) partitions the "
            "conservancy GeoDataFrame by <code>R_NAME</code>. Each downstream task in the "
            "chain receives the resulting list as its <code>argvalues</code>, processing "
            "one ranch per invocation:"
        ),
        make_table(
            [
                ["Task id",           "Task",                        "Maps over"],
                ["calculate_ndvi",    "calculate_ndvi_range",         "roi ← split_roi_groups"],
                ["draw_ndvi",         "draw_historic_timeseries",     "dataframe ← calculate_ndvi"],
                ["get_ranch_name",    "column_first_unique_value",    "df ← split_roi_groups"],
                ["zip_ranch_ndvi",    "groupbykey",                   "zips draw_ndvi + get_ranch_name"],
                ["persist_ndvi",      "persist_text",                 "[text, filename_suffix] ← zip_ranch_ndvi"],
                ["convrt_ranch_png",  "html_to_png",                  "html_path ← persist_ndvi"],
            ],
            [3.5*cm, 4.5*cm, 8*cm],
        ),

        h2("9.3 Screenshot Configuration"),
        make_table(
            [
                ["Task",                    "wait_for_timeout", "max_concurrent_pages", "Reason"],
                ["convrt_ranch_png",        "10 ms",           "3",                    "NDVI charts are self-contained HTML; fast render, parallelised"],
                ["convrt_br_png",           "10 ms",           "1",                    "Overall bar chart is self-contained HTML"],
                ["convrt_monthly_png",      "10 ms",           "1",                    "Monthly stacked bar chart is self-contained HTML"],
                ["convert_map_png",         "40 000 ms",       "1",                    "Rainfall map loads external tile layers — long wait ensures tiles render before screenshot"],
            ],
            [3.5*cm, 3*cm, 3.5*cm, 6.5*cm],
        ),

        h2("9.4 Dashboard Assembly"),
        p(
            "<code>gather_dashboard</code> builds the final dashboard "
            "(<code>bl_events_dashboard</code>) from the workflow details, time range, "
            "and groupers, and exactly four widgets:"
        ),
        bullet("Rainfall Map — the interactive map (&sect;5)"),
        bullet("Raingauge Measurements — the overall rainfall bar chart (&sect;4.1)"),
        bullet("Monthly Rainfall Readings — the monthly stacked bar chart (&sect;4.2)"),
        bullet("Rainfall by Station Summary — the summary table (&sect;4.3)"),
        p(
            "Per-ranch NDVI charts are <i>not</i> added to the dashboard — they are only "
            "written as standalone output files and embedded in the Word report."
        ),
    ]

    # ── 10. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("10. Software Versions"), hr(),
        make_table(
            [
                ["Package",                          "Version",           "Channel"],
                ["ecoscope-platform",                 "2.18.0",            "repo.prefix.dev/ecoscope-workflows"],
                ["ecoscope-workflows-ext-custom",     "0.1.0rc14.*",       "repo.prefix.dev/ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-ste",        "0.0.0rc1.*",        "repo.prefix.dev/ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-mnc",        "1.0.0.*",           "repo.prefix.dev/ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-wwf-virunga","0.0.0rc9.*",        "repo.prefix.dev/ecoscope-workflows-custom"],
                ["ecoscope-workflows-ext-big-life",   "1.0.0.*",           "repo.prefix.dev/ecoscope-workflows-custom"],
                ["pydeck",                             "0.9.2",             "conda-forge"],
                ["opentelemetry-sdk",                  "&gt;=1.20.0,&lt;2.0.0", "conda-forge"],
            ],
            [6.5*cm, 4*cm, 6*cm],
        ),
        p(
            "The Big Life-specific tasks (event-detail title mapping, month-name "
            "localisation, clustered map layer, weather-report generation) live in "
            "<code>ecoscope-workflows-ext-big-life</code>; the bar and historic "
            "time-series charts come from <code>ecoscope-workflows-ext-wwf-virunga</code>; "
            "and the Dropbox fetch, reprojection, envelope/view-state, and layer "
            "combination tasks come from <code>ecoscope-workflows-ext-ste</code>. "
            "The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build PDF ──────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
