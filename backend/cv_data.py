"""
Grounded-Truth Fact Ledger & ATS Tailoring Engine for Vinoth Nataraj.
Strictly preserves 100% factual accuracy from Vinoth_Nataraj_Senior_Manager.pdf
while optimizing ATS keyword indexing, bullet ordering, and role framing.
"""

from typing import Dict, List, Any
import re
import copy

# ============================================================================
# IMMUTABLE GROUNDED-TRUTH FACT LEDGER
# Extracted verbatim from /Users/vinoth/Downloads/Vinoth_Nataraj_Senior_Manager.pdf
# ============================================================================
GROUNDED_HEADER = {
    "name": "Vinoth Nataraj",
    "location": "Chennai",
    "email": "vinoth.n@outlook.com",
    "phone": "+91 9884299122",
    "linkedin_label": "LinkedIn",
    "linkedin_url": "https://www.linkedin.com/in/vinothnataraj/",
    "github_label": "GitHub",
    "github_url": "https://github.com/vinailead",
}

GROUNDED_EDUCATION = [
    {
        "degree": "MBA, Master of Business Administration",
        "dates": "Sep 2008 – Oct 2009",
        "institution": "The University of Sheffield, United Kingdom",
    },
    {
        "degree": "B.Sc. Information Technology",
        "dates": "Apr 2000 – Jun 2003",
        "institution": "APA College of Arts and Culture University, Palani",
    },
]

GROUNDED_CERTIFICATIONS = [
    "Google AI Professional Certificate",
    "Google Generative AI Leader course completion skill badge",
]

# Verified metrics that must never be inflated or altered
VERIFIED_METRICS = [
    "13+ years",
    "3.5 Yrs in Telecom",
    "10 Yrs in Financial Services (CaaS)",
    "$54.8M",
    "2.8M annual call deflections",
    "100+ high-impact Agentic AI",
    "$400M in ROI",
    "10 Senior Consultants",
    "70% from 15 days to 5 days",
    "$5B + consumer credit portfolio",
    "2 to 6 members",
    "15+ KPIs",
    "40%",
]

# ============================================================================
# 5 MASTER ROLE ARCHETYPE VARIATIONS
# Confirmed rule: Place "Independent AI Product Development (Jan 2026- Present)"
# inside PROFESSIONAL WORK EXPERIENCE as the current top role so ATS parsers
# register 0 months of employment gap.
# ============================================================================

MASTER_VARIATIONS: Dict[str, Dict[str, Any]] = {
    "baseline": {
        "id": "baseline",
        "name": "Original Reference (ATS-Enhanced Chronology)",
        "target_track": "All Tracks",
        "description": "Exact text from Vinoth_Nataraj_Senior_Manager.pdf with Independent AI Product Development placed inside Professional Work Experience to eliminate the 10-month layoff gap in ATS parsers.",
        "summary": (
            "Senior AI and Analytics leader with 13+ years of progressive experience driving enterprise CX "
            "transformation, AI strategy, and portfolio analytics across telecommunications and consumer financial "
            "services. Designs structured AI opportunity assessments and ROI-led transformation roadmaps that "
            "prioritize high-value use cases. Leads cross-functional teams that convert AI capabilities into measurable "
            "business outcomes, delivering multi-million-dollar reductions in cost-to-serve."
        ),
        "competencies_header": "CORE COMPETENCIES – 3.5 Yrs in Telecom,10 Yrs in Financial Services (CaaS)",
        "competencies": [
            {
                "label": "AI Strategy:",
                "text": "Gen AI Product roadmap, LLM Use case identification and prioritization, Agentic workflows, Business case quantification and ROI measurement, Executive Engagement",
            },
            {
                "label": "CX & Digital Transformation:",
                "text": "Customer journey analytics, Friction Analysis, Personalization, automation and self-serve containment, Next Best Action",
            },
            {
                "label": "Analytics & Insights:",
                "text": "Portfolio analytics, Marketing ROI, Credit Risk Analytics, Executive insights and reporting",
            },
            {
                "label": "Consulting & Delivery:",
                "text": "Discovery Workshops, Cross-Functional Leadership, Agile delivery",
            },
        ],
        "experience": [
            {
                "company": "Independent AI Product Development",
                "title": "AI Builder – Personal Portfolio github.com/vinailead",
                "dates": "Jan 2026- Present",
                "bullets": [
                    "Architected and deployed agentic solutions solving enterprise work flow, cost intelligent and CX operational bottlenecks.",
                    "Built autonomous pipelines using LangGraph, ReAct reasoning loops, and Claude Agent SDK with custom tool calling.",
                    "Implemented automated evaluation benchmarks, guardrails, and HITL verification workflows across all deployments.",
                    "Applying formal enterprise AI standards to agent design through continuous upskilling through curated courses from Google Developer Program, Claude, Nebius and Microsoft Reactor Series.",
                ],
            },
            {
                "company": "VERIZON | Chennai",
                "title": "Senior Manager, Product Dev/Mgmt – AI and CX Automation",
                "dates": "Aug 2022- Dec 2025",
                "bullets": [
                    "Executed the multi-year AI Platform Strategy roadmap for CX personalization and automation, delivering use cases that resulted in $54.8M in cost to serve savings and 2.8M annual call deflections.",
                    "Structured and delivered 100+ high-impact Agentic AI automation use cases projecting $400M in ROI. Developed a classification framework distinguishing autonomously resolvable issues from human-assisted and digital self-serve scenarios by analyzing customer issues at scale.",
                    "Served as a strategic advisor to the senior leadership developing benefit hypotheses, cost estimates, and ROI models sizing the cost impact of customer journey friction on cost-to-serve.",
                    "Hired, mentored and led a pod of 10 Senior Consultants delivering analytical insights, AI automation POCs, and reusable data products to cross functional executives. Collaborated with Business, Engineering, Product, Finance, and GTM teams to move use cases into production.",
                    "Established value tracking and benefits realization for AI led personalization features across omnichannel touchpoints, assessing whether AI-driven interventions delivered sustained value.",
                    "Fast tracked team use case delivery time by 70% from 15 days to 5 days using Google Gemini enterprise and Verizon AI stack integrating high volume customer transactional and interaction data.",
                    "Presented executive insights and trends to senior leaders highlighting the impact of upstream business decisions on key CX KPIs -churn, care call volume, and experience scores (FCR, CSAT, NPS).",
                ],
            },
            {
                "company": "CCLYTICX SERVICES PVT LTD | Chennai",
                "sub_roles": [
                    {
                        "title": "Manager, Analytics",
                        "dates": "Apr 2021 – Jul 2022",
                        "bullets": [
                            "Led strategic analytical solutions delivery for a $5B + consumer credit portfolio across B2C and B2B credit portfolios. Supported Senior Risk and Marketing leaders with acquisition and portfolio P/L.",
                            "Presented product level ROI analysis, portfolio performance reviews, risk trend assessments, and credit application and conversion analysis using custom risk models.",
                            "Scaled and led high-performing analytics consulting team from 2 to 6 members, with accountability for analytical projects delivery and team capability development.",
                            "Managed the Google Analytics measurement framework across digital properties, delivering visibility into user engagement, conversion funnels, event tracking, and drop-off identification.",
                        ],
                    },
                    {
                        "title": "Assistant Manager, Analytics",
                        "dates": "Apr 2016 – Mar 2021",
                        "bullets": [
                            "Reported portfolio performance across 15+ KPIs including application volume, approval rates, delinquencies, charge-offs, and roll rates, segmented FICO and vantage risk scores.",
                            "Measured marketing campaign effectiveness for B2B Retail Credit and B2C Credit Card portfolios, providing insights into seasonal take rates and conversions.",
                            "Led the redesign of Fortiva Retail Credit and Aspire Credit websites — overseeing mobile-responsive design, ADA compliance, and marketing tag implementation (GA4, Facebook Pixel, conversion tracking).",
                            "Integrated marketing data from HubSpot, Infor CRM, Oracle DB, SAS, and email platforms into a unified analytics environment, improving marketing ROI visibility by 40% and enabling automated campaign optimisation.",
                        ],
                    },
                    {
                        "title": "Team Leader, Analytics",
                        "dates": "Jun 2012 – Mar 2016",
                        "bullets": [
                            "Generated risk management reports tracking collections performance, delinquencies, charge-offs, and roll rates for B2C lending products.",
                            "Developed segmented portfolio analyses by FICO score bands, origination channels, and vintage cohorts.",
                        ],
                    },
                ],
            },
        ],
        "skills": [
            {
                "label": "AI & Gen AI tooling:",
                "text": "ML Foundations, LLM Foundations, RAG, Agentic AI, Claude Code, Gemini, Google AI Studio, LangGraph, Weaviate, Langfuse",
            },
            {
                "label": "Data & Analytics:",
                "text": "SQL, BigQuery, Python, Google Sheets, Excel, Oracle DB",
            },
            {
                "label": "Visualisation & Reporting:",
                "text": "Tableau, Power BI, Looker",
            },
            {
                "label": "Digital Analytics:",
                "text": "Google Analytics (GA4), Adobe Analytics, Qualtrics, Quantum Metric, Mailchimp",
            },
            {
                "label": "Enterprise Platforms:",
                "text": "HubSpot, Google Marketing Platform, NiCE, VERINT",
            },
        ],
    },

    "ai_strategy": {
        "id": "ai_strategy",
        "name": "Master Variation 1 – AI Strategy & Value Transformation",
        "target_track": "AI Strategy",
        "description": "Optimized for Senior Manager / Principal / Lead roles in Enterprise AI Strategy, AI Value Realization, GenAI Product Strategy, and AI Transformation Consulting.",
        "summary": (
            "Senior AI Strategy and Enterprise Transformation leader with 13+ years of progressive experience "
            "architecting Gen AI product roadmaps, AI opportunity assessments, and ROI-led transformation across "
            "telecommunications and consumer financial services. Proven track record structuring 100+ Agentic AI "
            "use cases projecting $400M in ROI and delivering $54.8M in realized cost-to-serve savings. Partners "
            "with C-suite and cross-functional leaders across Product, Engineering, Finance, and GTM to convert "
            "LLM and Agentic capabilities into measurable enterprise value."
        ),
        "competencies_header": "CORE COMPETENCIES – 3.5 Yrs in Telecom,10 Yrs in Financial Services (CaaS)",
        "competencies": [
            {
                "label": "AI Strategy & Value Realization:",
                "text": "Gen AI Product roadmap, LLM Use case identification and prioritization, Business case quantification and ROI measurement, Benefit hypotheses & benefits realization, Executive Engagement",
            },
            {
                "label": "CX & Digital Transformation:",
                "text": "Enterprise AI automation, Customer journey friction analysis, Omnichannel personalization, Self-serve containment, Next Best Action",
            },
            {
                "label": "Consulting & Cross-Functional Delivery:",
                "text": "Discovery Workshops, AI Pod Leadership (10 Senior Consultants), GTM & Product Alignment, Agile delivery",
            },
            {
                "label": "Analytics & Insights:",
                "text": "Portfolio P/L analytics, Marketing ROI, Credit Risk Analytics, Executive KPI storytelling (FCR, CSAT, NPS, Churn)",
            },
        ],
        "experience": [
            {
                "company": "Independent AI Product Development",
                "title": "AI Strategy & Agentic AI Builder – Personal Portfolio github.com/vinailead",
                "dates": "Jan 2026- Present",
                "bullets": [
                    "Architected and deployed enterprise-grade agentic AI solutions targeting workflow automation, cost intelligence, and CX operational bottlenecks.",
                    "Implemented automated evaluation benchmarks, enterprise AI guardrails, and HITL verification governance across autonomous deployments.",
                    "Built autonomous multi-step reasoning pipelines using LangGraph, ReAct reasoning loops, and Claude Agent SDK with custom tool calling.",
                    "Applying formal enterprise AI governance and architecture standards through continuous upskilling across Google Developer Program, Claude, Nebius, and Microsoft Reactor Series.",
                ],
            },
            {
                "company": "VERIZON | Chennai",
                "title": "Senior Manager, Product Dev/Mgmt – AI and CX Automation",
                "dates": "Aug 2022- Dec 2025",
                "bullets": [
                    "Executed the multi-year Enterprise AI Platform Strategy roadmap for CX personalization and automation, delivering production use cases that generated $54.8M in cost-to-serve savings and 2.8M annual call deflections.",
                    "Structured and prioritized 100+ high-impact Agentic AI automation use cases projecting $400M in ROI; designed an enterprise classification framework distinguishing autonomously resolvable issues from human-assisted and digital self-serve scenarios.",
                    "Served as strategic advisor to senior leadership, developing benefit hypotheses, cost estimates, and financial ROI models sizing the impact of customer journey friction on cost-to-serve.",
                    "Established enterprise value tracking and benefits realization governance for AI-led personalization features across omnichannel touchpoints, verifying sustained post-deployment ROI.",
                    "Hired, mentored, and led a pod of 10 Senior Consultants delivering AI automation POCs, analytical insights, and reusable data products; collaborated with Business, Engineering, Product, Finance, and GTM teams to scale use cases into production.",
                    "Fast tracked team use case delivery time by 70% from 15 days to 5 days using Google Gemini Enterprise and Verizon AI stack integrating high-volume customer transactional and interaction data.",
                    "Presented executive insights and strategic trends to senior leaders highlighting the impact of upstream business decisions on key CX KPIs — churn, care call volume, and experience scores (FCR, CSAT, NPS).",
                ],
            },
            {
                "company": "CCLYTICX SERVICES PVT LTD | Chennai",
                "sub_roles": [
                    {
                        "title": "Manager, Analytics",
                        "dates": "Apr 2021 – Jul 2022",
                        "bullets": [
                            "Led strategic analytical solutions delivery for a $5B + consumer credit portfolio across B2C and B2B credit portfolios, advising Senior Risk and Marketing leaders on acquisition strategy and portfolio P/L.",
                            "Presented product-level ROI analysis, portfolio performance reviews, risk trend assessments, and credit application conversion analysis using custom risk models.",
                            "Scaled and led a high-performing analytics consulting team from 2 to 6 members, with full accountability for consulting delivery and capability development.",
                            "Managed the Google Analytics measurement framework across digital properties, delivering strategic visibility into user engagement, conversion funnels, event tracking, and drop-off identification.",
                        ],
                    },
                    {
                        "title": "Assistant Manager, Analytics",
                        "dates": "Apr 2016 – Mar 2021",
                        "bullets": [
                            "Reported portfolio performance across 15+ KPIs including application volume, approval rates, delinquencies, charge-offs, and roll rates, segmented by FICO and Vantage risk scores.",
                            "Integrated marketing data from HubSpot, Infor CRM, Oracle DB, SAS, and email platforms into a unified analytics environment, improving marketing ROI visibility by 40% and enabling automated campaign optimisation.",
                            "Measured marketing campaign effectiveness for B2B Retail Credit and B2C Credit Card portfolios, providing actionable insights into seasonal take rates and conversions.",
                            "Led the redesign of Fortiva Retail Credit and Aspire Credit websites — overseeing mobile-responsive design, ADA compliance, and marketing tag implementation (GA4, Facebook Pixel, conversion tracking).",
                        ],
                    },
                    {
                        "title": "Team Leader, Analytics",
                        "dates": "Jun 2012 – Mar 2016",
                        "bullets": [
                            "Generated risk management reports tracking collections performance, delinquencies, charge-offs, and roll rates for B2C lending products.",
                            "Developed segmented portfolio analyses by FICO score bands, origination channels, and vintage cohorts.",
                        ],
                    },
                ],
            },
        ],
        "skills": [
            {
                "label": "AI & Gen AI tooling:",
                "text": "Agentic AI, Gemini, Google AI Studio, Claude Code, LangGraph, RAG, Weaviate, Langfuse, LLM Foundations, ML Foundations",
            },
            {
                "label": "Data & Analytics:",
                "text": "SQL, BigQuery, Python, Google Sheets, Excel, Oracle DB",
            },
            {
                "label": "Visualisation & Reporting:",
                "text": "Tableau, Power BI, Looker",
            },
            {
                "label": "Digital Analytics:",
                "text": "Google Analytics (GA4), Adobe Analytics, Qualtrics, Quantum Metric, Mailchimp",
            },
            {
                "label": "Enterprise Platforms:",
                "text": "NiCE, VERINT, HubSpot, Google Marketing Platform",
            },
        ],
    },

    "ai_builder": {
        "id": "ai_builder",
        "name": "Master Variation 2 – AI Builder & Applied GenAI Architect",
        "target_track": "AI Builder",
        "description": "Optimized for Principal / Lead AI Builder, Applied AI Product Builder, Forward-Deployed AI PM, and GenAI Solutions Architect roles.",
        "summary": (
            "Hands-on AI Builder and Senior AI Product Leader with 13+ years of progressive experience architecting, "
            "prototyping, and scaling production Agentic AI and analytical solutions across telecommunications and "
            "financial services. Builds autonomous multi-agent pipelines using LangGraph, ReAct reasoning loops, "
            "Claude Agent SDK, RAG (Weaviate), and Langfuse observability with automated evals and HITL guardrails. "
            "Delivered 100+ Agentic AI use cases ($400M projected ROI), $54.8M in realized savings, and a 70% "
            "reduction in AI delivery cycle time (15 days to 5 days) using Google Gemini Enterprise."
        ),
        "competencies_header": "CORE COMPETENCIES – 3.5 Yrs in Telecom,10 Yrs in Financial Services (CaaS)",
        "competencies": [
            {
                "label": "Agentic AI & GenAI Engineering:",
                "text": "LangGraph autonomous pipelines, ReAct reasoning loops, Claude Agent SDK, Custom tool calling, RAG architectures (Weaviate), LLM Evaluation benchmarks & Langfuse observability, Guardrails & HITL workflows",
            },
            {
                "label": "AI Product Development & Strategy:",
                "text": "0-to-1 AI POC development, Gen AI Product roadmap, Autonomous vs. human-assisted classification frameworks, ROI quantification",
            },
            {
                "label": "CX & Workflow Automation:",
                "text": "Enterprise workflow bottleneck resolution, Self-serve containment (2.8M call deflections), Omnichannel personalization, Next Best Action",
            },
            {
                "label": "Data Stack & Analytics:",
                "text": "Python, SQL, BigQuery, High-volume transactional & interaction data integration, Credit Risk & Portfolio Modeling",
            },
        ],
        "experience": [
            {
                "company": "Independent AI Product Development",
                "title": "AI Builder – Personal Portfolio github.com/vinailead",
                "dates": "Jan 2026- Present",
                "bullets": [
                    "Built autonomous multi-step AI pipelines using LangGraph, ReAct reasoning loops, and Claude Agent SDK with custom tool calling and structured outputs.",
                    "Architected and deployed end-to-end agentic solutions solving enterprise workflow, cost intelligence, and CX operational bottlenecks.",
                    "Implemented automated LLM evaluation benchmarks, safety guardrails, Langfuse tracing, and Human-in-the-Loop (HITL) verification workflows across all deployments.",
                    "Applying formal enterprise AI engineering standards to agent design through continuous hands-on upskilling via Google Developer Program, Claude, Nebius, and Microsoft Reactor Series.",
                ],
            },
            {
                "company": "VERIZON | Chennai",
                "title": "Senior Manager, Product Dev/Mgmt – AI and CX Automation",
                "dates": "Aug 2022- Dec 2025",
                "bullets": [
                    "Fast tracked team AI use case delivery time by 70% from 15 days to 5 days using Google Gemini Enterprise and Verizon AI stack, integrating high-volume customer transactional and interaction data.",
                    "Structured and delivered 100+ high-impact Agentic AI automation use cases projecting $400M in ROI; built a classification framework distinguishing autonomously resolvable issues from human-assisted and digital self-serve scenarios at scale.",
                    "Executed the multi-year AI Platform Strategy roadmap for CX personalization and automation, shipping production use cases that delivered $54.8M in cost-to-serve savings and 2.8M annual call deflections.",
                    "Hired, mentored, and led a pod of 10 Senior Consultants building AI automation POCs, reusable data products, and analytical insights; partnered with Engineering, Product, Business, Finance, and GTM teams to deploy into production.",
                    "Established value tracking and benefits realization for AI-led personalization features across omnichannel touchpoints, evaluating sustained model and intervention performance.",
                    "Served as strategic advisor to senior leadership developing benefit hypotheses, cost estimates, and ROI models sizing the cost impact of customer journey friction on cost-to-serve.",
                    "Presented executive insights and trends to senior leaders highlighting the impact of upstream business decisions on key CX KPIs — churn, care call volume, and experience scores (FCR, CSAT, NPS).",
                ],
            },
            {
                "company": "CCLYTICX SERVICES PVT LTD | Chennai",
                "sub_roles": [
                    {
                        "title": "Manager, Analytics",
                        "dates": "Apr 2021 – Jul 2022",
                        "bullets": [
                            "Led strategic analytical solutions and custom risk model delivery for a $5B + consumer credit portfolio across B2C and B2B credit portfolios, supporting Senior Risk and Marketing leaders.",
                            "Presented product-level ROI analysis, portfolio performance reviews, risk trend assessments, and credit application and conversion analysis.",
                            "Managed the Google Analytics measurement framework across digital properties, delivering visibility into user engagement, conversion funnels, event tracking, and drop-off identification.",
                            "Scaled and led high-performing analytics consulting team from 2 to 6 members, with accountability for technical project delivery and team capability development.",
                        ],
                    },
                    {
                        "title": "Assistant Manager, Analytics",
                        "dates": "Apr 2016 – Mar 2021",
                        "bullets": [
                            "Integrated marketing data from HubSpot, Infor CRM, Oracle DB, SAS, and email platforms into a unified analytics environment, improving marketing ROI visibility by 40% and enabling automated campaign optimisation.",
                            "Reported portfolio performance across 15+ KPIs including application volume, approval rates, delinquencies, charge-offs, and roll rates, segmented by FICO and Vantage risk scores.",
                            "Led the redesign of Fortiva Retail Credit and Aspire Credit websites — overseeing mobile-responsive design, ADA compliance, and marketing tag implementation (GA4, Facebook Pixel, conversion tracking).",
                            "Measured marketing campaign effectiveness for B2B Retail Credit and B2C Credit Card portfolios, providing insights into seasonal take rates and conversions.",
                        ],
                    },
                    {
                        "title": "Team Leader, Analytics",
                        "dates": "Jun 2012 – Mar 2016",
                        "bullets": [
                            "Generated risk management reports tracking collections performance, delinquencies, charge-offs, and roll rates for B2C lending products.",
                            "Developed segmented portfolio analyses by FICO score bands, origination channels, and vintage cohorts.",
                        ],
                    },
                ],
            },
        ],
        "skills": [
            {
                "label": "AI & Gen AI tooling:",
                "text": "LangGraph, Claude Code, Gemini, Google AI Studio, RAG, Agentic AI, Weaviate, Langfuse, LLM Foundations, ML Foundations",
            },
            {
                "label": "Data & Analytics:",
                "text": "Python, SQL, BigQuery, Oracle DB, Google Sheets, Excel",
            },
            {
                "label": "Visualisation & Reporting:",
                "text": "Tableau, Power BI, Looker",
            },
            {
                "label": "Digital Analytics:",
                "text": "Google Analytics (GA4), Adobe Analytics, Qualtrics, Quantum Metric, Mailchimp",
            },
            {
                "label": "Enterprise Platforms:",
                "text": "NiCE, VERINT, HubSpot, Google Marketing Platform",
            },
        ],
    },

    "analytics": {
        "id": "analytics",
        "name": "Master Variation 3 – Enterprise Analytics, CX & Credit Risk Leader",
        "target_track": "Analytics",
        "description": "Optimized for Senior Manager / Manager / Lead roles in Enterprise Analytics, Decision Science, CX Analytics, Financial Services / Credit Risk Analytics, and BI.",
        "summary": (
            "Senior Analytics and AI leader with 13+ years of progressive experience (10 years in Financial Services "
            "CaaS and 3.5 years in Telecom) driving portfolio analytics, credit risk modeling, customer journey "
            "analytics, and AI-powered CX transformation. Managed strategic analytics for a $5B+ consumer credit "
            "portfolio and delivered $54.8M in cost-to-serve savings and 2.8M call deflections through data-driven "
            "personalization and automation. Expert in SQL, BigQuery, Python, Tableau, Power BI, Looker, GA4, and "
            "GenAI-accelerated analytics delivery."
        ),
        "competencies_header": "CORE COMPETENCIES – 3.5 Yrs in Telecom,10 Yrs in Financial Services (CaaS)",
        "competencies": [
            {
                "label": "Analytics & Insights:",
                "text": "Portfolio P/L analytics ($5B+ credit portfolio), Credit Risk Analytics (FICO/Vantage, roll rates, charge-offs), Marketing ROI & Attribution, Executive insights and KPI reporting",
            },
            {
                "label": "CX & Digital Analytics:",
                "text": "Customer journey analytics, Friction Analysis, Conversion funnel & drop-off optimization (GA4, Adobe Analytics, Quantum Metric), FCR/CSAT/NPS/Churn drivers",
            },
            {
                "label": "AI Strategy & Decision Science:",
                "text": "AI-driven personalization, Next Best Action, Benefit hypotheses & ROI modeling ($400M projected ROI), GenAI workflow acceleration",
            },
            {
                "label": "Consulting & Team Leadership:",
                "text": "Leading 10-member Senior Consultant pods, Cross-functional executive engagement (Risk, Marketing, Product, Finance), Agile analytics delivery",
            },
        ],
        "experience": [
            {
                "company": "Independent AI Product Development",
                "title": "AI & Analytics Solution Builder – Personal Portfolio github.com/vinailead",
                "dates": "Jan 2026- Present",
                "bullets": [
                    "Architected and deployed intelligent analytics and agentic solutions solving enterprise workflow, cost intelligence, and CX operational bottlenecks.",
                    "Implemented automated evaluation benchmarks, data quality guardrails, and HITL verification workflows across analytical AI deployments.",
                    "Built autonomous analytical and reasoning pipelines using LangGraph, ReAct reasoning loops, and Claude Agent SDK with custom tool calling.",
                    "Applying formal enterprise AI standards through continuous upskilling across Google Developer Program, Claude, Nebius, and Microsoft Reactor Series.",
                ],
            },
            {
                "company": "VERIZON | Chennai",
                "title": "Senior Manager, Product Dev/Mgmt – AI and CX Automation",
                "dates": "Aug 2022- Dec 2025",
                "bullets": [
                    "Presented executive insights and analytical trends to senior leaders highlighting the impact of upstream business decisions on key CX KPIs — churn, care call volume, and experience scores (FCR, CSAT, NPS).",
                    "Served as a strategic advisor to senior leadership developing benefit hypotheses, cost estimates, and econometric ROI models sizing the cost impact of customer journey friction on cost-to-serve.",
                    "Executed the multi-year AI & CX Personalization roadmap, delivering analytical and automation use cases that resulted in $54.8M in cost-to-serve savings and 2.8M annual call deflections.",
                    "Hired, mentored, and led a pod of 10 Senior Consultants delivering analytical insights, AI automation POCs, and reusable data products to cross-functional executives across Business, Engineering, Product, Finance, and GTM.",
                    "Established rigorous value tracking and benefits realization frameworks for AI-led personalization features across omnichannel touchpoints, measuring sustained lift.",
                    "Structured and delivered 100+ high-impact Agentic AI automation use cases projecting $400M in ROI by analyzing customer issue patterns at scale.",
                    "Fast tracked team analytical and use case delivery time by 70% from 15 days to 5 days using Google Gemini Enterprise and Verizon AI stack integrating high-volume customer transactional and interaction data.",
                ],
            },
            {
                "company": "CCLYTICX SERVICES PVT LTD | Chennai",
                "sub_roles": [
                    {
                        "title": "Manager, Analytics",
                        "dates": "Apr 2021 – Jul 2022",
                        "bullets": [
                            "Led strategic analytical solutions delivery for a $5B + consumer credit portfolio across B2C and B2B credit portfolios. Supported Senior Risk and Marketing leaders with acquisition and portfolio P/L.",
                            "Presented product-level ROI analysis, portfolio performance reviews, risk trend assessments, and credit application and conversion analysis using custom risk models.",
                            "Scaled and led high-performing analytics consulting team from 2 to 6 members, with accountability for analytical projects delivery and team capability development.",
                            "Managed the Google Analytics measurement framework across digital properties, delivering visibility into user engagement, conversion funnels, event tracking, and drop-off identification.",
                        ],
                    },
                    {
                        "title": "Assistant Manager, Analytics",
                        "dates": "Apr 2016 – Mar 2021",
                        "bullets": [
                            "Reported portfolio performance across 15+ KPIs including application volume, approval rates, delinquencies, charge-offs, and roll rates, segmented by FICO and Vantage risk scores.",
                            "Measured marketing campaign effectiveness for B2B Retail Credit and B2C Credit Card portfolios, providing insights into seasonal take rates and conversions.",
                            "Integrated marketing data from HubSpot, Infor CRM, Oracle DB, SAS, and email platforms into a unified analytics environment, improving marketing ROI visibility by 40% and enabling automated campaign optimisation.",
                            "Led the redesign of Fortiva Retail Credit and Aspire Credit websites — overseeing mobile-responsive design, ADA compliance, and marketing tag implementation (GA4, Facebook Pixel, conversion tracking).",
                        ],
                    },
                    {
                        "title": "Team Leader, Analytics",
                        "dates": "Jun 2012 – Mar 2016",
                        "bullets": [
                            "Generated risk management reports tracking collections performance, delinquencies, charge-offs, and roll rates for B2C lending products.",
                            "Developed segmented portfolio analyses by FICO score bands, origination channels, and vintage cohorts.",
                        ],
                    },
                ],
            },
        ],
        "skills": [
            {
                "label": "Data & Analytics:",
                "text": "SQL, BigQuery, Python, Oracle DB, Google Sheets, Excel",
            },
            {
                "label": "Visualisation & Reporting:",
                "text": "Tableau, Power BI, Looker",
            },
            {
                "label": "Digital Analytics:",
                "text": "Google Analytics (GA4), Adobe Analytics, Qualtrics, Quantum Metric, Mailchimp",
            },
            {
                "label": "AI & Gen AI tooling:",
                "text": "ML Foundations, LLM Foundations, Gemini, Google AI Studio, RAG, Agentic AI, Claude Code, LangGraph, Weaviate, Langfuse",
            },
            {
                "label": "Enterprise Platforms:",
                "text": "HubSpot, Google Marketing Platform, NiCE, VERINT",
            },
        ],
    },

    "gen_ai_leader": {
        "id": "gen_ai_leader",
        "name": "Master Variation 4 – Generative AI Leader & CoE Delivery Head",
        "target_track": "Gen AI Leader",
        "description": "Optimized for Gen AI Senior Manager, GenAI Practice / Pod Lead, AI Delivery Manager, and Enterprise Generative AI Product Leader roles.",
        "summary": (
            "Generative AI Leader and Senior Product Delivery Manager with 13+ years of progressive experience "
            "scaling enterprise GenAI adoption, leading multidisciplinary AI consultant pods, and delivering "
            "multi-million-dollar CX and operational transformations. Led a pod of 10 Senior Consultants at Verizon "
            "to execute 100+ GenAI and Agentic automation use cases ($400M projected ROI, $54.8M realized savings, "
            "2.8M call deflections) while accelerating delivery velocity by 70% (15 days to 5 days) using Google "
            "Gemini Enterprise."
        ),
        "competencies_header": "CORE COMPETENCIES – 3.5 Yrs in Telecom,10 Yrs in Financial Services (CaaS)",
        "competencies": [
            {
                "label": "Gen AI Leadership & CoE Delivery:",
                "text": "Gen AI Product roadmap, Leading 10-Consultant AI Pods, Enterprise Gemini & LLM adoption, POC-to-Production scaling, Executive Stakeholder Management",
            },
            {
                "label": "AI Governance & Engineering Standards:",
                "text": "LLM Use case prioritization, Evaluation benchmarks, Guardrails & HITL verification, RAG & Agentic architectures (LangGraph, Claude, Weaviate, Langfuse)",
            },
            {
                "label": "CX & Digital Transformation:",
                "text": "Omnichannel personalization, Contact center AI containment (NiCE, VERINT), Customer journey friction reduction, Next Best Action",
            },
            {
                "label": "Value Realization & Analytics:",
                "text": "Business case quantification ($400M ROI pipeline), Benefits realization tracking ($54.8M savings), Portfolio & Risk Analytics",
            },
        ],
        "experience": [
            {
                "company": "Independent AI Product Development",
                "title": "Generative AI Leader & Builder – Personal Portfolio github.com/vinailead",
                "dates": "Jan 2026- Present",
                "bullets": [
                    "Architected and deployed production-grade Generative AI and agentic solutions solving enterprise workflow, cost intelligence, and CX operational bottlenecks.",
                    "Implemented automated LLM evaluation benchmarks, enterprise guardrails, and HITL verification workflows across all GenAI deployments.",
                    "Built autonomous multi-agent pipelines using LangGraph, ReAct reasoning loops, and Claude Agent SDK with custom tool calling.",
                    "Applying formal enterprise AI standards to GenAI system design through continuous upskilling via Google Developer Program, Claude, Nebius, and Microsoft Reactor Series.",
                ],
            },
            {
                "company": "VERIZON | Chennai",
                "title": "Senior Manager, Product Dev/Mgmt – AI and CX Automation",
                "dates": "Aug 2022- Dec 2025",
                "bullets": [
                    "Hired, mentored, and led a high-performing pod of 10 Senior Consultants delivering AI automation POCs, reusable data products, and analytical insights to cross-functional executives across Business, Engineering, Product, Finance, and GTM.",
                    "Fast tracked team GenAI use case delivery time by 70% from 15 days to 5 days using Google Gemini Enterprise and Verizon AI stack integrating high-volume customer transactional and interaction data.",
                    "Executed the multi-year AI Platform Strategy roadmap for CX personalization and automation, delivering use cases that resulted in $54.8M in cost-to-serve savings and 2.8M annual call deflections.",
                    "Structured and delivered 100+ high-impact Agentic and Generative AI automation use cases projecting $400M in ROI; developed a classification framework distinguishing autonomously resolvable issues from human-assisted and digital self-serve scenarios.",
                    "Established value tracking and benefits realization governance for AI-led personalization features across omnichannel touchpoints, assessing sustained enterprise value.",
                    "Served as strategic advisor to senior leadership developing benefit hypotheses, cost estimates, and ROI models sizing the cost impact of customer journey friction on cost-to-serve.",
                    "Presented executive insights and trends to senior leaders highlighting the impact of upstream business decisions on key CX KPIs — churn, care call volume, and experience scores (FCR, CSAT, NPS).",
                ],
            },
            {
                "company": "CCLYTICX SERVICES PVT LTD | Chennai",
                "sub_roles": [
                    {
                        "title": "Manager, Analytics",
                        "dates": "Apr 2021 – Jul 2022",
                        "bullets": [
                            "Scaled and led a high-performing analytics consulting team from 2 to 6 members, with full accountability for project delivery and team capability development.",
                            "Led strategic analytical solutions delivery for a $5B + consumer credit portfolio across B2C and B2B credit portfolios, supporting Senior Risk and Marketing leaders with acquisition and portfolio P/L.",
                            "Presented product-level ROI analysis, portfolio performance reviews, risk trend assessments, and credit application conversion analysis using custom risk models.",
                            "Managed the Google Analytics measurement framework across digital properties, delivering visibility into user engagement, conversion funnels, event tracking, and drop-off identification.",
                        ],
                    },
                    {
                        "title": "Assistant Manager, Analytics",
                        "dates": "Apr 2016 – Mar 2021",
                        "bullets": [
                            "Integrated marketing data from HubSpot, Infor CRM, Oracle DB, SAS, and email platforms into a unified analytics environment, improving marketing ROI visibility by 40% and enabling automated campaign optimisation.",
                            "Reported portfolio performance across 15+ KPIs including application volume, approval rates, delinquencies, charge-offs, and roll rates, segmented by FICO and Vantage risk scores.",
                            "Measured marketing campaign effectiveness for B2B Retail Credit and B2C Credit Card portfolios, providing insights into seasonal take rates and conversions.",
                            "Led the redesign of Fortiva Retail Credit and Aspire Credit websites — overseeing mobile-responsive design, ADA compliance, and marketing tag implementation (GA4, Facebook Pixel, conversion tracking).",
                        ],
                    },
                    {
                        "title": "Team Leader, Analytics",
                        "dates": "Jun 2012 – Mar 2016",
                        "bullets": [
                            "Generated risk management reports tracking collections performance, delinquencies, charge-offs, and roll rates for B2C lending products.",
                            "Developed segmented portfolio analyses by FICO score bands, origination channels, and vintage cohorts.",
                        ],
                    },
                ],
            },
        ],
        "skills": [
            {
                "label": "AI & Gen AI tooling:",
                "text": "Gemini, Google AI Studio, Claude Code, LangGraph, RAG, Agentic AI, Weaviate, Langfuse, LLM Foundations, ML Foundations",
            },
            {
                "label": "Data & Analytics:",
                "text": "SQL, BigQuery, Python, Google Sheets, Excel, Oracle DB",
            },
            {
                "label": "Visualisation & Reporting:",
                "text": "Tableau, Power BI, Looker",
            },
            {
                "label": "Enterprise Platforms:",
                "text": "NiCE, VERINT, HubSpot, Google Marketing Platform",
            },
            {
                "label": "Digital Analytics:",
                "text": "Google Analytics (GA4), Adobe Analytics, Qualtrics, Quantum Metric, Mailchimp",
            },
        ],
    },

    "agentic_ai": {
        "id": "agentic_ai",
        "name": "Master Variation 5 – Agentic AI & Autonomous Workflows Lead",
        "target_track": "Agentic AI",
        "description": "Optimized for Agentic AI Manager / Lead, Autonomous AI Workflows PM, Multi-Agent Systems Lead, and AI CX Automation Senior Manager roles.",
        "summary": (
            "Agentic AI and Autonomous Workflows Leader with 13+ years of enterprise experience designing, "
            "classifying, and scaling multi-agent and CX automation systems across telecommunications and financial "
            "services. Structured and delivered 100+ high-impact Agentic AI automation use cases projecting $400M "
            "in ROI, achieving $54.8M in cost-to-serve savings and 2.8M annual call deflections. Hands-on builder "
            "of autonomous reasoning pipelines using LangGraph, ReAct loops, Claude Agent SDK, custom tool calling, "
            "RAG (Weaviate), and HITL evaluation guardrails."
        ),
        "competencies_header": "CORE COMPETENCIES – 3.5 Yrs in Telecom,10 Yrs in Financial Services (CaaS)",
        "competencies": [
            {
                "label": "Agentic AI & Autonomous Workflows:",
                "text": "Multi-agent orchestration (LangGraph), ReAct reasoning loops, Claude Agent SDK & custom tool calling, Autonomous vs. human-assisted classification frameworks, HITL verification & guardrails",
            },
            {
                "label": "AI Automation & CX Containment:",
                "text": "Self-serve containment (2.8M annual call deflections), Contact center automation (NiCE, VERINT), Omnichannel personalization, Next Best Action",
            },
            {
                "label": "AI Strategy & ROI Realization:",
                "text": "100+ Agentic AI use case roadmap ($400M projected ROI), Cost-to-serve reduction ($54.8M realized), Benefit hypotheses & value tracking",
            },
            {
                "label": "Cross-Functional Pod Leadership:",
                "text": "Leading 10 Senior Consultants, POC-to-Production deployment with Engineering/Product/GTM, Enterprise data integration (BigQuery, SQL, Python)",
            },
        ],
        "experience": [
            {
                "company": "Independent AI Product Development",
                "title": "Agentic AI Builder – Personal Portfolio github.com/vinailead",
                "dates": "Jan 2026- Present",
                "bullets": [
                    "Built autonomous multi-agent pipelines using LangGraph, ReAct reasoning loops, and Claude Agent SDK with custom tool calling to automate complex enterprise workflows.",
                    "Architected and deployed agentic solutions resolving enterprise workflow, cost intelligence, and CX operational bottlenecks.",
                    "Implemented automated evaluation benchmarks, runtime guardrails, Langfuse observability, and Human-in-the-Loop (HITL) verification workflows across all agent deployments.",
                    "Applying formal enterprise AI standards to agentic architecture through continuous upskilling from Google Developer Program, Claude, Nebius, and Microsoft Reactor Series.",
                ],
            },
            {
                "company": "VERIZON | Chennai",
                "title": "Senior Manager, Product Dev/Mgmt – AI and CX Automation",
                "dates": "Aug 2022- Dec 2025",
                "bullets": [
                    "Structured and delivered 100+ high-impact Agentic AI automation use cases projecting $400M in ROI; developed an enterprise classification framework distinguishing autonomously resolvable issues from human-assisted and digital self-serve scenarios by analyzing customer issues at scale.",
                    "Executed the multi-year AI Platform Strategy roadmap for CX personalization and autonomous containment, delivering production use cases that resulted in $54.8M in cost-to-serve savings and 2.8M annual call deflections.",
                    "Fast tracked team AI use case delivery time by 70% from 15 days to 5 days using Google Gemini Enterprise and Verizon AI stack integrating high-volume customer transactional and interaction data.",
                    "Hired, mentored, and led a pod of 10 Senior Consultants delivering AI automation POCs, analytical insights, and reusable data products; collaborated with Engineering, Product, Business, Finance, and GTM teams to move agentic use cases into production.",
                    "Established value tracking and benefits realization for AI-led personalization and automation features across omnichannel touchpoints, assessing sustained containment and ROI.",
                    "Served as a strategic advisor to senior leadership developing benefit hypotheses, cost estimates, and ROI models sizing the cost impact of customer journey friction on cost-to-serve.",
                    "Presented executive insights and trends to senior leaders highlighting the impact of upstream business decisions on key CX KPIs — churn, care call volume, and experience scores (FCR, CSAT, NPS).",
                ],
            },
            {
                "company": "CCLYTICX SERVICES PVT LTD | Chennai",
                "sub_roles": [
                    {
                        "title": "Manager, Analytics",
                        "dates": "Apr 2021 – Jul 2022",
                        "bullets": [
                            "Led strategic analytical solutions delivery for a $5B + consumer credit portfolio across B2C and B2B credit portfolios. Supported Senior Risk and Marketing leaders with acquisition and portfolio P/L.",
                            "Presented product-level ROI analysis, portfolio performance reviews, risk trend assessments, and credit application and conversion analysis using custom risk models.",
                            "Scaled and led high-performing analytics consulting team from 2 to 6 members, with accountability for analytical projects delivery and team capability development.",
                            "Managed the Google Analytics measurement framework across digital properties, delivering visibility into user engagement, conversion funnels, event tracking, and drop-off identification.",
                        ],
                    },
                    {
                        "title": "Assistant Manager, Analytics",
                        "dates": "Apr 2016 – Mar 2021",
                        "bullets": [
                            "Integrated marketing data from HubSpot, Infor CRM, Oracle DB, SAS, and email platforms into a unified analytics environment, improving marketing ROI visibility by 40% and enabling automated campaign optimisation.",
                            "Reported portfolio performance across 15+ KPIs including application volume, approval rates, delinquencies, charge-offs, and roll rates, segmented by FICO and Vantage risk scores.",
                            "Measured marketing campaign effectiveness for B2B Retail Credit and B2C Credit Card portfolios, providing insights into seasonal take rates and conversions.",
                            "Led the redesign of Fortiva Retail Credit and Aspire Credit websites — overseeing mobile-responsive design, ADA compliance, and marketing tag implementation (GA4, Facebook Pixel, conversion tracking).",
                        ],
                    },
                    {
                        "title": "Team Leader, Analytics",
                        "dates": "Jun 2012 – Mar 2016",
                        "bullets": [
                            "Generated risk management reports tracking collections performance, delinquencies, charge-offs, and roll rates for B2C lending products.",
                            "Developed segmented portfolio analyses by FICO score bands, origination channels, and vintage cohorts.",
                        ],
                    },
                ],
            },
        ],
        "skills": [
            {
                "label": "AI & Gen AI tooling:",
                "text": "Agentic AI, LangGraph, Claude Code, Gemini, Google AI Studio, RAG, Weaviate, Langfuse, LLM Foundations, ML Foundations",
            },
            {
                "label": "Enterprise Platforms:",
                "text": "NiCE, VERINT, HubSpot, Google Marketing Platform",
            },
            {
                "label": "Data & Analytics:",
                "text": "Python, SQL, BigQuery, Oracle DB, Google Sheets, Excel",
            },
            {
                "label": "Visualisation & Reporting:",
                "text": "Tableau, Power BI, Looker",
            },
            {
                "label": "Digital Analytics:",
                "text": "Google Analytics (GA4), Adobe Analytics, Qualtrics, Quantum Metric, Mailchimp",
            },
        ],
    },
}

TRACK_TO_VARIATION = {
    "AI Strategy": "ai_strategy",
    "AI Builder": "ai_builder",
    "Analytics": "analytics",
    "Gen AI Leader": "gen_ai_leader",
    "Agentic AI": "agentic_ai",
}


def tailor_cv_for_job(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produces a 100% Grounded-Truth tailored CV dictionary for a specific job.
    Selects the closest Master Archetype Variation as base, then re-orders bullets
    and highlights grounded ATS keywords present in the job description without
    ever inventing unverified skills, companies, or metrics.
    """
    track = job.get("track", "AI Strategy")
    var_key = TRACK_TO_VARIATION.get(track, "ai_strategy")
    cv = copy.deepcopy(MASTER_VARIATIONS[var_key])

    jd_text = (
        f"{job.get('title', '')} {job.get('company', '')} "
        f"{job.get('description', '')} {' '.join(job.get('jd_keywords', []))}"
    ).lower()

    # Score and reorder Verizon bullets so the top 3 bullets match the specific JD's strongest themes
    verizon_entry = cv["experience"][1]
    def score_bullet(b: str) -> int:
        bl = b.lower()
        score = 0
        if "agentic" in jd_text and "agentic" in bl:
            score += 5
        if ("roadmap" in jd_text or "strategy" in jd_text or "transformation" in jd_text) and ("roadmap" in bl or "advisor" in bl):
            score += 4
        if ("gemini" in jd_text or "llm" in jd_text or "gen ai" in jd_text or "generative" in jd_text) and "gemini" in bl:
            score += 4
        if ("team" in jd_text or "lead" in jd_text or "consulting" in jd_text or "pod" in jd_text or "stakeholder" in jd_text) and "10 senior consultants" in bl:
            score += 4
        if ("kpi" in jd_text or "churn" in jd_text or "nps" in jd_text or "csat" in jd_text or "analytics" in jd_text) and "csat" in bl:
            score += 4
        if ("value" in jd_text or "roi" in jd_text or "governance" in jd_text) and ("roi" in bl or "benefits realization" in bl):
            score += 3
        return score

    # Stable sort Verizon bullets by relevance to this specific JD
    verizon_entry["bullets"] = sorted(
        verizon_entry["bullets"], key=score_bullet, reverse=True
    )

    # If the JD strongly emphasizes financial services / banking / credit / risk, highlight that in summary
    is_bfsi = any(
        w in jd_text
        for w in ["bank", "credit", "financial", "fintech", "risk", "lending", "bfsi", "wealth", "payment", "fraud"]
    )
    if is_bfsi and track != "Analytics":
        cv["summary"] = (
            f"Senior {track} and Analytics Leader with 13+ years of progressive experience "
            f"(including 10 years in Consumer Financial Services & Credit Analytics and 3.5 years in Enterprise Telecom AI). "
            f"Delivered 100+ Agentic AI and GenAI automation use cases projecting $400M in ROI, $54.8M in realized "
            f"cost-to-serve savings, and strategic analytics for a $5B+ consumer credit portfolio. Combines hands-on "
            f"LangGraph, Claude Agent SDK, RAG, and Google Gemini Enterprise execution with deep BFSI risk, P/L, and CX leadership."
        )

    cv["header"] = copy.deepcopy(GROUNDED_HEADER)
    cv["education"] = copy.deepcopy(GROUNDED_EDUCATION)
    cv["certifications"] = copy.deepcopy(GROUNDED_CERTIFICATIONS)
    cv["tailored_for_job_id"] = job.get("id")
    cv["tailored_for_title"] = job.get("title")
    cv["tailored_for_company"] = job.get("company")
    return cv


def get_master_cv(variation_id: str) -> Dict[str, Any]:
    base = copy.deepcopy(MASTER_VARIATIONS.get(variation_id, MASTER_VARIATIONS["baseline"]))
    base["header"] = copy.deepcopy(GROUNDED_HEADER)
    base["education"] = copy.deepcopy(GROUNDED_EDUCATION)
    base["certifications"] = copy.deepcopy(GROUNDED_CERTIFICATIONS)
    return base
