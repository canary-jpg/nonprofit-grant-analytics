""" 
Nonprofit Grant Compliance Dashboard
A Streamlit application for grant management, compliance monitoring, and outcome tracking
"""

import streamlit as st 
import pandas as pd 
import sqlite3 
import plotly.express as px 
import plotly.graph_objects as go 
from datetime import datetime, timedelta 
import os 

#page configuration
st.set_page_config(
    page_title='Grant Compliance Dashboard',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

#custom CSS
st.markdown(""" 
    <style>
    .main {
        padding: 0rem 1rem;
    }
    div[data-testid='stMetric'] {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 2px solid #dee2e6;
    }
    div[data-testid='stMetric'] > label {
        color: #495057 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    div[data-testid='stMetric'] > div {
        color: #212529 !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    div[data-testid='stMetric'] [data-testid='stMetricDelta'] {
        color: #6c757d !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    .alert_box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .alert_warning {
        background-color: #fff3cd;
        border-left; 4px solid #ffc107;
        color: #856404;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        color: #721c24;
    }
    .alert_success {
        background-color: #d4eeda;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #212529 !important;
    }
    [data-testid='stSidebar'] {
        background-color: #f8f9fa !important;
    }
    </style>
""", unsafe_allow_html=True)

#database connection
@st.cache_resource()
def get_connection():
    """Create database connection """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    possible_paths = [
        os.path.join(script_dir, 'nonprofit_grants.db'),
        os.path.join(script_dir, '..', 'data', 'nonprofit_grants.db'),
        'nonprofit_grants.db',
        '../data/nonprofit_grants.db'
    ]

    for db_path in possible_paths:
        if os.path.exists(db_path):
            return sqlite3.connect(db_path, check_same_thread=False)
    raise FileExistsError('Could not find nonprofit_grants.db')

@st.cache_data(ttl=300)
def run_query(query):
    """ Execute SQL query and return Dataframe"""
    conn = get_connection()
    return pd.read_sql_query(query, conn)

#load data functions
def load_grant_summary():
    query = '''
        SELECT * FROM v_grant_summary
        ORDER BY days_remaining
     '''
    return run_query(query)

def load_compliance_alerts():
    query = '''
        SELECT
            ca.*,
            g.grant_name,
            g.funder_name
        FROM v_compliance_alerts ca
        JOIN grants g on ca.grant_id = g.grant_id
        ORDER BY days_overdue DESC
     '''
    return run_query(query)

def load_outcome_performance():
    query = '''
        SELECT * FROM v_outcome_performance
        ORDER BY achievement_percentage DESC
     '''
    return run_query(query)

def load_budget_by_category():
    query = '''
        SELECT
            g.grant_name,
            bc.category_name,
            bc.budgeted_amount,
            bc.spent_amount,
            bc.budgeted_amount - bc.spent_amount as remaining,
            ROUND(100.0 * bc.spent_amount / bc.budgeted_amount, 2) as spent_percentage
        FROM budget_categories bc
        JOIN grants g on bc.grant_id = g.grant_id
        ORDER BY g.grant_name, bc.category_name
     '''
    return run_query(query)

def load_monthly_spending():
    query = '''
        SELECT
            strftime('%Y-%m', expense_date) as month,
            g.grant_name,
            SUM(e.amount) as total_spent
        FROM expenses e
        JOIN grants g ON e.grant_id = g.grant_id
        WHERE expense_date >= date('now', '-12 months')
        GROUP BY month, g.grant_name
        ORDER BY month
     '''
    return run_query(query)

def load_deliverables_status():
    query = ''' 
        SELECT
            g.grant_name,
            d.deliverable_name,
            d.due_date,
            d.status,
            d.completion_date,
            CASE
                WHEN d.status = 'Overdue' THEN julianday('now') - julianday(d.due_date)
                WHEN d.status = 'Completed' AND d.completion_date > d.due_date
                    THEN julianday(d.completion_date) - julianday(d.due_date)
                ELSE 0
            END as days_late
            FROM deliverables d
            JOIN grants g ON d.grant_id = g.grant_id
            ORDER BY d.due_date DESC
    '''
    return run_query(query)

def load_participant_demographics():
    query = '''
        SELECT
            g.grant_name,
            p.age_group,
            p.demographic_category,
            COUNT(*) as participant_count
        FROM participants p
        JOIN grants g ON p.grant_id = g.grant_id
        GROUP BY g.grant_name, p.age_group, p.demographic_category
     '''
    return run_query(query)

def load_reports_timeline():
    query = '''
        SELECT
            g.grant_name,
            r.report_type,
            r.due_date,
            r.submission_date,
            r.status
        FROM reports r
        JOIN grants g ON r.grant_id = g.grant_id
        ORDER BY r.due_date DESC
     '''
    return run_query(query)

def load_staff_allocations():
    query = '''
        SELECT
            g.grant_name,
            s.staff_name,
            s.role,
            s.fte_percentage,
            s.salary_allocation
        FROM staff_allocations s
        JOIN grants g ON s.grant_id = g.grant_id
        ORDER BY g.grant_name, s.salary_allocation DESC
     '''
    return run_query(query)

#main app
def main():
    st.title('📊 Nonprofit Grant Compliance Dashboard')
    st.markdown("**Comprehensive grant management, compliance monitoring, and outcome tracking**")

    #sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Select Dashboard",
        ["Overview", "Financial Management", "Compliance & Reporting", "Outcomes & Impact", "Grant Details"]
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Demo Dashboard**\n\n"
        "This portfolio demonstration uses synthetic data. "
        "All grant and participant information is fictitious."
    )

    #page routing
    if page == "Overview":
        show_overview()
    elif page == "Financial Management":
        show_financial()
    elif page == "Compliance & Reporting":
        show_compliance()
    elif page == "Outcomes & Impact":
        show_outcomes()
    elif page == "Grant Details":
        show_grant_details()

def show_overview():
    """ Overview dashboard with key metrics"""
    st.header("📋 Grant Portfolio Overview")

    #load data
    grants_df = load_grant_summary()
    alerts_df = load_compliance_alerts()
    outcomes_df = load_outcome_performance()

    #top metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_funding = grants_df['total_amount'].sum()
        st.metric(
            "Total Grant Funding",
            f"${total_funding:,.0f}",
            delta='Active Portfolio'
        )
    
    with col2:
        total_spent = grants_df['total_spent'].sum()
        avg_utilization = (total_spent / total_funding * 100) if total_funding > 0 else 0
        st.metric(
            "Budget Utilized",
            f"{avg_utilization:.1f}%",
            delta=f"${total_spent:,.0f} spent"
        )
    
    with col3:
        active_grants = len(grants_df[grants_df['status'] == 'Active'])
        st.metric(
            "Active Grants",
            f"{active_grants}",
            delta=f"{len(grants_df)} total"
        )
    
    with col4:
        total_alerts = len(alerts_df)
        st.metric(
            "Compliance Alerts",
            f"{total_alerts}",
            delta='Needs Attention', 
            delta_color='inverse'
        )

    st.markdown("---")

    #charts row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Grant Budget Status")
        fig = go.Figure()

        for _, grant in grants_df.iterrows():
            fig.add_trace(go.Bar(
                name=grant['grant_name'][:30],
                x=['Spent', 'Remaining'],
                y=[grant['total_spent'], grant['remaining_budget']],
                text=[f"${grant['total_spent']:,.0f}", f"${grant['remaining_budget']:,.0f}"],
                textposition='inside'
            ))
        fig.update_layout(barmode='stack', showlegend=True, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Grant Timeline")
        timeline_data = grants_df[['grant_name', 'days_remaining']].copy()
        timeline_data['status'] = timeline_data['days_remaining'].apply(
            lambda x: 'Ending Soon' if x < 90 else 'Active'
        )

        fig = px.bar(
            timeline_data,
            x='days_remaining',
            y='grant_name',
            orientation='h',
            color='status',
            color_discrete_map={'Active': '#28a745', 'Ending Soon': '#ffc107'},
            labels={'days_remaning': 'Days Remaining', 'grant_name': 'Grant'}
        )
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    #alerts section
    st.subheader("🚨 Priority Alerts")
    if len(alerts_df) > 0:
        for _, alert in alerts_df.head(5).iterrows():
            alert_type = alert['alert_type']

            if 'Overdue' in alert_type:
                alert_class = 'danger'
            elif 'Budget' in alert_type:
                alert_class = 'warning'
            else:
                alert_class = 'warning'
            
            st.markdown(f"""
            <div class="alert-box alert-{alert_class}">
                <strong>{alert_type}: {alert['grant_name']}</strong><br>
                Item: {alert['item_name']}<br>
                {'Days Overdue: ' + str(int(alert['days_overdue']) if alert['due_date'] else 'Amount Over: ' + str(alert['days_overdue']) + '%')}
            </div>
             """, unsafe_allow_html=True)
    else:
        st.success("✅ No compliance alerts - all grants on track!")


def show_financial():
    '''Financial management dashboard '''
    st.header("💰 Financial Management")

    grants_df = load_grant_summary()
    budget_df = load_budget_by_category()
    spending_df = load_monthly_spending()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_budget = grants_df['total_amount'].sum()
        st.metric('Total Budget', f'${total_budget:,.0f}')
    
    with col2:
        total_spent = grants_df['total_spent'].sum()
        st.metric('Total Spent', f'{total_spent:,.0f}')

    with col3:
        remaining = grants_df['remaining_budget'].sum()
        st.metric('Remaining Budget', f'{remaining:,.0f}')

    with col4:
        avg_burn = grants_df['spent_percentage'].sum()
        st.metric('Avg Burn Rate', f'{avg_burn:.1f}')

    st.markdown('---')

    #charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Spending by Category")
        category_totals = budget_df.groupby('category_name').agg({
            'budgeted_amount': 'sum', 
            'spent_amount': 'sum'
        }).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Budgeted',
            x=category_totals['category_name'],
            y=category_totals['budgeted_amount'],
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            name='Spent',
            x=category_totals['category_name'],
            y=category_totals['spent_amount'],
            marker_color='darkblue'
        ))
        fig.update_layout(barmode='group', height=400)
        fig.update_xaxes(tickangle=45) 
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader('Monthly Spending Trend')
        if len(spending_df) > 0:
            fig = px.line(
                spending_df,
                x='month',
                y='total_spent',
                color='grant_name',
                markers=True,
                labels={'total_spent': 'Amount Spent ($)', 'month': 'Month'}
            
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info('No spending data available for the last 12 months')

    st.markdown('---')

    #budget details table
    st.subheader('Budget Details by Grant')

    def highlight_overspent(val):
        if val > 100:
            return 'background=color: #f8d7da'
        elif val > 90:
            return 'background-color: #fff3cd'
        else:
            return ''
    
    display_df = budget_df[['grant_name', 'category_name', 'budgeted_amount',
                           'spent_amount', 'remaining', 'spent_percentage']].copy()
    display_df['budgeted_amount'] = display_df['budgeted_amount'].apply(lambda x: f"${x:,.2f}")
    display_df['spent_amount'] = display_df['spent_amount'].apply(lambda x: f"${x:,.2f}")
    display_df['remaining'] = display_df['remaining'].apply(lambda x: f"{x:,.2f}")

    st.dataframe(display_df, use_container_width=True, height=400)

def show_compliance():
    ''' Compliance and reporting dashboard'''
    st.header('📝 Compliance & Reporting')

    #load data
    alerts_df = load_compliance_alerts()
    deliverables_df = load_deliverables_status()
    reports_df = load_reports_timeline()

    #compliance metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_deliverables = len(deliverables_df)
        completed = len(deliverables_df[deliverables_df['status'] == 'Completed'])
        st.metric("Deliverables", f"{completed}/{total_deliverables}",
                  delta=f"{completed/total_deliverables*100:.0f}% complete")
    
    with col2:
        overdue_deliverables = len(deliverables_df[deliverables_df['status'] == 'Overdue'])
        st.metric("Overdue Items", f"{overdue_deliverables}", delta_color='inverse')

    with col3:
        total_reports = len(reports_df)
        submitted = len(reports_df[reports_df['status'] == 'Submitted'])
        st.metric("Reports", f"{submitted}/{total_reports}", 
                 delta=f"{submitted/total_reports*100:.0f}% submitted")
    
    with col4:
        total_alerts = len(alerts_df)
        st.metric("Active Alerts", f"{total_alerts}", delta_color="inverse")

    st.markdown("---")

    #charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Deliverables Status')
        status_count = deliverables_df['status'].value_counts()
        fig = px.pie(
            values=status_count.values,
            names=status_count.index,
            color=status_count.index,
            color_discrete_map={
                'Completed': '#28a745',
                'In Progress': '#17a2b8',
                'Not Started': '#6c757d',
                'Overdue': '#dc3545'
            }
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Report Submission Status")
        report_status = reports_df['status'].value_counts()
        fig = px.bar(
            x=report_status.index,
            y=report_status.values,
            labels={'x': 'Status', 'y': 'Count'},
            color=report_status.index,
            color_discrete_map={
                'Submitted': '#28a745',
                'In Progress': '#ffc107',
                'Not Started': '#6c757d',
                'Overdue': '#dc3545'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('---')

        #upcoming deadlines
        st.subheader('📆 Upcoming Deadlines')
        upcoming = deliverables_df[
            (deliverables_df['status'].isin(['Not Started', 'In Progress'])) &
            (pd.to_datetime(deliverables_df['due_date']) <= datetime.now() + timedelta(days=30))

        ].sort_values('due_date')

        if len(upcoming) > 0:
            for _, item in upcoming.head(10).iterrows():
                days_until = (pd.to_datetime(item['due_date']) - datetime.now()).days

                if days_until < 7:
                    alert_class = 'danger'
                elif days_until < 14:
                    alert_class = 'warning'
                else:
                    alert_class = 'success'
                
                st.markdown(f"""
                    <div class="alert-box alert-{alert_class}">
                        <strong>{item['grant_name']}</strong><br>
                        {item['deliverable_name']}<br>
                        Due: {item['due_date']} ({days_until} days)<br>
                        Status: {item['status']}
                    </div>
                 """, unsafe_allow_html=True)
        else:
            st.success("✅ No upcoming deadlines in the next 30 days")



def show_outcomes():
    '''Outcomes and impact dashboard '''
    st.header("📈 Outcomes & Impact")

    #load data
    outcomes_df = load_outcome_performance()
    participants_df = load_participant_demographics()
    grants_df = load_grant_summary()

    #outcome metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_participants = run_query("SELECT COUNT(*) as count FROM participants")['count'].iloc[0]
        st.metric("Total Participants", f"{total_participants:,}")

    with col2:
        on_track = len(outcomes_df[outcomes_df['status'] == 'On Track'])
        total_metrics = len(outcomes_df)
        st.metric("Metrics on Track", f"{on_track}/{total_metrics}",
                delta=f"{on_track/total_metrics*100:.0f}%")

    with col3:
        avg_achievement = outcomes_df['achievement_percentage'].mean()
        st.metric("Acg Achievement", f'{avg_achievement:.0f}%')

    with col4:
        at_risk = len(outcomes_df[outcomes_df['status'] == 'At Risk'])
        st.metric("At Risk Metrics", f"{at_risk}",
                    delta_color='inverse')

    st.markdown('---')

    #charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Outcome Achievement by Grant")
        grant_performance = outcomes_df.groupby('grant_name')['achievement_percentage'].mean().reset_index()
        fig = px.bar(
            grant_performance,
            x='grant_name',
            y='achievement_percentage',
            color='achievement_percentage',
            color_continuous_scale='RdYlGn',
            labels={'achievement_percentage': 'Achievement %', 'grant_name': 'Grant'}
        )
        fig.add_hline(y=100, line_dash='dash', line_color='green', annotation_text='Target')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader('Participants by Demographics')
        if len(participants_df) > 0:
            demo_totals = participants_df.groupby('demographic_category')['participant_count'].sum().reset_index()
            fig = px.pie(
                data_frame=participants_df,
                names="demographic_category",
                values="participant_count"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('---')

    #detailed metrics table
    st.subheader("Detailed Outcome Metrics")
    display_outcomes = outcomes_df[['grant_name', 'metric_name', 'target_value',
                                    'current_value', 'achievement_percentage', 
                                    'unit_of_measure', 'status']].copy()
    st.dataframe(display_outcomes, use_container_width=True, height=400)


def show_grant_details():
    """ Detailed grant information"""
    st.header('📄 Grant Details')

    #load data
    grants_df = load_grant_summary()
    staff_df = load_staff_allocations()

    #grant selector
    grant_names = grants_df['grant_name'].tolist()
    selected_grant = st.selectbox('Select a grant to view details:', grant_names)

    if selected_grant:
        grant = grants_df[grants_df['grant_name'] == selected_grant].iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Award", f"${grant['total_amount']:,.0f}")
            st.metric("Funder", grant['funder_name'])

        with col2:
            st.metric("Spent", f"${grant['total_spent']:,.0f}")
            st.metric("Start Date", grant['start_date'])

        with col3:
            st.metric("Remaining", f"${grant['remaining_budget']:,.0f}")
            st.metric("End Date", grant['end_date'])

        st.markdown('---')

        st.subheader('Staff Allocations')
        grant_staff = staff_df[staff_df['grant_name'] == selected_grant]

        if len(grant_staff) > 0:
            col1, col2 = st.columns(2)

            with col1:
                fig = px.pie(
                    grant_staff,
                    values='salary_allocation', 
                    names='role',
                    title='Personnel Budget by Role'
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.dataframe(grant_staff[['staff_name', 'role', 'fte_percentage',
                                        'salary_allocation']], use_container_width=True)

        st.markdown('---')

        #budget breakdown
        st.subheader("Budget Breakdown")
        budget_data = run_query(f"""
            SELECT 
                category_name,
                budgeted_amount,
                spent_amount,
                budgeted_amount - spent_amount AS remaining
            FROM budget_categories
            WHERE grant_id = '{grant['grant_id']}'
""")
        if len(budget_data) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Budgeted',
                x=budget_data['category_name'],
                y=budget_data['budgeted_amount'],
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                name='Spent',
                x=budget_data['category_name'],
                y=budget_data['spent_amount'],
                marker_color='darkblue'
            ))
            fig.update_layout(barmode='group')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()


        


