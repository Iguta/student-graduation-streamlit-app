import streamlit as st
import boto3
import json
import os
from dotenv import load_dotenv
import logging
# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure AWS credentials
def get_aws_session():
    """Create AWS session with credentials from environment variables"""
    try:
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            # aws_session_token=os.getenv('AWS_SESSION_TOKEN'),  # Include if using temporary credentials
            region_name=os.getenv('AWS_REGION')
        )
        return session
    except Exception as e:
        logger.error(f"Failed to create AWS session: {e}")
        return None

def invoke_endpoint(data):
    """Invoke SageMaker endpoint with input data"""
    try:
        session = get_aws_session()
        if not session:
            st.error("Failed to create AWS session")
            return None
            
        runtime_client = session.client('sagemaker-runtime')
        
        response = runtime_client.invoke_endpoint(
            EndpointName=os.getenv('ENDPOINT_NAME'),
            ContentType='application/json',
            Body=json.dumps(data)
        )
        
        result = json.loads(response['Body'].read().decode())
        logger.info(f"Prediction result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error invoking endpoint: {e}")
        st.error(f"Error getting prediction: {str(e)}")
        return None