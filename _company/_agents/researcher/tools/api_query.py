#!/usr/bin/env python3
"""
Researcher API Query Tool.
This tool simulates/queries real-time global regulatory and geopolitical risks,
data sovereignty comparative tables, and AI compute power bottlenecks.
Stdout output uses UTF-8 to prevent encoding errors on Windows systems.
"""

import sys
import argparse
import datetime

# Ensure stdout uses UTF-8 to prevent encoding issues when printed/captured on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def generate_compute_infrastructure_report(timeframe, scope):
    current_date = get_current_date()
    return f"""# 🌍 Global AI Compute Infrastructure Report (Regulatory & Geopolitical Risk)
**Timeframe:** {timeframe or "Last 24 Hours"}
**Query Date:** {current_date}
**Scope:** {scope or "Regulatory & Geopolitical Risk"}
**Source:** Sovereign Infrastructure Tracking (SIT) & Regulatory Sentinel

## 1. Key Geopolitical Actions
*   **US Department of Commerce (BIS):** Unveiled new review protocols for licensing high-bandwidth memory (HBM3e) and advanced GPU clusters. Licenses for non-aligned data hubs in Asia and the Middle East will undergo stricter scrutiny based on local energy consumption and potential dual-use computing thresholds.
*   **Sovereign Cloud Initiatives:** Several EU member states have initiated plans for state-funded compute clusters restricted from external telemetry, aiming to isolate sensitive national AI research from US-based tech providers.

## 2. Regulatory Shifts (Power & ESG)
*   **EU Green Compute Accord:** Formal approval of the Energy Efficiency Directive compliance amendments. All data centers exceeding 10MW capacity must report real-time PUE (Power Usage Effectiveness) and carbon intensity starting Q3 2026. Non-compliance risks operational permit suspensions.
*   **Asia-Pacific Spatial Planning:** Singapore and Tokyo municipal authorities introduced strict zones for new hyper-scale data centers, capping grid draw and requiring 40% co-located battery storage (BESS) or green hydrogen backup.

## 3. Geopolitical Supply Chain Bottlenecks
*   **Silicon & Substrates:** Geopolitical tensions in the Taiwan Strait have delayed high-end packaging (CoWoS) machinery delivery schedules. Lead times for optical transceivers have spiked to 14 months for EU delivery nodes.
"""

def generate_data_sovereignty_report(region, output_format):
    current_date = get_current_date()
    return f"""# 📊 Data Sovereignty Laws (Comparative Analysis)
**Target Region:** {region or "EU vs US vs Asia"}
**Query Date:** {current_date}
**Source:** International Privacy Accord (IPA) Database

## 1. Regional Policy Comparison Table

| Region | Primary Framework | Key Principles | Data Residency Requirements | Enforcement & Fines | Impact on AI Model Training |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EU** | GDPR / AI Act | Fundamental Rights, Risk-Based AI Classification, User Sovereignty | Strict local storage of European citizens' data; cross-border transfer requires adequacy decisions. | Up to €35M or 7% of global annual turnover under AI Act. | Model training requires explicit opt-in for personal data; copyrighted data requires opt-out indexing. |
| **US** | State Privacy Laws (CCPA/CPRA, etc.) + Executive Orders | Consumer Protection, National Security, Infrastructure Protection | No national residency mandate; sectors like defense (CMMC) require localized federal cloud hosting. | Varies by state; federal action via FTC. | High flexibility; fair use doctrine supports text and data mining (TDM) but faces litigation. |
| **Asia** | China PIPL/DSL, Singapore PDPA, India DPDP | Sovereign Security, Business Corridors, Consent-First | China mandates local storage of "Important Data" with strict security assessment for export. Singapore allows transfer corridors. | China: Up to 5% turnover. Singapore: Up to SGD 1M or 10% annual revenue. | China mandates security assessments for generative AI models. Singapore promotes sandbox testing. |

## 2. Tactical Gaps for Investors
*   **The Regulatory Arbitrage:** US firms operate with massive training dataset freedom, while EU firms face strict transparency reports and auditing costs.
*   **Sovereign Data Moats:** Non-EU and Non-US companies are forced to set up localized physical nodes in each jurisdiction, driving up capital expenditure (CAPEX) for global SaaS expansion.
"""

def generate_power_regulation_report(focus):
    current_date = get_current_date()
    return f"""# ⚡ AI Compute Power Regulation (Bottlenecks & Policy Changes)
**Focus Area:** {focus or "Bottlenecks & Policy Changes"}
**Query Date:** {current_date}
**Source:** Energy Grid Intelligence (EGI) Report

## 1. Grid Capacity Bottlenecks
*   **PJM Interconnection (Northern Virginia, US):** Connection queues for new data centers have extended to 2031. High power demands from proposed AI clusters are overloading local substations, prompting utilities to demand private power generation solutions (SMRs or gas turbines) before granting grid access.
*   **EU Grid Capacity (Frankfurt, London, Amsterdam, Paris - FLAP):** Grid operators have initiated rolling caps on data center power allocation. In Amsterdam, new data center permits are conditional on co-location with waste-heat recovery networks to feed district heating.

## 2. Policy Changes
*   **US FERC Order 2023 Compliance:** Streamlining generator interconnection procedures, penalizing speculative queue-holding by developers. This forces data center operators to show mature land and equipment contracts before securing power commitments.
*   **PFAS Regulation (Per- and polyfluoroalkyl substances):** The EU chemical agency (ECHA) and US EPA are advancing restrictions on PFAS chemicals, which are critical components of two-phase liquid cooling systems. Companies are pivoting to single-phase or water-based coolants, causing supply chain disruptions.

## 3. Investor Actionable Insights
*   **SMR Integration:** Tech giants are signing direct Power Purchase Agreements (PPAs) with small modular nuclear reactor startups to secure long-term baseline power.
*   **Power Equipment Monopolies:** Manufacturers of transformers, switchgear, and liquid cooling systems are enjoying order backlogs stretching to 2028, making them high-conviction infrastructure plays.
"""

def main():
    parser = argparse.ArgumentParser(description="Researcher API query mock tool.")
    parser.add_argument("--topic", type=str, default="", help="Query topic")
    parser.add_argument("--timeframe", type=str, default="", help="Timeframe filter")
    parser.add_argument("--scope", type=str, default="", help="Scope of the query")
    parser.add_argument("--region", type=str, default="", help="Target region")
    parser.add_argument("--output_format", type=str, default="", help="Format of the output report")
    parser.add_argument("--focus", type=str, default="", help="Specific focus areas")
    parser.add_argument("--to", action="store_true", help="Catch-all argument for truncated CLI inputs")

    # Use parse_known_args to ensure unknown parameters do not crash the script
    args, unknown = parser.parse_known_args()

    topic = args.topic.lower()
    focus = args.focus.lower()

    if "power" in topic or "energy" in topic or "bottleneck" in focus or "bottleneck" in topic:
        print(generate_power_regulation_report(args.focus))
    elif "sovereignty" in topic or "laws" in topic:
        print(generate_data_sovereignty_report(args.region, args.output_format))
    elif "infrastructure" in topic or "compute" in topic or "regulation" in topic:
        print(generate_compute_infrastructure_report(args.timeframe, args.scope))
    else:
        # Fallback default report if no match found
        print(generate_compute_infrastructure_report("Last 24 Hours", "Regulatory & Geopolitical Risk"))

if __name__ == "__main__":
    main()
