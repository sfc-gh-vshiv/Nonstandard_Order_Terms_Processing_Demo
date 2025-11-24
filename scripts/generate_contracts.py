#!/usr/bin/env python3
"""
Generate dummy contract documents in PDF format for document processing demo.
These contracts contain various non-standard terms that an audit team would need to review.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime, timedelta
import random

def create_contract_1():
    """Software License Agreement with unusual payment terms and liability caps"""
    filename = "../contracts/contract_001_software_license.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    Story.append(Paragraph("SOFTWARE LICENSE AGREEMENT", title_style))
    Story.append(Spacer(1, 12))
    
    # Contract metadata
    meta_style = styles['Normal']
    Story.append(Paragraph(f"<b>Contract Number:</b> SLA-2024-001", meta_style))
    Story.append(Paragraph(f"<b>Effective Date:</b> January 15, 2024", meta_style))
    Story.append(Paragraph(f"<b>Expiration Date:</b> January 14, 2027", meta_style))
    Story.append(Spacer(1, 20))
    
    # Parties
    Story.append(Paragraph("<b>PARTIES</b>", styles['Heading2']))
    Story.append(Paragraph("""
    This Software License Agreement ("Agreement") is entered into between <b>TechVendor Solutions Inc.</b> 
    ("Licensor"), a Delaware corporation with principal offices at 123 Innovation Drive, San Francisco, CA 94105, 
    and <b>Global Finance Corp.</b> ("Licensee"), a New York corporation with principal offices at 
    456 Wall Street, New York, NY 10005.
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Non-standard payment terms
    Story.append(Paragraph("<b>ARTICLE 1: PAYMENT TERMS</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>1.1 Base License Fee:</b> Licensee shall pay an annual license fee of $850,000, payable in quarterly 
    installments of $212,500. <b><font color="red">AUDIT NOTE: First payment due within 15 days of contract 
    execution (non-standard - typically 30 days).</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>1.2 Variable Usage Fees:</b> In addition to the base fee, Licensee shall pay usage fees calculated as 
    follows: $0.15 per transaction for the first 1,000,000 transactions per month, $0.10 per transaction for 
    transactions 1,000,001 to 5,000,000, and $0.05 per transaction thereafter. <b><font color="red">AUDIT NOTE: 
    Usage fees are uncapped and could result in significant cost overruns.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>1.3 Automatic Price Escalation:</b> The license fee shall automatically increase by the greater of 
    (a) 8% annually or (b) the Consumer Price Index plus 3%. <b><font color="red">AUDIT NOTE: Escalation clause 
    is above market rate (typical 3-5%).</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Liability provisions
    Story.append(Paragraph("<b>ARTICLE 2: LIABILITY AND INDEMNIFICATION</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>2.1 Limitation of Liability:</b> Licensor's total liability under this Agreement shall not exceed 
    the lesser of (i) $50,000 or (ii) the fees paid by Licensee in the three months preceding the claim. 
    <b><font color="red">AUDIT NOTE: Liability cap is significantly lower than annual contract value 
    ($850,000) - only 5.9% of annual fees.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>2.2 Licensee Indemnification:</b> Licensee shall indemnify, defend, and hold harmless Licensor from 
    any claims arising from Licensee's use of the Software, including but not limited to data breaches, 
    regulatory violations, and third-party claims. This indemnification obligation survives termination of 
    this Agreement for a period of seven (7) years. <b><font color="red">AUDIT NOTE: Unlimited indemnification 
    obligation with extended survival period.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Termination
    Story.append(Paragraph("<b>ARTICLE 3: TERMINATION</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>3.1 Termination for Convenience:</b> Licensor may terminate this Agreement for any reason upon 
    30 days written notice. Licensee may terminate only upon 180 days written notice and payment of a 
    termination fee equal to 50% of the remaining contract value. <b><font color="red">AUDIT NOTE: 
    Asymmetric termination rights with substantial early termination penalty.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>3.2 Data Retention:</b> Upon termination, Licensor shall retain Licensee's data for 90 days, after 
    which all data will be permanently deleted. Data extraction services are available for a fee of $25,000. 
    <b><font color="red">AUDIT NOTE: Short data retention period with additional extraction fees.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Renewal
    Story.append(Paragraph("<b>ARTICLE 4: RENEWAL</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>4.1 Automatic Renewal:</b> This Agreement shall automatically renew for successive three-year terms 
    unless either party provides written notice of non-renewal at least 180 days prior to the end of the 
    then-current term. <b><font color="red">AUDIT NOTE: Auto-renewal with extended notice period 
    (typical is 60-90 days).</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 20))
    
    # Signatures
    Story.append(Paragraph("<b>SIGNATURES</b>", styles['Heading2']))
    Story.append(Spacer(1, 12))
    
    sig_data = [
        ['LICENSOR: TechVendor Solutions Inc.', 'LICENSEE: Global Finance Corp.'],
        ['', ''],
        ['_________________________________', '_________________________________'],
        ['Sarah Mitchell, CEO', 'Robert Chen, CFO'],
        ['Date: January 15, 2024', 'Date: January 15, 2024']
    ]
    
    sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    Story.append(sig_table)
    
    doc.build(Story)
    print(f"✓ Generated {filename}")

def create_contract_2():
    """Consulting Services Agreement with unusual IP and payment terms"""
    filename = "../contracts/contract_002_consulting_services.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    Story.append(Paragraph("PROFESSIONAL SERVICES AGREEMENT", title_style))
    Story.append(Spacer(1, 12))
    
    Story.append(Paragraph(f"<b>Contract Number:</b> PSA-2024-042", styles['Normal']))
    Story.append(Paragraph(f"<b>Effective Date:</b> March 1, 2024", styles['Normal']))
    Story.append(Paragraph(f"<b>Term:</b> 18 months", styles['Normal']))
    Story.append(Spacer(1, 20))
    
    Story.append(Paragraph("<b>PARTIES</b>", styles['Heading2']))
    Story.append(Paragraph("""
    This Professional Services Agreement is between <b>Apex Consulting Group LLC</b> ("Consultant") 
    and <b>Global Finance Corp.</b> ("Client").
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Scope and fees
    Story.append(Paragraph("<b>ARTICLE 1: SCOPE AND FEES</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>1.1 Services:</b> Consultant shall provide financial systems implementation and advisory services 
    as detailed in Exhibit A.
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>1.2 Fee Structure:</b> Client shall pay Consultant as follows:
    <br/>• Senior Partner: $650/hour
    <br/>• Manager: $425/hour  
    <br/>• Senior Consultant: $325/hour
    <br/>• Consultant: $225/hour
    <br/><br/><b><font color="red">AUDIT NOTE: No cap on total hours or monthly billing. Rates are 
    15-20% above market average.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>1.3 Expenses:</b> Client shall reimburse all expenses without markup, including travel, meals, 
    lodging, and incidentals. Business class air travel is authorized for flights over 3 hours. 
    <b><font color="red">AUDIT NOTE: No expense caps or approval requirements specified.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>1.4 Success Fee:</b> Upon successful go-live of the system implementation, Client shall pay 
    Consultant a success fee equal to 15% of all fees paid during the engagement. <b><font color="red">
    AUDIT NOTE: Success fee could add $200K+ to total cost. Definition of 'successful go-live' is vague.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # IP provisions
    Story.append(Paragraph("<b>ARTICLE 2: INTELLECTUAL PROPERTY</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>2.1 Work Product:</b> All methodologies, frameworks, tools, templates, and know-how used or 
    developed during this engagement shall remain the exclusive property of Consultant. Client receives 
    a non-exclusive, non-transferable license to use deliverables solely for its internal business purposes. 
    <b><font color="red">AUDIT NOTE: Client does not own work product despite paying for development. 
    License restrictions may limit future use.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>2.2 Residual Knowledge:</b> Consultant may freely use any residual knowledge, skills, or experience 
    gained during this engagement, including for competing clients. <b><font color="red">AUDIT NOTE: 
    Consultant can use insights gained from Client's confidential information for competitors.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Payment terms
    Story.append(Paragraph("<b>ARTICLE 3: PAYMENT TERMS</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>3.1 Invoicing:</b> Consultant shall invoice Client bi-weekly. Payment is due within 10 business days 
    of invoice date. <b><font color="red">AUDIT NOTE: Accelerated payment terms (typical is 30 days).</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>3.2 Late Fees:</b> Overdue amounts shall accrue interest at 2% per month (24% APR). Additionally, 
    Consultant may suspend services if payment is more than 5 days overdue. <b><font color="red">AUDIT NOTE: 
    High late fee rate and aggressive suspension clause.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>3.3 Disputed Invoices:</b> Client must pay all undisputed amounts and may only withhold amounts 
    specifically identified as disputed in writing within 5 days of invoice receipt. <b><font color="red">
    AUDIT NOTE: Short dispute window may not allow adequate time for invoice review.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Warranties
    Story.append(Paragraph("<b>ARTICLE 4: WARRANTIES AND DISCLAIMERS</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>4.1 Limited Warranty:</b> Consultant warrants that services will be performed in a professional manner. 
    EXCEPT AS EXPRESSLY PROVIDED HEREIN, CONSULTANT MAKES NO WARRANTIES, EXPRESS OR IMPLIED, INCLUDING 
    WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. <b><font color="red">AUDIT NOTE: 
    Minimal warranty protection. No guarantee of results or outcomes.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 20))
    
    # Signatures
    Story.append(Paragraph("<b>SIGNATURES</b>", styles['Heading2']))
    Story.append(Spacer(1, 12))
    
    sig_data = [
        ['CONSULTANT: Apex Consulting Group LLC', 'CLIENT: Global Finance Corp.'],
        ['', ''],
        ['_________________________________', '_________________________________'],
        ['David Thompson, Managing Partner', 'Jennifer Martinez, VP Procurement'],
        ['Date: March 1, 2024', 'Date: March 1, 2024']
    ]
    
    sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    Story.append(sig_table)
    
    doc.build(Story)
    print(f"✓ Generated {filename}")

def create_contract_3():
    """Cloud Services Agreement with data sovereignty and SLA issues"""
    filename = "../contracts/contract_003_cloud_services.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    Story.append(Paragraph("CLOUD SERVICES AGREEMENT", title_style))
    Story.append(Spacer(1, 12))
    
    Story.append(Paragraph(f"<b>Contract Number:</b> CSA-2024-089", styles['Normal']))
    Story.append(Paragraph(f"<b>Effective Date:</b> February 1, 2024", styles['Normal']))
    Story.append(Paragraph(f"<b>Initial Term:</b> 5 years", styles['Normal']))
    Story.append(Spacer(1, 20))
    
    Story.append(Paragraph("<b>PARTIES</b>", styles['Heading2']))
    Story.append(Paragraph("""
    This Cloud Services Agreement is between <b>CloudScale Technologies Inc.</b> ("Provider") 
    and <b>Global Finance Corp.</b> ("Customer").
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Service levels
    Story.append(Paragraph("<b>ARTICLE 1: SERVICE LEVELS</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>1.1 Availability Commitment:</b> Provider commits to 99.5% uptime availability, measured monthly. 
    <b><font color="red">AUDIT NOTE: 99.5% allows for 3.6 hours of downtime per month - below industry 
    standard of 99.9% for financial services.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>1.2 Service Credits:</b> If availability falls below 99.5%, Customer shall receive service credits 
    as follows:
    <br/>• 99.0% - 99.49%: 5% credit
    <br/>• 98.0% - 98.99%: 10% credit  
    <br/>• Below 98.0%: 15% credit
    <br/><br/><b><font color="red">AUDIT NOTE: Maximum credit is only 15% of monthly fees. No right to 
    terminate for poor performance. Credits are Customer's sole remedy.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>1.3 Planned Maintenance:</b> Provider may perform maintenance during business hours with 24 hours 
    notice. Planned maintenance windows do not count against availability commitments. <b><font color="red">
    AUDIT NOTE: Maintenance during business hours could disrupt operations. No limit on frequency or duration.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Data provisions
    Story.append(Paragraph("<b>ARTICLE 2: DATA LOCATION AND SECURITY</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>2.1 Data Storage:</b> Customer data will be stored in Provider's global data center network. 
    Provider reserves the right to move data between facilities for load balancing, disaster recovery, 
    or operational efficiency. <b><font color="red">AUDIT NOTE: No guarantee of data location. May violate 
    data sovereignty requirements for EU/UK customers.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>2.2 Data Access:</b> Provider personnel may access Customer data for troubleshooting, maintenance, 
    and service improvement purposes. Provider may use anonymized data for analytics and product development. 
    <b><font color="red">AUDIT NOTE: Broad data access rights. 'Anonymized' data may still contain sensitive 
    business information.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>2.3 Security Audits:</b> Provider maintains SOC 2 Type II certification. Customer may request audit 
    reports annually. On-site audits require 90 days notice and Provider approval, subject to a fee of 
    $50,000 per audit. <b><font color="red">AUDIT NOTE: Limited audit rights with significant fees. 
    No right to conduct security assessments without Provider approval.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Pricing
    Story.append(Paragraph("<b>ARTICLE 3: PRICING AND PAYMENT</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>3.1 Base Subscription:</b> Customer shall pay $45,000 per month for the base platform subscription 
    (up to 500 users and 10TB storage).
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>3.2 Overage Charges:</b> 
    <br/>• Additional users: $95/user/month
    <br/>• Additional storage: $150/TB/month
    <br/>• API calls over 10M/month: $0.002 per call
    <br/>• Data egress: $0.12/GB
    <br/><br/><b><font color="red">AUDIT NOTE: Overage charges are significantly higher than base rates. 
    No caps or alerts configured. Data egress fees could be substantial.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>3.3 Price Changes:</b> Provider may increase prices upon 60 days notice. If Customer does not 
    accept the increase, Customer may terminate with 30 days notice, but must pay an early termination 
    fee equal to 6 months of the then-current monthly fees. <b><font color="red">AUDIT NOTE: Provider 
    can force price increases with termination penalty as only alternative.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Termination
    Story.append(Paragraph("<b>ARTICLE 4: TERM AND TERMINATION</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>4.1 Initial Term:</b> The initial term is five (5) years. This Agreement automatically renews for 
    successive two-year terms unless Customer provides written notice of non-renewal at least 12 months 
    prior to the end of the then-current term. <b><font color="red">AUDIT NOTE: Very long initial commitment 
    with extended renewal notice period.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>4.2 Early Termination:</b> Customer may terminate early only for Provider's material breach that 
    remains uncured for 90 days after written notice. Customer must pay all remaining fees through the end 
    of the then-current term. <b><font color="red">AUDIT NOTE: Customer must pay for full term even if 
    terminating for cause. Extended cure period.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>4.3 Data Portability:</b> Upon termination, Provider will make Customer data available for download 
    for 30 days. Data export is provided in Provider's standard format only. Conversion to other formats 
    available for additional fee. <b><font color="red">AUDIT NOTE: Short data retrieval window. May require 
    additional fees for usable data format.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 20))
    
    # Signatures
    Story.append(Paragraph("<b>SIGNATURES</b>", styles['Heading2']))
    Story.append(Spacer(1, 12))
    
    sig_data = [
        ['PROVIDER: CloudScale Technologies Inc.', 'CUSTOMER: Global Finance Corp.'],
        ['', ''],
        ['_________________________________', '_________________________________'],
        ['Michael Roberts, SVP Sales', 'Patricia Wong, CIO'],
        ['Date: February 1, 2024', 'Date: February 1, 2024']
    ]
    
    sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    Story.append(sig_table)
    
    doc.build(Story)
    print(f"✓ Generated {filename}")

def create_contract_4():
    """Vendor Agreement with unusual warranty and support terms"""
    filename = "../contracts/contract_004_equipment_purchase.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    Story.append(Paragraph("HARDWARE PURCHASE AND MAINTENANCE AGREEMENT", title_style))
    Story.append(Spacer(1, 12))
    
    Story.append(Paragraph(f"<b>Contract Number:</b> HW-2024-156", styles['Normal']))
    Story.append(Paragraph(f"<b>Purchase Order:</b> PO-24-8892", styles['Normal']))
    Story.append(Paragraph(f"<b>Date:</b> April 10, 2024", styles['Normal']))
    Story.append(Spacer(1, 20))
    
    Story.append(Paragraph("<b>PARTIES</b>", styles['Heading2']))
    Story.append(Paragraph("""
    This Agreement is between <b>DataCenter Equipment Solutions LLC</b> ("Vendor") 
    and <b>Global Finance Corp.</b> ("Buyer").
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Equipment and pricing
    Story.append(Paragraph("<b>ARTICLE 1: EQUIPMENT AND PRICING</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>1.1 Equipment:</b> Vendor shall provide the following:
    <br/>• 50x High-Performance Servers (Model: DCS-9000X)
    <br/>• 10x Network Switches (Model: NS-5000)  
    <br/>• 5x Storage Arrays (Model: SA-10000, 500TB each)
    <br/>• Installation and configuration services
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>1.2 Purchase Price:</b> Total purchase price is $2,850,000, payable as follows:
    <br/>• 40% ($1,140,000) upon contract execution
    <br/>• 40% ($1,140,000) upon delivery
    <br/>• 20% ($570,000) upon acceptance
    <br/><br/><b><font color="red">AUDIT NOTE: Large upfront payment before delivery. No provision for 
    payment withholding if equipment is defective.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Warranty
    Story.append(Paragraph("<b>ARTICLE 2: WARRANTY</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>2.1 Limited Warranty:</b> Vendor warrants that equipment will be free from defects in materials 
    and workmanship for 90 days from delivery. This warranty does not cover:
    <br/>• Normal wear and tear
    <br/>• Damage from improper use or unauthorized modifications
    <br/>• Environmental factors (temperature, humidity, power fluctuations)
    <br/>• Software or firmware issues
    <br/>• Components not manufactured by Vendor
    <br/><br/><b><font color="red">AUDIT NOTE: Only 90-day warranty on $2.85M purchase (industry standard 
    is 1-3 years). Extensive exclusions may void warranty for common issues.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>2.2 Warranty Remedy:</b> Vendor's sole obligation under warranty is to repair or replace defective 
    components, at Vendor's discretion. Replacement components may be new or refurbished. <b><font color="red">
    AUDIT NOTE: No refund option. Vendor may provide refurbished parts for new equipment.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>2.3 Warranty Claims:</b> Buyer must report defects within 5 business days of discovery. Vendor 
    shall have 30 days to investigate claims. Buyer must provide remote access to equipment for diagnostics. 
    <b><font color="red">AUDIT NOTE: Short reporting window. Vendor has extended investigation period.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Maintenance
    Story.append(Paragraph("<b>ARTICLE 3: MAINTENANCE AND SUPPORT</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>3.1 Maintenance Agreement:</b> After warranty expiration, Buyer must purchase annual maintenance 
    at 22% of the original purchase price ($627,000/year). Maintenance fees increase by 10% annually. 
    <b><font color="red">AUDIT NOTE: Mandatory maintenance at 22% of purchase price is above market rate 
    (typical 15-18%). Steep annual increases.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>3.2 Support Terms:</b> Maintenance includes:
    <br/>• 8x5 phone support (business hours only)
    <br/>• 4-hour response time for critical issues
    <br/>• Next business day parts replacement
    <br/>• 2 on-site visits per year
    <br/><br/><b><font color="red">AUDIT NOTE: No 24x7 support for critical financial systems. 
    Response time is not resolution time. Limited on-site support.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>3.3 Mandatory Upgrades:</b> Vendor may require firmware or software upgrades as a condition of 
    continued support. Upgrades must be installed within 30 days of release. Failure to upgrade may void 
    support obligations. <b><font color="red">AUDIT NOTE: Forced upgrades could cause compatibility issues. 
    Short installation window may not allow adequate testing.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Acceptance
    Story.append(Paragraph("<b>ARTICLE 4: DELIVERY AND ACCEPTANCE</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>4.1 Delivery:</b> Vendor shall deliver equipment within 90-120 days of contract execution. Delivery 
    dates are estimates only and not guaranteed. <b><font color="red">AUDIT NOTE: No firm delivery commitment. 
    No penalty for late delivery.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>4.2 Acceptance Testing:</b> Buyer has 10 business days from installation to conduct acceptance testing. 
    If Buyer does not provide written rejection within this period, equipment is deemed accepted. Rejection 
    must include detailed test results demonstrating failure to meet specifications. <b><font color="red">
    AUDIT NOTE: Short acceptance window for complex equipment. Automatic acceptance if deadline missed.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>4.3 Risk of Loss:</b> Risk of loss transfers to Buyer upon delivery to Buyer's loading dock, regardless 
    of installation status. <b><font color="red">AUDIT NOTE: Buyer bears risk before equipment is installed 
    or tested.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Limitation of liability
    Story.append(Paragraph("<b>ARTICLE 5: LIMITATION OF LIABILITY</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>5.1 Liability Cap:</b> Vendor's total liability shall not exceed the purchase price paid for the 
    specific defective equipment unit, not to exceed $100,000 in aggregate. <b><font color="red">AUDIT NOTE: 
    Liability capped at $100K for $2.85M purchase. No coverage for consequential damages or business interruption.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 20))
    
    # Signatures
    Story.append(Paragraph("<b>SIGNATURES</b>", styles['Heading2']))
    Story.append(Spacer(1, 12))
    
    sig_data = [
        ['VENDOR: DataCenter Equipment Solutions LLC', 'BUYER: Global Finance Corp.'],
        ['', ''],
        ['_________________________________', '_________________________________'],
        ['James Anderson, VP Sales', 'Kevin O\'Brien, Director of IT'],
        ['Date: April 10, 2024', 'Date: April 10, 2024']
    ]
    
    sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    Story.append(sig_table)
    
    doc.build(Story)
    print(f"✓ Generated {filename}")

def create_contract_5():
    """Master Service Agreement with problematic indemnification and insurance"""
    filename = "../contracts/contract_005_master_service_agreement.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    Story.append(Paragraph("MASTER SERVICE AGREEMENT", title_style))
    Story.append(Spacer(1, 12))
    
    Story.append(Paragraph(f"<b>Contract Number:</b> MSA-2024-033", styles['Normal']))
    Story.append(Paragraph(f"<b>Effective Date:</b> May 15, 2024", styles['Normal']))
    Story.append(Paragraph(f"<b>Term:</b> 3 years with automatic renewal", styles['Normal']))
    Story.append(Spacer(1, 20))
    
    Story.append(Paragraph("<b>PARTIES</b>", styles['Heading2']))
    Story.append(Paragraph("""
    This Master Service Agreement is between <b>SecureData Processing Inc.</b> ("Service Provider") 
    and <b>Global Finance Corp.</b> ("Client").
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Indemnification
    Story.append(Paragraph("<b>ARTICLE 1: INDEMNIFICATION</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>1.1 Client Indemnification:</b> Client shall indemnify, defend, and hold harmless Service Provider, 
    its affiliates, officers, directors, employees, and agents from and against any and all claims, damages, 
    losses, liabilities, costs, and expenses (including reasonable attorneys' fees) arising from or related to:
    <br/>• Client's use of the services
    <br/>• Client's breach of this Agreement
    <br/>• Client's violation of any law or regulation
    <br/>• Any claim that Client's data infringes third-party rights
    <br/>• Any claim by Client's employees, customers, or third parties related to the services
    <br/>• Any security breach or data loss involving Client's data
    <br/><br/><b><font color="red">AUDIT NOTE: Extremely broad indemnification. Client indemnifies for 
    security breaches even if caused by Service Provider's negligence.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>1.2 Service Provider Indemnification:</b> Service Provider shall indemnify Client only for third-party 
    claims that the services directly infringe a U.S. patent or copyright, provided that Client: (a) promptly 
    notifies Service Provider in writing, (b) grants Service Provider sole control of the defense and settlement, 
    and (c) provides reasonable cooperation at Client's expense. This indemnification does not apply if the 
    infringement arises from Client's modifications or use with non-approved systems. <b><font color="red">
    AUDIT NOTE: Asymmetric indemnification. Service Provider's obligations are narrow with many exclusions.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Insurance
    Story.append(Paragraph("<b>ARTICLE 2: INSURANCE REQUIREMENTS</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>2.1 Client Insurance:</b> Client shall maintain the following insurance coverage throughout the term:
    <br/>• Commercial General Liability: $5,000,000 per occurrence
    <br/>• Professional Liability: $10,000,000 per claim
    <br/>• Cyber Liability: $25,000,000 per incident
    <br/>• Workers' Compensation: Statutory limits
    <br/><br/>Client shall name Service Provider as an additional insured on all policies. Certificates of 
    insurance must be provided annually. <b><font color="red">AUDIT NOTE: Unusually high insurance requirements 
    for a service agreement. Client bears insurance costs to protect Service Provider.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>2.2 Service Provider Insurance:</b> Service Provider maintains standard commercial insurance. 
    Specific coverage details are confidential. <b><font color="red">AUDIT NOTE: No specific insurance 
    requirements for Service Provider. No transparency on coverage limits.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Data handling
    Story.append(Paragraph("<b>ARTICLE 3: DATA HANDLING AND SECURITY</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>3.1 Data Processing:</b> Service Provider will process Client data in accordance with its standard 
    security practices. Service Provider may use subcontractors without prior notice to Client. Service 
    Provider is not responsible for data quality, accuracy, or completeness. <b><font color="red">AUDIT NOTE: 
    Vague security commitments. Unlimited subcontracting without approval. No data quality guarantees.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>3.2 Data Breach Notification:</b> In the event of a data breach, Service Provider will notify Client 
    within 30 days of discovering the breach. Service Provider's notification obligation is limited to email 
    notice to Client's primary contact. Client is responsible for all regulatory notifications, customer 
    communications, and breach remediation costs. <b><font color="red">AUDIT NOTE: 30-day notification period 
    exceeds regulatory requirements (typically 72 hours). Client bears all breach costs even if caused by 
    Service Provider.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>3.3 Data Retention:</b> Service Provider may retain Client data indefinitely for backup, disaster 
    recovery, and legal compliance purposes. Client data may be stored in any jurisdiction where Service 
    Provider maintains facilities. <b><font color="red">AUDIT NOTE: Indefinite data retention creates ongoing 
    risk. No control over data location or deletion.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Dispute resolution
    Story.append(Paragraph("<b>ARTICLE 4: DISPUTE RESOLUTION</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>4.1 Mandatory Arbitration:</b> Any dispute arising from this Agreement shall be resolved by binding 
    arbitration administered by the American Arbitration Association in Delaware. Each party shall bear its 
    own costs and attorneys' fees. The arbitrator's decision is final and binding with no right of appeal. 
    <b><font color="red">AUDIT NOTE: Mandatory arbitration in Service Provider's home state. No right to 
    appeal even if arbitrator makes legal errors.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>4.2 Class Action Waiver:</b> Client waives any right to bring or participate in any class action, 
    collective action, or representative proceeding against Service Provider. <b><font color="red">AUDIT NOTE: 
    Eliminates ability to join with other affected clients in disputes.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>4.3 Confidential Proceedings:</b> All arbitration proceedings and results shall be confidential. 
    Client may not disclose the existence or outcome of any dispute without Service Provider's prior written 
    consent. <b><font color="red">AUDIT NOTE: Confidentiality clause may prevent Client from warning others 
    about Service Provider's practices.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 12))
    
    # Limitation of liability
    Story.append(Paragraph("<b>ARTICLE 5: LIMITATION OF LIABILITY</b>", styles['Heading2']))
    Story.append(Paragraph("""
    <b>5.1 Liability Cap:</b> Service Provider's total aggregate liability under this Agreement shall not 
    exceed the lesser of (i) $25,000 or (ii) the fees paid by Client in the one month preceding the claim. 
    <b><font color="red">AUDIT NOTE: Extremely low liability cap for data processing services. One month 
    of fees may be insufficient to cover actual damages.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 6))
    
    Story.append(Paragraph("""
    <b>5.2 Excluded Damages:</b> IN NO EVENT SHALL SERVICE PROVIDER BE LIABLE FOR ANY INDIRECT, INCIDENTAL, 
    CONSEQUENTIAL, SPECIAL, OR PUNITIVE DAMAGES, INCLUDING LOST PROFITS, LOST DATA, BUSINESS INTERRUPTION, 
    OR REPUTATIONAL HARM, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. <b><font color="red">AUDIT NOTE: 
    Broad exclusion of consequential damages eliminates recovery for most business impacts.</font></b>
    """, styles['BodyText']))
    Story.append(Spacer(1, 20))
    
    # Signatures
    Story.append(Paragraph("<b>SIGNATURES</b>", styles['Heading2']))
    Story.append(Spacer(1, 12))
    
    sig_data = [
        ['SERVICE PROVIDER: SecureData Processing Inc.', 'CLIENT: Global Finance Corp.'],
        ['', ''],
        ['_________________________________', '_________________________________'],
        ['Rachel Kim, Chief Legal Officer', 'Thomas Anderson, General Counsel'],
        ['Date: May 15, 2024', 'Date: May 15, 2024']
    ]
    
    sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    Story.append(sig_table)
    
    doc.build(Story)
    print(f"✓ Generated {filename}")

if __name__ == "__main__":
    print("Generating dummy contract documents for audit team demo...\n")
    
    try:
        create_contract_1()
        create_contract_2()
        create_contract_3()
        create_contract_4()
        create_contract_5()
        
        print("\n" + "="*70)
        print("✓ Successfully generated 5 contract PDFs")
        print("="*70)
        print("\nContract Summary:")
        print("1. contract_001_software_license.pdf - Unusual payment terms and liability caps")
        print("2. contract_002_consulting_services.pdf - IP ownership and fee structure issues")
        print("3. contract_003_cloud_services.pdf - Data sovereignty and SLA concerns")
        print("4. contract_004_equipment_purchase.pdf - Warranty and support problems")
        print("5. contract_005_master_service_agreement.pdf - Indemnification and insurance issues")
        print("\nAll contracts contain highlighted audit notes for non-standard terms.")
        
    except Exception as e:
        print(f"\n✗ Error generating contracts: {str(e)}")
        print("Make sure reportlab is installed: pip install reportlab")

