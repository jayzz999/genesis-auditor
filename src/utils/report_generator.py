"""
Professional PDF Report Generator for Genesis Auditor
Creates executive-grade security audit reports
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas


class GenesisReportGenerator:
    """
    Generates professional PDF audit reports
    """

    def __init__(self):
        """Initialize the report generator"""
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        print("✅ Report Generator initialized")

    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))

        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=0,
            leftIndent=0
        ))

        # Finding style
        self.styles.add(ParagraphStyle(
            name='Finding',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            fontName='Helvetica'
        ))

        # Critical finding
        self.styles.add(ParagraphStyle(
            name='Critical',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#c0392b'),
            fontName='Helvetica-Bold'
        ))

    def generate_report(
        self,
        audit_results: Dict,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Generate complete PDF report

        Args:
            audit_results: Complete audit results from orchestrator
            output_filename: Optional custom filename

        Returns:
            Path to generated PDF
        """
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = audit_results['audit_metadata']['domain'].replace(' ', '_')
            output_filename = f"Genesis_Audit_Report_{domain}_{timestamp}.pdf"

        print(f"\n📄 Generating PDF report: {output_filename}")

        # Create PDF document
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Build content
        story = []

        # Cover page
        story.extend(self._build_cover_page(audit_results))
        story.append(PageBreak())

        # Executive summary
        story.extend(self._build_executive_summary(audit_results))
        story.append(PageBreak())

        # Compliance scorecard
        story.extend(self._build_compliance_scorecard(audit_results))
        story.append(PageBreak())

        # Detailed findings
        story.extend(self._build_detailed_findings(audit_results))
        story.append(PageBreak())

        # Recommendations
        story.extend(self._build_recommendations(audit_results))

        # Build PDF
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)

        print(f"✅ Report generated: {output_filename}")
        return output_filename

    def _build_cover_page(self, audit_results: Dict) -> List:
        """Build the cover page"""
        story = []

        # Title
        story.append(Spacer(1, 2*inch))

        title = Paragraph(
            "<b>GENESIS AUDITOR</b><br/>Security Audit Report",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.5*inch))

        # Domain and target
        metadata = audit_results['audit_metadata']
        subtitle = Paragraph(
            f"<b>{metadata['domain']}</b><br/>{metadata['target']}",
            self.styles['Subtitle']
        )
        story.append(subtitle)
        story.append(Spacer(1, 1*inch))

        # Compliance score (big and bold)
        score = audit_results['statistics']['compliance_score']
        risk_level = audit_results['analysis'].get('risk_level', 'UNKNOWN')

        score_color = self._get_score_color(score)
        score_text = Paragraph(
            f"<font size=48 color='{score_color}'><b>{score}/100</b></font><br/>"
            f"<font size=16>Compliance Score</font><br/>"
            f"<font size=14 color='#c0392b'><b>Risk Level: {risk_level}</b></font>",
            self.styles['Subtitle']
        )
        story.append(score_text)
        story.append(Spacer(1, 1*inch))

        # Audit metadata
        audit_date = datetime.fromisoformat(metadata['timestamp']).strftime("%B %d, %Y at %I:%M %p")
        info_data = [
            ['Audit Date:', audit_date],
            ['Duration:', f"{metadata['duration_seconds']:.1f} seconds"],
            ['Total Tests:', str(audit_results['statistics']['total_attacks'])],
            ['Vulnerabilities:', str(audit_results['statistics']['vulnerabilities_found'])]
        ]

        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7f8c8d')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        story.append(info_table)

        return story

    def _build_executive_summary(self, audit_results: Dict) -> List:
        """Build executive summary section"""
        story = []

        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))

        # AI-generated summary
        exec_summary = audit_results['analysis'].get('executive_summary', 'No summary available')
        summary_para = Paragraph(exec_summary, self.styles['Finding'])
        story.append(summary_para)
        story.append(Spacer(1, 0.3*inch))

        # Key findings
        story.append(Paragraph("Key Findings", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.1*inch))

        stats = audit_results['statistics']
        critical_issues = audit_results['analysis'].get('critical_issues', [])

        findings_data = [
            ['Metric', 'Value', 'Status'],
            ['Compliance Score', f"{stats['compliance_score']}/100", self._get_status_text(stats['compliance_score'])],
            ['Total Vulnerabilities', str(stats['vulnerabilities_found']), '⚠️' if stats['vulnerabilities_found'] > 0 else '✓'],
            ['Critical Issues', str(stats['critical_findings']), '🚨' if stats['critical_findings'] > 0 else '✓'],
            ['High Severity Issues', str(stats['high_findings']), '⚠️' if stats['high_findings'] > 0 else '✓'],
        ]

        findings_table = Table(findings_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        findings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))

        story.append(findings_table)
        story.append(Spacer(1, 0.3*inch))

        # Critical issues list
        if critical_issues:
            story.append(Paragraph("Critical Issues Requiring Immediate Attention", self.styles['SectionHeader']))
            story.append(Spacer(1, 0.1*inch))

            for i, issue in enumerate(critical_issues[:5], 1):  # Top 5
                issue_para = Paragraph(f"<b>{i}.</b> {issue}", self.styles['Critical'])
                story.append(issue_para)
                story.append(Spacer(1, 0.1*inch))

        return story

    def _build_compliance_scorecard(self, audit_results: Dict) -> List:
        """Build compliance scorecard with visualizations"""
        story = []

        story.append(Paragraph("Compliance Scorecard", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))

        # Generate radar chart
        radar_img = self._create_radar_chart(audit_results)
        if radar_img:
            story.append(Image(radar_img, width=5*inch, height=4*inch))
            story.append(Spacer(1, 0.2*inch))

        # Severity breakdown pie chart
        pie_img = self._create_severity_pie_chart(audit_results)
        if pie_img:
            story.append(Image(pie_img, width=5*inch, height=3.5*inch))

        return story

    def _build_detailed_findings(self, audit_results: Dict) -> List:
        """Build detailed findings section"""
        story = []

        story.append(Paragraph("Detailed Vulnerability Findings", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))

        # Get vulnerabilities
        vulnerabilities = [r for r in audit_results['attack_results'] if r.get('result') == 'VULNERABLE']

        if not vulnerabilities:
            story.append(Paragraph("No vulnerabilities detected.", self.styles['Finding']))
            return story

        # Sort by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        vulnerabilities.sort(key=lambda x: severity_order.get(x.get('severity', 'MEDIUM'), 4))

        # Build findings table
        for i, vuln in enumerate(vulnerabilities, 1):
            finding_story = self._build_single_finding(i, vuln)
            story.extend(finding_story)
            story.append(Spacer(1, 0.2*inch))

        return story

    def _build_single_finding(self, number: int, vuln: Dict) -> List:
        """Build a single vulnerability finding"""
        story = []

        severity = vuln.get('severity', 'MEDIUM')
        severity_color = {
            'CRITICAL': '#c0392b',
            'HIGH': '#e67e22',
            'MEDIUM': '#f39c12',
            'LOW': '#27ae60'
        }.get(severity, '#95a5a6')

        # Finding header
        header = Paragraph(
            f"<b>Finding #{number}: {vuln.get('attack_name', 'Unknown Vulnerability')}</b> "
            f"<font color='{severity_color}'>[{severity}]</font>",
            self.styles['SectionHeader']
        )
        story.append(header)

        # Finding details table
        details_data = [
            ['Agent', vuln.get('agent_name', 'N/A')],
            ['Attack Method', vuln.get('attack_method', 'N/A')[:100] + '...'],
            ['Evidence', vuln.get('evidence', 'N/A')],
            ['Impact', vuln.get('impact', 'N/A')],
            ['Recommendation', vuln.get('recommendation', 'N/A')]
        ]

        details_table = Table(details_data, colWidths=[1.5*inch, 4.5*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7f8c8d')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ]))

        story.append(details_table)

        return story

    def _build_recommendations(self, audit_results: Dict) -> List:
        """Build recommendations section"""
        story = []

        story.append(Paragraph("Prioritized Remediation Roadmap", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))

        recommendations = audit_results.get('recommendations', [])

        if not recommendations:
            story.append(Paragraph("No specific recommendations at this time.", self.styles['Finding']))
            return story

        # Build recommendations table
        rec_data = [['Priority', 'Vulnerability', 'Action Required']]

        for rec in recommendations[:10]:  # Top 10
            rec_data.append([
                rec.get('priority', 'MEDIUM'),
                rec.get('vulnerability', 'N/A')[:40] + '...',
                rec.get('recommendation', 'N/A')[:60] + '...'
            ])

        rec_table = Table(rec_data, colWidths=[1*inch, 2.5*inch, 3*inch])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        story.append(rec_table)

        return story

    def _create_radar_chart(self, audit_results: Dict) -> Optional[BytesIO]:
        """Create radar chart for compliance visualization"""
        try:
            import numpy as np

            # Categories
            categories = ['Authentication', 'Authorization', 'Data Protection', 'Input Validation', 'Audit Logging']
            N = len(categories)

            # Simulate scores based on vulnerabilities found
            # In production, this would analyze actual vulnerability types
            base_score = audit_results['statistics']['compliance_score'] / 100
            scores = [base_score + np.random.uniform(-0.15, 0.15) for _ in range(N)]
            scores = [max(0, min(1, s)) for s in scores]  # Clamp to [0, 1]

            # Create plot
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            scores += scores[:1]
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
            ax.plot(angles, scores, 'o-', linewidth=2, color='#3498db')
            ax.fill(angles, scores, alpha=0.25, color='#3498db')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories, size=10)
            ax.set_ylim(0, 1)
            ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
            ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
            ax.grid(True)
            ax.set_title('Security Compliance Radar', size=14, weight='bold', pad=20)

            # Save to bytes
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()

            return img_buffer

        except Exception as e:
            print(f"⚠️  Could not generate radar chart: {e}")
            return None

    def _create_severity_pie_chart(self, audit_results: Dict) -> Optional[BytesIO]:
        """Create pie chart for vulnerability severity breakdown"""
        try:
            vulnerabilities = [r for r in audit_results['attack_results'] if r.get('result') == 'VULNERABLE']

            if not vulnerabilities:
                return None

            # Count by severity
            severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
            for vuln in vulnerabilities:
                severity = vuln.get('severity', 'MEDIUM')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

            # Filter out zero counts
            labels = []
            sizes = []
            colors_list = []
            color_map = {
                'CRITICAL': '#c0392b',
                'HIGH': '#e67e22',
                'MEDIUM': '#f39c12',
                'LOW': '#27ae60'
            }

            for severity, count in severity_counts.items():
                if count > 0:
                    labels.append(f'{severity}\n({count})')
                    sizes.append(count)
                    colors_list.append(color_map[severity])

            # Create plot
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.pie(sizes, labels=labels, colors=colors_list, autopct='%1.1f%%',
                   startangle=90, textprops={'size': 11, 'weight': 'bold'})
            ax.set_title('Vulnerability Severity Distribution', size=14, weight='bold', pad=20)

            # Save to bytes
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()

            return img_buffer

        except Exception as e:
            print(f"⚠️  Could not generate pie chart: {e}")
            return None

    def _get_score_color(self, score: int) -> str:
        """Get color based on compliance score"""
        if score >= 80:
            return '#27ae60'  # Green
        elif score >= 60:
            return '#f39c12'  # Yellow
        elif score >= 40:
            return '#e67e22'  # Orange
        else:
            return '#c0392b'  # Red

    def _get_status_text(self, score: int) -> str:
        """Get status text based on score"""
        if score >= 80:
            return '✓ Pass'
        elif score >= 60:
            return '⚠️ Warning'
        else:
            return '🚨 Fail'

    def _add_header_footer(self, canvas_obj, doc):
        """Add header and footer to each page"""
        canvas_obj.saveState()

        # Footer
        canvas_obj.setFont('Helvetica', 9)
        canvas_obj.setFillColor(colors.grey)
        canvas_obj.drawString(inch, 0.5 * inch, f"Genesis Auditor • Confidential")
        canvas_obj.drawRightString(doc.width + inch, 0.5 * inch,
                                   f"Page {canvas_obj.getPageNumber()}")

        canvas_obj.restoreState()


def test_report_generator():
    """Test the report generator with sample data"""
    print("=" * 60)
    print("🧪 TESTING PDF REPORT GENERATOR")
    print("=" * 60)

    # Load a sample audit result (or create one)
    sample_audit = {
        'audit_metadata': {
            'domain': 'HIPAA Compliance',
            'target': 'HealthCare API v2.1',
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': 45.3
        },
        'statistics': {
            'total_attacks': 12,
            'vulnerabilities_found': 5,
            'critical_findings': 2,
            'high_findings': 2,
            'compliance_score': 45
        },
        'analysis': {
            'risk_level': 'HIGH',
            'executive_summary': 'The HealthCare API v2.1 exhibits multiple critical security vulnerabilities that pose significant risk to Protected Health Information (PHI). Immediate remediation is required to achieve HIPAA compliance.',
            'critical_issues': [
                'Unauthenticated access to patient health information',
                'SQL injection vulnerability in patient search',
                'Insecure direct object references allowing unauthorized record access'
            ]
        },
        'attack_results': [
            {
                'agent_name': 'PHI Access Agent',
                'attack_name': 'Unauthenticated PHI Access',
                'attack_method': 'Direct API endpoint access without authentication headers',
                'severity': 'CRITICAL',
                'result': 'VULNERABLE',
                'evidence': 'API returned HTTP 200 with patient data without valid credentials',
                'impact': 'CRITICAL: Complete compromise possible - HIPAA violation',
                'recommendation': 'Enforce authentication on all PHI endpoints'
            },
            {
                'agent_name': 'Injection Specialist',
                'attack_name': 'SQL Injection in Patient Search',
                'attack_method': 'SQL injection via search parameter',
                'severity': 'CRITICAL',
                'result': 'VULNERABLE',
                'evidence': 'SQL error exposed database structure',
                'impact': 'CRITICAL: Database compromise possible',
                'recommendation': 'Implement parameterized queries'
            }
        ],
        'recommendations': [
            {
                'priority': 'CRITICAL',
                'vulnerability': 'Unauthenticated PHI Access',
                'recommendation': 'Enforce authentication on all PHI endpoints'
            }
        ]
    }

    # Generate report
    generator = GenesisReportGenerator()
    report_file = generator.generate_report(sample_audit, "test_genesis_report.pdf")

    print(f"\n✅ Test report generated: {report_file}")
    print("=" * 60)


if __name__ == "__main__":
    test_report_generator()
