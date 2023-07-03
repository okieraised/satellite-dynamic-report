import dash
from dash import html, Input, Output, State
import dash_leaflet as dl
import plotly.graph_objects as go

from constants.constants import MAPBOX_API_KEY, MapType, BASEMAP_URL, DEFAULT_DATA, DEFAULT_SITE, YEARS, DropdownMapper
from geospatial.geotiff import GeoTiffObject
from layout.default_layout import generate_default_time_series_fig
from layout.layout import slider_layout, generate_title_layout, \
    generate_time_series_graph_by_site, render_basemap, generate_default_histogram_graph, \
    generate_default_graph_layout, generate_aggregate_graph, generate_aggregate_figure

from time_series.time_series import query_time_series_data, VariableMapper
from utils.datetime_utils import get_date_from_week_number, validate_file_format
from utils.logging import logger
from utils.query_data import map_data_path_to_week, get_aggregate_of_data, query_geojson_urls, get_obj_path

csv_data = query_time_series_data()
default_df = get_aggregate_of_data(data_type=DEFAULT_DATA, site_name=DEFAULT_SITE)
geojson_urls = query_geojson_urls()


app = dash.Dash(
        __name__,
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1"
            }
        ],
        title="Dynamic Report",
        suppress_callback_exceptions=True,
        prevent_initial_callbacks=True,
    )

server = app.server

app.layout = html.Div(
    id="root",
    children=[
        generate_title_layout(),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[slider_layout, render_basemap(map_type=MapType.DEFAULT, geojson_urls=geojson_urls)],
                ),
                html.Div(
                    id="graph-container",
                    children=[generate_default_histogram_graph(),
                              generate_aggregate_graph(data=default_df, xaxis="Time", yaxis="Pixel Value",
                                                       title=f"Time series of Max/Min/Avg of pixels at {DEFAULT_SITE}")],
                ),
            ]
        ),
        html.Div(
            id="graph-container-bottom",
            children=[
                generate_time_series_graph_by_site(dropdown_id="data-dropdown-2", graph_id="selected-data-3", data=csv_data),
                generate_time_series_graph_by_site(dropdown_id="data-dropdown-3", graph_id="selected-data-4", data=csv_data)],
        ),
    ]
)




########################################################################################################################
# Callback
########################################################################################################################

@app.callback(
    [
        Output(component_id='heatmap-container', component_property='children'),
        Output(component_id='selected-data-1', component_property='figure')
    ],
    [
        Input(component_id="slider", component_property="value"),
        Input(component_id="data-type-dropdown", component_property="value"),
        Input(component_id="week-dropdown", component_property="value"),
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id='basemap-dropdown', component_property='value')

    ],
    prevent_initial_call=True,
    allow_duplicate=True,
)
def update_basemap(year: int, data_type: str, week_number: int, site_name: str, input_map_style):

    logger.info(f"year: {year} | data_type: {data_type} | week_number: {week_number} | site_name: {site_name} | "
                f"input_map_value: {input_map_style}")

    map_figure = [dl.TileLayer(url=BASEMAP_URL.format(map_style=input_map_style, access_token=MAPBOX_API_KEY))]
    # if geojson_urls:
    #     for geojson_url in geojson_urls:
    #         map_figure.append(dl.GeoJSON(url=geojson_url))

    default_hist = generate_default_graph_layout()

    try:
        data_mapper = map_data_path_to_week(data_type=data_type, site_name=site_name, year=year)

        file_name = data_mapper.get(week_number)
        logger.info(f"file name: {file_name}")

        if file_name:
            prefix = f'{data_type}/{site_name}/'.lower()
            obj_path = ''.join([prefix, file_name])
            logger.info(f"rendering object {obj_path}")

            tif_data = GeoTiffObject(obj_path)
            tif_url = tif_data.gen_url()
            tif_color_scale = tif_data.generate_color_scheme()
            logger.info(f"geotiff url: {tif_url}")
            logger.info(f"geotiff max_pix: {tif_data.max_pix()} | geotiff min_pix: {tif_data.min_pix()} | "
                        f"geotiff center: {tif_data.center}")

            map_figure.extend([
                    dl.GeoTIFFOverlay(id="raster", interactive=True, url=tif_url, band=0, opacity=1,
                                      **tif_color_scale),
                    dl.Colorbar(width=200, height=20, min=tif_color_scale.get('domainMin'),
                                max=tif_color_scale.get('domainMax'),
                                position="topleft",
                                tickDecimals=2, unit=" ",
                                colorscale=tif_color_scale.get('colorscale'),
                                style={"color": "white", "weight": 2})
                ])

            map_figure = [dl.Map(children=map_figure, center=tif_data.center, zoom=15)]

            figure = dict(
                data=[go.Histogram(x=tif_data.get_pixels(), nbinsx=20)],
                layout=dict(
                    paper_bgcolor="#1f2630",
                    plot_bgcolor="#1f2630",
                    font=dict(color="#2cfec1"),
                    autofill=True,
                    margin=dict(t=75, r=50, b=50, l=50),
                    title=f"Distribution of pixel values for {data_type} at {site_name}",
                    xaxis={
                        'title': dict(
                            text="Value"
                        ),
                    },
                    yaxis={
                        'title': dict(
                            text="Count",
                        ),
                        'type': 'log'
                    }
                )
            )

            return map_figure, figure

        return map_figure, default_hist

    except Exception as err:
        logger.error(f"{err}")
        return map_figure, default_hist


@app.callback(
    [
        Output(component_id='selected-data-2', component_property='figure', allow_duplicate=True)
    ],
    [
        Input(component_id="raster", component_property='click_lat_lng_val'),
    ],
    [
        State('selected-data-2', 'figure'),
        State(component_id="slider", component_property="value"),
        State(component_id="week-dropdown", component_property="value"),
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)
def show_pixel(click_lat_lng, fig, year: int, week: int):
    logger.info(f"show_pixel: year: {year} | week: {week}")
    try:
        old_data = fig.get('data')
        new_data = [d for d in old_data if d['name'] != 'selected pixel']

        if not click_lat_lng:
            raise dash.exceptions.PreventUpdate("cancel the callback")

        lat = click_lat_lng[0]
        long = click_lat_lng[1]
        value = click_lat_lng[2]
        logger.info(f"lat: {lat} | long: {long} | value: {value}")

        new_data.append(go.Scatter(x=[get_date_from_week_number(year=year, week=week)],
                                   y=[value], mode="markers", name='selected pixel'))
        fig['data'] = new_data
        return [go.Figure(fig)]
    except Exception as err:
        logger.error(f"{err}")
        raise dash.exceptions.PreventUpdate("No value found. Cancel the callback")


@app.callback(
    [
        Output(component_id='selected-data-3', component_property='figure'),
        Output(component_id='data-dropdown-2', component_property='options'),
    ],
    [
        Input(component_id='data-dropdown-2', component_property='value'),
        Input(component_id='site-dropdown', component_property='value'),
    ],
    allow_duplicate=True,
    prevent_initial_call=True
)
@app.callback(
    [
        Output(component_id='selected-data-4', component_property='figure'),
        Output(component_id='data-dropdown-3', component_property='options'),
    ],
    [
        Input(component_id='data-dropdown-3', component_property='value'),
        Input(component_id='site-dropdown', component_property='value'),
    ],
    allow_duplicate=True,
    prevent_initial_call=True
)
def update_time_series_graph(variable_input, site_input):
    logger.info(f"update time series graph - variable_input: {variable_input} | site_input: {site_input}")

    try:
        site_data = csv_data.get(site_input, None)

        # If no site data is available -> return blank map
        if not site_data:
            logger.error(f"Site {site_input} not found.")
            return generate_default_time_series_fig(), []

        site_options = site_data["var"]
        if not site_options:
            logger.error(f"Site {site_input} has no options.")
            return generate_default_time_series_fig(), []

        site_df = site_data["data"]
        if site_df.empty:
            logger.error(f"Site {site_input} has no data.")
            return generate_default_time_series_fig(), []

        if variable_input not in site_df.columns:
            variable_input = site_options[0].get("value")
            # return generate_default_time_series_fig(), site_options

        y_axis_title = VariableMapper.get(variable_input)

        fig = dict(
            data=[go.Scatter(x=site_df.index.tolist(), y=site_df[variable_input].tolist())],
            layout=dict(
                paper_bgcolor="#1f2630",
                plot_bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
                autofill=True,
                margin=dict(t=75, r=50, b=50, l=50),
                title=f"Time Series of {y_axis_title} of {site_input}",
                xaxis={
                    'title': dict(
                        text="Year"
                    ),
                    'tickformat': '%Y-%m-%d'
                },
                yaxis={
                    'title': dict(
                        text=y_axis_title
                    )
                }
            )
        )

        return fig, site_options
    except Exception as err:
        logger.error(f"{err}")
        return generate_default_time_series_fig(), []


@app.callback(
    [
        Output(component_id='selected-data-2', component_property='figure')
    ],
    [
        Input(component_id="data-type-dropdown", component_property="value"),
        Input(component_id="site-dropdown", component_property="value"),

    ],
    allow_duplicate=True,
)
def update_aggregate_figure(data_type: str, site_name: str):
    try:
        df = get_aggregate_of_data(data_type=data_type, site_name=site_name)
        if not df.empty:
            fig_data = [go.Scatter(x=df.index.tolist(), y=df[col_name].tolist(), name=col_name, mode="markers")
                        for col_name in df.columns]

            return [go.Figure(generate_aggregate_figure(data=fig_data, xaxis="Time", yaxis="Pixel Value",
                                                        title=f"Time series of Max/Min/Avg of pixels at {site_name}"))]
        else:
            return [go.Figure(generate_aggregate_figure(data=[go.Scatter(x=[], y=[])]))]
    except Exception as err:
        logger.error(f"{err}")
        raise dash.exceptions.PreventUpdate("Cancel the callback")


@app.callback(
    [
        Output(component_id='slider', component_property='marks'),
        # Output(component_id='week-dropdown', component_property='options')
    ],
    [
        Input(component_id="data-type-dropdown", component_property="value"),
        Input(component_id="site-dropdown", component_property="value"),

    ],
    allow_duplicate=True,
)
def update_available_year_data_slider(data_type: str, site_name: str):

    res = {}

    available_years = []

    logger.info(f"update year slider input - data_type: {data_type} | site_name: {site_name}")

    o_paths = get_obj_path(data_type=data_type, site_name=site_name)

    prefix = f'{data_type}/{site_name}/'.lower()
    if len(o_paths) > 0:
        for o_path in o_paths:
            f_path = o_path.split(prefix)[1]
            try:
                d_date = str(f_path).split('.')[0]
                if not validate_file_format(d_date):
                    continue

                d_component = d_date.split('-')
                d_year = d_component[0]
                available_years.append(int(d_year))
            except Exception as err:
                logger.error(f"{err}")
                continue

    no_data_years = set(YEARS).symmetric_difference(set(available_years))
    logger.info(f"available_years: {available_years}")
    logger.info(f"no_data_years: {no_data_years}")

    if len(available_years) > 0:
        res = {
            str(year): {
                "label": str(year),
                "style": {"color": "#7fafdf" if year in available_years else "#FF0000"},
            }
            for year in YEARS
        }

        return [res]

    return [{
        str(year): {
            "label": str(year),
            "style": {"color": "#FF0000"},
        }
        for year in YEARS
    }]


if __name__ == "__main__":
    app.run_server(debug=True, port=18050, processes=1, threaded=True, use_reloader=False) # host="0.0.0.0",


