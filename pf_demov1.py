# -*- coding: utf-8 -*-
"""
Plain.ai - Intelisense, AI Insight Console
@author: Madhur Sarin
"""
import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


from PIL import Image

# st.set_page_config(page_title='Plain.ai - Intelisense', layout='wide',
#                    # page_icon='icon3.png'
#                    )



# sb = st.sidebar.write("Intelisense")


# start section 1........................
# this is the header
# two column layout for the header
t1, t2 = st.columns((0.20, 1.3))



t1.image('icon3.png', width=150)  # adding icon to variable t1
t2.title("AI Insights & Predictive Maintenance Console ") # dashboard title
t2.markdown(
    " **Published  Week:  52 , Date:  23-Dec to 30-Dec , 2021**" )


# End of section 1.......................

### Section 2 - Load data from excel database - refactor to csv
excel_file = 'result.xls'
sheet_name = 'tw_summary'

# summary of dashboard
df_tw = pd.read_excel(excel_file,
                         sheet_name=sheet_name,
                         usecols='B:G',
                         header=0)

# database of past results

df_db = pd.read_excel(excel_file,
                         sheet_name='pw_database',
                         usecols='B:H',
                         header=0)

# aggregated  summary of historical predictions
df_hist = pd.read_excel(excel_file,
                         sheet_name='hist_summary',
                         usecols='B:H',
                         header=0)

# list of machines that needs actions with details

df_action = pd.read_excel(excel_file,
                         sheet_name='action',
                         usecols='B:G',
                         header=0)
# RF/AI output to be configured for slice and dice
df_out = pd.read_excel(excel_file,
                         sheet_name='tw_out_pivot_dash',
                         usecols='A:J',
                         header=0)

df_out_face = pd.read_excel(excel_file,
                         sheet_name='tw_out',
                         usecols='A:AO',
                         header=0)

# end of section 2

# start of section 3, laying the metrics on the dashboard and calculations
# dashboard summary, 7 column layout for metrics

m1, m2, m3, m4, m5,m6,m7 = st.columns((1,1,1,1,1,1,1))

m1.write('')
# m7.metric(label ='Opportunity TD',value = "$ "+  str(int(df_tw['Total TY'])),
#           # delta = str(int(to['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse'
#           )
m2.metric(label ='Predicted Failure',value = int(df_tw['Predicted Failure TY']),
          # delta = str(int(to['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse'
          )

m3.metric(label ='Planned Maintenance',value = int(df_tw['Planned Maintenance TY']),
          # delta = str(int(to['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse'
          )
m4.metric(label ='Common Incidents',value = int(df_tw['Common Incidents']),
          # delta = str(int(to['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse'
          )

m6.metric(label ='Benefit Potential TW ($)',value = "$ "+ str(int(df_tw['Benefit Potential']))  )
          # delta = str(int(to['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse'


r1, r2 = st.columns((1, 1))
r2.title("                                                                                            ")
# Comparative accuracy tw
abc = df_db
abc = abc[abc['Week'] == 51]
m5.metric(label ='AI Accuracy LW',value = str( int(abc['Accuracy'])) + ' %',delta = str(int(abc['PW Accuracy ']))
                                                                                    +' % Over Previous', delta_color = 'inverse')

st.markdown("Trend by Week")
# week_sel = st.selectbox('Choose Week', df_db, help='Filter report to show only one week')

selected_option_2 = st.multiselect("Select one or more week :", [51,50,49,48,47,46,'All'],help= 'Filter report to show only one week' )

if "All" in selected_option_2:
    selected_option_2 = [51, 50, 49,48,47,46]

week_sel = selected_option_2

# 3 coloumn layout for 3 graphs

g1, g2, g3 = st.columns((1, 1, 1))

fgdf = df_db

# fgdf = fgdf[fgdf['Week'] == 51]

fgdf= fgdf.loc[fgdf['Week'].isin(week_sel)]

fig = px.bar(fgdf, x='Week', y=['Actual Failure', 'Predicted Failure','Actual Maintained'], template='seaborn')

# fig.update_traces(marker_color='#264653')

fig.update_layout(title_text="Failures by Week ", title_x=0, margin=dict(l=0, r=20, b=20, t=50),
                  yaxis_title=None, xaxis_title=None,barmode='group',showlegend=False)

g1.plotly_chart(fig, use_container_width=True)

# 2nd bar chart

fig = px.line(fgdf, x='Week', y=['Accuracy'], template='seaborn')

fig.update_traces(line_color='#33FF57' )

fig.update_layout(title_text="Accuracy", title_x=0, margin=dict(l=0, r=20, b=20, t=50),
                  yaxis_title=None, xaxis_title=None,showlegend=False)

g2.plotly_chart(fig, use_container_width=True)

# 3rd Bar chart

fig = px.bar(fgdf, x='Week', y=['Missed Opportunity'], template='seaborn')

fig.update_traces(marker_color='#FF5733')

fig.update_layout(title_text="Missed Opportunity $", title_x=0, margin=dict(l=0, r=20, b=20, t=50),
                  yaxis_title=None, xaxis_title=None,showlegend=False)

g3.plotly_chart(fig, use_container_width=True)

# Performance Section

# with st.expander("Historical AI Accuracy & Benefits Summary"):
df_hist = df_hist.drop(columns='Unnamed: 1')
hhc24 = df_hist

fig = go.Figure(
    data=[go.Table(columnorder=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], columnwidth=[18, 12],
                   header=dict(
                       values=list(hhc24.columns),
                       font=dict(size=16, color='white'),
                       fill_color='#264653',
                       line_color='rgba(255,255,255,0.2)',
                       align=['left', 'center'],
                       # text wrapping
                       height=24
                   )
                   , cells=dict(
            values=[hhc24[K].tolist() for K in hhc24.columns],
            font=dict(size=14),
            align=['left', 'center'],
            # fill_color=colourcode,
            line_color='rgba(255,255,255,0.2)',
            height=24))])

fig.update_layout(title_text="Aggregated Summary of AI performance and potential impact of predictions AO week 52", title_font_color='#264653',
                  title_x=0, margin=dict(l=0, r=10, b=10, t=30), height=100)

st.plotly_chart(fig, use_container_width=True)


with st.expander("Business Diagnostics & Action Sheet"):
    # df_action = df_action.drop(columns='Unnamed: 1')
    # --- PLOT PIE CHART
    g1, g2, g3 = st.columns((1, 1, 1))
    pie_chart1 = px.pie(df_action,
                       title='Failures By Location',
                       values='Count',
                       names='Location')

    g1.plotly_chart(pie_chart1,use_container_width=True)

    pie_chart2 = px.pie(df_action,
                       title='Failures By Model Type',
                       values='Count',
                       names='Model ')
    g2.plotly_chart(pie_chart2,use_container_width=True)

    pie_chart3 = px.pie(df_action,
                        title='Failures By Model Type',
                        values='Count',
                        names='Failure Type')
    g3.plotly_chart(pie_chart3,use_container_width=True)

    hhc24 = df_action

    fig = go.Figure(
        data=[go.Table(columnorder=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], columnwidth=[18, 12],
                       header=dict(
                           values=list(hhc24.columns),
                           font=dict(size=16, color='white'),
                           fill_color='#264653',
                           line_color='rgba(255,255,255,0.2)',
                           align=['left', 'center'],
                           # text wrapping
                           height=24
                       )
                       , cells=dict(
                values=[hhc24[K].tolist() for K in hhc24.columns],
                font=dict(size=14),
                align=['left', 'center'],
                # fill_color=colourcode,
                line_color='rgba(255,255,255,0.2)',
                height=24))])

    fig.update_layout(title_text="Aggregated Summary of AI performance and potential impact of predictions AO week 52",
                      title_font_color='#264653',
                      title_x=0, margin=dict(l=0, r=10, b=10, t=30), height=250)

    st.plotly_chart(fig, use_container_width=True)



with st.expander("AI Diagnostics"):

    selected_option_3 = st.multiselect("Select Model :", ['model1','model2','model3','model4'],
                                       help='Filter report to show only one Model')

    if "All" in selected_option_3:
        selected_option_3 = ['model1','model2','model3','model4']

    abc = selected_option_3

    selected_option_4 = st.multiselect("Select Outcome :", [0,1,'All'],help='Filter report to show only one ID')

    if "All" in selected_option_4:
        selected_option_4 = [0,1]
        # [22,23,35,42,40,47,69,71,73,76,1,10,43,53,68,75,82,84,93,25
        # ,28,29,44,46,50,51,57,61,62,78,83,88]

    g1, g2, g3 , g4 = st.columns((1, 1, 1,1))

    fgdf =  df_out_face

    efg = selected_option_4

    # fgdf = fgdf[fgdf['Week'] == 51]

    fgdf = fgdf.loc[fgdf['model'].isin(abc)]
    fgdf = fgdf.loc[fgdf['Class_binary'].isin(efg)]

    fig = px.box(fgdf, x="model", y="volt", color="Class_binary", points="all")
    fig.update_layout(title_text="Voltage Distribution", title_x=0, margin=dict(l=0, r=20, b=20, t=50))
    g1.plotly_chart(fig, use_container_width=True)

    fig = px.box(fgdf, x="model", y="rotate", color="Class_binary", points="all")
    fig.update_layout(title_text="Rotation Distribution", title_x=0, margin=dict(l=0, r=20, b=20, t=50))
    g2.plotly_chart(fig, use_container_width=True)

    fig = px.box(fgdf, x="model", y="pressure", color="Class_binary", points="all")
    fig.update_layout(title_text="Pressure Distribution", title_x=0, margin=dict(l=0, r=20, b=20, t=50))
    g3.plotly_chart(fig, use_container_width=True)

    fig = px.box(fgdf, x="model", y="vibration", color="Class_binary", points="all")
    fig.update_layout(title_text="Vibration Distribution", title_x=0, margin=dict(l=0, r=20, b=20, t=50))
    g4.plotly_chart(fig, use_container_width=True)

    # n1,n2 =st.columns((1,1))
    # import plotly.express as px
    #
    # fig = px.scatter(fgdf, x="model", y="volt", color="Class_binary", facet_col="model",marginal_x="box")
    # fig.update_layout(title_text="Vibration Distribution", title_x=0, margin=dict(l=0, r=20, b=20, t=50))
    # n1.plotly_chart(fig, use_container_width=True)






