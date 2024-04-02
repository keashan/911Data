import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input

from data_processing import get_data
from app import app
from data_processing.get_data import get_category_list, get_month_list

import plotly.express as px

# month_color = {"January": "#FF0000", "February": "#FFA500", "March": "#FFFF00", "April": "#008000", "May": "#0000FF",
#              "June": "#4B0082"}
# priority_color = {"1": "#FF0000", "2": "#FFA500", "3": "#FFFF00", "4": "#008000", "5": "#0000FF", "6": "#4B0082"}


def home_page():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div(children=[
                    html.Div("Filter Area", className="card_title"),
                    html.Div("Deposition Category", id="filter_description_text"),
                    dcc.Dropdown(
                        id="filter_category",
                        options=get_category_list(),
                        multi=True
                    ),
                    html.Div("Month"),
                    dcc.Dropdown(
                        id="filter_month",
                        options=get_month_list(),
                        multi=True
                    ),
                ], className="card")
            ], width=3, xs=12, sm=12, md=12, lg=3, xl=3),
            dbc.Col([
                dbc.Row([
                    html.Div("Summary in Numbers", className="card_title")
                ], className="row_class"),
                dbc.Row([
                    dbc.Col([
                        html.Div(children=[
                            html.Div("Loading", id="total_calls", className="card_title value_card_title"),
                            html.Div("Total Calls"),
                        ], className="card value_card")
                    ], lg=2, xl=2, md=4, sm=4, xs=6, className="mb-2"),
                    dbc.Col([
                        html.Div(children=[
                            html.Div("Loading", id="no_report", className="card_title value_card_title"),
                            html.Div("No Report Required"),
                        ], className="card value_card")
                    ], lg=2, xl=2, md=4, sm=4, xs=6, className="mb-2"),
                    dbc.Col([
                        html.Div(children=[
                            html.Div("Loading", id="cancelled_calls", className="card_title value_card_title"),
                            html.Div("Cancelled Calls"),
                        ], className="card value_card")
                    ], lg=2, xl=2, md=4, sm=4, xs=6, className="mb-2"),
                    dbc.Col([
                        html.Div(children=[
                            html.Div("Loading", id="report_taken", className="card_title value_card_title"),
                            html.Div("Report Taken Calls"),
                        ], className="card value_card")
                    ], lg=2, xl=2, md=4, sm=4, xs=6, className="mb-2"),
                    dbc.Col([
                        html.Div(children=[
                            html.Div("Loading", id="no_response", className="card_title value_card_title"),
                            html.Div("No Response Calls"),
                        ], className="card value_card")
                    ], lg=2, xl=2, md=4, sm=4, xs=6, className="mb-2"),
                    dbc.Col([
                        html.Div(children=[
                            html.Div("Loading", id="unable_to_locate", className="card_title value_card_title"),
                            html.Div("Unable to Locate"),
                        ], className="card value_card")
                    ], lg=2, xl=2, md=4, sm=4, xs=6, className="mb-2"),
                ], className="row_class"),
            ], width=9, xs=9, sm=12, md=12, lg=9, xl=9),
        ], className="row_class"),
        dbc.Row([
            dbc.Col([
                html.Div(children=[
                    html.Div("Total Calls by Month", className="card_title"),
                    dcc.Loading(
                        dcc.Graph(id="total_calls_by_month"),
                        type="dot"
                    )
                ], className="card")
            ], width=4, xl=4, lg=4, md=6, sm=12, xs=12, className="mb-2"),
            dbc.Col([
                html.Div(children=[
                    html.Div("Total Calls by Weekday", className="card_title"),
                    dcc.Loading(
                        dcc.Graph(id="total_calls_by_weekday"),
                        type="dot"
                    )
                ], className="card")
            ], width=8, xl=8, lg=8, md=6, sm=12, xs=12, className="mb-2"),
        ], className="row_class"),
        dbc.Row([
            dbc.Col([
                html.Div(children=[
                    html.Div("Total Call by Priority", className="card_title"),
                    dcc.Loading(
                        dcc.Graph(id="total_calls_by_priority"),
                        type="dot"
                    ),
                ], className="card")
            ], width=6, xl=6, lg=6, md=6, sm=12, xs=12, className="mb-2"),
            dbc.Col([
                html.Div(children=[
                    html.Div("Call Type Description Analysis", className="card_title"),
                    dcc.Loading(
                        dcc.Graph(id="call_type_description_analysis"),
                        type="dot"
                    ),
                ], className="card")
            ], width=6, xl=6, lg=6, md=6, sm=12, xs=12, className="mb-2"),
        ], className="row_class"),
        dbc.Row([
            html.Div(children=[
                html.Div(children=[
                    html.Div("Total Calls by Hour of the Day", className="card_title"),
                    dcc.Loading(
                        dcc.Graph(id="calls_by_hour_graph"),
                        type="dot",
                    ),
                ], className="card")
            ]),

        ], className="mb-2"),
        dbc.Row([
            html.Div(children=[
                html.Div(children=[
                    html.Div("Total Calls by Hour of the Day - Animated", className="card_title"),
                    dcc.Loading(
                        dcc.Graph(id="animated_calls_by_hour_graph"),
                        type="dot",
                    ),
                ], className="card")
            ]),

        ], className="mb-2"),

    ], fluid=True)


# Generate KPI numbers
@app.callback(
    [Output("total_calls", "children"),
     Output("no_report", "children"),
     Output("cancelled_calls", "children"),
     Output("report_taken", "children"),
     Output("no_response", "children"),
     Output("unable_to_locate", "children")],
    [Input("filter_month", "value"),
     Input("filter_category", "value")]
)
def update_summary_numbers(month, category):
    df_summary = get_data.get_call_data(month, category)
    all_calls = f'{df_summary.shape[0]:,}'
    no_report = f'{df_summary[df_summary["FINAL_DISPO"].str.contains("No report required", case=False)].shape[0]:,}'
    cancelled_calls = f'{df_summary[df_summary["FINAL_DISPO"].str.contains("Canceled", case=False)].shape[0]:,}'
    report_taken = f'{df_summary[df_summary["FINAL_DISPO"].str.contains("Report taken", case=False)].shape[0]:,}'
    no_response = f'{df_summary[df_summary["FINAL_DISPO"].str.contains("No response", case=False)].shape[0]:,}'
    unable_to_locate = f'{df_summary[df_summary["FINAL_DISPO"].str.contains("Unable to locate", case=False)].shape[0]:,}'
    del df_summary
    return all_calls, no_report, cancelled_calls, report_taken, no_response, unable_to_locate


# Generate total calls by month graph, total calls by weekday graph, total calls by priority graph
@app.callback(
    [Output("total_calls_by_month", "figure"),
     Output("total_calls_by_weekday", "figure"),
     Output("total_calls_by_priority", "figure")],
    [Input("filter_month", "value"),
     Input("filter_category", "value")]
)
def update_total_calls_by_month_weekday(month, category):
    # get filtered data
    df_call_data = get_data.get_call_data(month, category)
    # rename "EID" column to "Call Count"
    df_call_data.rename(columns={"EID": "Call Count"}, inplace=True)
    # group data to have total calls by priority, weekday
    df_priority = df_call_data.groupby(["PRIORITY"]).count()["Call Count"].reset_index()
    df_call_data = df_call_data.groupby(["Weekday", "Month"]).count()["Call Count"].reset_index()
    # create figure for total calls by weekday
    fig_weekday = px.bar(df_call_data, x="Weekday", y="Call Count", color="Month", height=350)
                         # color_discrete_map=month_color)
    fig_weekday.update_layout({
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': '#002366',
    },
        showlegend=False)
    # Group data to have total calls by month
    df_call_data = df_call_data.groupby("Month")[["Call Count"]].sum().reset_index()
    # Create figure for total calls by month
    fig_month = px.bar(df_call_data, x="Month", y="Call Count", color="Month", height=350)
    fig_month.update_layout({
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': '#002366'
    },
        showlegend=False)
    # Create figure for total calls by priority
    fig_priority = px.pie(df_priority, values="Call Count", names="PRIORITY", color="PRIORITY", height=350)
    fig_priority.update_layout({
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': '#002366'
    },
        showlegend=False)
    del df_call_data
    del df_priority
    return fig_month, fig_weekday, fig_priority


# Generate call type description analysis graph(wordcloud)
@app.callback(
    Output("call_type_description_analysis", "figure"),
    [Input("filter_month", "value"),
     Input("filter_category", "value")]
)
def update_call_type_description_analysis(month, category):
    # get filtered data
    df_call_data = get_data.get_call_data(month, category)
    # Convert to call type data to a list
    call_type_list = df_call_data["CALL_TYPE"].to_list()
    del df_call_data
    # Create the wordcloud using the call type list
    word_cloud = get_data.get_word_cloud(call_type_list)
    # Create figure for wordcloud
    fig_cloud = px.imshow(word_cloud, height=350)
    fig_cloud.update_xaxes(visible=False)
    fig_cloud.update_yaxes(visible=False)
    fig_cloud.update_layout(margin=dict(l=10, r=10, b=0, t=25, pad=4))

    fig_cloud.update_layout({
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': '#002366'
    },
        showlegend=False)

    return fig_cloud


# Generate total calls by hour of the day and animated calls by hour of the day graph
@app.callback(
    [Output("calls_by_hour_graph", "figure"),
     Output("animated_calls_by_hour_graph", "figure")],
    [Input("filter_month", "value"),
     Input("filter_category", "value")]
)
def update_graph(filter_month, filter_category):
    # Load csv file again.
    df_data = get_data.load_data()
    selected_months = []
    # Filter data based on month and category
    if filter_month:
        if isinstance(filter_month, list):
            selected_months = filter_month
        else:
            selected_months.append(filter_month)
        df_data = df_data[df_data["Month"].isin(selected_months)]

    selected_categories = []
    if filter_category:
        if isinstance(filter_category, list):
            selected_categories = filter_category
        else:
            selected_categories.append(filter_category)
        df_data = df_data[df_data["FINAL_DISPO"].isin(selected_categories)]

    # Sort data by time and month
    df_data.sort_values(by=["Offence Time", "Month_Number"], inplace=True)
    # Group data by hour of the day and month
    df_hour = df_data.groupby(["Month", "Offence Time"]).size().to_frame("EID").reset_index()
    del df_data
    # Rename "EID" column to "Call Count"
    df_hour.rename(columns={"EID": "Call Count"}, inplace=True)

    # Create figure for total calls by hour of the day
    fig_hour = px.bar(df_hour, x="Offence Time", y="Call Count", color="Month", height=350)
    fig_hour.update_layout({
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': '#002366'
    },
        showlegend=False)

    # Create figure for animated calls by hour of the day
    fig_animated_hour = px.bar(df_hour, x="Month", y="Call Count", color="Month", animation_frame="Offence Time",
                               height=350, range_y=[0, df_hour["Call Count"].max()], text="Call Count")

    fig_animated_hour.update_layout({
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': '#002366'
    },
        showlegend=False)

    # Update legend position
    fig_animated_hour.update_layout(legend={"orientation": "v"}, legend_x=1, legend_y=1)

    # Update frame and transition duration
    fig_animated_hour.layout.updatemenus[0].buttons[0].args[1]["frame"] = {
        "duration": 1_500}
    fig_animated_hour.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1_000
    del df_hour
    return fig_hour, fig_animated_hour
