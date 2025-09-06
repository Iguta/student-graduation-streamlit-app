import streamlit as st
import pandas as pd
import plotly.express as px
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# #features available for analysis
#                     "Marital status": marital_status_dict[marital_status],
#                     "Application order": application_order,
#                     "Course": course_dict[course],
#                     "Admission grade": admission_grade,
#                     "Tuition fees up to date": yes_or_no_dict[fees_up_to_date],
#                     "Gender": gender_dict[gender],
#                     "Scholarship holder": yes_or_no_dict[scholarship],
#                     "Age at enrollment": age,
#                     "International": yes_or_no_dict[international],
#                     "Curricular units 1st sem (grade)": first_sem_grade,
#                     "Curricular units 2nd sem (grade)": second_sem_grade
available_features = [
    "Marital status",
    "Application order",
    "Course",
    "Admission grade",
    "Tuition fees up to date",
    "Gender",
    "Scholarship holder",
    "Age at enrollment",
    "International",
    "Curricular units 1st sem (grade)",
    "Curricular units 2nd sem (grade)"
]
target_col = "Target"

def create_visualization(csv_file_path=f"{os.getcwd()}/data/students.csv"):
    logging.info(f"Loading dataset from: {csv_file_path}")

    st.title("📊 Student Performance Analysis")
    st.write("Analyze how different student characteristics relate to academic success")
    
    # Load data automatically
    try:
        df = pd.read_csv(csv_file_path)
        logging.info(f"Dataset loaded with shape: {df.shape}")
        
        # Display basic info
        with st.expander("📋 Dataset Overview"):
            st.write("**First 5 rows:**")
            st.dataframe(df.head())
                    
        # Create tabs focused on target analysis
        tab1,  tab2 = st.tabs([
            "🎯 Target vs Features", 
            "📊 Target Analysis",

        ])
        with tab1:
            # Pie chart for target distribution
            target_counts = df[target_col].value_counts()
            fig = px.pie(
                values=target_counts.values, 
                names=target_counts.index,
                title=f"Distribution of {target_col}"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            selected_features = st.multiselect(
            "Features to Analyze Against Target:",
            available_features,
            default=["Marital status", "Age at enrollment", "Tuition fees up to date"],  # Select first 3 by default
            help="Features that might influence the target variable"
            )
                
            st.divider()
                # Create visualizations for each selected feature vs target
            for feature in selected_features:
                feature_unique = df[feature].nunique()
                feature_type = 'categorical' if df[feature].dtype == 'object' or feature_unique <= 10 else 'numerical'
                
                        
                if feature_type == 'numerical':
                    # Box plot for numerical feature vs categorical target
                    fig = px.box(
                        df, x=target_col, y=feature,
                        title=f"{feature} distribution by {target_col}",
                        color=target_col
                    )
                    
                else:  # Both target and  categorical
                    # Grouped bar chart showing percentages
                    crosstab = pd.crosstab(df[feature], df[target_col], normalize='index') * 100
                    fig = px.bar(
                        crosstab.reset_index(), 
                        x=feature, y=crosstab.columns.tolist(),
                        title=f"{feature} vs {target_col} (Percentage)",
                        barmode='group'
                    )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                
                st.divider()
            

            
            
    except FileNotFoundError:
        st.error(f"Could not find the dataset file: {csv_file_path}")
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
