"""Resume content, word for word from resume_nikko_comidoy.pdf (Oct 2026).

Single source for the first-install seed (migration 0002) and `manage.py load_resume`,
which publishes it as a new revision of the live home page. Plain data only: the seed
migration imports this module, so keep it free of model imports.
"""

from datetime import date

PROFILE = {
    "name": "Nikko Comidoy",
    "headline": "Senior Support Software Engineer | Production Debugging | Python, TypeScript and APIs",
    "location": "Kitchener, Ontario, Canada",
    "email": "nikkomidoy@gmail.com",
    "phone": "548-333-0036",
    "linkedin_url": "https://www.linkedin.com/in/nikkocomidoy",
    "summary": (
        "Support and production software engineer with 11+ years of experience building and "
        "debugging Python, Django, TypeScript and REST API systems, including 5+ years as the "
        "senior escalation point for Prezzee's customer-facing platforms across the US, UK, "
        "Australia and New Zealand. I own production issues end to end: tracing logs and source "
        "code to the root cause, shipping and deploying the fix, explaining it clearly to "
        "customers and stakeholders, and building internal tooling so the next investigation "
        "takes less time. I use agentic coding tools such as Claude Code and Cursor in my daily "
        "investigation and development workflow. Teams that hire me get an engineer who stops "
        "repeat incidents, lifts the load off frontline support, and keeps customers confident "
        "during their worst production days."
    ),
}

SKILL_GROUPS = [
    (
        "Production and Support Engineering",
        "Production debugging, incident management, root cause analysis (RCA), log analysis, "
        "issue reproduction, customer testing coordination, SLA and support metrics, "
        "technical escalation",
    ),
    (
        "Languages and Frameworks",
        "Python, Django, TypeScript, JavaScript, Node.js, React, SQL, Celery",
    ),
    (
        "APIs, Systems and Integrations",
        "REST APIs, GraphQL, third-party integrations, distributed systems, Redis, "
        "SSO and authentication (OAuth 2.0)",
    ),
    (
        "AI and Developer Tooling",
        "Claude Code, Cursor, LLM prompting, Python automation, internal tooling, Git, GitHub, "
        "GitLab, GitHub Copilot",
    ),
    ("Observability and Collaboration", "Datadog, Sentry, Jira, Confluence"),
]

EXPERIENCES = [
    {
        "company": "Deel Inc.",
        "client": "Client: Prezzee",
        "location": "Remote, US and Canada Operations",
        "role": "Applications Development and Support Engineer",
        "start_date": date(2023, 2, 1),
        "end_date": date(2026, 9, 30),
        "highlights": [
            "Led the US shift as senior escalation point for frontline support engineers, owning 25+ complex production escalations per month across APIs, authentication flows and third-party integrations, resulting in 95%+ SLA attainment and fewer issues reaching core Engineering.",
            "Traced root causes across unfamiliar codebases, Datadog logs and Sentry traces in a distributed Python/Django and TypeScript environment, resulting in a 30% reduction in mean time to resolution (MTTR) for customer-facing incidents.",
            "Built Python internal tools and workflow automations for log analysis, data checks and repetitive fixes, eliminating 10+ hours of manual engineering and support effort every week.",
            "Designed, tested and deployed fixes and enhancements using agentic coding tools (Claude Code, Cursor), shortening the cycle from root cause to production fix by up to 40%.",
            "Worked directly with customers and partners to gather requirements, confirm reproduction steps, coordinate testing and explain fixes in plain language, resulting in 25% fewer reopened tickets.",
            "Drove RCA and post-incident reviews, feeding recurring customer trends to Product and Engineering, resulting in 15+ preventative fixes and new monitoring alerts that stopped repeat incidents.",
        ],
    },
    {
        "company": "Prezzee",
        "client": "engaged through Yempo",
        "location": "Manila, Philippines",
        "role": "Software Engineer",
        "start_date": date(2021, 8, 1),
        "end_date": date(2023, 1, 31),
        "highlights": [
            "Developed and maintained Python/Django applications and backend services supporting business-critical Prezzee gifting workflows.",
            "Built and supported REST and GraphQL APIs backed by SQL and Redis, and resolved production incidents across a global, follow-the-sun environment.",
            "Monitored application performance and partnered with developers, Product and operations to troubleshoot complex issues within service-level expectations.",
            "Delivered bug fixes, enhancements and reliability improvements, building the platform knowledge that led to US shift leadership and senior escalation ownership.",
        ],
    },
    {
        "company": "ZEN Rooms",
        "client": "",
        "location": "Taguig, Philippines",
        "role": "Senior Python Engineer",
        "start_date": date(2020, 7, 1),
        "end_date": date(2021, 3, 31),
        "highlights": [
            "Designed internal tools and backend applications in Python and Django that automated business processes and improved operational efficiency.",
            "Built and integrated APIs connecting existing systems, and investigated and resolved production bugs across backend services.",
            "Translated business requirements into technical solutions with product and cross-functional teams, and contributed to code reviews and testing.",
        ],
    },
    {
        "company": "Thorgate Digital OÜ",
        "client": "",
        "location": "Tallinn, Estonia",
        "role": "Software Engineer",
        "start_date": date(2019, 7, 1),
        "end_date": date(2020, 2, 29),
        "highlights": [
            "Built full-stack web applications with Python, Django, React and JavaScript, integrating frontend features with backend APIs.",
            "Investigated and resolved bugs across frontend and backend components, and took part in code reviews, testing and architecture improvements.",
        ],
    },
    {
        "company": "Detail Online Technology",
        "client": "",
        "location": "Davao, Philippines",
        "role": "Software Developer",
        "start_date": date(2018, 6, 1),
        "end_date": date(2019, 5, 31),
        "highlights": [
            "Designed and developed data validation and processing systems that improved data accuracy and reliability.",
            "Investigated and resolved technical issues across application and data-processing systems with cross-functional teams.",
        ],
    },
    {
        "company": "Ingenuity Global Consulting",
        "client": "",
        "location": "Davao, Philippines",
        "role": "Software Developer",
        "start_date": date(2014, 12, 1),
        "end_date": date(2017, 9, 30),
        "highlights": [
            "Developed backend and frontend features, integrations and APIs for multiple startup clients, from development through deployment.",
            "Worked directly with clients and project managers to gather requirements, troubleshoot issues and ship fixes across varied technology stacks.",
        ],
    },
]

EDUCATION = [
    {
        "degree": "Bachelor of Science in Information Technology",
        "school": "University of Southeastern Philippines",
        "location": "Davao",
        "start_date": date(2010, 6, 1),
        "end_date": date(2014, 4, 30),
    },
]


def experience_rows() -> list[dict]:
    """EXPERIENCES as model field values (bullets joined one per line)."""
    return [
        {**exp, "summary": "", "highlights": "\n".join(exp["highlights"])} for exp in EXPERIENCES
    ]
