# Contract Generator for Document Processing Demos

A Streamlit web application that generates realistic contract documents with non-standard terms for demonstrating document processing capabilities to audit teams within finance organizations.

## Overview

This tool generates verbose, realistic contract PDFs containing various **non-standard terms** that typically require audit team review. Each contract includes highlighted audit notes identifying problematic clauses for easy reference.

## Features

### Contract Generation
- **10 Contract Types**: Software License, Professional Services, Cloud Services, Hardware Purchase, Master Service Agreement, Consulting, Distribution, Maintenance, Joint Venture, and Strategic Alliance agreements
- **Verbose & Realistic**: Contracts are comprehensive with multiple articles, subsections, and legal language inspired by the CUAD (Contract Understanding Atticus Dataset)
- **Customizable Risk Factors**: 
  - Uncapped variable fees
  - Low liability caps
  - Data sovereignty issues
  - Asymmetric termination rights
  - IP ownership problems
  - Warranty gaps
- **Document Complexity Control**: Generate minimal, standard, detailed, or comprehensive contracts

### Amendment Support
- Create amendments for any existing contract
- Modify pricing, terms, services, liability, and termination clauses
- Amendments automatically link to base contracts
- Track amendment history

### Batch Generation
- Generate up to 10,000 contracts at once
- Select specific contract types to include
- Configure risk factors and document complexity for entire batch
- Real-time progress tracking with performance metrics
- Organized output in timestamped folders

### Web Interface
- **Interactive Streamlit App**: Modern, user-friendly interface with Material Icons
- **PDF Viewer**: View contracts directly in the browser
- **Contract Management**: Browse, view, amend, and delete contracts
- **Folder Organization**: Contracts organized by date or custom timestamps
- **Persistent Storage**: Contracts are saved to disk and reload on app restart

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
cd app
pip install -r requirements.txt
```

The requirements include:
- `reportlab` - PDF generation
- `streamlit[pdf]>=1.51.0` - Web framework with PDF viewing support
- `pandas` - Data handling

## Usage

### Starting the Application

```bash
cd app
streamlit run contract_app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Generating Contracts

#### Single Contract
1. Select "New Contract" mode in the sidebar
2. Choose contract type and vendor details
3. Configure contract value, term, and effective date
4. Select risk factors to include
5. Set document complexity level
6. Click "Generate Contract"

#### Batch Generation
1. Select "Batch Generation" mode in the sidebar
2. Enter the number of contracts to generate
3. Choose which contract types to include
4. Configure risk factors and document complexity
5. Optionally create a new timestamped folder
6. Click "Generate Batch"

#### Creating Amendments
1. Browse to any contract in the list
2. Click the "Amend" button
3. Configure amendment details:
   - Amendment number and date
   - Pricing modifications
   - Term extensions
   - New services
   - Liability and termination changes
4. Click "Generate Amendment"
5. The amendment PDF is automatically displayed

### Managing Contracts

- **View**: Click the "View" button to display the PDF in the browser
- **Amend**: Click the "Amend" button to create an amendment
- **Delete**: Click the "Delete" button to remove a contract (with confirmation)
- **Delete Folder**: Click the delete icon next to a folder name to remove all contracts in that folder
- **Refresh**: Click "Refresh List" to reload contracts from disk
- **Cleanup**: Use the "Cleanup Options" in the sidebar to delete all contracts

## Contract Types & Common Issues

Each contract type includes realistic problematic terms:

### Software License Agreement
- Accelerated payment terms (15 days vs. standard 30)
- Uncapped variable usage fees
- Above-market price escalation (8% annually)
- Low liability caps (5-6% of contract value)
- Asymmetric termination with 50% penalty
- 180-day auto-renewal notice period

### Professional Services Agreement
- Above-market hourly rates (15-20% premium)
- No caps on hours or expenses
- Consultant retains all IP rights
- Aggressive payment terms (10 days)
- High late fees (24% APR)
- 30% early termination penalty

### Cloud Services Agreement
- Below-standard SLA (99.5% vs. 99.9%)
- Uncapped usage-based pricing
- No guaranteed data location
- Broad provider data access rights
- Short data retention periods (90 days)
- Inadequate liability caps

### Other Agreement Types
- Hardware Purchase: Short warranties, mandatory expensive maintenance
- Master Service Agreement: Broad indemnification, asymmetric terms
- Distribution Agreement: Restrictive territory clauses, minimum purchase requirements
- Maintenance Agreement: Limited support hours, expensive on-call rates
- Joint Venture: Unequal profit sharing, exit restrictions
- Strategic Alliance: Non-compete clauses, IP sharing issues

## Output Structure

Contracts are organized in the `contracts/` folder:

```
contracts/
├── 2025-11-25/              # Date-based folders
│   ├── contract_sla_*.pdf
│   ├── contract_psa_*.pdf
│   └── ...
├── 20251125_143022/         # Timestamped folders (batch generation)
│   ├── contract_*.pdf
│   └── amendment_*.pdf
└── ...
```

## Use Cases

- **Document Processing Demos**: Showcase AI/ML capabilities for contract analysis
- **Audit Team Training**: Help teams identify problematic contract terms
- **Procurement Process Improvement**: Demonstrate need for contract review automation
- **Risk Assessment Tools**: Test systems for identifying financial and legal risks
- **Compliance Checking**: Validate automated compliance review systems
- **LLM Training**: Generate training data for contract understanding models

## Audit Focus Areas

Contracts highlight issues relevant to finance audit teams:

- **Financial Risk**: Uncapped fees, escalation clauses, termination penalties
- **Operational Risk**: SLA gaps, support limitations, forced upgrades
- **Legal Risk**: Indemnification imbalances, liability caps, arbitration clauses
- **Compliance Risk**: Data sovereignty, breach notification, insurance requirements
- **Strategic Risk**: Long lock-in periods, IP ownership, vendor dependencies

## Technical Details

### Architecture
- **Frontend**: Streamlit web framework with Material Design icons
- **PDF Generation**: ReportLab library for professional document formatting
- **Contract Engine**: Modular generator supporting multiple contract types
- **Storage**: File-based with automatic folder organization
- **Session Management**: Streamlit session state for UI interactions

### File Naming Convention
- Contracts: `contract_{type}_{timestamp}_{id}.pdf`
- Amendments: `amendment_{contract_id}_no{number}_{timestamp}.pdf`

### Contract Abbreviations
- `sla` - Software License Agreement
- `psa` - Professional Services Agreement
- `csa` - Cloud Services Agreement
- `hpa` - Hardware Purchase Agreement
- `msa` - Master Service Agreement
- `ca` - Consulting Agreement
- `da` - Distribution Agreement
- `ma` - Maintenance Agreement
- `jva` - Joint Venture Agreement
- `saa` - Strategic Alliance Agreement

## Notes

- All companies, names, and details are fictional
- Contracts are for demonstration purposes only
- Not intended for actual legal use
- Audit notes are highlighted in red within the documents
- CUAD dataset (`CUAD_v1/`) is used for inspiration but not included in git

## License

This project is for demonstration purposes. All generated contracts are fictional and should not be used for actual legal agreements.

## Support

For issues or questions, contact: vinod.s@snowflake.com
