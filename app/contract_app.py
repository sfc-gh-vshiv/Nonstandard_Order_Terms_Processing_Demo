#!/usr/bin/env python3
"""
Streamlit app for generating realistic contract documents with non-standard terms.
Includes support for amendments and uses CUAD dataset for inspiration.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import os
import shutil
from pathlib import Path
import hashlib

# Import the contract generator
from contract_generator import ContractGenerator

# Page configuration
st.set_page_config(
    page_title="📄 Contract Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for enhanced styling (from reference app) ---
def get_custom_css():
    """Return custom CSS for enhanced visual styling."""
    return """
    <style>
    /* Import Google Fonts for modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
    
    /* Material Icons */
    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined';
        font-weight: normal;
        font-style: normal;
        font-size: 20px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-feature-settings: 'liga';
        -webkit-font-smoothing: antialiased;
    }
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Modern Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: -0.025em;
        color: #1a202c;
    }
    
    /* Enhanced metric cards with modern design */
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .success-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #a7f3d0;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    .success-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #10b981, #059669);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #fcd34d;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .warning-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #f59e0b, #d97706);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    </style>
    """

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

def scan_contracts_folder():
    """Scan the contracts folder and load existing contracts"""
    contracts = []
    base_path = Path("../contracts")
    
    if not base_path.exists():
        return contracts
    
    # Find all PDF files in the contracts folder
    for pdf_file in base_path.rglob("*.pdf"):
        try:
            # Extract information from filename and path
            filename = pdf_file.name
            folder_name = pdf_file.parent.name
            
            # Parse filename: contract_type_timestamp_id.pdf or amendment_id_noX_timestamp.pdf
            if filename.startswith("amendment_"):
                # Amendment file
                parts = filename.replace(".pdf", "").split("_")
                contract_id = parts[1] if len(parts) > 1 else "unknown"
                contract_type = "Amendment"
                is_amendment = True
            else:
                # Regular contract file
                parts = filename.replace("contract_", "").replace(".pdf", "").split("_")
                type_abbrev = parts[0] if len(parts) > 0 else "unknown"
                contract_id = parts[2] if len(parts) > 2 else "unknown"
                
                # Map abbreviations to full names
                type_map = {
                    'sla': 'Software License Agreement',
                    'psa': 'Professional Services Agreement',
                    'csa': 'Cloud Services Agreement',
                    'hpa': 'Hardware Purchase Agreement',
                    'ma': 'Master Service Agreement',
                    'msa': 'Master Service Agreement',
                    'ca': 'Consulting Agreement',
                    'da': 'Distribution Agreement',
                    'jva': 'Joint Venture Agreement',
                    'saa': 'Strategic Alliance Agreement'
                }
                contract_type = type_map.get(type_abbrev, 'Unknown Agreement')
                is_amendment = False
            
            # Get file stats
            stat = pdf_file.stat()
            file_size = stat.st_size
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            
            # Try to parse folder name for date
            try:
                if len(folder_name) == 10 and folder_name.count('-') == 2:
                    # Date format: YYYY-MM-DD
                    date_str = folder_name
                elif len(folder_name) == 15 and '_' in folder_name:
                    # Timestamp format: YYYYMMDD_HHMMSS
                    date_part = folder_name.split('_')[0]
                    date_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
                else:
                    date_str = modified_time.strftime('%Y-%m-%d')
            except:
                date_str = modified_time.strftime('%Y-%m-%d')
            
            contract = {
                'contract_id': contract_id,
                'name': f"Contract {contract_id.upper()}" if not is_amendment else f"Amendment {contract_id.upper()}",
                'type': contract_type,
                'vendor': 'Various',  # Can't determine from filename
                'value': 0,  # Can't determine from filename
                'date': date_str,
                'filename': str(pdf_file),
                'issues': 0,  # Can't determine from filename
                'file_size': file_size,
                'modified': modified_time,
                'folder': folder_name,
                'is_amendment': is_amendment
            }
            
            contracts.append(contract)
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
            continue
    
    # Sort by modified time (newest first)
    contracts.sort(key=lambda x: x['modified'], reverse=True)
    return contracts

def init_session_state():
    """Initialize session state variables"""
    if 'generated_contracts' not in st.session_state:
        # Load existing contracts from disk
        st.session_state.generated_contracts = scan_contracts_folder()
    if 'contract_history' not in st.session_state:
        st.session_state.contract_history = {c['contract_id']: c for c in st.session_state.generated_contracts}
    if 'viewing_contract' not in st.session_state:
        st.session_state.viewing_contract = None
    if 'amending_contract' not in st.session_state:
        st.session_state.amending_contract = None
    if 'delete_target' not in st.session_state:
        st.session_state.delete_target = None
    if 'delete_type' not in st.session_state:
        st.session_state.delete_type = None

def get_contracts_folder(use_timestamp=False):
    """Get or create the contracts folder with optional timestamp-based organization"""
    base_path = Path("../contracts")
    
    if use_timestamp:
        # Create a new timestamped folder for this batch
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamped_folder = base_path / timestamp
        timestamped_folder.mkdir(parents=True, exist_ok=True)
        return timestamped_folder
    else:
        # Use date-based folder (default behavior)
        today = datetime.now().strftime("%Y-%m-%d")
        dated_folder = base_path / today
        dated_folder.mkdir(parents=True, exist_ok=True)
        return dated_folder

def cleanup_contracts_folder():
    """Clean up the contracts folder"""
    base_path = Path("../contracts")
    if base_path.exists():
        shutil.rmtree(base_path)
        base_path.mkdir(parents=True, exist_ok=True)
        return True
    return False

def delete_contract_file(contract):
    """Delete a single contract file"""
    try:
        pdf_path = Path(contract['filename'])
        if pdf_path.exists():
            pdf_path.unlink()
            return True
    except Exception as e:
        st.error(f"Error deleting file: {e}")
    return False

def delete_folder(folder_name):
    """Delete an entire folder of contracts"""
    try:
        folder_path = Path("../contracts") / folder_name
        if folder_path.exists():
            shutil.rmtree(folder_path)
            return True
    except Exception as e:
        st.error(f"Error deleting folder: {e}")
    return False

@st.dialog("Confirm Deletion")
def confirm_delete_dialog():
    """Show confirmation dialog for deletion"""
    delete_type = st.session_state.delete_type
    delete_target = st.session_state.delete_target
    
    if delete_type == "all":
        st.warning(":material/warning: **Warning: This action cannot be undone!**")
        st.write("You are about to delete **ALL contracts** from all folders.")
        st.write("This will permanently remove all generated contract files.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(":material/delete_forever: Delete All", type="primary", width="stretch"):
                if cleanup_contracts_folder():
                    st.session_state.generated_contracts = []
                    st.session_state.contract_history = {}
                    st.session_state.viewing_contract = None
                    st.session_state.delete_target = None
                    st.session_state.delete_type = None
                    st.success(":material/check_circle: All contracts deleted")
                    st.rerun()
        with col2:
            if st.button(":material/cancel: Cancel", width="stretch"):
                st.session_state.delete_target = None
                st.session_state.delete_type = None
                st.rerun()
    
    elif delete_type == "folder":
        folder_name = delete_target
        contracts_in_folder = [c for c in st.session_state.generated_contracts if c['folder'] == folder_name]
        
        st.warning(":material/warning: **Warning: This action cannot be undone!**")
        st.write(f"You are about to delete the folder **{folder_name}**.")
        st.write(f"This will permanently remove **{len(contracts_in_folder)} contract(s)**.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(":material/delete_forever: Delete Folder", type="primary", width="stretch"):
                if delete_folder(folder_name):
                    # Remove contracts from session state
                    st.session_state.generated_contracts = [
                        c for c in st.session_state.generated_contracts 
                        if c['folder'] != folder_name
                    ]
                    # Update contract history
                    st.session_state.contract_history = {
                        c['contract_id']: c for c in st.session_state.generated_contracts
                    }
                    # Clear viewing contract if it was in the deleted folder
                    if st.session_state.viewing_contract and st.session_state.viewing_contract['folder'] == folder_name:
                        st.session_state.viewing_contract = None
                    
                    st.session_state.delete_target = None
                    st.session_state.delete_type = None
                    st.success(f":material/check_circle: Folder {folder_name} deleted")
                    st.rerun()
        with col2:
            if st.button(":material/cancel: Cancel", width="stretch"):
                st.session_state.delete_target = None
                st.session_state.delete_type = None
                st.rerun()
    
    elif delete_type == "contract":
        contract = delete_target
        
        st.warning(":material/warning: **Warning: This action cannot be undone!**")
        st.write(f"You are about to delete:")
        st.write(f"**{contract['name']}**")
        st.caption(f"{contract['type']} • {contract['date']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(":material/delete_forever: Delete Contract", type="primary", width="stretch"):
                if delete_contract_file(contract):
                    # Remove from session state
                    st.session_state.generated_contracts = [
                        c for c in st.session_state.generated_contracts 
                        if c['filename'] != contract['filename']
                    ]
                    # Update contract history
                    if contract['contract_id'] in st.session_state.contract_history:
                        del st.session_state.contract_history[contract['contract_id']]
                    
                    # Clear viewing contract if it was the deleted one
                    if st.session_state.viewing_contract and st.session_state.viewing_contract['filename'] == contract['filename']:
                        st.session_state.viewing_contract = None
                    
                    st.session_state.delete_target = None
                    st.session_state.delete_type = None
                    st.success(f":material/check_circle: Contract deleted")
                    st.rerun()
        with col2:
            if st.button(":material/cancel: Cancel", width="stretch"):
                st.session_state.delete_target = None
                st.session_state.delete_type = None
                st.rerun()

def show_amendment_dialog():
    """Show amendment creation dialog"""
    base_contract = st.session_state.amending_contract
    
    # Header with back button
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button(":material/arrow_back: Back", width="stretch"):
            st.session_state.amending_contract = None
            st.rerun()
    with col_title:
        st.title(":material/edit_document: Create Amendment")
    
    st.divider()
    
    # Show base contract info
    st.subheader("Base Contract")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Contract", base_contract['name'])
    with col2:
        st.metric("Type", base_contract['type'])
    with col3:
        st.metric("Date", base_contract['date'])
    
    st.divider()
    
    # Amendment configuration
    st.subheader("Amendment Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        amendment_number = st.number_input("Amendment Number", min_value=1, max_value=10, value=1)
    with col2:
        amendment_date = st.date_input("Amendment Date", value=datetime.now())
    
    st.write("**Changes to Include**")
    
    # Pricing changes
    change_pricing = st.checkbox("Modify Pricing Terms", value=True)
    if change_pricing:
        # Handle contracts loaded from disk (value = 0)
        base_value = base_contract['value'] if base_contract['value'] > 0 else 500000
        new_value = st.number_input("New Annual Value ($)", 
                                    min_value=int(base_value * 0.5),
                                    max_value=int(base_value * 2),
                                    value=int(base_value * 1.15))
    
    # Term changes
    change_term = st.checkbox("Extend/Modify Term", value=False)
    if change_term:
        term_extension = st.number_input("Additional Years", min_value=1, max_value=5, value=2)
    
    # Service changes
    add_services = st.checkbox("Add New Services/Products", value=False)
    if add_services:
        new_services = st.text_area("Describe new services", value="Additional cloud storage and API access")
    
    # Other changes
    col1, col2, col3 = st.columns(3)
    with col1:
        modify_liability = st.checkbox("Modify Liability Terms", value=False)
    with col2:
        modify_termination = st.checkbox("Modify Termination Clauses", value=False)
    with col3:
        add_audit_rights = st.checkbox("Add/Modify Audit Rights", value=False)
    
    # Folder organization
    use_timestamp_folder = st.checkbox(
        ":material/create_new_folder: Create new timestamped folder",
        value=False,
        help="When checked, amendment will be saved in a new folder with timestamp."
    )
    
    st.divider()
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(":material/check_circle: Generate Amendment", type="primary", width="stretch"):
            with st.spinner("Generating amendment..."):
                generator = ContractGenerator()
                
                amendment_config = {
                    'base_contract': base_contract,
                    'amendment_number': amendment_number,
                    'amendment_date': amendment_date,
                    'changes': {
                        'pricing': {'enabled': change_pricing, 'new_value': new_value if change_pricing else None},
                        'term': {'enabled': change_term, 'extension': term_extension if change_term else None},
                        'services': {'enabled': add_services, 'description': new_services if add_services else None},
                        'liability': modify_liability,
                        'termination': modify_termination,
                        'audit_rights': add_audit_rights
                    },
                    'output_folder': str(get_contracts_folder(use_timestamp=use_timestamp_folder))
                }
                
                result = generator.generate_amendment(amendment_config)
                
                # Add folder information for consistency with scanned contracts
                folder_name = Path(result['filename']).parent.name
                result['folder'] = folder_name
                # Get actual file size
                try:
                    pdf_path = Path(result['filename'])
                    if pdf_path.exists():
                        result['file_size'] = pdf_path.stat().st_size
                    else:
                        result['file_size'] = 0
                except:
                    result['file_size'] = 0
                result['modified'] = datetime.now()
                result['is_amendment'] = True
                
                st.session_state.generated_contracts.append(result)
                
                st.success(f":material/check_circle: Amendment generated: {result['filename']}")
                
                # Automatically view the generated amendment
                st.session_state.viewing_contract = result
                st.session_state.amending_contract = None
                st.balloons()
                st.rerun()

def show_pdf_viewer_inline():
    """Display the PDF viewer inline on the right side"""
    contract = st.session_state.viewing_contract
    
    # Header with close button
    col_title, col_close = st.columns([5, 1])
    with col_title:
        st.subheader(":material/picture_as_pdf: PDF Viewer")
    with col_close:
        if st.button(":material/close: Close", key="close_pdf", help="Close viewer", width="stretch"):
            st.session_state.viewing_contract = None
            st.rerun()
    
    # Contract info
    st.write(f"**{contract['name']}**")
    st.caption(f"{contract['type']}")
    st.caption(f":material/calendar_today: {contract['date']} • :material/folder: {contract['folder']}")
    
    st.divider()
    
    # PDF Viewer
    try:
        # Check if file exists
        pdf_path = Path(contract['filename'])
        if pdf_path.exists():
            # Display PDF using st.pdf with fixed height for inline viewing
            with st.container():
                st.pdf(str(pdf_path), height=1500)
        else:
            st.error(f":material/error: PDF file not found")
            st.caption(f"{contract['filename']}")
            st.info("The file may have been moved or deleted.")
    except Exception as e:
        st.error(f":material/error: Error displaying PDF: {str(e)}")
        st.info("Make sure streamlit[pdf] is installed: `pip install 'streamlit[pdf]>=1.51.0'`")
        
        # Show more details about the error
        with st.expander("Error Details"):
            st.code(str(e))
            st.write(f"**File path:** {contract['filename']}")
            st.write(f"**File exists:** {pdf_path.exists()}")

def main():
    init_session_state()
    
    # Header
    st.title(":material/description: Contract Generator")
    st.markdown("Generate realistic contracts with non-standard terms for document processing demos")
    st.caption("v2.0 | Contract Generator | Builder: vinod.s@snowflake.com")
    
    # Sidebar
    with st.sidebar:
        st.header(":material/settings: Configuration")
        
        mode = st.radio(
            "Generation Mode",
            ["New Contract", "Batch Generation"],
            help="Choose whether to generate a new contract or multiple contracts"
        )
        
        st.divider()
        
        if mode == "New Contract":
            show_new_contract_ui()
        else:
            show_batch_generation_ui()
        
        st.divider()
        
        # Cleanup option at the bottom
        with st.expander(":material/delete: Cleanup Options"):
            st.write("Delete all generated contracts from all folders")
            if st.button(":material/delete_forever: Delete All Contracts", type="secondary", width="stretch"):
                st.session_state.delete_type = "all"
                st.session_state.delete_target = None
                st.rerun()
    
    # Show delete confirmation dialog
    if st.session_state.delete_type:
        confirm_delete_dialog()
    
    # Show amendment dialog if a contract is being amended
    if st.session_state.amending_contract:
        show_amendment_dialog()
        return
    
    # Main content area - split into left (contracts list) and right (PDF viewer)
    if st.session_state.viewing_contract:
        col1, col2 = st.columns([1, 2])
    else:
        col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(":material/folder_open: Generated Contracts")
        
        # Add refresh button
        if st.button(":material/refresh: Refresh List", help="Reload contracts from disk"):
            st.session_state.generated_contracts = scan_contracts_folder()
            st.session_state.contract_history = {c['contract_id']: c for c in st.session_state.generated_contracts}
            st.rerun()
        
        if st.session_state.generated_contracts:
            # Show statistics at the top
            total = len(st.session_state.generated_contracts)
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Contracts", total)
            with col_b:
                # Count folders
                folders = set(c['folder'] for c in st.session_state.generated_contracts)
                st.metric("Folders", len(folders))
            
            st.divider()
            
            # Group contracts by folder
            contracts_by_folder = {}
            for contract in st.session_state.generated_contracts:
                folder = contract['folder']
                if folder not in contracts_by_folder:
                    contracts_by_folder[folder] = []
                contracts_by_folder[folder].append(contract)
            
            # Display contracts grouped by folder in collapsible expanders
            for folder_idx, folder in enumerate(sorted(contracts_by_folder.keys(), reverse=True)):
                contracts = contracts_by_folder[folder]
                is_first = (folder_idx == 0)
                
                # Folder header with delete button
                col_folder, col_delete = st.columns([5, 1])
                with col_folder:
                    folder_expander = st.expander(f":material/folder: {folder} ({len(contracts)} contracts)", expanded=is_first)
                with col_delete:
                    folder_delete_key = f"delete_folder_{folder_idx}_{folder}"
                    if st.button(":material/delete:", key=folder_delete_key, help="Delete entire folder", width="stretch"):
                        st.session_state.delete_type = "folder"
                        st.session_state.delete_target = folder
                        st.rerun()
                
                # Show contracts inside the expander
                with folder_expander:
                    for contract_idx, contract in enumerate(contracts[:20]):
                        container = st.container()
                        with container:
                            # Contract info with description on the right
                            col_name, col_desc = st.columns([1, 2])
                            with col_name:
                                st.write(f"**{contract['name']}**")
                            with col_desc:
                                st.caption(f"{contract['type']}")
                            
                            # Details line
                            file_size_kb = contract['file_size'] / 1024 if contract['file_size'] > 0 else 0
                            st.caption(f"{contract['date']} • {file_size_kb:.1f} KB")
                            
                            # Action buttons at the bottom
                            col_view, col_amend, col_delete = st.columns(3)
                            file_hash = hashlib.md5(contract['filename'].encode()).hexdigest()[:8]
                            
                            with col_view:
                                view_key = f"view_{folder_idx}_{contract_idx}_{file_hash}"
                                if st.button(":material/visibility: View", key=view_key, help="View PDF", width="stretch"):
                                    st.session_state.viewing_contract = contract
                                    st.session_state.amending_contract = None
                                    st.rerun()
                            
                            with col_amend:
                                amend_key = f"amend_{folder_idx}_{contract_idx}_{file_hash}"
                                if st.button(":material/edit_document: Amend", key=amend_key, help="Create Amendment", width="stretch"):
                                    st.session_state.amending_contract = contract
                                    st.rerun()
                            
                            with col_delete:
                                delete_key = f"delete_{folder_idx}_{contract_idx}_{file_hash}"
                                if st.button(":material/delete: Delete", key=delete_key, help="Delete contract", width="stretch"):
                                    st.session_state.delete_type = "contract"
                                    st.session_state.delete_target = contract
                                    st.rerun()
                        
                        st.divider()
        else:
            st.info("No contracts found. Use the sidebar to create your first contract!")
    
    with col2:
        if st.session_state.viewing_contract:
            # Show PDF viewer
            show_pdf_viewer_inline()
        else:
            # Show statistics
            st.header(":material/analytics: Statistics")
            if st.session_state.generated_contracts:
                total = len(st.session_state.generated_contracts)
                
                # Count by type
                types = {}
                for c in st.session_state.generated_contracts:
                    types[c['type']] = types.get(c['type'], 0) + 1
                
                st.write("**By Type:**")
                for t, count in sorted(types.items(), key=lambda x: x[1], reverse=True)[:5]:
                    st.write(f"• {t}: {count}")
                
                st.divider()
                
                # Recent activity
                st.write("**Recent Activity:**")
                for contract in st.session_state.generated_contracts[:5]:
                    st.caption(f"• {contract['name']} ({contract['date']})")
            else:
                st.info("Statistics will appear here once you generate contracts.")

def show_new_contract_ui():
    """UI for generating a new contract"""
    st.subheader("New Contract")
    
    contract_type = st.selectbox(
        "Contract Type",
        [
            "Software License Agreement",
            "Professional Services Agreement",
            "Cloud Services Agreement",
            "Hardware Purchase Agreement",
            "Master Service Agreement",
            "Consulting Agreement",
            "Distribution Agreement",
            "Maintenance Agreement",
            "Joint Venture Agreement",
            "Strategic Alliance Agreement"
        ]
    )
    
    # Vendor information
    vendor_name = st.text_input("Vendor Name", value=f"TechVendor Solutions Inc.")
    
    # Contract details
    col1, col2 = st.columns(2)
    with col1:
        contract_value = st.number_input("Annual Value ($)", min_value=10000, max_value=10000000, value=500000, step=50000)
        term_years = st.number_input("Term (years)", min_value=1, max_value=10, value=3)
    with col2:
        effective_date = st.date_input("Effective Date", value=datetime.now())
        auto_renewal = st.checkbox("Auto-renewal", value=True)
    
    # Risk factors
    st.write("**Risk Factors**")
    col1, col2 = st.columns(2)
    with col1:
        include_uncapped_fees = st.checkbox("Uncapped variable fees", value=True)
        include_low_liability = st.checkbox("Low liability caps", value=True)
        include_data_sovereignty = st.checkbox("Data sovereignty issues", value=False)
    with col2:
        include_asymmetric_terms = st.checkbox("Asymmetric termination", value=True)
        include_ip_issues = st.checkbox("IP ownership problems", value=False)
        include_warranty_gaps = st.checkbox("Warranty gaps", value=False)
    
    # Document size
    doc_size = st.select_slider(
        "Document Complexity",
        options=["Minimal", "Standard", "Detailed", "Comprehensive"],
        value="Standard"
    )
    
    # Folder organization option
    use_timestamp_folder = st.checkbox(
        ":material/create_new_folder: Create new timestamped folder",
        value=False,
        help="When checked, contract will be saved in a new folder with timestamp (e.g., 20251125_143022). "
             "When unchecked, contract will be added to today's date folder (e.g., 2025-11-25)."
    )
    
    if st.button(":material/add_circle: Generate Contract", type="primary", width="stretch"):
        with st.spinner("Generating contract..."):
            generator = ContractGenerator()
            
            config = {
                'type': contract_type,
                'vendor_name': vendor_name,
                'value': contract_value,
                'term_years': term_years,
                'effective_date': effective_date,
                'auto_renewal': auto_renewal,
                'risk_factors': {
                    'uncapped_fees': include_uncapped_fees,
                    'low_liability': include_low_liability,
                    'data_sovereignty': include_data_sovereignty,
                    'asymmetric_terms': include_asymmetric_terms,
                    'ip_issues': include_ip_issues,
                    'warranty_gaps': include_warranty_gaps
                },
                'doc_size': doc_size,
                'output_folder': str(get_contracts_folder(use_timestamp=use_timestamp_folder))
            }
            
            result = generator.generate_contract(config)
            
            # Add folder information for consistency with scanned contracts
            folder_name = Path(result['filename']).parent.name
            result['folder'] = folder_name
            # Get actual file size
            try:
                pdf_path = Path(result['filename'])
                if pdf_path.exists():
                    result['file_size'] = pdf_path.stat().st_size
                else:
                    result['file_size'] = 0
            except:
                result['file_size'] = 0
            result['modified'] = datetime.now()
            result['is_amendment'] = False
            
            st.session_state.generated_contracts.append(result)
            st.session_state.contract_history[result['contract_id']] = result
            
            st.success(f":material/check_circle: Contract generated: {result['filename']}")
            st.balloons()
            st.rerun()

def show_amendment_ui():
    """UI for generating an amendment"""
    st.subheader("Contract Amendment")
    
    if not st.session_state.generated_contracts:
        st.warning(":material/warning: No contracts available. Generate a contract first.")
        return
    
    contract_options = {f"{c['name']} ({c['date']})": c['contract_id'] 
                       for c in st.session_state.generated_contracts}
    
    selected_contract = st.selectbox("Select Base Contract", options=list(contract_options.keys()))
    contract_id = contract_options[selected_contract]
    base_contract = st.session_state.contract_history[contract_id]
    
    st.info(f"**Base:** {base_contract['name']} | **Value:** ${base_contract['value']:,}")
    
    amendment_number = st.number_input("Amendment Number", min_value=1, max_value=10, value=1)
    amendment_date = st.date_input("Amendment Date", value=datetime.now())
    
    st.write("**Changes to Include**")
    
    change_pricing = st.checkbox("Modify Pricing Terms", value=True)
    if change_pricing:
        # Handle contracts loaded from disk (value = 0)
        base_value = base_contract['value'] if base_contract['value'] > 0 else 500000
        new_value = st.number_input("New Annual Value ($)", 
                                    min_value=int(base_value * 0.5),
                                    max_value=int(base_value * 2),
                                    value=int(base_value * 1.15))
    
    change_term = st.checkbox("Extend/Modify Term", value=False)
    if change_term:
        term_extension = st.number_input("Additional Years", min_value=1, max_value=5, value=2)
    
    add_services = st.checkbox("Add New Services/Products", value=False)
    if add_services:
        new_services = st.text_area("Describe new services", value="Additional cloud storage and API access")
    
    modify_liability = st.checkbox("Modify Liability Terms", value=False)
    modify_termination = st.checkbox("Modify Termination Clauses", value=False)
    add_audit_rights = st.checkbox("Add/Modify Audit Rights", value=False)
    
    # Folder organization option
    use_timestamp_folder = st.checkbox(
        ":material/create_new_folder: Create new timestamped folder",
        value=False,
        help="When checked, amendment will be saved in a new folder with timestamp (e.g., 20251125_143022). "
             "When unchecked, amendment will be added to today's date folder (e.g., 2025-11-25)."
    )
    
    if st.button(":material/edit_document: Generate Amendment", type="primary", width="stretch"):
        with st.spinner("Generating amendment..."):
            generator = ContractGenerator()
            
            amendment_config = {
                'base_contract': base_contract,
                'amendment_number': amendment_number,
                'amendment_date': amendment_date,
                'changes': {
                    'pricing': {'enabled': change_pricing, 'new_value': new_value if change_pricing else None},
                    'term': {'enabled': change_term, 'extension': term_extension if change_term else None},
                    'services': {'enabled': add_services, 'description': new_services if add_services else None},
                    'liability': modify_liability,
                    'termination': modify_termination,
                    'audit_rights': add_audit_rights
                },
                'output_folder': str(get_contracts_folder(use_timestamp=use_timestamp_folder))
            }
            
            result = generator.generate_amendment(amendment_config)
            
            # Add folder information for consistency with scanned contracts
            folder_name = Path(result['filename']).parent.name
            result['folder'] = folder_name
            result['file_size'] = 0  # Will be set after file is created
            result['modified'] = datetime.now()
            result['is_amendment'] = True
            
            st.session_state.generated_contracts.append(result)
            
            st.success(f":material/check_circle: Amendment generated: {result['filename']}")
            st.balloons()
            st.rerun()

def show_batch_generation_ui():
    """UI for batch generation with performance optimization"""
    st.subheader("Batch Generation")
    
    st.write("Generate multiple contracts at once for comprehensive testing.")
    
    # Use number input instead of slider for large quantities
    num_contracts = st.number_input(
        "Number of Contracts", 
        min_value=1, 
        max_value=10000, 
        value=10,
        step=1,
        help="Enter the number of contracts to generate (1-10,000)"
    )
    
    # Option to organize in timestamped folder
    use_timestamp_folder = st.checkbox(
        ":material/create_new_folder: Create new timestamped folder",
        value=True,
        help="When checked, contracts will be saved in a new folder with timestamp (e.g., 20251125_143022). "
             "When unchecked, contracts will be added to today's date folder (e.g., 2025-11-25)."
    )
    
    st.write("**Contract Types to Include**")
    col1, col2 = st.columns(2)
    with col1:
        include_software = st.checkbox("Software License", value=True)
        include_services = st.checkbox("Professional Services", value=True)
        include_cloud = st.checkbox("Cloud Services", value=True)
        include_hardware = st.checkbox("Hardware Purchase", value=True)
        include_msa = st.checkbox("Master Service Agreement", value=True)
    with col2:
        include_consulting = st.checkbox("Consulting", value=True)
        include_distribution = st.checkbox("Distribution", value=False)
        include_maintenance = st.checkbox("Maintenance", value=False)
        include_jv = st.checkbox("Joint Venture", value=False)
        include_alliance = st.checkbox("Strategic Alliance", value=False)
    
    st.divider()
    
    # Risk Factors
    st.write("**Risk Factors**")
    col1, col2 = st.columns(2)
    with col1:
        include_uncapped_fees = st.checkbox("Uncapped variable fees", value=True)
        include_low_liability = st.checkbox("Low liability caps", value=True)
        include_data_sovereignty = st.checkbox("Data sovereignty issues", value=False)
    with col2:
        include_asymmetric_terms = st.checkbox("Asymmetric termination", value=True)
        include_ip_issues = st.checkbox("IP ownership problems", value=False)
        include_warranty_gaps = st.checkbox("Warranty gaps", value=False)
    
    st.divider()
    
    # Document Complexity
    doc_size = st.select_slider(
        "Document Complexity",
        options=["Minimal", "Standard", "Detailed", "Comprehensive"],
        value="Comprehensive",
        help="Controls the length and detail level of generated contracts"
    )
    
    if st.button(":material/rocket_launch: Generate Batch", type="primary", width="stretch"):
        # Determine which types to generate
        types = []
        if include_software: types.append("Software License Agreement")
        if include_services: types.append("Professional Services Agreement")
        if include_cloud: types.append("Cloud Services Agreement")
        if include_hardware: types.append("Hardware Purchase Agreement")
        if include_msa: types.append("Master Service Agreement")
        if include_consulting: types.append("Consulting Agreement")
        if include_distribution: types.append("Distribution Agreement")
        if include_maintenance: types.append("Maintenance Agreement")
        if include_jv: types.append("Joint Venture Agreement")
        if include_alliance: types.append("Strategic Alliance Agreement")
        
        if not types:
            st.error("Please select at least one contract type!")
            return
        
        generator = ContractGenerator()
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        stats_placeholder = st.empty()
        
        start_time = datetime.now()
        generated_count = 0
        
        for i in range(num_contracts):
            contract_type = random.choice(types)
            status_text.text(f"Generating {i+1}/{num_contracts}: {contract_type}...")
            
            # Get output folder once at the start of batch generation
            if i == 0:
                output_folder = str(get_contracts_folder(use_timestamp=use_timestamp_folder))
            
            config = {
                'type': contract_type,
                'batch_mode': True,
                'output_folder': output_folder,
                'doc_size': doc_size,
                'risk_factors': {
                    'uncapped_fees': include_uncapped_fees,
                    'low_liability': include_low_liability,
                    'data_sovereignty': include_data_sovereignty,
                    'asymmetric_terms': include_asymmetric_terms,
                    'ip_issues': include_ip_issues,
                    'warranty_gaps': include_warranty_gaps
                }
            }
            
            result = generator.generate_contract(config)
            
            # Add folder information for consistency with scanned contracts
            folder_name = Path(result['filename']).parent.name
            result['folder'] = folder_name
            # Get actual file size
            try:
                pdf_path = Path(result['filename'])
                if pdf_path.exists():
                    result['file_size'] = pdf_path.stat().st_size
                else:
                    result['file_size'] = 0
            except:
                result['file_size'] = 0
            result['modified'] = datetime.now()
            result['is_amendment'] = False
            
            st.session_state.generated_contracts.append(result)
            st.session_state.contract_history[result['contract_id']] = result
            generated_count += 1
            
            # Update progress
            progress = (i + 1) / num_contracts
            progress_bar.progress(progress)
            
            # Show stats every 10 contracts or at the end
            if (i + 1) % 10 == 0 or i == num_contracts - 1:
                elapsed = (datetime.now() - start_time).total_seconds()
                rate = generated_count / elapsed if elapsed > 0 else 0
                remaining = (num_contracts - generated_count) / rate if rate > 0 else 0
                
                stats_placeholder.info(
                    f"**Progress:** {generated_count}/{num_contracts} | "
                    f"**Rate:** {rate:.1f} contracts/sec | "
                    f"**Est. remaining:** {remaining:.0f}s"
                )
        
        # Clear progress indicators
        status_text.empty()
        progress_bar.empty()
        stats_placeholder.empty()
        
        # Final summary
        elapsed_total = (datetime.now() - start_time).total_seconds()
        st.success(f":material/check_circle: Successfully generated {num_contracts} contracts in {elapsed_total:.1f} seconds!")
        st.balloons()
        
        # Show summary table
        with st.expander(":material/summarize: Batch Summary"):
            df = pd.DataFrame([
                {
                    'Contract': c['name'],
                    'Type': c['type'],
                    'Value': f"${c['value']:,}",
                    'Issues': c['issues']
                }
                for c in st.session_state.generated_contracts[-num_contracts:]
            ])
            st.dataframe(df, use_container_width=True)
        
        st.rerun()

if __name__ == "__main__":
    main()
