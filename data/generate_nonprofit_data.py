"""
Nonprofit Grant Compliance Dashboard - Synthetic Data Generator
Creates a realistic SQLite database for grant management and compliance tracking
"""

import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

fake = Faker()
Faker.seed(42)
random.seed(42)

class NonprofitDataGenerator:
    def __init__(self, db_name='nonprofit_grants.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
    def create_tables(self):
        """Create all necessary database tables"""
        
        # Grants table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grants (
                grant_id TEXT PRIMARY KEY,
                grant_name TEXT NOT NULL,
                funder_name TEXT NOT NULL,
                funder_type TEXT,
                total_amount REAL NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT,
                grant_officer TEXT,
                purpose TEXT,
                reporting_frequency TEXT
            )
        ''')
        
        # Budget categories table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget_categories (
                category_id TEXT PRIMARY KEY,
                grant_id TEXT NOT NULL,
                category_name TEXT NOT NULL,
                budgeted_amount REAL NOT NULL,
                spent_amount REAL DEFAULT 0,
                FOREIGN KEY (grant_id) REFERENCES grants(grant_id)
            )
        ''')
        
        # Expenses table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id TEXT PRIMARY KEY,
                grant_id TEXT NOT NULL,
                category_id TEXT NOT NULL,
                expense_date TEXT NOT NULL,
                vendor TEXT,
                description TEXT,
                amount REAL NOT NULL,
                approved_by TEXT,
                FOREIGN KEY (grant_id) REFERENCES grants(grant_id),
                FOREIGN KEY (category_id) REFERENCES budget_categories(category_id)
            )
        ''')
        
        # Deliverables table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS deliverables (
                deliverable_id TEXT PRIMARY KEY,
                grant_id TEXT NOT NULL,
                deliverable_name TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT,
                completion_date TEXT,
                notes TEXT,
                FOREIGN KEY (grant_id) REFERENCES grants(grant_id)
            )
        ''')
        
        # Outcome metrics table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS outcome_metrics (
                metric_id TEXT PRIMARY KEY,
                grant_id TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                target_value REAL NOT NULL,
                current_value REAL DEFAULT 0,
                measurement_period TEXT,
                unit_of_measure TEXT,
                FOREIGN KEY (grant_id) REFERENCES grants(grant_id)
            )
        ''')
        
        # Program participants table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS participants (
                participant_id TEXT PRIMARY KEY,
                grant_id TEXT NOT NULL,
                enrollment_date TEXT NOT NULL,
                age_group TEXT,
                demographic_category TEXT,
                status TEXT,
                completion_date TEXT,
                FOREIGN KEY (grant_id) REFERENCES grants(grant_id)
            )
        ''')
        
        # Reports table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                report_id TEXT PRIMARY KEY,
                grant_id TEXT NOT NULL,
                report_type TEXT NOT NULL,
                due_date TEXT NOT NULL,
                submission_date TEXT,
                status TEXT,
                submitted_by TEXT,
                FOREIGN KEY (grant_id) REFERENCES grants(grant_id)
            )
        ''')
        
        # Staff allocations table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff_allocations (
                allocation_id TEXT PRIMARY KEY,
                grant_id TEXT NOT NULL,
                staff_name TEXT NOT NULL,
                role TEXT,
                fte_percentage REAL NOT NULL,
                salary_allocation REAL NOT NULL,
                FOREIGN KEY (grant_id) REFERENCES grants(grant_id)
            )
        ''')
        
        self.conn.commit()
        print("✓ Database tables created successfully")
    
    def generate_grants(self, n=5):
        """Generate synthetic grant data"""
        funder_types = ['Federal', 'Foundation', 'Corporate', 'State', 'Individual']
        purposes = [
            'Youth Education Programs',
            'Healthcare Access',
            'Food Security Initiatives',
            'Mental Health Services',
            'Job Training and Placement',
            'Housing Assistance',
            'Arts and Culture Programming',
            'Environmental Conservation'
        ]
        statuses = ['Active', 'Active', 'Active', 'Active', 'Completed']
        frequencies = ['Quarterly', 'Semi-Annual', 'Annual']
        
        grants = []
        base_date = datetime.now() - timedelta(days=365)
        
        for i in range(n):
            grant_id = f'GR{i+1:03d}'
            start_date = base_date + timedelta(days=random.randint(0, 180))
            duration_months = random.choice([12, 18, 24, 36])
            end_date = start_date + timedelta(days=duration_months * 30)
            
            grants.append({
                'grant_id': grant_id,
                'grant_name': f"{random.choice(purposes)} {random.choice(['Initiative', 'Program', 'Project'])}",
                'funder_name': fake.company(),
                'funder_type': random.choice(funder_types),
                'total_amount': round(random.uniform(50000, 500000), 2),
                'start_date': str(start_date.date()),
                'end_date': str(end_date.date()),
                'status': random.choice(statuses),
                'grant_officer': fake.name(),
                'purpose': random.choice(purposes),
                'reporting_frequency': random.choice(frequencies)
            })
        
        df = pd.DataFrame(grants)
        df.to_sql('grants', self.conn, if_exists='append', index=False)
        print(f"✓ Generated {n} grants")
        return grants
    
    def generate_budget_categories(self, grants):
        """Generate budget categories for each grant"""
        categories = [
            'Personnel Salaries',
            'Fringe Benefits',
            'Program Supplies',
            'Equipment',
            'Travel',
            'Consultants',
            'Facilities',
            'Indirect Costs'
        ]
        
        budget_cats = []
        for grant in grants:
            total = grant['total_amount']
            remaining = total
            
            # Distribute budget across categories
            for idx, category in enumerate(categories):
                if idx == len(categories) - 1:
                    amount = remaining
                else:
                    # Personnel typically gets 40-50%, other categories vary
                    if category == 'Personnel Salaries':
                        percentage = random.uniform(0.40, 0.50)
                    elif category == 'Fringe Benefits':
                        percentage = random.uniform(0.15, 0.20)
                    elif category == 'Indirect Costs':
                        percentage = random.uniform(0.08, 0.12)
                    else:
                        percentage = random.uniform(0.03, 0.10)
                    
                    amount = total * percentage
                    remaining -= amount
                
                cat_id = f"BC{len(budget_cats)+1:04d}"
                
                # Calculate spent amount (vary by grant status and time elapsed)
                start = datetime.strptime(grant['start_date'], '%Y-%m-%d')
                end = datetime.strptime(grant['end_date'], '%Y-%m-%d')
                days_elapsed = (datetime.now() - start).days
                total_days = (end - start).days
                
                if grant['status'] == 'Completed':
                    spent_pct = random.uniform(0.90, 1.00)
                else:
                    progress = min(days_elapsed / total_days, 1.0) if total_days > 0 else 0
                    spent_pct = progress * random.uniform(0.85, 1.15)  # Some variance
                
                spent = amount * spent_pct
                
                budget_cats.append({
                    'category_id': cat_id,
                    'grant_id': grant['grant_id'],
                    'category_name': category,
                    'budgeted_amount': round(amount, 2),
                    'spent_amount': round(spent, 2)
                })
        
        df = pd.DataFrame(budget_cats)
        df.to_sql('budget_categories', self.conn, if_exists='append', index=False)
        print(f"✓ Generated {len(budget_cats)} budget categories")
        return budget_cats
    
    def generate_expenses(self, grants, budget_cats, n_per_grant=50):
        """Generate expense transactions"""
        expenses = []
        
        for grant in grants:
            grant_cats = [c for c in budget_cats if c['grant_id'] == grant['grant_id']]
            start = datetime.strptime(grant['start_date'], '%Y-%m-%d')
            end = datetime.strptime(grant['end_date'], '%Y-%m-%d')
            
            for i in range(n_per_grant):
                expense_id = f"EXP{len(expenses)+1:05d}"
                category = random.choice(grant_cats)
                
                # Generate expense date within grant period
                days_range = (min(datetime.now(), end) - start).days
                if days_range > 0:
                    expense_date = start + timedelta(days=random.randint(0, days_range))
                else:
                    expense_date = start
                
                # Amount based on category budget
                max_amount = category['budgeted_amount'] / n_per_grant * random.uniform(0.5, 2.0)
                
                expenses.append({
                    'expense_id': expense_id,
                    'grant_id': grant['grant_id'],
                    'category_id': category['category_id'],
                    'expense_date': str(expense_date.date()),
                    'vendor': fake.company(),
                    'description': f"{category['category_name']} - {fake.bs()}",
                    'amount': round(random.uniform(100, max_amount), 2),
                    'approved_by': fake.name()
                })
        
        df = pd.DataFrame(expenses)
        df.to_sql('expenses', self.conn, if_exists='append', index=False)
        print(f"✓ Generated {len(expenses)} expenses")
        return expenses
    
    def generate_deliverables(self, grants):
        """Generate grant deliverables and milestones"""
        deliverable_types = [
            'Quarterly Financial Report',
            'Program Outcome Report',
            'Participant Survey Results',
            'Annual Evaluation',
            'Site Visit Preparation',
            'Interim Progress Report',
            'Final Report',
            'Budget Modification Request'
        ]
        
        deliverables = []
        for grant in grants:
            start = datetime.strptime(grant['start_date'], '%Y-%m-%d')
            end = datetime.strptime(grant['end_date'], '%Y-%m-%d')
            duration = (end - start).days
            
            # Generate 8-12 deliverables per grant
            n_deliverables = random.randint(8, 12)
            
            for i in range(n_deliverables):
                deliverable_id = f"DEL{len(deliverables)+1:04d}"
                
                # Spread deliverables across grant period
                due_date = start + timedelta(days=int(duration * (i / n_deliverables)))
                
                # Determine status
                if due_date < datetime.now() - timedelta(days=30):
                    status = random.choice(['Completed', 'Completed', 'Completed', 'Late'])
                    completion = due_date + timedelta(days=random.randint(-5, 10))
                elif due_date < datetime.now():
                    status = random.choice(['Completed', 'In Progress', 'Overdue'])
                    completion = due_date + timedelta(days=random.randint(0, 5)) if status == 'Completed' else None
                else:
                    status = random.choice(['Not Started', 'In Progress'])
                    completion = None
                
                deliverables.append({
                    'deliverable_id': deliverable_id,
                    'grant_id': grant['grant_id'],
                    'deliverable_name': random.choice(deliverable_types),
                    'due_date': str(due_date.date()),
                    'status': status,
                    'completion_date': str(completion.date()) if completion else None,
                    'notes': fake.sentence() if random.random() > 0.5 else None
                })
        
        df = pd.DataFrame(deliverables)
        df.to_sql('deliverables', self.conn, if_exists='append', index=False)
        print(f"✓ Generated {len(deliverables)} deliverables")
        return deliverables
    
    def generate_outcome_metrics(self, grants):
        """Generate outcome metrics for each grant"""
        metrics_by_purpose = {
            'Youth Education Programs': [
                ('Students Enrolled', 'Participants'),
                ('Program Completion Rate', 'Percentage'),
                ('Average Grade Improvement', 'Points'),
                ('Parent Satisfaction Score', 'Rating')
            ],
            'Healthcare Access': [
                ('Patients Served', 'Individuals'),
                ('Services Provided', 'Sessions'),
                ('Preventive Care Visits', 'Visits'),
                ('Patient Satisfaction', 'Rating')
            ],
            'Food Security Initiatives': [
                ('Meals Distributed', 'Meals'),
                ('Families Served', 'Households'),
                ('Food Bank Visits', 'Visits'),
                ('Pounds of Food Distributed', 'Pounds')
            ],
            'Mental Health Services': [
                ('Clients Served', 'Individuals'),
                ('Counseling Sessions', 'Sessions'),
                ('Crisis Interventions', 'Interventions'),
                ('Client Improvement Rate', 'Percentage')
            ],
            'Job Training and Placement': [
                ('Trainees Enrolled', 'Participants'),
                ('Certifications Earned', 'Certificates'),
                ('Job Placements', 'Placements'),
                ('Average Wage Increase', 'Dollars')
            ]
        }
        
        default_metrics = [
            ('Program Participants', 'Individuals'),
            ('Program Activities', 'Events'),
            ('Community Reach', 'People'),
            ('Satisfaction Rate', 'Percentage')
        ]
        
        metrics = []
        for grant in grants:
            purpose = grant['purpose']
            metric_list = metrics_by_purpose.get(purpose, default_metrics)
            
            for metric_name, unit in metric_list:
                metric_id = f"MET{len(metrics)+1:04d}"
                
                # Set targets based on metric type
                if unit == 'Percentage':
                    target = random.uniform(75, 95)
                    current = target * random.uniform(0.60, 1.10)
                elif unit == 'Rating':
                    target = random.uniform(4.0, 5.0)
                    current = target * random.uniform(0.85, 1.05)
                elif unit == 'Participants' or unit == 'Individuals':
                    target = random.randint(50, 500)
                    current = target * random.uniform(0.50, 1.20)
                else:
                    target = random.randint(100, 1000)
                    current = target * random.uniform(0.60, 1.15)
                
                metrics.append({
                    'metric_id': metric_id,
                    'grant_id': grant['grant_id'],
                    'metric_name': metric_name,
                    'target_value': round(target, 2),
                    'current_value': round(current, 2),
                    'measurement_period': grant['reporting_frequency'],
                    'unit_of_measure': unit
                })
        
        df = pd.DataFrame(metrics)
        df.to_sql('outcome_metrics', self.conn, if_exists='append', index=False)
        print(f"✓ Generated {len(metrics)} outcome metrics")
        return metrics
    
    def generate_participants(self, grants):
        """Generate program participant data"""
        age_groups = ['0-5', '6-12', '13-17', '18-24', '25-44', '45-64', '65+']
        demographics = ['Low Income', 'Minority', 'Veteran', 'Disabled', 'Homeless', 'General']
        statuses = ['Active', 'Active', 'Active', 'Completed', 'Dropped']
        
        participants = []
        for grant in grants:
            n_participants = random.randint(30, 200)
            start = datetime.strptime(grant['start_date'], '%Y-%m-%d')
            end = datetime.strptime(grant['end_date'], '%Y-%m-%d')
            
            for i in range(n_participants):
                participant_id = f"PAR{len(participants)+1:05d}"
                enrollment_date = start + timedelta(days=random.randint(0, (end - start).days))
                status = random.choice(statuses)
                
                if status == 'Completed':
                    completion = enrollment_date + timedelta(days=random.randint(30, 180))
                else:
                    completion = None
                
                participants.append({
                    'participant_id': participant_id,
                    'grant_id': grant['grant_id'],
                    'enrollment_date': str(enrollment_date.date()),
                    'age_group': random.choice(age_groups),
                    'demographic_category': random.choice(demographics),
                    'status': status,
                    'completion_date': str(completion.date()) if completion else None
                })
        
        df = pd.DataFrame(participants)
        df.to_sql('participants', self.conn, if_exists='append', index=False)
        print(f"✓ Generated {len(participants)} participants")
        return participants
    
    def generate_reports(self, grants):
        """Generate grant reports"""
        report_types = ['Financial Report', 'Programmatic Report', 'Interim Report', 'Final Report']
        statuses = ['Submitted', 'Submitted', 'In Progress', 'Overdue']
        
        reports = []
        for grant in grants:
            start = datetime.strptime(grant['start_date'], '%Y-%m-%d')
            end = datetime.strptime(grant['end_date'], '%Y-%m-%d')
            
            # Generate reports based on frequency
            if grant['reporting_frequency'] == 'Quarterly':
                n_reports = int((end - start).days / 90)
            elif grant['reporting_frequency'] == 'Semi-Annual':
                n_reports = int((end - start).days / 180)
            else:
                n_reports = int((end - start).days / 365)
            
            n_reports = max(2, min(n_reports, 12))
            
            for i in range(n_reports):
                report_id = f"REP{len(reports)+1:04d}"
                due_date = start + timedelta(days=int((end - start).days * ((i + 1) / n_reports)))
                
                if due_date < datetime.now() - timedelta(days=15):
                    status = 'Submitted'
                    submission = due_date + timedelta(days=random.randint(-5, 10))
                elif due_date < datetime.now():
                    status = random.choice(['Submitted', 'In Progress', 'Overdue'])
                    submission = due_date + timedelta(days=random.randint(0, 5)) if status == 'Submitted' else None
                else:
                    status = 'Not Started'
                    submission = None
                
                reports.append({
                    'report_id': report_id,
                    'grant_id': grant['grant_id'],
                    'report_type': random.choice(report_types),
                    'due_date': str(due_date.date()),
                    'submission_date': str(submission.date()) if submission else None,
                    'status': status,
                    'submitted_by': fake.name() if status == 'Submitted' else None
                })
        
        df = pd.DataFrame(reports)
        df.to_sql('reports', self.conn, if_exists='append', index=False)
        print(f"✓ Generated {len(reports)} reports")
        return reports
    
    def generate_staff_allocations(self, grants):
        """Generate staff allocations to grants"""
        roles = ['Program Director', 'Program Manager', 'Case Manager', 'Administrative Assistant', 'Evaluator']
        
        allocations = []
        for grant in grants:
            n_staff = random.randint(3, 6)
            
            for i in range(n_staff):
                allocation_id = f"SA{len(allocations)+1:04d}"
                role = roles[i] if i < len(roles) else random.choice(roles)
                
                # FTE percentage varies by role
                if role == 'Program Director':
                    fte = random.uniform(0.10, 0.25)
                elif role == 'Program Manager':
                    fte = random.uniform(0.50, 1.00)
                else:
                    fte = random.uniform(0.20, 0.75)
                
                # Salary based on role and FTE
                base_salary = {
                    'Program Director': 90000,
                    'Program Manager': 65000,
                    'Case Manager': 50000,
                    'Administrative Assistant': 40000,
                    'Evaluator': 70000
                }.get(role, 50000)
                
                allocation = base_salary * fte
                
                allocations.append({
                    'allocation_id': allocation_id,
                    'grant_id': grant['grant_id'],
                    'staff_name': fake.name(),
                    'role': role,
                    'fte_percentage': round(fte * 100, 1),
                    'salary_allocation': round(allocation, 2)
                })
        
        df = pd.DataFrame(allocations)
        df.to_sql('staff_allocations', self.conn, if_exists='append', index=False)
        print(f"✓ Generated {len(allocations)} staff allocations")
        return allocations
    
    def create_views(self):
        """Create useful SQL views for analytics"""
        
        # Grant summary view
        self.cursor.execute('''
            CREATE VIEW IF NOT EXISTS v_grant_summary AS
            SELECT 
                g.grant_id,
                g.grant_name,
                g.funder_name,
                g.total_amount,
                g.start_date,
                g.end_date,
                g.status,
                SUM(bc.spent_amount) as total_spent,
                g.total_amount - SUM(bc.spent_amount) as remaining_budget,
                ROUND(100.0 * SUM(bc.spent_amount) / g.total_amount, 2) as spent_percentage,
                julianday(g.end_date) - julianday('now') as days_remaining
            FROM grants g
            LEFT JOIN budget_categories bc ON g.grant_id = bc.grant_id
            GROUP BY g.grant_id
        ''')
        
        # Compliance alerts view
        self.cursor.execute('''
            CREATE VIEW IF NOT EXISTS v_compliance_alerts AS
            SELECT 
                'Overdue Report' as alert_type,
                grant_id,
                report_type as item_name,
                due_date,
                julianday('now') - julianday(due_date) as days_overdue
            FROM reports
            WHERE status = 'Overdue'
            UNION ALL
            SELECT 
                'Overdue Deliverable' as alert_type,
                grant_id,
                deliverable_name as item_name,
                due_date,
                julianday('now') - julianday(due_date) as days_overdue
            FROM deliverables
            WHERE status = 'Overdue'
            UNION ALL
            SELECT 
                'Budget Overspent' as alert_type,
                bc.grant_id,
                bc.category_name as item_name,
                NULL as due_date,
                ROUND(100.0 * (bc.spent_amount - bc.budgeted_amount) / bc.budgeted_amount, 2) as days_overdue
            FROM budget_categories bc
            WHERE bc.spent_amount > bc.budgeted_amount
        ''')
        
        # Outcome performance view
        self.cursor.execute('''
            CREATE VIEW IF NOT EXISTS v_outcome_performance AS
            SELECT 
                om.grant_id,
                g.grant_name,
                om.metric_name,
                om.target_value,
                om.current_value,
                ROUND(100.0 * om.current_value / om.target_value, 2) as achievement_percentage,
                om.unit_of_measure,
                CASE 
                    WHEN om.current_value >= om.target_value THEN 'On Track'
                    WHEN om.current_value >= om.target_value * 0.75 THEN 'Needs Attention'
                    ELSE 'At Risk'
                END as status
            FROM outcome_metrics om
            JOIN grants g ON om.grant_id = g.grant_id
        ''')
        
        self.conn.commit()
        print("✓ Created analytical views")
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        print("✓ Database connection closed")

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("Nonprofit Grant Compliance Dashboard - Data Generator")
    print("=" * 60)
    print()
    
    # Initialize generator
    generator = NonprofitDataGenerator()
    
    # Create schema
    print("Creating database schema...")
    generator.create_tables()
    print()
    
    # Generate data
    print("Generating synthetic data...")
    grants = generator.generate_grants(n=5)
    budget_cats = generator.generate_budget_categories(grants)
    expenses = generator.generate_expenses(grants, budget_cats)
    deliverables = generator.generate_deliverables(grants)
    participants = generator.generate_participants(grants)
    metrics = generator.generate_outcome_metrics(grants)
    reports = generator.generate_reports(grants)
    staff = generator.generate_staff_allocations(grants)
    print()
    
    # Create views
    print("Creating analytical views...")
    generator.create_views()
    print()
    
    # Summary statistics
    print("=" * 60)
    print("Database Summary:")
    print("=" * 60)
    cursor = generator.conn.cursor()
    
    tables = ['grants', 'budget_categories', 'expenses', 'deliverables', 
              'outcome_metrics', 'participants', 'reports', 'staff_allocations']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table.replace('_', ' ').title()}: {count:,} records")
    
    print()
    print("✓ Database generation complete!")
    print(f"✓ Database file: nonprofit_grants.db")
    print()
    print("Next steps:")
    print("  1. Connect to database with: sqlite3 nonprofit_grants.db")
    print("  2. Run: SELECT * FROM v_grant_summary;")
    print("  3. Build Streamlit dashboard using this data")
    
    # Close connection
    generator.close()