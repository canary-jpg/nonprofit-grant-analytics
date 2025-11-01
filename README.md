# Nonprofit Grant Compliance Dashboard
A comprehensive grant management and compliance tracking solution designed for nonprofit organizations, demonstrating advanced capabilities in financial monitoring, deliverable tracking,outcome measurement, and automated reporting.

![Alt text](nonprofit_dash.png?raw=true 'Overview')

## 🎯 Overview
This portfolio project showcases end-to-end data analytics capabilities specifically tailored for nonprofit grant management. It demostrates proficiency in:

* Grant Portfolio Management - Multi-grant tracking, budget monitoring, timeline management
* Financial Compliance - Real-time spending analysis, budget variance tracking, category-level reporting
* Deliverables & Reporting - Automated deadline tracking, compliance alerts, submission monitoring
* Outcome Measurement - Program metrics, participant tracking, achievement analysis
* Funder Reporting - Automated report generation, compliance documentation, audit preparation

## 🚀 Features
### Grant Portfolio Overview
* Financial Summary - Total funding, utilization rates, remaining budgets across all grants
* Timeline Management - Visual grant timelines, expiration alerts, renewal tracking
* Priority Alerts - Automated notifications for overdue deliverables, budget overruns, upcoming deadlines
* Portfolio Health - At-a-glance status of all active grants

### Financial Management Dashboard
* Budget Tracking - Real-time spending vs. budget by category and grant
* Monthly Spending Trends - Identify spending patterns and forecast needs
* Category Analysis - Personnel, supplies, equipment, indirect costs breakdown
* Variance Reports - Highligt budget overruns and underspending
* Burn Rate Analysis - Project remaining funds based on current spending

### Compliance & Reporting
* Deliverable Tracking - All grant requirements, due dates, completion status
* Automated Alerts - 30/60/90-day deadline warnings
* Report Calendar - Quarterly, semi-annual, and annual report schedules
* Submission Tracking - Monitor on-time vs. late report submissions
* Compliance Score - Overall portfolio compliance health metric

### Outcomes & Impact
* Participant Tracking - Enrollment, demographics, completion rates
* Outcome Metrics - Progress toward grant-specific goals and targets
* Achievement Analysis - Identify programs meeting, exceeding, or falling short of goals
* Demographic Reporting - Servce diverse populations, track equity metrics
* Impact Visualization - Tell your story with data for funders and stakeholders

### Grant-Level Details
* Deep Dive Analysis - Complete financial and programmatic view of individual grants
* Staff Allocations - FTE percentages, salary distributions, personnel budgets
* Expense History - Transaction-level spending records
* Funder Requirements - Specific deliverables, metrics, and reporting schedules

## 🛠️ Technology Stack
* Python 3.12 - Core programming language
* SQLite - Relational database for grant data storage
* Pandas - Data manipulation and analysis
* Streamlit - Interactive web dashboard framework
* Plotly - Advanced data visualizations
* Faker - Synthetic data generation for demostration

## 📁 Project Structure
```
nonprofit-grant-analytics/
├── data/
│   ├── generate_nonprofit_data.py    # Database creation script
│   └── nonprofit_grants.db           # SQLite database
├── dashboard/
│   ├── streamlit_app.py              # Main dashboard application
│   └── .streamlit/
│       └── config.toml               # Theme configuration
├── screenshots/                       # Dashboard screenshots
├── README.md                          # This file
└── requirements.txt                   # Python dependencies
```

## 🔧 Installation & Setup
### Prerequisites
* Python 3.8 or higher
* pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/nonprofit-grant-analytics.git
cd nonprofit-grant-analytics
```
### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
#### Requirements
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
Faker>=19.0.0
matplotlib>=3.7.0
```
### Step 3: Generated Synthetic Database
```bash
cd data
python generate_nonprofit_data.py
```
This creates a SQLite database with:
* 5 grants for various funder types (Federal, Foundation, Corporate, State)
* Budget categories with realistic spending patterns
* 250+ expense transactions
* 50+ deliverables with due dates and status tracking
* Outcome metrics with targets and current values
* 500+ program participants with demographics
* Report schedules and submission tracking
* Staff allocation

### Step 4: Launch Dashboard
```bash
cd ../dashboard
streamlit run streamlit_app.py
```
This dashboard will open automatically in your browser at `http:localhost:8501`

## 📊 Database Schema
### Core Tables
**grants** - Master grant information
* Grant ID, name, funder details
* Award amount, start/end dates
* Status, grant officer, purpose
* Reporting frequency
**budget_categories** - Budget line items
* Category name (Personnel, Supplies, Equipment, etc.)
* Budgeted vs. spent amounts
* Linked to parent grant
**expenses** - Individual transactions
* Expense date, vendor, description
* Amount, approval information
* Linked to grant and budget category
**deliverables** - Grant requirements
* Deliverable name, due date
* Status (Completed, In Progress, Overdue)
* Completion date, notes
**outcome_metrics** - Program goals
* Metric name, target value, current value
* Unit of measure, measurement period
* Achievement percentage
**participants** - Program enrollees
* Enrollment date, demographics
* Age group, status
* Completion tracking
**reports** - Funder reporting schedule
* Report type, due date, submission date
* Status, submitted by
**staff_allocations** - Personnel assignments
* Staff name, role
* FTE percentage, salary allocations

### Analytical Views
**v_grant_summary**
```sql
-- Consolidated grant portfolio overview
SELECT 
    grant_id, grant_name, funder_name,
    total_amount, total_spent, remaining_budget,
    spent_percentage, days_remaining
FROM v_grant_summary;
```

**v_compliance_alerts**
```sql
-- All compliance issues requiring attention
SELECT 
    alert_type, grant_name, item_name,
    due_date, days_overdue
FROM v_compliance_alerts
ORDER BY days_overdue DESC;
```

**v_outcome_performance**
```sql
-- Outcome metric achievement tracking
SELECT 
    grant_name, metric_name,
    target_value, current_value,
    achievement_percentage, status
FROM v_outcome_performance;
```

## 🎓 Use Cases
### For Small to Mid-Size Nonprofits ($500K-$5M budget)
* Manage 3-10 concurrent grants efficiently
* Reduce time spent on manual reporting by 80%
* Ensure compliance with all funder requirements
* Demonstrate impact to current and prospective funders
* Avoid penalties and maintain strong funder relationships

### For Grant Managers
* Real-time visibility into all grant obligations
* Automated deadline reminders
* Quick access to spending data for budget modifications
* Easy report generation for funders
* Track staff time allocation across grants

### For Executive Directors
* Portfolio-level financial health monitoring
* Identify at-risk grants before they become problems
* Data-driven decisions about grant renewals
* Board reporting with professional visualizations
* Strategic planning with historical data

### For Program Management
* Track participant enrollment and outcomes
* Monitor progress toward grant-specific goals
* Identify underperforming programs early
* Document success stories with data
* Support grant applications with outcomes data

## 💡 Skills Demonstrated
### Technical Skills:
* SQL database design and normalization
* Python data analysis (Pandas, data manipulation)
* Interactive visualization (Plotly, Streamlit)
* ETL processes and automation
* Multi-dimensional data modeling
### Domain Expertise:
* Grant compliance requirements (Federal, Foundation, Corporate)
* Nonprofit financial management
* Outcome measurement and evaluation
* Program operations and reporting
* Funder relationship management
### Business Value:
* Translating operational needs into technical solutions
* Creating actionable insights from complex data
* Automating manual processes
* Risk identification and mitigation
* ROI analysis and efficiency gains

## 🚀 Deployment Options
### Local Development
Current setup - runs on `localhost:8501`

### Streamlit Cloud (Recommended for Demo)
Free hosting with easy deployment
1. Push code to GitHub (public repository)
2. Connect repo to Streamlit Cloud
3. Deploy with one click
4. Share public URL with stakeholders

### Production Deployment Options
### Docker Container:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "dashboard/streamlit_app.py"]
```

### Cloud Platforms:
* AWS (EC2, Elastic Beanstalk)
* Google Cloud Platform (Cloud Run)
* Microsoft Azure (App Service)
* Heroku, Railway, Render

**On-Premises**: For organizations with data sovereignty requirements, can be deployed on interal servers with secure access controls.

## 📈 Business Impact
### Time Savings
* Manual Reporting: Reduce from 8-10 hours/month to 1-2 hours
* Budget Monitoring: Real-time vs. quarterly spreadsheet reviews
* Compliance Tracking: Automated vs. manual calendar management
* Report Generation: Minutes vs. hours for funder reports
**Estimated Value:** $15,000 - $25,000 annually in staff time savings

### Risk Reduction
* Missed Deadlines: Automated alerts prevent late submissions
* Budget Overruns: Early warning system for overspending
* Compliance Violations: Proactive monitoring vs. reactive fixes
* Audit Preparation: Always audit-ready with organized data
**Estimated Value:** Avoid $10,000- $50,000 in penalties and funder relationship damage

### Strategic Value
* Data-Driven Decisions: Grant renewal decisions based on outcomes data
* Funder Relations: Professional reporting strengthens partnerships
* Board Relations: Clean communication of organizational impact

## 📧 About This Project
This portfolio demonstration project built to showcase data analytics capabilities for nonprofit organizations. The database contains entirely synthethic data - all grant names, funder names, particpant information, and financial data are fictitious and randomly generated

**Built by:** Hazel Donaldson
**Purpose:** Demonstrate capability to build custom analytics solutions for nonprofit grant management
**Tech Stack:** Python, SQLite, Streamlit, Plotly, Pandas

## 🤝 Services Offered
I build custom data analytics solutions for nonprofits including: 
* **Grant Management Dashboards** - Track multiple grants, budgets, and compliance requirements
* **Outcome Measurement Systems** - Demonstrate program impact to funders
* **Financial Reporting Automation** - Reduce manual reporting time
* **Database Integration** - Connect to your existing systems (Salesforce, QuicBooks, custom databases)
* **Funder Report Generation** - Automated quarterly/annual reports

**Ideal for:**
* Nonprofits managing 3-10 grants simultaneously
* Organizations with custom databases or multiple systems
* Grant managers spending 5+ hours/week on manual reporting
* Programs needing to demonstrate outcomes to funders

**Contact:**
* Email: hazel90.hd@gmail.com
* LinkedIn: linkedin.com/in/hazel-donaldson


## 📝 License
This project is available for portfolio demonstration purposes. For commercial use, customization for your organziation, or to discuss implementation, please contact directly.

## 🙏🏾 Acknowledgments
* Built with Streamlit open-source framework
* Data visualization powered by Plotly
* Synthetic data generation using Faker library
* Inspired by real-world nonprofit grant management challenges

## 💼 Related Projects
**Mental Health Practice Analytics** - Healthcare data analytics for clinical outcomes, compliance, and revenue optimatization
View Project: https://github.com/canary-jpg/mental-health-analytics

⚠️ **Important Note:** This is a portfolio demonstration using entirely synthetic data. All grant name, funder names, participant information, and financial data are fictitious and randomly generated for demonstration purposes only.