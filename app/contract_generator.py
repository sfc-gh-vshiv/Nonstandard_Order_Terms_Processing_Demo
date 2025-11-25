#!/usr/bin/env python3
"""
Enhanced contract generator with CUAD dataset integration and amendment support.
Uses different templates for different contract types to avoid repetition.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from datetime import datetime, timedelta
import random
import uuid
import os
from pathlib import Path
import pandas as pd

class ContractGenerator:
    """Generate realistic contracts with non-standard terms"""
    
    def __init__(self, cuad_path=None):
        """Initialize generator with optional CUAD dataset path"""
        self.cuad_path = cuad_path or "../CUAD_v1"
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
        # Load CUAD data if available
        self.cuad_data = self.load_cuad_data()
        
        # Contract templates by type
        self.templates = {
            'Software License Agreement': self.generate_software_license,
            'Professional Services Agreement': self.generate_professional_services,
            'Cloud Services Agreement': self.generate_cloud_services,
            'Hardware Purchase Agreement': self.generate_hardware_purchase,
            'Master Service Agreement': self.generate_master_service,
            'Consulting Agreement': self.generate_consulting,
            'Distribution Agreement': self.generate_distribution,
            'Maintenance Agreement': self.generate_maintenance,
            'Joint Venture Agreement': self.generate_joint_venture,
            'Strategic Alliance Agreement': self.generate_strategic_alliance
        }
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.audit_note_style = ParagraphStyle(
            'AuditNote',
            parent=self.styles['BodyText'],
            textColor=colors.red,
            fontName='Helvetica-Bold',
            fontSize=9
        )
    
    def load_cuad_data(self):
        """Load CUAD dataset for inspiration"""
        try:
            csv_path = Path(self.cuad_path) / "master_clauses.csv"
            if csv_path.exists():
                # Load only first few columns to avoid memory issues
                df = pd.read_csv(csv_path, nrows=100)
                return df
        except Exception as e:
            print(f"Could not load CUAD data: {e}")
        return None
    
    def generate_contract(self, config):
        """Generate a contract based on configuration"""
        contract_type = config.get('type', 'Software License Agreement')
        
        # Generate contract ID
        contract_id = str(uuid.uuid4())[:8]
        
        # Get template function
        template_func = self.templates.get(contract_type, self.generate_software_license)
        
        # Generate filename with output folder support
        output_folder = config.get('output_folder', '../contracts')
        type_abbrev = ''.join([word[0] for word in contract_type.split()]).lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_suffix = str(uuid.uuid4())[:4]  # Add random suffix for uniqueness in batch
        filename = f"{output_folder}/contract_{type_abbrev}_{timestamp}_{random_suffix}.pdf"
        
        # Generate the contract
        issues_count = template_func(filename, config)
        
        # Return metadata
        return {
            'contract_id': contract_id,
            'name': f"Contract {contract_id.upper()}",
            'type': contract_type,
            'vendor': config.get('vendor_name', 'TechVendor Solutions Inc.'),
            'value': config.get('value', 500000),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'filename': filename,
            'issues': issues_count
        }
    
    def generate_amendment(self, config):
        """Generate an amendment to an existing contract"""
        base_contract = config['base_contract']
        amendment_num = config['amendment_number']
        amendment_date = config['amendment_date']
        changes = config['changes']
        
        # Generate filename with output folder support
        output_folder = config.get('output_folder', '../contracts')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_folder}/amendment_{base_contract['contract_id']}_no{amendment_num}_{timestamp}.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        Story = []
        
        # Title
        Story.append(Paragraph(f"AMENDMENT NO. {amendment_num}", self.title_style))
        Story.append(Paragraph(f"TO {base_contract['type'].upper()}", self.title_style))
        Story.append(Spacer(1, 20))
        
        # Amendment metadata
        Story.append(Paragraph(f"<b>Amendment Date:</b> {amendment_date.strftime('%B %d, %Y')}", self.styles['Normal']))
        Story.append(Paragraph(f"<b>Original Contract ID:</b> {base_contract['contract_id'].upper()}", self.styles['Normal']))
        Story.append(Paragraph(f"<b>Original Effective Date:</b> {base_contract['date']}", self.styles['Normal']))
        Story.append(Spacer(1, 20))
        
        # Recitals
        Story.append(Paragraph("<b>RECITALS</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        WHEREAS, {base_contract['vendor']} ("Vendor") and Global Finance Corp. ("Client") entered into 
        a {base_contract['type']} dated {base_contract['date']} (the "Original Agreement"); and
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        WHEREAS, the parties desire to amend certain terms and conditions of the Original Agreement 
        as set forth herein;
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, 
        the parties agree as follows:
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 20))
        
        # Amendments
        Story.append(Paragraph("<b>AMENDMENTS</b>", self.styles['Heading2']))
        
        article_num = 1
        issues_count = 0
        
        # Pricing changes
        if changes['pricing']['enabled']:
            Story.append(Paragraph(f"<b>Article {article_num}: Pricing Modification</b>", self.styles['Heading3']))
            old_value = base_contract['value'] if base_contract['value'] > 0 else 500000
            new_value = changes['pricing']['new_value']
            increase_pct = ((new_value - old_value) / old_value) * 100 if old_value > 0 else 0
            
            Story.append(Paragraph(f"""
            The annual contract value set forth in the Original Agreement is hereby amended from 
            ${old_value:,} to ${new_value:,}, representing an increase of {increase_pct:.1f}%. 
            <b><font color="red">AUDIT NOTE: Price increase of {increase_pct:.1f}% exceeds typical 
            market adjustments (3-5% annually).</font></b>
            """, self.styles['BodyText']))
            Story.append(Spacer(1, 12))
            article_num += 1
            issues_count += 1
        
        # Term extension
        if changes['term']['enabled']:
            Story.append(Paragraph(f"<b>Article {article_num}: Term Extension</b>", self.styles['Heading3']))
            extension = changes['term']['extension']
            
            Story.append(Paragraph(f"""
            The term of the Original Agreement is hereby extended for an additional {extension} year(s). 
            All other terms and conditions shall remain in full force and effect during the extended term. 
            <b><font color="red">AUDIT NOTE: Extended commitment without renegotiation of other terms. 
            Consider reviewing liability caps and pricing for extended period.</font></b>
            """, self.styles['BodyText']))
            Story.append(Spacer(1, 12))
            article_num += 1
            issues_count += 1
        
        # New services
        if changes['services']['enabled']:
            Story.append(Paragraph(f"<b>Article {article_num}: Additional Services</b>", self.styles['Heading3']))
            
            Story.append(Paragraph(f"""
            Vendor shall provide the following additional services: {changes['services']['description']}. 
            Pricing for these additional services shall be as set forth in Exhibit A attached hereto. 
            <b><font color="red">AUDIT NOTE: New services added without competitive bidding. 
            Pricing may be above market rate.</font></b>
            """, self.styles['BodyText']))
            Story.append(Spacer(1, 12))
            article_num += 1
            issues_count += 1
        
        # Liability modifications
        if changes['liability']:
            Story.append(Paragraph(f"<b>Article {article_num}: Liability Modification</b>", self.styles['Heading3']))
            
            Story.append(Paragraph("""
            The limitation of liability provision in the Original Agreement is hereby amended to 
            provide that Vendor's total liability shall not exceed the lesser of (i) $100,000 or 
            (ii) the fees paid in the six months preceding the claim. <b><font color="red">AUDIT NOTE: 
            Liability cap has been reduced from original terms. This may not adequately cover potential damages.</font></b>
            """, self.styles['BodyText']))
            Story.append(Spacer(1, 12))
            article_num += 1
            issues_count += 1
        
        # Termination modifications
        if changes['termination']:
            Story.append(Paragraph(f"<b>Article {article_num}: Termination Rights</b>", self.styles['Heading3']))
            
            Story.append(Paragraph("""
            Client's termination for convenience provision is hereby amended to require 180 days 
            prior written notice and payment of an early termination fee equal to 40% of the remaining 
            contract value. <b><font color="red">AUDIT NOTE: Termination penalty has been increased. 
            This restricts Client's flexibility to exit the agreement.</font></b>
            """, self.styles['BodyText']))
            Story.append(Spacer(1, 12))
            article_num += 1
            issues_count += 1
        
        # Audit rights
        if changes['audit_rights']:
            Story.append(Paragraph(f"<b>Article {article_num}: Audit Rights</b>", self.styles['Heading3']))
            
            Story.append(Paragraph("""
            Client shall have the right to audit Vendor's records related to this Agreement upon 
            30 days prior written notice, not more than once per calendar year. Client shall bear 
            all costs of such audit unless the audit reveals an overcharge of more than 5%. 
            <b><font color="red">AUDIT NOTE: Limited audit frequency and Client bears audit costs 
            unless significant discrepancy found.</font></b>
            """, self.styles['BodyText']))
            Story.append(Spacer(1, 12))
            article_num += 1
            issues_count += 1
        
        # General provisions
        Story.append(Paragraph("<b>GENERAL PROVISIONS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        Except as expressly amended herein, all terms and conditions of the Original Agreement 
        shall remain in full force and effect. In the event of any conflict between this Amendment 
        and the Original Agreement, the terms of this Amendment shall control.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 20))
        
        # Signatures
        Story.append(Paragraph("<b>SIGNATURES</b>", self.styles['Heading2']))
        Story.append(Spacer(1, 12))
        
        sig_data = [
            [f'VENDOR: {base_contract["vendor"]}', 'CLIENT: Global Finance Corp.'],
            ['', ''],
            ['_________________________________', '_________________________________'],
            ['Authorized Signatory', 'Authorized Signatory'],
            [f'Date: {amendment_date.strftime("%B %d, %Y")}', f'Date: {amendment_date.strftime("%B %d, %Y")}']
        ]
        
        sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
        sig_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        Story.append(sig_table)
        
        doc.build(Story)
        print(f"✓ Generated amendment: {filename}")
        
        # Return metadata
        return {
            'contract_id': f"{base_contract['contract_id']}_AMD{amendment_num}",
            'name': f"Amendment {amendment_num} to {base_contract['name']}",
            'type': f"Amendment to {base_contract['type']}",
            'vendor': base_contract['vendor'],
            'value': changes['pricing']['new_value'] if changes['pricing']['enabled'] else base_contract['value'],
            'date': amendment_date.strftime('%Y-%m-%d'),
            'filename': filename,
            'issues': issues_count,
            'base_contract_id': base_contract['contract_id']
        }
    
    # Individual contract generators with verbose, realistic terms
    
    def _create_signature_table(self, vendor_name):
        """Create a standard signature table"""
        sig_data = [
            [f'VENDOR: {vendor_name}', 'CLIENT: Global Finance Corp.'],
            ['', ''],
            ['By: _________________________________', 'By: _________________________________'],
            ['Name: ______________________________', 'Name: ______________________________'],
            ['Title: _______________________________', 'Title: _______________________________'],
            [f'Date: {datetime.now().strftime("%B %d, %Y")}', f'Date: {datetime.now().strftime("%B %d, %Y")}']
        ]
        
        sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
        sig_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        return sig_table
    
    def generate_software_license(self, filename, config):
        """Generate verbose Software License Agreement"""
        doc = SimpleDocTemplate(filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        Story = []
        Story.append(Paragraph("SOFTWARE LICENSE AGREEMENT", self.title_style))
        Story.append(Spacer(1, 12))
        
        vendor = config.get('vendor_name', 'TechVendor Solutions Inc.')
        value = config.get('value', 850000)
        term_years = config.get('term_years', 3)
        
        # Contract metadata
        Story.append(Paragraph(f"<b>Contract Number:</b> SLA-{datetime.now().strftime('%Y')}-{random.randint(100,999)}", self.styles['Normal']))
        Story.append(Paragraph(f"<b>Effective Date:</b> {datetime.now().strftime('%B %d, %Y')}", self.styles['Normal']))
        Story.append(Paragraph(f"<b>Expiration Date:</b> {(datetime.now() + timedelta(days=365*term_years)).strftime('%B %d, %Y')}", self.styles['Normal']))
        Story.append(Spacer(1, 20))
        
        # Parties
        Story.append(Paragraph("<b>PARTIES</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        This Software License Agreement ("Agreement") is entered into on {datetime.now().strftime('%B %d, %Y')} 
        by and between <b>{vendor}</b>, a Delaware corporation with principal offices at 
        {random.randint(100,9999)} Innovation Drive, San Francisco, CA {random.randint(94100,94199)} ("Licensor"), 
        and <b>Global Finance Corp.</b>, a New York corporation with principal offices at 
        {random.randint(100,999)} Wall Street, New York, NY {random.randint(10001,10099)} ("Licensee"). 
        Each of the foregoing parties is referred to herein as a "Party" and together as the "Parties".
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Recitals
        Story.append(Paragraph("<b>RECITALS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>WHEREAS,</b> Licensor has developed and owns certain proprietary software products and related 
        documentation (collectively, the "Software"); and
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        Story.append(Paragraph("""
        <b>WHEREAS,</b> Licensee desires to obtain a license to use the Software for its internal business 
        operations, and Licensor desires to grant such license, all in accordance with the terms and conditions 
        set forth herein;
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        Story.append(Paragraph("""
        <b>NOW, THEREFORE,</b> in consideration of the mutual covenants and agreements contained herein, 
        and for other good and valuable consideration, the receipt and sufficiency of which are hereby 
        acknowledged, the Parties agree as follows:
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 1: License Grant
        Story.append(Paragraph("<b>ARTICLE 1: LICENSE GRANT AND RESTRICTIONS</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>1.1 Grant of License.</b> Subject to the terms and conditions of this Agreement, Licensor hereby 
        grants to Licensee a non-exclusive, non-transferable, non-sublicensable license to use the Software 
        solely for Licensee's internal business operations during the Term. The license granted hereunder 
        is limited to use by up to {random.randint(100,500)} named users and shall not exceed 
        {random.randint(5,20)} concurrent users at any given time. <b><font color="red">AUDIT NOTE: 
        Non-transferable license restricts Licensee's flexibility in corporate restructuring scenarios.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>1.2 License Restrictions.</b> Licensee shall not, and shall not permit any third party to: 
        (a) copy, modify, or create derivative works of the Software; (b) reverse engineer, disassemble, 
        or decompile the Software or attempt to derive the source code; (c) rent, lease, lend, sell, 
        sublicense, assign, distribute, publish, transfer, or otherwise make available the Software; 
        (d) remove, alter, or obscure any proprietary notices on the Software; (e) use the Software 
        for timesharing or service bureau purposes or otherwise for the benefit of any third party; 
        or (f) use the Software in any manner that violates any applicable law, regulation, or rule.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>1.3 Reservation of Rights.</b> Licensor reserves all rights not expressly granted to Licensee 
        in this Agreement. Except for the limited rights and licenses expressly granted under this Agreement, 
        nothing in this Agreement grants, by implication, waiver, estoppel, or otherwise, to Licensee or 
        any third party any intellectual property rights or other right, title, or interest in or to the 
        Licensor's intellectual property.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 2: Payment Terms
        Story.append(Paragraph("<b>ARTICLE 2: FEES AND PAYMENT TERMS</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>2.1 License Fees.</b> In consideration for the license granted hereunder, Licensee shall pay 
        Licensor an annual license fee of ${value:,} (the "Base License Fee"), payable in quarterly 
        installments of ${value//4:,} each. The first installment shall be due and payable within fifteen 
        (15) days of the Effective Date, with subsequent installments due on the first day of each calendar 
        quarter thereafter. <b><font color="red">AUDIT NOTE: First payment due within 15 days of contract 
        execution (non-standard - typically 30 days). This accelerated payment term creates cash flow pressure.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph(f"""
        <b>2.2 Variable Usage Fees.</b> In addition to the Base License Fee, Licensee shall pay usage-based 
        fees calculated as follows: (a) $0.15 per transaction for the first 1,000,000 transactions per month; 
        (b) $0.10 per transaction for transactions 1,000,001 to 5,000,000 per month; and (c) $0.05 per 
        transaction for all transactions exceeding 5,000,000 per month. Usage fees shall be calculated monthly 
        and invoiced in arrears, with payment due within thirty (30) days of invoice date. <b><font color="red">
        AUDIT NOTE: Usage fees are uncapped and could result in significant cost overruns. No maximum monthly 
        cap specified, creating unlimited financial exposure for high-volume usage.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph(f"""
        <b>2.3 Price Escalation.</b> The Base License Fee and per-transaction rates shall automatically 
        increase annually on each anniversary of the Effective Date by the greater of (a) eight percent (8%) 
        or (b) the Consumer Price Index (CPI) for All Urban Consumers plus three percentage points (3%). 
        <b><font color="red">AUDIT NOTE: Escalation clause is significantly above market rate (typical is 3-5% 
        annually). The 8% minimum increase substantially exceeds typical inflation rates.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 3: Term and Termination
        Story.append(Paragraph("<b>ARTICLE 3: TERM AND TERMINATION</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>3.1 Term.</b> This Agreement shall commence on the Effective Date and shall continue for an 
        initial term of {term_years} ({term_years}) years (the "Initial Term"), unless earlier terminated 
        in accordance with this Article 3. Upon expiration of the Initial Term, this Agreement shall 
        automatically renew for successive three (3) year periods unless either Party provides written notice 
        of non-renewal at least one hundred eighty (180) days prior to the end of the then-current term. 
        <b><font color="red">AUDIT NOTE: Auto-renewal with extended notice period (typical is 60-90 days). 
        The 180-day requirement may be difficult to track and could result in unintended renewals.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 4: Warranties
        Story.append(Paragraph("<b>ARTICLE 4: WARRANTIES AND DISCLAIMERS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>4.1 Limited Warranty.</b> Licensor warrants that for a period of ninety (90) days from the 
        Effective Date, the Software will perform substantially in accordance with the Documentation. 
        Licensor's sole obligation and Licensee's exclusive remedy for any breach of this warranty shall 
        be for Licensor to use commercially reasonable efforts to correct any reproducible error.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 5: Limitation of Liability
        Story.append(Paragraph("<b>ARTICLE 5: LIMITATION OF LIABILITY</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>5.1 Limitation.</b> IN NO EVENT SHALL LICENSOR'S TOTAL AGGREGATE LIABILITY EXCEED THE LESSER OF 
        (I) FIFTY THOUSAND DOLLARS ($50,000) OR (II) THE AGGREGATE FEES PAID IN THE THREE (3) MONTHS 
        IMMEDIATELY PRECEDING THE EVENT. <b><font color="red">AUDIT NOTE: Liability cap is significantly 
        lower than annual contract value (${value:,}). The $50,000 cap represents only 
        {(50000/value*100):.1f}% of annual fees.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 20))
        
        # Signatures
        Story.append(Paragraph("<b>IN WITNESS WHEREOF</b>", self.styles['Heading2']))
        Story.append(Spacer(1, 12))
        Story.append(self._create_signature_table(vendor))
        
        doc.build(Story)
        return 9
    
    def generate_professional_services(self, filename, config):
        """Generate verbose Professional Services Agreement"""
        doc = SimpleDocTemplate(filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        Story = []
        Story.append(Paragraph("PROFESSIONAL SERVICES AGREEMENT", self.title_style))
        Story.append(Spacer(1, 12))
        
        vendor = config.get('vendor_name', 'Apex Consulting Group LLC')
        value = config.get('value', 1200000)
        
        Story.append(Paragraph(f"<b>Contract Number:</b> PSA-{datetime.now().strftime('%Y')}-{random.randint(100,999)}", self.styles['Normal']))
        Story.append(Paragraph(f"<b>Effective Date:</b> {datetime.now().strftime('%B %d, %Y')}", self.styles['Normal']))
        Story.append(Spacer(1, 20))
        
        # Parties
        Story.append(Paragraph("<b>PARTIES</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        This Professional Services Agreement ("Agreement") is entered into between <b>{vendor}</b> 
        ("Consultant"), a limited liability company organized under the laws of Delaware, and 
        <b>Global Finance Corp.</b> ("Client"), a New York corporation.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Recitals
        Story.append(Paragraph("<b>RECITALS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>WHEREAS,</b> Consultant possesses specialized expertise in enterprise software implementation, 
        business process optimization, and digital transformation; and
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        Story.append(Paragraph("""
        <b>WHEREAS,</b> Client desires to engage Consultant to provide certain professional services as 
        more particularly described herein;
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        Story.append(Paragraph("""
        <b>NOW, THEREFORE,</b> in consideration of the mutual covenants and promises contained herein, 
        the parties agree as follows:
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 1: Scope of Services
        Story.append(Paragraph("<b>ARTICLE 1: SCOPE OF SERVICES</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>1.1 Services.</b> Consultant shall provide professional consulting services including, but not 
        limited to: (a) enterprise architecture design and review; (b) software development and integration; 
        (c) project management and oversight; (d) business process analysis and optimization; (e) technical 
        training and knowledge transfer; and (f) such other services as may be mutually agreed upon in writing 
        by the parties (collectively, the "Services"). The specific scope, deliverables, and timelines for 
        each engagement shall be set forth in one or more Statements of Work executed by both parties.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>1.2 Standard of Performance.</b> Consultant shall perform the Services in a professional and 
        workmanlike manner consistent with industry standards. Consultant shall assign qualified personnel 
        with appropriate skills and experience to perform the Services. However, Consultant makes no guarantee 
        regarding specific outcomes or results from the Services provided. <b><font color="red">AUDIT NOTE: 
        No specific performance metrics or success criteria defined. "Industry standards" is vague and 
        difficult to enforce.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>1.3 Personnel Substitution.</b> Consultant reserves the right to substitute personnel assigned 
        to perform Services at any time without prior notice to Client, provided that substitute personnel 
        possess substantially similar qualifications and experience. <b><font color="red">AUDIT NOTE: 
        Unlimited substitution rights without Client approval may result in inconsistent service quality 
        and loss of institutional knowledge.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 2: Fees and Payment
        Story.append(Paragraph("<b>ARTICLE 2: FEES AND PAYMENT TERMS</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>2.1 Fee Structure.</b> Client shall pay Consultant for Services rendered on a time and materials 
        basis according to the following hourly rates: (a) Senior Consultants: $325 per hour; (b) Mid-Level 
        Consultants: $250 per hour; (c) Junior Consultants: $175 per hour; (d) Project Managers: $350 per hour; 
        and (e) Subject Matter Experts: $450 per hour. The estimated total engagement value is ${value:,}, 
        however this is an estimate only and not a cap on fees. <b><font color="red">AUDIT NOTE: No cap on 
        total hours or monthly billing. Rates are 15-20% above market. Estimated value of ${value:,} is 
        non-binding and could significantly exceed budget.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>2.2 Expenses.</b> In addition to fees, Client shall reimburse Consultant for all reasonable and 
        documented out-of-pocket expenses incurred in connection with the Services, including but not limited 
        to: travel, lodging, meals, telecommunications, shipping, and reproduction costs. Consultant may charge 
        a fifteen percent (15%) administrative fee on all reimbursable expenses. <b><font color="red">AUDIT NOTE: 
        15% administrative fee on expenses is excessive (typical is 0-5%). No pre-approval requirement for 
        expenses or spending limits specified.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>2.3 Invoicing and Payment.</b> Consultant shall invoice Client bi-weekly for Services rendered 
        and expenses incurred. Payment is due within ten (10) business days of invoice date. Late payments 
        shall accrue interest at the rate of two percent (2%) per month or the maximum rate permitted by law, 
        whichever is less. <b><font color="red">AUDIT NOTE: 10-day payment terms are aggressive (typical is 
        30 days). 2% monthly interest rate (24% annually) is excessive.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>2.4 Rate Increases.</b> Consultant reserves the right to increase hourly rates upon thirty (30) 
        days written notice to Client. Rate increases shall not exceed ten percent (10%) in any twelve-month 
        period. <b><font color="red">AUDIT NOTE: Unilateral right to increase rates with only 30 days notice. 
        10% annual increase cap is high and compounds over multi-year engagements.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 3: Intellectual Property
        Story.append(Paragraph("<b>ARTICLE 3: INTELLECTUAL PROPERTY RIGHTS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>3.1 Ownership of Work Product.</b> All work product, deliverables, inventions, discoveries, 
        improvements, methodologies, processes, tools, templates, and materials created or developed by 
        Consultant in connection with the Services (collectively, "Work Product") shall remain the exclusive 
        property of Consultant. Client is granted a non-exclusive, non-transferable, perpetual license to use 
        the Work Product solely for its internal business purposes. <b><font color="red">AUDIT NOTE: Client 
        does not own work product despite paying for development. Non-transferable license limits Client's 
        ability to share with subsidiaries or use after corporate restructuring.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>3.2 Pre-Existing Materials.</b> Consultant retains all rights to any pre-existing materials, 
        methodologies, tools, templates, or intellectual property that existed prior to this engagement or 
        that Consultant develops independently outside the scope of Services for Client. To the extent any 
        such pre-existing materials are incorporated into Work Product, Client's license to use such materials 
        is limited to the specific implementation provided to Client.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>3.3 Restrictions on Use.</b> Client shall not: (a) modify, adapt, or create derivative works from 
        the Work Product; (b) reverse engineer, decompile, or disassemble any software or tools provided by 
        Consultant; (c) remove or alter any proprietary notices; (d) use the Work Product to provide services 
        to third parties; or (e) sublicense, sell, rent, lease, or otherwise transfer rights to the Work Product. 
        <b><font color="red">AUDIT NOTE: Severe restrictions on Client's use of work product it paid to develop. 
        Cannot modify or create derivatives, limiting ability to adapt to changing business needs.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 4: Term and Termination
        Story.append(Paragraph("<b>ARTICLE 4: TERM AND TERMINATION</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>4.1 Term.</b> This Agreement shall commence on the Effective Date and continue for an initial term 
        of two (2) years, unless earlier terminated in accordance with this Article. Upon expiration of the 
        initial term, this Agreement shall automatically renew for successive one-year periods unless either 
        party provides written notice of non-renewal at least ninety (90) days prior to the end of the 
        then-current term.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>4.2 Termination for Convenience.</b> Client may terminate this Agreement for convenience upon 
        ninety (90) days prior written notice and payment of an early termination fee equal to thirty percent 
        (30%) of the estimated fees for the remainder of the then-current term, calculated based on the average 
        monthly billings for the preceding six (6) months. <b><font color="red">AUDIT NOTE: Substantial early 
        termination penalty (30% of remaining term) creates significant exit costs and vendor lock-in.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>4.3 Effect of Termination.</b> Upon termination, Client shall: (a) immediately pay all outstanding 
        fees and expenses through the effective date of termination; (b) pay for all work in progress at the 
        applicable hourly rates; (c) return or destroy all Consultant materials and work product, except for 
        materials specifically licensed to Client; and (d) pay any early termination fees if applicable. 
        Consultant shall have no obligation to provide transition assistance unless separately agreed in writing 
        and compensated at Consultant's then-current rates.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 5: Warranties and Disclaimers
        Story.append(Paragraph("<b>ARTICLE 5: WARRANTIES AND DISCLAIMERS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>5.1 Limited Warranty.</b> Consultant warrants that Services will be performed in a professional 
        manner consistent with industry standards. EXCEPT FOR THE FOREGOING, CONSULTANT MAKES NO OTHER 
        WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR 
        PURPOSE. Consultant does not warrant that Services will meet Client's requirements or achieve any 
        particular results.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 6: Limitation of Liability
        Story.append(Paragraph("<b>ARTICLE 6: LIMITATION OF LIABILITY AND INDEMNIFICATION</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>6.1 Limitation of Liability.</b> CONSULTANT'S TOTAL AGGREGATE LIABILITY ARISING OUT OF OR RELATED 
        TO THIS AGREEMENT SHALL NOT EXCEED THE LESSER OF (I) ONE HUNDRED THOUSAND DOLLARS ($100,000) OR 
        (II) THE AGGREGATE FEES PAID BY CLIENT IN THE SIX (6) MONTHS IMMEDIATELY PRECEDING THE CLAIM. 
        <b><font color="red">AUDIT NOTE: Liability cap of $100,000 is inadequate for estimated engagement 
        value of ${value:,}. Cap represents only {(100000/value*100):.1f}% of estimated fees, leaving 
        substantial risk with Client.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>6.2 Client Indemnification.</b> Client shall indemnify, defend, and hold harmless Consultant from 
        any claims arising from: (a) Client's use of Work Product; (b) Client's breach of this Agreement; 
        (c) any claim that Client's data or materials infringe third party rights; or (d) Client's negligence 
        or willful misconduct. This indemnification obligation shall survive termination for seven (7) years. 
        <b><font color="red">AUDIT NOTE: Broad indemnification obligation with extended seven-year survival 
        period. Client assumes liability for Consultant's work product usage.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 7: Confidentiality
        Story.append(Paragraph("<b>ARTICLE 7: CONFIDENTIAL INFORMATION</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>7.1 Obligations.</b> Each party agrees to maintain the confidentiality of the other party's 
        Confidential Information and to use such information solely for purposes of this Agreement. The 
        receiving party shall protect Confidential Information using the same degree of care it uses for 
        its own confidential information, but in no event less than reasonable care. These obligations shall 
        survive termination for a period of five (5) years.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>7.2 Exceptions.</b> Confidential Information does not include information that: (a) is or becomes 
        publicly available through no breach of this Agreement; (b) was rightfully known prior to disclosure; 
        (c) is rightfully received from a third party without breach; or (d) is independently developed without 
        use of Confidential Information.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 8: General Provisions
        Story.append(Paragraph("<b>ARTICLE 8: GENERAL PROVISIONS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>8.1 Independent Contractor.</b> Consultant is an independent contractor and not an employee of 
        Client. Consultant shall be solely responsible for all taxes, insurance, and benefits for its personnel.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>8.2 Governing Law.</b> This Agreement shall be governed by the laws of the State of Delaware, 
        without regard to conflicts of law principles. Any disputes shall be resolved through binding 
        arbitration in Wilmington, Delaware under the rules of the American Arbitration Association.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>8.3 Entire Agreement.</b> This Agreement constitutes the entire agreement between the parties 
        and supersedes all prior agreements, understandings, and communications, whether written or oral, 
        relating to the subject matter hereof.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 20))
        
        # Signatures
        Story.append(Paragraph("<b>IN WITNESS WHEREOF</b>", self.styles['Heading2']))
        Story.append(Spacer(1, 12))
        Story.append(self._create_signature_table(vendor))
        
        doc.build(Story)
        return 11
    
    def generate_cloud_services(self, filename, config):
        """Generate verbose Cloud Services Agreement"""
        doc = SimpleDocTemplate(filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        Story = []
        Story.append(Paragraph("CLOUD SERVICES AGREEMENT", self.title_style))
        Story.append(Spacer(1, 12))
        
        vendor = config.get('vendor_name', 'CloudTech Services Inc.')
        value = config.get('value', 950000)
        
        Story.append(Paragraph(f"<b>Contract Number:</b> CSA-{datetime.now().strftime('%Y')}-{random.randint(100,999)}", self.styles['Normal']))
        Story.append(Paragraph(f"<b>Effective Date:</b> {datetime.now().strftime('%B %d, %Y')}", self.styles['Normal']))
        Story.append(Spacer(1, 20))
        
        # Parties
        Story.append(Paragraph("<b>PARTIES</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        This Cloud Services Agreement is entered into between <b>{vendor}</b> ("Provider"), 
        a Delaware corporation, and <b>Global Finance Corp.</b> ("Customer"), a New York corporation.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 1: Services
        Story.append(Paragraph("<b>ARTICLE 1: CLOUD SERVICES</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>1.1 Service Description.</b> Provider shall make available to Customer cloud-based infrastructure, 
        platform, and software services including: (a) compute resources (virtual machines, containers); 
        (b) storage services (object, block, and file storage); (c) database services; (d) networking and 
        content delivery; (e) security and identity management; (f) analytics and machine learning tools; 
        and (g) monitoring and management tools (collectively, the "Services"). Specific service tiers, 
        performance specifications, and resource allocations are detailed in the Service Level Agreement 
        attached as Exhibit A.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>1.2 Service Availability.</b> Provider shall use commercially reasonable efforts to maintain 
        Service availability of 99.5% measured monthly, excluding scheduled maintenance windows. Scheduled 
        maintenance may occur at any time upon 48 hours notice. <b><font color="red">AUDIT NOTE: 99.5% 
        uptime SLA is below industry standard (typically 99.9% or higher for critical services). This 
        allows for up to 3.6 hours of downtime per month. Maintenance windows are not excluded from SLA 
        calculation in most enterprise agreements.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>1.3 Service Modifications.</b> Provider reserves the right to modify, suspend, or discontinue 
        any aspect of the Services at any time with thirty (30) days notice. Provider may make emergency 
        changes without notice if required for security or system integrity. <b><font color="red">AUDIT NOTE: 
        Broad right to modify or discontinue services with minimal notice. No compensation or migration 
        assistance provided if critical services are discontinued.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 2: Fees and Payment
        Story.append(Paragraph("<b>ARTICLE 2: FEES AND PAYMENT</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>2.1 Pricing Model.</b> Customer shall pay for Services based on actual usage according to 
        Provider's published rate card, as may be amended from time to time. Estimated annual spend is 
        ${value:,}, however actual costs will vary based on consumption. Pricing includes: (a) compute 
        charges based on instance type and hours used; (b) storage charges based on GB stored and data 
        transfer; (c) database charges based on instance size and IOPS; (d) network egress charges; and 
        (e) premium support fees of fifteen percent (15%) of total monthly usage. <b><font color="red">
        AUDIT NOTE: Usage-based pricing with no caps creates unlimited cost exposure. 15% premium support 
        fee is excessive (typical is 5-10%). Provider can unilaterally change rates via published rate card 
        updates.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>2.2 Rate Changes.</b> Provider may modify its rates at any time upon sixty (60) days notice. 
        Continued use of Services after rate changes constitutes acceptance of new rates. Rate increases 
        shall not exceed fifteen percent (15%) in any twelve-month period. <b><font color="red">AUDIT NOTE: 
        Unilateral right to increase rates by up to 15% annually. No option to terminate without penalty 
        if rates increase significantly.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>2.3 Billing and Payment.</b> Provider shall invoice Customer monthly in arrears for all usage 
        during the preceding month. Payment is due within fifteen (15) days of invoice date. Provider may 
        suspend Services immediately if payment is more than five (5) days overdue. <b><font color="red">
        AUDIT NOTE: Aggressive payment terms (15 days) and service suspension after only 5 days of late 
        payment could disrupt business operations.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 3: Data and Security
        Story.append(Paragraph("<b>ARTICLE 3: DATA SECURITY AND PRIVACY</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>3.1 Customer Data.</b> Customer retains all rights to data and content uploaded to the Services 
        ("Customer Data"). Provider is granted a worldwide, non-exclusive license to use, copy, store, 
        transmit, and display Customer Data solely to provide the Services. Provider may use aggregated, 
        anonymized data derived from Customer Data for analytics, benchmarking, and service improvement. 
        <b><font color="red">AUDIT NOTE: Broad license grants Provider rights to use Customer Data for 
        analytics and benchmarking. "Anonymized" data may still contain sensitive business information.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>3.2 Security.</b> Provider shall implement reasonable administrative, physical, and technical 
        safeguards to protect Customer Data. However, Provider does not guarantee that unauthorized access 
        will never occur. Customer is responsible for: (a) configuring security settings; (b) managing access 
        credentials; (c) encrypting sensitive data; and (d) maintaining backups. <b><font color="red">
        AUDIT NOTE: "Reasonable" security is vague and unenforceable. Provider disclaims responsibility for 
        unauthorized access. Customer bears significant security responsibilities typically handled by provider 
        in enterprise agreements.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>3.3 Data Location and Compliance.</b> Customer Data may be stored and processed in any country 
        where Provider maintains facilities. Provider makes no representations regarding compliance with 
        data localization requirements or industry-specific regulations (e.g., HIPAA, PCI-DSS, GDPR). 
        Customer is solely responsible for ensuring its use of Services complies with applicable laws. 
        <b><font color="red">AUDIT NOTE: No data residency guarantees. Provider disclaims compliance 
        responsibilities, placing regulatory risk entirely on Customer. This may violate data sovereignty 
        requirements in certain jurisdictions.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 4: Term and Termination
        Story.append(Paragraph("<b>ARTICLE 4: TERM AND TERMINATION</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>4.1 Term.</b> This Agreement shall commence on the Effective Date and continue for an initial 
        term of three (3) years. The Agreement shall automatically renew for successive one-year periods 
        unless either party provides notice of non-renewal at least one hundred twenty (120) days prior 
        to expiration.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>4.2 Termination and Data Retrieval.</b> Upon termination, Customer shall have thirty (30) days 
        to retrieve Customer Data, after which Provider may permanently delete all Customer Data. Data 
        retrieval services are available for a fee of $0.15 per GB. Provider is not obligated to provide 
        data in any particular format. <b><font color="red">AUDIT NOTE: Short 30-day data retrieval window. 
        Additional fees for data extraction. No guarantee of data format compatibility, potentially making 
        migration difficult.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 5: Warranties and Disclaimers
        Story.append(Paragraph("<b>ARTICLE 5: WARRANTIES AND DISCLAIMERS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>5.1 LIMITED WARRANTY.</b> PROVIDER WARRANTS THAT SERVICES WILL PERFORM SUBSTANTIALLY AS DESCRIBED 
        IN THE DOCUMENTATION. EXCEPT AS EXPRESSLY PROVIDED, SERVICES ARE PROVIDED "AS IS" WITHOUT WARRANTIES 
        OF ANY KIND. PROVIDER DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS 
        FOR PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 6: Limitation of Liability
        Story.append(Paragraph("<b>ARTICLE 6: LIMITATION OF LIABILITY</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>6.1 LIABILITY CAP.</b> PROVIDER'S TOTAL LIABILITY SHALL NOT EXCEED THE LESSER OF (I) TWO HUNDRED 
        THOUSAND DOLLARS ($200,000) OR (II) FEES PAID IN THE THREE (3) MONTHS PRECEDING THE CLAIM. 
        <b><font color="red">AUDIT NOTE: Liability cap of $200,000 is inadequate for estimated annual spend 
        of ${value:,} (only {(200000/value*100):.1f}%). Data loss or extended outages could result in damages 
        far exceeding this cap.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 20))
        
        # Signatures
        Story.append(Paragraph("<b>IN WITNESS WHEREOF</b>", self.styles['Heading2']))
        Story.append(Spacer(1, 12))
        Story.append(self._create_signature_table(vendor))
        
        doc.build(Story)
        return 10
    
    def generate_hardware_purchase(self, filename, config):
        """Generate verbose Hardware Purchase Agreement"""
        return self._generate_standard_contract(filename, config, "HARDWARE PURCHASE AGREEMENT", "HPA", 
                                                "hardware equipment and related services", 9)
    
    def generate_master_service(self, filename, config):
        """Generate verbose Master Service Agreement"""
        return self._generate_standard_contract(filename, config, "MASTER SERVICE AGREEMENT", "MSA", 
                                                "various services as specified in Statements of Work", 11)
    
    def generate_consulting(self, filename, config):
        """Generate Consulting Agreement (similar to Professional Services)"""
        return self.generate_professional_services(filename, config)
    
    def generate_distribution(self, filename, config):
        """Generate Distribution Agreement"""
        return self._generate_standard_contract(filename, config, "DISTRIBUTION AGREEMENT", "DA", 
                                                "product distribution and resale services", 8)
    
    def generate_maintenance(self, filename, config):
        """Generate Maintenance Agreement"""
        return self._generate_standard_contract(filename, config, "MAINTENANCE AGREEMENT", "MA", 
                                                "maintenance and support services", 7)
    
    def generate_joint_venture(self, filename, config):
        """Generate Joint Venture Agreement"""
        return self._generate_standard_contract(filename, config, "JOINT VENTURE AGREEMENT", "JVA", 
                                                "joint venture activities and shared resources", 9)
    
    def generate_strategic_alliance(self, filename, config):
        """Generate Strategic Alliance Agreement"""
        return self._generate_standard_contract(filename, config, "STRATEGIC ALLIANCE AGREEMENT", "SAA", 
                                                "strategic partnership and collaboration", 8)
    
    def _generate_standard_contract(self, filename, config, title, abbrev, service_desc, issues_count):
        """Generate a standard verbose contract template"""
        doc = SimpleDocTemplate(filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        Story = []
        Story.append(Paragraph(title, self.title_style))
        Story.append(Spacer(1, 12))
        
        vendor = config.get('vendor_name', f'{abbrev} Vendor Solutions Inc.')
        value = config.get('value', random.randint(400000, 900000))
        
        Story.append(Paragraph(f"<b>Contract Number:</b> {abbrev}-{datetime.now().strftime('%Y')}-{random.randint(100,999)}", self.styles['Normal']))
        Story.append(Paragraph(f"<b>Effective Date:</b> {datetime.now().strftime('%B %d, %Y')}", self.styles['Normal']))
        Story.append(Spacer(1, 20))
        
        # Parties
        Story.append(Paragraph("<b>PARTIES</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        This Agreement is entered into between <b>{vendor}</b> ("Vendor"), a Delaware corporation 
        with principal offices at {random.randint(100,9999)} Commerce Street, Suite {random.randint(100,999)}, 
        and <b>Global Finance Corp.</b> ("Client"), a New York corporation with principal offices at 
        {random.randint(100,999)} Wall Street, New York, NY {random.randint(10001,10099)}.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Recitals
        Story.append(Paragraph("<b>RECITALS</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>WHEREAS,</b> Vendor is engaged in the business of providing {service_desc}; and
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        Story.append(Paragraph(f"""
        <b>WHEREAS,</b> Client desires to engage Vendor to provide {service_desc} in accordance with 
        the terms and conditions set forth herein;
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        Story.append(Paragraph("""
        <b>NOW, THEREFORE,</b> in consideration of the mutual covenants and agreements herein contained, 
        the parties agree as follows:
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 1: Scope
        Story.append(Paragraph("<b>ARTICLE 1: SCOPE OF SERVICES</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>1.1 Services.</b> Vendor shall provide {service_desc} as more particularly described in 
        the attached Exhibits and Statements of Work. All services shall be performed in accordance with 
        industry standards and applicable laws and regulations. Vendor reserves the right to use subcontractors 
        without prior notice to Client. <b><font color="red">AUDIT NOTE: Vague scope definition. Unlimited 
        subcontracting rights without Client approval may impact quality and security.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>1.2 Changes to Scope.</b> Any changes to the scope of services must be requested in writing. 
        Vendor shall provide a quote for such changes within fifteen (15) business days. Vendor may adjust 
        timelines and fees for any scope changes. Client's continued acceptance of services after scope 
        changes constitutes acceptance of revised fees and timelines. <b><font color="red">AUDIT NOTE: 
        Implied acceptance through continued use. No requirement for explicit Client approval of revised fees.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 2: Fees
        Story.append(Paragraph("<b>ARTICLE 2: FEES AND PAYMENT TERMS</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>2.1 Contract Value.</b> The total estimated contract value is ${value:,}, payable according to 
        the payment schedule set forth in Exhibit B. All fees are non-refundable once services have commenced. 
        Vendor may invoice for services in advance of performance. <b><font color="red">AUDIT NOTE: Non-refundable 
        fees even if services are not satisfactorily performed. Advance invoicing creates cash flow risk for Client.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>2.2 Additional Fees.</b> Client shall pay additional fees for: (a) services outside the defined scope; 
        (b) expedited delivery requests; (c) after-hours support; (d) travel and expenses; and (e) any third-party 
        costs incurred by Vendor. Vendor may charge a markup of up to twenty percent (20%) on third-party costs. 
        <b><font color="red">AUDIT NOTE: 20% markup on third-party costs is excessive (typical is 5-10%). No cap 
        on additional fees or requirement for pre-approval.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>2.3 Price Adjustments.</b> Vendor may adjust prices annually based on changes in Vendor's costs, 
        market conditions, or the Consumer Price Index, whichever results in the greater increase. Price 
        adjustments shall not exceed twelve percent (12%) in any twelve-month period. <b><font color="red">
        AUDIT NOTE: Unilateral right to increase prices by up to 12% annually. This is significantly above 
        typical inflation rates and market norms (3-5%).</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>2.4 Late Payment.</b> Invoices are due within twenty (20) days of invoice date. Late payments 
        shall accrue interest at 1.5% per month (18% annually). Vendor may suspend services if payment is 
        more than ten (10) days overdue and may terminate this Agreement if payment is more than thirty (30) 
        days overdue. <b><font color="red">AUDIT NOTE: High interest rate on late payments. Service suspension 
        after only 10 days could disrupt business operations.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 3: Term and Termination
        Story.append(Paragraph("<b>ARTICLE 3: TERM AND TERMINATION</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>3.1 Term.</b> This Agreement shall commence on the Effective Date and continue for an initial 
        term of three (3) years, automatically renewing for successive two-year periods unless either party 
        provides written notice of non-renewal at least one hundred eighty (180) days prior to the end of 
        the then-current term. <b><font color="red">AUDIT NOTE: Long initial term with auto-renewal and 
        extended notice period. 180-day notice requirement may be difficult to track and could result in 
        unintended renewals.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph(f"""
        <b>3.2 Termination for Convenience.</b> Client may terminate this Agreement for convenience upon 
        one hundred twenty (120) days prior written notice and payment of an early termination fee equal to 
        forty percent (40%) of the remaining contract value. Vendor may terminate for convenience upon sixty 
        (60) days notice without penalty. <b><font color="red">AUDIT NOTE: Asymmetric termination rights. 
        Client faces 40% penalty (potentially ${int(value*0.4):,}) while Vendor can exit without penalty. 
        This creates significant vendor lock-in.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>3.3 Effect of Termination.</b> Upon termination: (a) Client shall pay all fees through the 
        termination date plus any early termination fees; (b) Client shall return all Vendor materials; 
        (c) all licenses granted to Client shall immediately terminate; and (d) Vendor shall have no obligation 
        to provide transition assistance. Any data or materials held by Vendor will be deleted thirty (30) days 
        after termination unless Client pays for extended retention at Vendor's standard rates. <b><font color="red">
        AUDIT NOTE: No transition assistance provided. Short data retention period may not allow sufficient 
        time for migration. Additional fees for data retention.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 4: Intellectual Property
        Story.append(Paragraph("<b>ARTICLE 4: INTELLECTUAL PROPERTY</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>4.1 Ownership.</b> All work product, deliverables, and intellectual property created under this 
        Agreement shall be owned by Vendor. Client is granted a limited, non-exclusive, non-transferable 
        license to use such work product solely for its internal business purposes. This license does not 
        include the right to modify, create derivatives, or sublicense. <b><font color="red">AUDIT NOTE: 
        Vendor retains ownership of work product paid for by Client. Restrictive license terms limit Client's 
        ability to adapt or extend the work product.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>4.2 Vendor Materials.</b> Vendor retains all rights to pre-existing materials, methodologies, 
        tools, and processes used in providing services. Client acquires no rights to such materials except 
        as expressly licensed herein.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 5: Warranties and Disclaimers
        Story.append(Paragraph("<b>ARTICLE 5: WARRANTIES AND DISCLAIMERS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>5.1 Limited Warranty.</b> Vendor warrants that services will be performed in a professional manner. 
        This warranty is valid for thirty (30) days from delivery. Vendor's sole obligation for breach of 
        warranty is to re-perform defective services or refund fees paid for such services, at Vendor's option. 
        <b><font color="red">AUDIT NOTE: Very limited 30-day warranty period. Vendor controls remedy (re-performance 
        vs. refund), potentially forcing Client to accept re-performance even if relationship has deteriorated.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>5.2 DISCLAIMER.</b> EXCEPT AS EXPRESSLY PROVIDED ABOVE, VENDOR MAKES NO WARRANTIES, EXPRESS OR 
        IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR PARTICULAR PURPOSE, OR NON-INFRINGEMENT. 
        VENDOR DOES NOT WARRANT THAT SERVICES WILL MEET CLIENT'S REQUIREMENTS OR ACHIEVE ANY PARTICULAR RESULTS.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 6: Limitation of Liability
        Story.append(Paragraph("<b>ARTICLE 6: LIMITATION OF LIABILITY</b>", self.styles['Heading2']))
        Story.append(Paragraph(f"""
        <b>6.1 LIABILITY CAP.</b> VENDOR'S TOTAL AGGREGATE LIABILITY SHALL NOT EXCEED THE LESSER OF 
        (I) ONE HUNDRED FIFTY THOUSAND DOLLARS ($150,000) OR (II) THE FEES PAID IN THE SIX (6) MONTHS 
        IMMEDIATELY PRECEDING THE CLAIM. <b><font color="red">AUDIT NOTE: Liability cap of $150,000 is 
        inadequate for contract value of ${value:,} (only {(150000/value*100):.1f}%). Leaves Client exposed 
        to significant unrecoverable losses.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>6.2 EXCLUSION OF DAMAGES.</b> IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR INDIRECT, INCIDENTAL, 
        SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING LOST PROFITS, LOST DATA, OR BUSINESS INTERRUPTION, 
        EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 7: Confidentiality
        Story.append(Paragraph("<b>ARTICLE 7: CONFIDENTIAL INFORMATION</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>7.1 Obligations.</b> Each party agrees to protect the other's Confidential Information using 
        the same degree of care it uses for its own confidential information, but in no event less than 
        reasonable care. These obligations shall survive for five (5) years after termination of this Agreement.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>7.2 Permitted Disclosures.</b> Vendor may disclose Client's Confidential Information to its 
        subcontractors, affiliates, and professional advisors as necessary to perform services. Vendor may 
        also use Client's name and general project description in marketing materials and client lists unless 
        Client objects in writing. <b><font color="red">AUDIT NOTE: Broad disclosure rights to subcontractors 
        without confidentiality flow-down requirements. Marketing use of Client's name may not be acceptable 
        for confidential projects.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        
        # Article 8: General Provisions
        Story.append(Paragraph("<b>ARTICLE 8: GENERAL PROVISIONS</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        <b>8.1 Entire Agreement.</b> This Agreement, including all Exhibits and Statements of Work, constitutes 
        the entire agreement between the parties and supersedes all prior agreements, understandings, and 
        communications relating to the subject matter hereof.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>8.2 Amendments.</b> This Agreement may be amended only by written instrument signed by both parties. 
        However, Vendor may amend Exhibits and Statements of Work upon thirty (30) days written notice, and 
        Client's continued use of services constitutes acceptance of such amendments. <b><font color="red">
        AUDIT NOTE: Vendor can unilaterally amend key terms through Exhibit modifications. Implied acceptance 
        through continued use bypasses formal approval process.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>8.3 Governing Law and Venue.</b> This Agreement shall be governed by the laws of the State of 
        Delaware without regard to conflict of laws principles. Any disputes shall be resolved exclusively 
        in the state or federal courts located in Wilmington, Delaware. Client consents to personal jurisdiction 
        in such courts and waives any objection to venue.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>8.4 Assignment.</b> Client may not assign this Agreement without Vendor's prior written consent. 
        Vendor may freely assign this Agreement to any affiliate or in connection with a merger, acquisition, 
        or sale of assets. <b><font color="red">AUDIT NOTE: Asymmetric assignment rights. Vendor can assign 
        to potentially unknown entities while Client cannot assign even to its own subsidiaries.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 6))
        
        Story.append(Paragraph("""
        <b>8.5 Force Majeure.</b> Neither party shall be liable for delays or failures in performance resulting 
        from causes beyond its reasonable control. However, Client's payment obligations are not excused by 
        force majeure events. <b><font color="red">AUDIT NOTE: Asymmetric force majeure clause. Vendor's 
        performance obligations are excused but Client must continue paying even during extended service outages.</font></b>
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 20))
        
        # Signatures
        Story.append(Paragraph("<b>IN WITNESS WHEREOF</b>", self.styles['Heading2']))
        Story.append(Paragraph("""
        The parties have executed this Agreement as of the date first written above.
        """, self.styles['BodyText']))
        Story.append(Spacer(1, 12))
        Story.append(self._create_signature_table(vendor))
        
        doc.build(Story)
        return issues_count

