#!/usr/bin/env python3
"""Generate assets/Eduard_Ruzsa_CV.pdf: one-page A4, monochrome, mirrors the site content.

Contact is GitHub only, matching the site. Base PDF fonts lack the arrow glyph,
so "4->2" is written out. Requires: pip install reportlab. Keep the output at 1 page.
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (HRFlowable, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

INK = HexColor("#09090b")
BODY = HexColor("#18181b")
MUTED = HexColor("#71717a")
RULE = HexColor("#d4d4d8")

OUT = Path(__file__).resolve().parent.parent / "assets" / "Eduard_Ruzsa_CV.pdf"

styles = {
    "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=17, leading=20, textColor=INK),
    "role": ParagraphStyle("role", fontName="Helvetica", fontSize=9.5, leading=12, textColor=BODY),
    "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED),
    "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
                              textColor=INK, spaceBefore=6, spaceAfter=2),
    "jobhead": ParagraphStyle("jobhead", fontName="Helvetica-Bold", fontSize=9, leading=11.5, textColor=INK),
    "dates": ParagraphStyle("dates", fontName="Helvetica", fontSize=8, leading=11.5, textColor=MUTED, alignment=2),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=7.7, leading=9.6, textColor=BODY,
                             leftIndent=7, bulletIndent=0, spaceAfter=0.8),
    "skill": ParagraphStyle("skill", fontName="Helvetica", fontSize=7.9, leading=10.2, textColor=BODY, spaceAfter=1),
    "edu": ParagraphStyle("edu", fontName="Helvetica", fontSize=7.7, leading=9.6, textColor=BODY),
    "summary": ParagraphStyle("summary", fontName="Helvetica", fontSize=8.3, leading=10.8, textColor=BODY),
}


def sect(title):
    return [Paragraph(title.upper(), styles["section"]),
            HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=3)]


def jobrow(left, right):
    t = Table([[Paragraph(left, styles["jobhead"]), Paragraph(right, styles["dates"])]],
              colWidths=[132 * mm, 46 * mm])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def job(role, company, location, dates, items):
    head = f"{role} &middot; {company} &nbsp;<font color='#71717a' size='7.5'>{location}</font>"
    return [jobrow(head, dates)] + [
        Paragraph(f"<bullet>&#8250;</bullet> <b>{h}:</b> {t}", styles["bullet"]) for h, t in items]


story = [
    Paragraph("Eduard Gergo Ruzsa", styles["name"]),
    Paragraph("Senior Backend Software Engineer &nbsp;&middot;&nbsp; Berlin, Germany", styles["role"]),
    Spacer(1, 2),
    Paragraph('<link href="https://github.com/eduardruzsa" color="#18181b"><u>github.com/eduardruzsa</u></link>'
              ' &nbsp;&middot;&nbsp; '
              '<link href="https://eduardruzsa.github.io" color="#18181b"><u>eduardruzsa.github.io</u></link>',
              styles["contact"]),
    Spacer(1, 4),
    Paragraph("Backend engineer with 7+ years of experience designing distributed systems and production APIs "
              "across fintech, manufacturing automation, and developer tooling. I care about clean architecture, "
              "reliability, and pragmatic AI-augmented workflows that let small teams ship like big ones.",
              styles["summary"]),
]

story += sect("Skills")
story += [
    Paragraph("<b>Backend:</b> Kotlin, Python, TypeScript, Java, C++, Ktor, GraphQL, gRPC, Protobuf, Temporal, "
              "Airflow, PostgreSQL", styles["skill"]),
    Paragraph("<b>Cloud &amp; DevOps:</b> AWS, RDS, Lambda, Docker, Kubernetes, Terraform, Helm, GitLab CI/CD, "
              "GitHub Actions, Prometheus, Grafana", styles["skill"]),
    Paragraph("<b>Architecture &amp; Leadership:</b> Microservices, Event-Driven Architecture, technical mentoring, "
              "hiring, code reviews, Agile/Scrum, AI-augmented engineering", styles["skill"]),
]

story += sect("Experience")
story += job("Senior Software Engineer", "Mirror", "Berlin, Germany", "2025 &#8211; now", [
    ("AI-augmented development", "sustained team velocity through a headcount reduction from 4 to 2 engineers; "
     "owned specification, architecture, and review of all AI-generated code across Kotlin and Rust services."),
    ("Transaction processing", "own the Kotlin/Temporal service turning bank transactions into encrypted settlement "
     "reports: cursor-based sync, worldwide timezone resolution, and multi-currency settlement via an in-house rates "
     "service (Polygon.io, ECB, BoE, SNB, Fed). Integrated the L2 attester chain and a remote signer; hardened with "
     "infinite-retry workflows and a gRPC channel leak fix."),
    ("Open banking platform", "architected a multi-provider consent lifecycle (Plaid, Yapily, Teller, Quiltt, MX) "
     "over gRPC with UK 90-day renewal, expiry webhooks, and idempotent activation. Delivered the Plaid, Yapily, and "
     "Teller integrations in a Rust gRPC bank-data service, including a breaking consent API redesign, and migrated "
     "the consent service onto it."),
    ("Observability", "added Prometheus business and Temporal SDK metrics, Grafana dashboards, alert rules, and "
     "runbooks across four production services."),
    ("E2E testing", "built a Kotlin/JUnit E2E framework with browser-driven tests against Plaid Link, Yapily, and "
     "Teller Connect, WireMock transaction injection, and AWS Secrets Manager config; suites run in parallel in CI."),
])
story += job("Software Engineer", "Portal", "London, United Kingdom", "2024 &#8211; 2025", [
    ("Traceability &amp; events", "co-designed an event-driven traceability system with schema modeling and a Kotlin "
     "outbox client library for durable delivery via Postgres, with partitioning and automatic retry."),
    ("Manufacturing services", "built device batch provisioning workflows, food pod production management with GS1 "
     "code generation, and a label generation service with a GraphQL API and QR codes."),
    ("Search service", "designed a Kotlin Ktor service for address search and reverse geocoding; cut API costs by "
     "90% through Caffeine caching."),
    ("Platform libraries", "led migration to Ktor 3, Koin 4, and gRPC 1.70; built Snowflake ID generation, backwards "
     "pagination, and a Gradle meta-plugin adopted by 6 developers."),
])
story += job("Software Engineer", "Arrival", "London, United Kingdom", "2022 &#8211; 2024", [
    ("Data pipelines", "developed Airflow pipelines on Kubernetes extracting, repairing, and pushing 100GB+ of PLM "
     "data from Siemens NX, cutting designer feedback loops from days to hours."),
    ("API", "designed data storage, validation, and provisioning with AWS RDS, Lambdas, and Hasura for a GraphQL "
     "service; fully automated data releases, replacing a manual process."),
    ("Infrastructure", "defined infrastructure as code with Terraform for reproducible RDS and VM instances."),
    ("Developer experience", "introduced Nix for reproducible environments; assisted the Docker-to-Podman transition."),
])
story += job("Software Engineering Lead", "Peakism", "London, United Kingdom, part-time", "2022 &#8211; 2023", [
    ("Technical leadership", "led MVP development of a web application (Python API + React TypeScript); defined "
     "architecture with the CEO, hired the first engineer, and managed AWS infrastructure and CI/CD."),
])
story += job("Software Engineer", "Autodesk", "Birmingham, United Kingdom", "2019 &#8211; 2022", [
    ("3D printing features", "developed a Qt settings editor for Fusion 360 and implemented per-model customization "
     "by decomposing the toolpathing kernel in C++, a feature that differentiates the product from competitors."),
    ("API development", "ported the public mesh API into a new sub-module with CMake integration without disrupting "
     "existing add-ins; built AWS Lambdas for CAD assembly processing."),
    ("Infrastructure", "built a multi-repository tool for automated building, testing, and merging using the GitHub "
     "API and Python."),
])

story += sect("Education")
story += [
    jobrow("BSc Computer Science &middot; University of Birmingham", "2016 &#8211; 2019"),
    Paragraph("Led a robot programming team; developed a multiplayer game with an 80% game-loop optimisation "
              "(ranked 3rd of 16 teams); evaluated post-quantum cryptography timing security in the final year.",
              styles["edu"]),
    jobrow("Mathematics and Computer Science &middot; Colegiul National Vasile Lucaciu", "2012 &#8211; 2016"),
    Paragraph("Baccalaureate: 9.70/10 Mathematics, 9.30/10 Computer Science. Cambridge Advanced English C2.",
              styles["edu"]),
]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
                        topMargin=12 * mm, bottomMargin=11 * mm,
                        title="Eduard Gergo Ruzsa - CV", author="Eduard Gergo Ruzsa",
                        subject="Senior Backend Software Engineer - CV")
doc.build(story)
print("pages:", doc.page)
