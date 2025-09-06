import streamlit as st
import os
from modules.helper import invoke_endpoint, get_aws_session
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

marital_status_dict = {
    "single": 1,
    "married": 2,
    "widower": 3,
    "divorced": 4,
    "facto union": 5,
    "legally separated": 6
}
yes_or_no_dict = {
    "No": 0, 
    "Yes": 1
}

gender_dict = {
    "Female": 0,
    "Male": 1
}


course_dict = {
    "Biofuel Production Technologies": 33,
    "Animation and Multimedia Design": 171,
    "Social Service (evening attendance)": 8014,
    "Agronomy": 9003,
    "Communication Design": 9070,
    "Veterinary Nursing": 9085,
    "Informatics Engineering": 9119,
    "Equinculture": 9130,
    "Management": 9147,
    "Social Service": 9238,
    "Tourism": 9254,
    "Nursing": 9500,
    "Oral Hygiene": 9556,
    "Advertising and Marketing Management": 9670,
    "Journalism and Communication": 9773,
    "Basic Education": 9853,
    "Management (evening attendance)": 9991
}

def prediction():
    st.title("🎓 Student Performance Predictor")
    
    # # Add AWS connection status
    # if st.sidebar.button("Test AWS Connection"):
    #     session = get_aws_session()
    #     if session:
    #         try:
    #             sts = session.client('sts')
    #             identity = sts.get_caller_identity()
    #             st.sidebar.success(f"Connected to AWS as: {identity['Arn']}")
    #         except Exception as e:
    #             st.sidebar.error(f"AWS Connection Failed: {e}")

    # Create input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            marital_status = st.selectbox(
                "Marital Status",
                options=list(marital_status_dict.keys()),
            )
            
            application_order = st.number_input(
                "Application Order",
                min_value=0,
                max_value=9,
                value=5,
                help="Order in which the student applied to the course"
            )
            
            course = st.selectbox(
                "Course",
                options=list(course_dict.keys()),
            )
            
            admission_grade = st.slider(
                "Admission Grade",
                min_value=0.0,
                max_value=200.0,
                value=100.0,
                step=10.0
            )
            
            fees_up_to_date = st.selectbox(
                "Tuition Fees Up to Date",
                options=list(yes_or_no_dict.keys()),
            )
            
        with col2:
            gender = st.selectbox(
                "Gender",
                options=list(gender_dict.keys()),
            )
            
            scholarship = st.selectbox(
                "Scholarship Holder",
                options=list(yes_or_no_dict.keys()),
            )
            
            age = st.number_input(
                "Age at Enrollment",
                min_value=16,
                max_value=70,
                value=18
            )
            
            international = st.selectbox(
                "International Student",
                options=list(yes_or_no_dict.keys()),
            )
            
            first_sem_grade = st.slider(
                "First Semester Grade",
                min_value=0.0,
                max_value=20.0,
                value=10.0,
                step=0.1
            )
            
            second_sem_grade = st.slider(
                "Second Semester Grade",
                min_value=0.0,
                max_value=20.0,
                value=10.0,
                step=0.1
            )

        submitted = st.form_submit_button("Predict Performance")

        if submitted:
            with st.spinner('Getting prediction...'):
                input_data = {
                    "Marital status": marital_status_dict[marital_status],
                    "Application order": application_order,
                    "Course": course_dict[course],
                    "Admission grade": admission_grade,
                    "Tuition fees up to date": yes_or_no_dict[fees_up_to_date],
                    "Gender": gender_dict[gender],
                    "Scholarship holder": yes_or_no_dict[scholarship],
                    "Age at enrollment": age,
                    "International": yes_or_no_dict[international],
                    "Curricular units 1st sem (grade)": first_sem_grade,
                    "Curricular units 2nd sem (grade)": second_sem_grade
                }

                # Log the input data
                logger.info(f"Input data: {input_data}")
                
                result = invoke_endpoint(input_data)
                
                if result is not None:
                    st.success("Prediction Complete!")
                    
                    # Handle the result based on your model's output format
                    probability = result[0] if isinstance(result, list) else result
                    dropout, success = probability["probabilities"][0], probability["probabilities"][1]
                    print(f"probability: {dropout}, {success}")
                    

                    
                    st.metric(
                        label="Probability to Graduate",
                        value=f"{success:.2%}"
                    )
                    
                    # Add interpretation
                    if success >= 0.7:
                        st.write("🎯 High probability To Graduate!")
                    elif success >= 0.4:
                        st.write("⚠️ Moderate probability to Graduate - monitor progress")
                    else:
                        st.write("❗ Lower probability to Graduate - may need additional support")

    # # Debug information in sidebar
    # if st.sidebar.checkbox("Show Debug Info"):
    #     st.sidebar.write("Environment Variables:")
    #     st.sidebar.write({
    #         "AWS_REGION": os.getenv("AWS_REGION"),
    #         "ENDPOINT_NAME": os.getenv("ENDPOINT_NAME")
    #     })
