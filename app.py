import streamlit as st
import boto3
import json

# AWS CONFIG
REGION = "us-east-1"
KNOWLEDGE_BASE_ID = "LDM48BQ6MA"

session = boto3.Session(
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["AWS_DEFAULT_REGION"]
)

# Bedrock Clients
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=REGION
)

bedrock_agent_runtime = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name=REGION
)

# UI
st.title("AI Campaign A/B Simulation Engine")

objective = st.text_input("Campaign Objective")
audience = st.text_input("Target Audience")

variant_a = st.text_input("Variant A Reward")
variant_b = st.text_input("Variant B Reward")

duration = st.text_input("Campaign Duration")

if st.button("Run Simulation"):

    prompt = f"""
    You are an AI-powered campaign simulation engine.

    Use historical campaign knowledge to simulate likely campaign outcomes.

    Compare these two variants.

    VARIANT A:
    Reward Type: {variant_a}

    VARIANT B:
    Reward Type: {variant_b}

    Objective:
    {objective}

    Audience:
    {audience}

    Duration:
    {duration}

    Return:
    - Predicted winning variant
    - Confidence score
    - Expected KPI uplift
    - Supporting historical patterns
    - Risk factors
    """

    response = bedrock_agent_runtime.retrieve_and_generate(
        input={
            "text": prompt
        },
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"            }
        }
    )

    result = response["output"]["text"]

    st.subheader("Simulation Result")
    st.write(result)
