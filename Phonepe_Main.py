import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import psycopg2
import requests
import json

# DataFrame Creation
# Sql Connection
mydb = psycopg2.connect(host= "localhost",port= 5432,database = "phonepe_pulse_data",user= "postgres",password = "Post!2025")
cur=mydb.cursor()
#Aggregated_Insurance_df
cur.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 = cur.fetchall()
aggregated_insurance_df = pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))

#Aggregated_Transaction_df
cur.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cur.fetchall()
aggregated_transaction_df = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))

#Aggregated_User_df
cur.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 = cur.fetchall()
aggregated_user_df = pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands",
                                               "Transaction_count", "Percentage"))

#Map_Insurance_df
cur.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 = cur.fetchall()
map_insurance_df = pd.DataFrame(table4, columns=("States", "Years", "Quarter", "Districts",
                                               "Transaction_count", "Transaction_amount"))

#Map_Transaction_df
cur.execute("SELECT * FROM map_transaction")
mydb.commit()
table5 = cur.fetchall()
map_transaction_df = pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Districts",
                                               "Transaction_count", "Transaction_amount"))

#Map_User_df
cur.execute("SELECT * FROM map_user")
mydb.commit()
table6 = cur.fetchall()
map_user_df = pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Districts",
                                               "Registered_Users", "App_Opens"))

#Top_Insurance_df
cur.execute("SELECT * FROM top_insurance")
mydb.commit()
table7 = cur.fetchall()
top_insurance_df = pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#Top_Transaction_df
cur.execute("SELECT * FROM top_transaction")
mydb.commit()
table8 = cur.fetchall()
top_transaction_df = pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#Top_User_df
cur.execute("SELECT * FROM top_user")
mydb.commit()
table9 = cur.fetchall()
top_user_df = pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes","RegisteredUsers"))


# Analysis functions
# Transaction_Year_wise
def transaction_amount_count_y(df, year):
    tac_year = df[df["Years"] == year]
    tac_year.reset_index(drop=True, inplace=True)

    tac_year_g=tac_year.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tac_year_g.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tac_year_g,x="States",y="Transaction_amount", title=f"TRANSACTION AMOUNT:BAR CHART, FOR THE YEAR: {year}")
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(tac_year_g,x="States",y="Transaction_count", title=f"TRANSACTION COUNT:BAR CHART, FOR THE YEAR: {year}")
        st.plotly_chart(fig_count)

    india_geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(india_geo_url)
    response_data = json.loads(response.content)

    states_name = []
    for feature in response_data["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()
    col3, col4 = st.columns(2)
    with col3:
        fig_india_1 = px.choropleth(tac_year_g, geojson=response_data, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="Viridis",
                                    range_color=(tac_year_g["Transaction_amount"].min(),
                                                 tac_year_g["Transaction_amount"].max()),
                                    hover_name="States", title=f"TRANSACTION AMOUNT:GEO CHART, FOR THE YEAR: {year}",
                                    fitbounds="locations", height=600, width=600)
        fig_india_1.update_geos(visible=False, fitbounds="locations")
        st.plotly_chart(fig_india_1)

    with col4:
        fig_india_2 = px.choropleth(tac_year_g, geojson=response_data, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="RAINBOW",
                                    range_color=(tac_year_g["Transaction_count"].min(),
                                                 tac_year_g["Transaction_count"].max()),
                                    hover_name="States", title=f"TRANSACTION COUNT:GEO CHART, FOR THE YEAR: {year}",
                                    fitbounds="locations", height=600, width=600)
        fig_india_2.update_geos(visible=False, fitbounds="locations")

        # fig_india_2.show()
        st.plotly_chart(fig_india_2)
    return tac_year

# Transaction_Year_wise
def transaction_amount_count_y_q(df, quarter):
    tac_year_q = df[df["Quarter"] == quarter]
    tac_year_q.reset_index(drop=True, inplace=True)

    tac_year_q_g=tac_year_q.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tac_year_q_g.reset_index(inplace=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tac_year_q_g,x="States",y="Transaction_amount",
                            title=f"TRANSACTION AMOUNT:BAR CHART, FOR THE YEAR: {tac_year_q['Years'].min()} AND QUARTER: {quarter}",
                            height= 700, width=700)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(tac_year_q_g,x="States",y="Transaction_count",
                           title=f"TRANSACTION COUNT:BAR CHART, FOR THE YEAR: {tac_year_q['Years'].min()} AND QUARTER: {quarter}",
                           height= 700, width=700)
        st.plotly_chart(fig_count)

    india_geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(india_geo_url)
    response_data = json.loads(response.content)

    states_name = []
    for feature in response_data["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()
    col3, col4 = st.columns(2)
    with col3:
        fig_india_1 = px.choropleth(tac_year_q_g, geojson=response_data, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="Viridis",
                                    range_color=(tac_year_q_g["Transaction_amount"].min(), tac_year_q_g["Transaction_amount"].max()),
                                    hover_name="States", fitbounds="locations", height= 600, width=600,
                                    title=f"TRANSACTION AMOUNT:GEO CHART, FOR THE YEAR: {tac_year_q['Years'].min()} AND QUARTER: {quarter}")
        fig_india_1.update_geos(visible=False, fitbounds="locations",projection_scale=2.0)
        st.plotly_chart(fig_india_1)

    with col4:
        fig_india_2 = px.choropleth(tac_year_q_g, geojson=response_data, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="RAINBOW",
                                    range_color=(tac_year_q_g["Transaction_count"].min(), tac_year_q_g["Transaction_count"].max()),
                                    hover_name="States", fitbounds="locations", height= 600, width=600,
                                    title=f"TRANSACTION COUNT:GEO CHART, FOR THE YEAR: {tac_year_q['Years'].min()} QUARTER: {quarter} ")
        fig_india_2.update_geos(visible=False, fitbounds="locations",projection_scale=2.0)
        st.plotly_chart(fig_india_2)
    return tac_year_q

# Transaction_Year_wise_transaction_Type_wise
def aggr_tran_transaction_type(df, state):
    tac_year_s = df[df["States"] == state]
    tac_year_s.reset_index(drop=True, inplace=True)

    tac_year_s_g=tac_year_s.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    tac_year_s_g.reset_index(inplace=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame=tac_year_s_g, names="Transaction_type", values="Transaction_amount", width=600,
                           title=f"TRANSACTION AMOUNT:PIE CHART, FOR THE STATE: {state.upper()}", hole=0.4)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2 = px.pie(data_frame=tac_year_s_g, names="Transaction_type", values="Transaction_count", width=600,
                           title=f"TRANSACTION COUNT:PIE CHART, FOR THE STATE: {state.upper()}", hole=0.4)
        st.plotly_chart(fig_pie_2)

# Aggregated User Analysis
def aggre_user_chart_y(df, year):
    agu_year = df[df["Years"] == year]
    agu_year.reset_index(drop=True, inplace=True)

    agu_year_g = pd.DataFrame(agu_year.groupby("Brands")["Transaction_count"].sum())
    agu_year_g.reset_index(inplace=True)

    fig_au_bar_1 = px.bar(agu_year_g, x="Brands", y="Transaction_count", title=f"TRANSACTION AMOUNT:BAR CHART:BRANDS FOR THE YEAR {year}",
                          width=600, height=600, color_discrete_sequence=px.colors.sequential.BuGn_r)
    st.plotly_chart(fig_au_bar_1)
    return agu_year

def aggre_user_chart_q(df, quarter):
    agu_y_q = df[df["Quarter"] == quarter]
    agu_y_q.reset_index(drop=True, inplace=True)

    agu_y_q_g = pd.DataFrame(agu_y_q.groupby("Brands")["Transaction_count"].sum())
    agu_y_q_g.reset_index(inplace=True)

    fig_au_bar_2 = px.bar(agu_y_q_g, x="Brands", y="Transaction_count",
                          title=f"TRANSACTION AMOUNT:BAR CHART:BRANDS FOR THE YEAR {aggre_user_y_filtered['Years'].min()} AND QUARTER {quarter}",
                          width=800, height=700, color_discrete_sequence=px.colors.sequential.BuGn_r)
    st.plotly_chart(fig_au_bar_2)
    return agu_y_q

def aggr_user_brands_y_q_state(df, state):
    agu_y_q_s = df[df["States"] == state]
    agu_y_q_s.reset_index(drop=True, inplace=True)
    fig_line_chart_1 = px.line(agu_y_q_s, x="Brands", y="Transaction_count", width=900, hover_data="Percentage",
                       title=f"LINE CHART:BRANDS:TRANSACTION COUNT, PERCENTAGE FOR THE STATE:{state.upper()}", markers=True)
    st.plotly_chart(fig_line_chart_1)

# District based State wise Analysis Map Insurance
def map_ins_district_y(df, state):
    map_tac_year_s = df[df["States"] == state]
    map_tac_year_s.reset_index(drop=True, inplace=True)

    map_tac_year_s_g=map_tac_year_s.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    map_tac_year_s_g.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar_chart_1 = px.bar(map_tac_year_s_g, x="Transaction_amount", y="Districts", orientation="h",
                                 title=f"TRANSACTION AMOUNT:BAR CHART: DISTRICT BASED FOR THE STATE: {state.upper()}",
                                 color_discrete_sequence=px.colors.sequential.BuGn_r, height=600)

        st.plotly_chart(fig_bar_chart_1)
    with col2:
        fig_bar_chart_2 = px.bar(map_tac_year_s_g, x="Transaction_count", y="Districts", orientation="h",
                                 title=f"TRANSACTION COUNT:BAR CHART: DISTRICT BASED FOR THE STATE: {state.upper()}",
                                 color_discrete_sequence=px.colors.sequential.BuGn_r, height=600)
        st.plotly_chart(fig_bar_chart_2)

# Creating function, map User Analysis
def map_user_tac_y(df, year):
    mapu_year = df[df["Years"] == year]
    mapu_year.reset_index(drop=True, inplace=True)

    mapu_year_g = pd.DataFrame(mapu_year.groupby("States")[["Registered_Users", "App_Opens"]].sum())
    mapu_year_g.reset_index(inplace=True)

    fig_mapu_linec_1 = px.line(mapu_year_g, x="States", y=["Registered_Users", "App_Opens"], width=900, height=800,
                       title=f"LINE CHART:REGISTERED_USERS AND APP_OPENS IN THE YEAR:{year}", markers=True)
    st.plotly_chart(fig_mapu_linec_1)
    return mapu_year

# Function for map User Quarter Analysis
def map_user_tac_y_q(df, quarter):
    mapu_year_q = df[df["Quarter"] == quarter]
    mapu_year_q.reset_index(drop=True, inplace=True)

    mapu_year_q_g = pd.DataFrame(mapu_year_q.groupby("States")[["Registered_Users", "App_Opens"]].sum())
    mapu_year_q_g.reset_index(inplace=True)

    fig_mapu_linec_2 = px.line(mapu_year_q_g, x="States", y=["Registered_Users", "App_Opens"], width=900, height=800,
                       title=f"LINE CHART:REGISTERED_USERS AND APP_OPENS FOR THE YEAR {df['Years'].min()} AND QUARTER {quarter}", markers=True)
    st.plotly_chart(fig_mapu_linec_2)
    return mapu_year_q

# District based State wise Analysis Map User
def map_user_district_y_q(df, state):
    mapu_y_q_s = df[df["States"] == state]
    mapu_y_q_s.reset_index(drop=True, inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_mu_bar_chart_1 = px.bar(mapu_y_q_s, x="Registered_Users", y="Districts", orientation="h",
                                 title=f"BAR CHART: REGISTERED USER :DISTRICT BASED FOR THE STATE: {state.upper()}",
                                 color_discrete_sequence=px.colors.sequential.BuGn_r, height=800)

        st.plotly_chart(fig_mu_bar_chart_1)
    with col2:
        fig_mu_bar_chart_2 = px.bar(mapu_y_q_s, x="App_Opens", y="Districts", orientation="h",
                                 title=f"BAR CHART: APP OPENS :DISTRICT BASED FOR THE STATE: {state.upper()}",
                                 color_discrete_sequence=px.colors.sequential.BuGn, height=800)
        st.plotly_chart(fig_mu_bar_chart_2)

# Function for Top Insurance State Analysis
def top_ins_tac_y_s(df, state):
    tins_year_s = df[df["States"] == state]
    tins_year_s.reset_index(drop=True, inplace=True)

    # tins_year_s_g = tins_year_s.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    # tins_year_s_g.reset_index(inplace=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_topins_barc_1 = px.bar(tins_year_s, x="Quarter", y="Transaction_count", hover_data="Pincodes",width=900, height=800,
                           title=f"BAR CHART:TRANSACTION COUNT FOR THE YEAR {df['Years'].min()}", color_discrete_sequence=px.colors.sequential.BuGn_r)
        st.plotly_chart(fig_topins_barc_1)

    with col2:
        fig_topins_barc_2 = px.bar(tins_year_s, x="Quarter", y="Transaction_amount", hover_data="Pincodes",width=900, height=800,
                           title=f"BAR CHART:TRANSACTION AMOUNT FOR THE YEAR {df['Years'].min()}", color_discrete_sequence=px.colors.sequential.BuGn)
        st.plotly_chart(fig_topins_barc_2)
    return tins_year_s

# Function for Top User Year Analysis
def top_user_tac_y(df, year):
    topu_year = df[df["Years"] == year]
    topu_year.reset_index(drop=True, inplace=True)

    topu_year_g = pd.DataFrame(topu_year.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    topu_year_g.reset_index(inplace=True)

    fig_topu_bar_1 = px.bar(topu_year_g, x="States", y="RegisteredUsers", color="Quarter", width=900, height=800,
                       title=f"BAR CHART:REGISTERED_USERS FOR THE YEAR: {year}", hover_name= "States",
                             color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_topu_bar_1)
    return topu_year

# Streamlit Section

st.set_page_config(layout="wide")
st.title("Phonepe Pulse Data Visualization")

with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Data Exploration", "Top Charts"])

if select == "Home":
    pass
elif select == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    with tab1:
        method_1 = st.radio("Select the method", ["Aggregated Insurance Analysis", "Aggregated Transaction Analysis", "Aggregated User Analysis"])
        if method_1 == "Aggregated Insurance Analysis":
            # Bar Chart and India Map Chart for Years
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the years", aggregated_insurance_df["Years"].min(),
                                  aggregated_insurance_df["Years"].max(), aggregated_insurance_df["Years"].min())
                # years = st.selectbox("Select the years", aggregated_insurance_df["Years"].unique())
            tac_year_filtered = transaction_amount_count_y(aggregated_insurance_df, years)

            # Bar Chart and India Map Chart for Quarters
            col1, col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the quarters", tac_year_filtered["Quarter"].min(),tac_year_filtered["Quarter"].max(),
                                    tac_year_filtered["Quarter"].min())
            transaction_amount_count_y_q(tac_year_filtered, quarters)

        elif method_1 == "Aggregated Transaction Analysis":
            st.write("Year Wise Analysis for Every States:")
            # Bar Chart and India Map Chart for Years
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the years", aggregated_transaction_df["Years"].min(),
                                  aggregated_transaction_df["Years"].max(), aggregated_transaction_df["Years"].min())
            agg_tran_tac_year_filtered = transaction_amount_count_y(aggregated_transaction_df, years)

            # Pie Chart for Years based on Transaction Type
            col1, col2 = st.columns(2)
            with col1:
                state= st.selectbox("Select the State for Year Wise Analysis",
                                    agg_tran_tac_year_filtered["States"].unique())
            aggr_tran_transaction_type(agg_tran_tac_year_filtered, state)

            st.write("Quarter Wise Analysis for Every States of the Above Selected Year:")
            # Bar Chart and India Map Chart for Quarters
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarters", agg_tran_tac_year_filtered["Quarter"].min(),
                                     agg_tran_tac_year_filtered["Quarter"].max(),
                                     agg_tran_tac_year_filtered["Quarter"].min())
            agg_tran_tac_y_q_filtered = transaction_amount_count_y_q(agg_tran_tac_year_filtered, quarters)

            # Pie Chart for Year and Quarter based on Transaction Type
            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State for Quarter Wise Analysis for the Selected Year",
                                     agg_tran_tac_y_q_filtered["States"].unique())
            aggr_tran_transaction_type(agg_tran_tac_y_q_filtered, state)

        elif method_1 == "Aggregated User Analysis":
            # Bar Chart and India Map Chart for Years
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the years", aggregated_user_df["Years"].min(),
                                  aggregated_user_df["Years"].max(), aggregated_user_df["Years"].min())
            aggre_user_y_filtered = aggre_user_chart_y(aggregated_user_df, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarters", aggre_user_y_filtered["Quarter"].min(),
                                     aggre_user_y_filtered["Quarter"].max(),
                                     aggre_user_y_filtered["Quarter"].min())
            aggre_user_y_q_filtered = aggre_user_chart_q(aggre_user_y_filtered, quarters)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State for Year Wise Analysis",
                                     aggre_user_y_q_filtered["States"].unique())
            aggr_user_brands_y_q_state(aggre_user_y_q_filtered, state)

    with tab2:
        method_2 = st.radio("Select the method", ["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])
        if method_2 == "Map Insurance Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the years for Map Insurance Analysis", map_insurance_df["Years"].min(),
                                  map_insurance_df["Years"].max(), map_insurance_df["Years"].min())

            map_ins_tac_year_filtered = transaction_amount_count_y(map_insurance_df, years)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State for Year Wise District Analysis MI",
                                     map_ins_tac_year_filtered["States"].unique())
            map_ins_district_y(map_ins_tac_year_filtered, state)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarters for Quarter Wise District Analysis MI",
                                     map_ins_tac_year_filtered["Quarter"].min(),
                                     map_ins_tac_year_filtered["Quarter"].max(),
                                     map_ins_tac_year_filtered["Quarter"].min())
            map_ins_tac_y_q_filtered = transaction_amount_count_y_q(map_ins_tac_year_filtered, quarters)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State for Quarter Wise District Analysis MI",
                                     map_ins_tac_y_q_filtered["States"].unique())
            map_ins_district_y(map_ins_tac_y_q_filtered, state)


        elif method_2 == "Map Transaction Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the years for Map Transaction Analysis", map_transaction_df["Years"].min(),
                                  map_transaction_df["Years"].max(), map_transaction_df["Years"].min())

            map_trans_tac_year_filtered = transaction_amount_count_y(map_transaction_df, years)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State for Year Wise District Analysis MP",
                                     map_trans_tac_year_filtered["States"].unique())
            map_ins_district_y(map_trans_tac_year_filtered, state)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarters for Quarter Wise District Analysis MP",
                                     map_trans_tac_year_filtered["Quarter"].min(),
                                     map_trans_tac_year_filtered["Quarter"].max(),
                                     map_trans_tac_year_filtered["Quarter"].min())
            map_trans_y_q_filtered = transaction_amount_count_y_q(map_trans_tac_year_filtered, quarters)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State for Quarter Wise District Analysis MP",
                                     map_trans_y_q_filtered["States"].unique())
            map_ins_district_y(map_trans_y_q_filtered, state)

        elif method_2 == "Map User Analysis":
            # LINE Chart for Years
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the years for Map User", map_user_df["Years"].min(),
                                  map_user_df["Years"].max(), map_user_df["Years"].min())
            map_user_y_filtered = map_user_tac_y(map_user_df, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarters for Quarter Wise District Analysis MU",
                                     map_user_y_filtered["Quarter"].min(),
                                     map_user_y_filtered["Quarter"].max(),
                                     map_user_y_filtered["Quarter"].min())
            map_user_y_q_filtered = map_user_tac_y_q(map_user_y_filtered, quarters)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State for Quarter Wise District Analysis MU",
                                     map_user_y_q_filtered["States"].unique())
            map_user_district_y_q(map_user_y_q_filtered, state)

    with tab3:
        method_3 = st.radio("Select the method", ["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])
        if method_3 == "Top Insurance Analysis":

            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the years for TI Analysis", top_insurance_df["Years"].min(),
                                  top_insurance_df["Years"].max(), top_insurance_df["Years"].min())
            top_ins_tac_y_filtered = transaction_amount_count_y(top_insurance_df, years)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State for Pincodes Wise District Analysis TI",
                                     top_ins_tac_y_filtered["States"].unique())
            top_ins_tacy_s_filtered = top_ins_tac_y_s(top_ins_tac_y_filtered, state)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter for TI Analysis", top_ins_tac_y_filtered["Quarter"].min(),
                                  top_ins_tac_y_filtered["Quarter"].max(), top_ins_tac_y_filtered["Quarter"].min())
            top_ins_tac_y_q_filtered = transaction_amount_count_y_q(top_ins_tac_y_filtered, quarters)

        elif method_3 == "Top Transaction Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the years for TT Analysis", top_transaction_df["Years"].min(),
                                  top_transaction_df["Years"].max(), top_transaction_df["Years"].min())
            top_trans_tac_y_filtered = transaction_amount_count_y(top_transaction_df, years)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State for Pincodes Wise District Analysis TT",
                                     top_trans_tac_y_filtered["States"].unique())
            top_trans_tacy_s_filtered = top_ins_tac_y_s(top_trans_tac_y_filtered, state)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter for TT Analysis", top_trans_tac_y_filtered["Quarter"].min(),
                                     top_trans_tac_y_filtered["Quarter"].max(), top_trans_tac_y_filtered["Quarter"].min())
            top_tran_tac_y_q_filtered = transaction_amount_count_y_q(top_trans_tac_y_filtered, quarters)


        elif method_3 == "Top User Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the years for TU Analysis", top_user_df["Years"].min(),
                                  top_user_df["Years"].max(), top_user_df["Years"].min())
            top_user_year_filtered = top_user_tac_y(top_user_df, years)


elif select == "Top Charts":
    pass