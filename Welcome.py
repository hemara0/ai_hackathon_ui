import streamlit as st

st.set_page_config(page_title="FHIR Tools", layout="wide")

st.title("FHIR Tools Workspace")

st.markdown(
    """
    <style>
    .hero-wrapper {
        max-width: 1080px;
        margin: 3rem auto 0;
        padding: 3rem 3.25rem 3.5rem;
        border-radius: 28px;
        background: radial-gradient(120% 140% at 20% 20%, rgba(84, 110, 255, 0.45), rgba(9, 21, 42, 0.95)),
                    linear-gradient(135deg, rgba(20, 27, 63, 0.95), rgba(17, 38, 85, 0.75));
        backdrop-filter: blur(6px);
        box-shadow: 0 24px 45px rgba(7, 17, 43, 0.45);
        position: relative;
        overflow: hidden;
    }
    .hero-wrapper::after {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(65% 70% at 80% 20%, rgba(255, 255, 255, 0.18), transparent 70%);
        mix-blend-mode: screen;
        opacity: 0;
        animation: glowSweep 5.5s ease-in-out 1.2s forwards;
        pointer-events: none;
    }
    .hero-text {
        text-align: center;
        color: #f5f7ff;
        position: relative;
        z-index: 1;
    }
    .hero-text h2 {
        font-size: 2.1rem;
        margin-bottom: 0.85rem;
        letter-spacing: 0.01em;
    }
    .hero-text p {
        font-size: 1.1rem;
        margin: 0.35rem 0;
        line-height: 1.65;
    }
    .hero-text strong {
        color: #ffffff;
    }
    .hero-text ul {
        text-align: left;
        display: inline-block;
        margin: 0.85rem auto 0.25rem;
        padding-left: 1.25rem;
        list-style-position: outside;
    }
    .hero-text li {
        margin-bottom: 0.35rem;
    }
    .narrative-block {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 1.25rem 1.5rem;
        margin-top: 1.2rem;
        display: inline-block;
        text-align: left;
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.12);
    }
    .hero-gallery {
        margin-top: 2.5rem;
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    .image-card {
        width: 220px;
        padding: 1rem;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.06);
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.1), 0 16px 32px rgba(5, 12, 28, 0.35);
        text-align: left;
        color: #f1f4ff;
        opacity: 0;
        transform: translateY(12px);
    }
    .image-card img {
        width: 100%;
        border-radius: 14px;
        margin-bottom: 0.75rem;
        box-shadow: 0 12px 24px rgba(8, 13, 28, 0.4);
    }
    .image-card span {
        font-size: 0.95rem;
        line-height: 1.45;
    }
    .fade-sequence {
        opacity: 0;
        animation-name: fadeInUp;
        animation-duration: 1.1s;
        animation-timing-function: ease-out;
        animation-fill-mode: forwards;
    }
    .image-card.fade-sequence {
        animation-duration: 1.15s;
    }
    .delay-1 { animation-delay: 0.2s; }
    .delay-2 { animation-delay: 0.9s; }
    .delay-3 { animation-delay: 1.6s; }
    .delay-4 { animation-delay: 2.3s; }
    .delay-5 { animation-delay: 3.0s; }
    .delay-6 { animation-delay: 3.7s; }
    .delay-7 { animation-delay: 4.4s; }
    .delay-8 { animation-delay: 5.1s; }
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    @keyframes glowSweep {
        0% {
            opacity: 0;
            transform: translateX(-20%);
        }
        40% {
            opacity: 0.55;
        }
        100% {
            opacity: 0;
            transform: translateX(25%);
        }
    }
    @media (max-width: 992px) {
        .hero-wrapper {
            padding: 2.5rem 1.8rem 3rem;
        }
        .hero-text h2 {
            font-size: 1.85rem;
        }
    }
    @media (max-width: 640px) {
        .hero-gallery {
            flex-direction: column;
            align-items: center;
        }
        .image-card {
            width: 100%;
            max-width: 320px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-wrapper">
        <div class="hero-text">
            <h2 class="fade-sequence delay-1">Welcome to your FHIR command center.</h2>
            <p class="fade-sequence delay-2">
                Curate, validate, and enrich clinical data with clarity while collaborating alongside AI-powered insights.
            </p>
            <p class="fade-sequence delay-3">
                Open the <strong>FHIR Validator</strong> to inspect JSON resources or connect with <strong>Chat with AI</strong> for guided exploration.
            </p>
            <p class="fade-sequence delay-4">
                We are building Omada's unified platform for Prior Authorization and Patient Access APIs with governance, automation, and guardrails baked in.
            </p>
            <div class="narrative-block fade-sequence delay-5">
                <p><strong>Two flagship proof-of-concepts:</strong></p>
                <ul>
                    <li><strong>HL7 Conformance:</strong> An n8n-orchestrated workspace to query, validate, map, and diff FHIR R4 artifacts, featuring RAG over official HL7 specs, human-approved auto-repair, and version impact analysis.</li>
                    <li><strong>Prior-Auth Compliance:</strong> A policy-aware copilot that assembles complete, citation-backed packets, auto-computes required metrics, and routes every response through human approval.</li>
                </ul>
                <p><em>Omada's Promise to Map:</em> Safety, security, citations, LLM-as-Judge, and immutable audit embedded at every turn.</p>
            </div>
        </div>
        <div class="hero-gallery">
            <div class="image-card fade-sequence delay-6">
                <img src="https://images.unsplash.com/photo-1581092795360-1b71a7a29a27?auto=format&fit=crop&w=600&q=80" alt="Clinician reviewing digital patient charts" />
                <span>Patient access insights illuminated with human-in-the-loop guardrails.</span>
            </div>
            <div class="image-card fade-sequence delay-7">
                <img src="https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=600&q=80" alt="Engineer working on code with data diagrams" />
                <span>FHIR artisans troubleshoot, diff, and auto-repair HL7 artifacts with confidence.</span>
            </div>
            <div class="image-card fade-sequence delay-8">
                <img src="https://images.unsplash.com/photo-1530023367847-a683933f4176?auto=format&fit=crop&w=600&q=80" alt="Team collaborating with analytics dashboard" />
                <span>Policy-aware copilots assemble citation-backed prior authorization packets.</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Select a page from the sidebar to begin.")
