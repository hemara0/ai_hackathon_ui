import streamlit as st

from json_validator import validate_json

st.set_page_config(page_title="JSON Workspace", layout="wide")

st.markdown(
    """
    <style>
    main[data-testid="stAppViewContainer"] {
        padding: 0;
    }
    .textarea-block {
        flex: 1;
        display: flex;
    }
    .textarea-block .stTextArea {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    .textarea-block textarea {
        flex: 1;
        resize: none;
        width: 100%;
        min-height: 100%;
        font-family: "Courier New", monospace;
        font-size: 0.95rem;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #d1d5db;
        background-color: #fff;
    }
    .bottom-bar {
        margin-top: auto;
        padding-top: 0.5rem;
    }
    .bottom-bar [data-testid="column"]:nth-child(n+3) {
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    .bottom-bar [data-testid="column"]:nth-child(3),
    .bottom-bar [data-testid="column"]:nth-child(4) {
        padding-right: 0.5rem;
    }
    .bottom-bar .stButton button {
        background-color: #1d4ed8;
        color: #ffffff;
        border: none;
        min-width: 120px;
        height: 3rem;
        border-radius: 0.5rem;
        font-weight: 600;
        white-space: nowrap;
        padding: 0 1.5rem;
    }
    .bottom-bar .stButton button:hover {
        background-color: #1e40af;
    }
    .bottom-bar .stButton button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.3);
    }
    .bottom-bar [data-testid="column"]:nth-child(2) {
        flex: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="full-page">', unsafe_allow_html=True)

st.markdown("### PAPAA - PriorAuth Patient Access API")
st.markdown('<div class="textarea-block">', unsafe_allow_html=True)
json_payload = st.text_area(
    "PAPAA - PriorAuth Patient Access API",
    placeholder="Paste or type your JSON here...",
    height=500,
    label_visibility="collapsed",
    key="json_payload",
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)
left_col, spacer_col, validate_col, submit_col = st.columns([2, 5, 2, 1])

with left_col:
    document_type = st.selectbox(
        "Document Type",
        ("Claim", "ClaimResponse"),
    )

spacer_col.empty()

with validate_col:
    validate_clicked = st.button("Beauty and Validate", use_container_width=True)

with submit_col:
    submit_clicked = st.button("Submit", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

feedback_container = st.container()

st.markdown('</div>', unsafe_allow_html=True)

if validate_clicked:
    validation_result = validate_json(json_payload)
    with feedback_container:
        if validation_result.is_valid:
            st.success(validation_result.message)
            st.json(validation_result.payload)
            st.toast("JSON validated successfully", icon="✅")
        else:
            st.error(validation_result.message)
            st.toast("JSON validation failed", icon="⚠️")

if submit_clicked:
    st.toast("Submit clicked", icon="🚀")
