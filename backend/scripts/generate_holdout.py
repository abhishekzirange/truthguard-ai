import json
import os

HOLDOUT_CLAIMS = [
    # ==========================================
    # 1. SOFTWARE VERSIONS / APIS (20 Claims)
    # ==========================================
    {
        "id": "holdout-001",
        "claim_text": "Django 3.2 is the latest stable release of the Django web framework.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://docs.djangoproject.com/en/dev/releases/",
        "rationale": "Django 3.2 reached End of Life in April 2024. Django 5.1/5.2 is the modern stable release series."
    },
    {
        "id": "holdout-002",
        "claim_text": "Django 5.1 is an active supported release of the Django framework.",
        "category": "software_version",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.djangoproject.com/download/",
        "rationale": "Django 5.1 was released in August 2024 and is currently receiving active bug fixes."
    },
    {
        "id": "holdout-003",
        "claim_text": "Rust 1.50 is the newest stable Rust compiler release available from Mozilla and the Rust Foundation.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://blog.rust-lang.org/",
        "rationale": "Rust 1.50 was released in February 2021. Rust is now on the 1.84+ series."
    },
    {
        "id": "holdout-004",
        "claim_text": "Rust 1.84 is a released stable version of the Rust programming language compiler.",
        "category": "software_version",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://github.com/rust-lang/rust/releases",
        "rationale": "Rust 1.84 was officially released to stable channels in early 2025."
    },
    {
        "id": "holdout-005",
        "claim_text": "Go 1.16 is the current active release of Go supported by the Go team.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://go.dev/doc/devel/release",
        "rationale": "Go 1.16 reached EOL in 2022. Go maintains support only for the two most recent major releases (Go 1.23/1.24)."
    },
    {
        "id": "holdout-006",
        "claim_text": "Go 1.23 is an active release of the Go programming language.",
        "category": "software_version",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://go.dev/doc/devel/release",
        "rationale": "Go 1.23 was released in August 2024 and is actively supported."
    },
    {
        "id": "holdout-007",
        "claim_text": "Ruby 2.7 is currently receiving regular security maintenance updates from the Ruby core team.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.ruby-lang.org/en/downloads/branches/",
        "rationale": "Ruby 2.7 reached EOL on March 31, 2023. Ruby 3.2, 3.3, and 3.4 are the supported branches."
    },
    {
        "id": "holdout-008",
        "claim_text": "Ruby 3.3 is an officially supported stable release of the Ruby language.",
        "category": "software_version",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.ruby-lang.org/en/news/2023/12/25/ruby-3-3-0-released/",
        "rationale": "Ruby 3.3.0 was released on December 25, 2023 and receives active maintenance."
    },
    {
        "id": "holdout-009",
        "claim_text": "Angular 12 is the latest major Angular version supported by Google.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://angular.dev/reference/releases",
        "rationale": "Angular 12 was released in May 2021 and its LTS ended in November 2022. Angular 18/19 are current."
    },
    {
        "id": "holdout-010",
        "claim_text": "Angular 18 introduced experimental support for zoneless change detection in Angular applications.",
        "category": "software_version",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://blog.angular.dev/angular-v18-is-now-available-e79d5f0270b8",
        "rationale": "Angular 18 officially introduced zoneless change detection via provideExperimentalZonelessChangeDetection in May 2024."
    },
    {
        "id": "holdout-011",
        "claim_text": "Vue 2 is the default version recommended for new projects created with the Vue CLI.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://v2.vuejs.org/lts/",
        "rationale": "Vue 2 reached official End of Life on December 31, 2023. Vue 3 is the default."
    },
    {
        "id": "holdout-012",
        "claim_text": "Vue 3 is the default standard production version of the Vue.js frontend framework.",
        "category": "software_version",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://vuejs.org/",
        "rationale": "Vue 3 has been the official default production version of Vue since February 2022."
    },
    {
        "id": "holdout-013",
        "claim_text": "Kubernetes 1.18 is currently supported with regular patch releases by the CNCF.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://kubernetes.io/releases/",
        "rationale": "Kubernetes 1.18 reached end of life in 2021. Kubernetes maintains support only for the last 3 minor versions."
    },
    {
        "id": "holdout-014",
        "claim_text": "Kubernetes 1.31 is an active production release of Kubernetes.",
        "category": "software_version",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://kubernetes.io/blog/2024/08/13/kubernetes-1-31-release/",
        "rationale": "Kubernetes 1.31 (Elli) was released in August 2024 and is under active community support."
    },
    {
        "id": "holdout-015",
        "claim_text": "Spring Boot 2.5 is the active production generation supported under open source licensing by VMware.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://spring.io/projects/spring-boot#support",
        "rationale": "Spring Boot 2.x OSS support ended in November 2023. Spring Boot 3.x is the active generation."
    },
    {
        "id": "holdout-016",
        "claim_text": "Spring Boot 3.3 is an actively maintained production release of Spring Boot.",
        "category": "software_version",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://spring.io/blog/2024/05/23/spring-boot-3-3-0-available-now",
        "rationale": "Spring Boot 3.3.0 was released in May 2024 and is supported until May 2025."
    },
    {
        "id": "holdout-017",
        "claim_text": "Terraform 0.12 is the latest stable HashiCorp Terraform release recommended for production infrastructure.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://github.com/hashicorp/terraform/releases",
        "rationale": "Terraform 0.12 was released in 2019. Modern Terraform is on version 1.9+."
    },
    {
        "id": "holdout-018",
        "claim_text": "Apache Spark 2.4 is the active mainline Spark version supported for modern lakehouses.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://spark.apache.org/releases/",
        "rationale": "Apache Spark 2.4 is deprecated and EOL. Spark 3.4 and 3.5 are current."
    },
    {
        "id": "holdout-019",
        "claim_text": "Linux kernel 2.6 is the current mainline kernel branch maintained by Linus Torvalds.",
        "category": "software_version",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://kernel.org/",
        "rationale": "Linux 2.6 reached EOL over a decade ago. Mainline Linux is on the 6.x kernel series."
    },
    {
        "id": "holdout-020",
        "claim_text": "Python 4.0 was released in 2024 with mandatory static typing and removed backwards compatibility.",
        "category": "software_version",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://peps.python.org/",
        "rationale": "Python 4.0 does not exist. Guido van Rossum and the Python Steering Council have confirmed Python will remain on 3.x."
    },

    # ==========================================
    # 2. PRODUCT PRICING (20 Claims)
    # ==========================================
    {
        "id": "holdout-021",
        "claim_text": "Anthropic Claude 3 Opus costs $15.00 per 1 million input tokens and $75.00 per 1 million output tokens.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.anthropic.com/pricing",
        "rationale": "Official Anthropic API pricing for Claude 3 Opus is exactly $15/1M input and $75/1M output."
    },
    {
        "id": "holdout-022",
        "claim_text": "Anthropic Claude 3.5 Sonnet costs $3.00 per 1 million input tokens and $15.00 per 1 million output tokens.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.anthropic.com/pricing",
        "rationale": "Official Anthropic API pricing for Claude 3.5 Sonnet is $3.00/1M input and $15.00/1M output."
    },
    {
        "id": "holdout-023",
        "claim_text": "OpenAI GPT-4 original launch pricing in 2023 was $0.03 per 1,000 prompt tokens.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://openai.com/pricing",
        "rationale": "Historical statement of original launch pricing for gpt-4 8k context in early 2023 was accurately $0.03/1k tokens."
    },
    {
        "id": "holdout-024",
        "claim_text": "OpenAI GPT-4o standard API pricing is $2.50 per 1 million input tokens and $10.00 per 1 million output tokens.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://openai.com/api/pricing/",
        "rationale": "Following the August 2024 price drop, GPT-4o is priced at $2.50/1M input and $10.00/1M output."
    },
    {
        "id": "holdout-025",
        "claim_text": "GitHub Copilot Individual subscription costs $10 per month or $100 per year.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://github.com/features/copilot/plans",
        "rationale": "GitHub Copilot Individual pricing remains $10 monthly or $100 annually."
    },
    {
        "id": "holdout-026",
        "claim_text": "Twitter Blue subscription costs $1 per year for all verified accounts.",
        "category": "pricing",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://help.twitter.com/en/using-x/x-premium",
        "rationale": "X Premium costs $3/mo (Basic) or $8/mo (Premium); $1/year is false."
    },
    {
        "id": "holdout-027",
        "claim_text": "Netflix Standard subscription in the United States currently costs $7.99 per month with no price increases since 2014.",
        "category": "pricing",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://help.netflix.com/en/node/24926",
        "rationale": "Netflix Standard in the US costs $15.49/mo; $7.99 was the 2014 price and has increased multiple times."
    },
    {
        "id": "holdout-028",
        "claim_text": "Spotify Premium Individual subscription in the US is $11.99 per month.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.spotify.com/us/premium/",
        "rationale": "Spotify raised the US Individual price to $11.99 in July 2024."
    },
    {
        "id": "holdout-029",
        "claim_text": "Amazon Prime annual membership in the United States costs $139 per year.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://www.amazon.com/amazonprime",
        "rationale": "Amazon Prime annual membership fee is $139 (raised from $119 in 2022)."
    },
    {
        "id": "holdout-030",
        "claim_text": "AWS S3 Standard storage in the us-east-1 region costs approximately $0.023 per GB for the first 50 TB per month.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://aws.amazon.com/s3/pricing/",
        "rationale": "AWS S3 Standard pricing tier is $0.023 per GB-month for first 50 TB in us-east-1."
    },
    {
        "id": "holdout-031",
        "claim_text": "Heroku offers a permanently free tier for web dynos and Postgres databases for all users.",
        "category": "pricing",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://blog.heroku.com/next-chapter",
        "rationale": "Heroku eliminated all free product plans and free Dynos on November 28, 2022."
    },
    {
        "id": "holdout-032",
        "claim_text": "OpenAI GPT-4o mini API pricing is $0.15 per 1 million input tokens and $0.60 per 1 million output tokens.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://openai.com/api/pricing/",
        "rationale": "GPT-4o mini was released at $0.15/1M prompt tokens and $0.60/1M completion tokens."
    },
    {
        "id": "holdout-033",
        "claim_text": "Databricks compute costs exactly $0.000001 per hour flat for all cluster sizes.",
        "category": "pricing",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://www.databricks.com/product/pricing",
        "rationale": "Databricks charges in DBU units ranging from $0.07 to $0.55+ per DBU depending on tier."
    },
    {
        "id": "holdout-034",
        "claim_text": "Google Workspace Business Starter costs $6 per user per month with a one-year commitment.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://workspace.google.com/pricing",
        "rationale": "Business Starter pricing is $6/user/month with standard 1-year contract."
    },
    {
        "id": "holdout-035",
        "claim_text": "Docker Desktop requires a commercial paid subscription for companies with more than 250 employees or $10 million in revenue.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.docker.com/pricing/faq/",
        "rationale": "Effective January 31, 2022, Docker requires paid licenses for organizations above those thresholds."
    },
    {
        "id": "holdout-036",
        "claim_text": "Figma provides a free Starter plan with up to 3 collaborative Figma files.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://www.figma.com/pricing/",
        "rationale": "Figma Starter tier includes 3 Figma and 3 FigJam files for free."
    },
    {
        "id": "holdout-037",
        "claim_text": "Slack Pro plan is $8.75 per active user per month when billed monthly.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://slack.com/pricing",
        "rationale": "Slack Pro is $8.75/user/month billed monthly ($7.25 billed annually)."
    },
    {
        "id": "holdout-038",
        "claim_text": "Midjourney Basic plan costs $10 per month.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://docs.midjourney.com/docs/plans",
        "rationale": "Midjourney Basic membership is $10 per month."
    },
    {
        "id": "holdout-039",
        "claim_text": "Vercel Pro team subscription costs $20 per team member per month.",
        "category": "pricing",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://vercel.com/pricing",
        "rationale": "Vercel Pro plan is $20/seat/month."
    },
    {
        "id": "holdout-040",
        "claim_text": "Snowflake cloud compute pricing will drop by exactly 98% across all cloud regions next Monday.",
        "category": "pricing",
        "ground_truth_verdict": "UNVERIFIED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.snowflake.com/pricing/",
        "rationale": "Unverified speculation with zero official corporate confirmation or pricing schedule."
    },

    # ==========================================
    # 3. REGULATIONS & STATUTORY POLICIES (15 Claims)
    # ==========================================
    {
        "id": "holdout-041",
        "claim_text": "The EU Artificial Intelligence Act entered into legal force in August 2024.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai",
        "rationale": "Regulation (EU) 2024/1689 entered into force on August 1, 2024."
    },
    {
        "id": "holdout-042",
        "claim_text": "The California Consumer Privacy Act was completely repealed and declared unconstitutional in 2023.",
        "category": "regulation",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://oag.ca.gov/privacy/ccpa",
        "rationale": "CCPA was not repealed; it was expanded and reinforced by Proposition 24 (CPRA)."
    },
    {
        "id": "holdout-043",
        "claim_text": "Under GDPR Article 83, maximum administrative fines can reach up to 20 million euros or 4% of worldwide annual turnover.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://gdpr-info.eu/art-83-gdpr/",
        "rationale": "Statutory text of GDPR Article 83(5) establishes the 20M EUR or 4% global turnover cap."
    },
    {
        "id": "holdout-044",
        "claim_text": "The US Federal Reserve mandates that all software developers store private keys on paper certificates inside Fort Knox.",
        "category": "regulation",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.federalreserve.gov/",
        "rationale": "Fabricated absurd statutory assertion with zero legal foundation."
    },
    {
        "id": "holdout-045",
        "claim_text": "Section 230 of the Communications Decency Act provides protection from liability for third-party user content on interactive computer services.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://www.law.cornell.edu/uscode/text/47/230",
        "rationale": "47 U.S. Code Section 230 remains active federal law in the United States."
    },
    {
        "id": "holdout-046",
        "claim_text": "The EU Digital Markets Act designated Alphabet, Amazon, Apple, ByteDance, Meta, and Microsoft as gatekeepers.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://ec.europa.eu/commission/presscorner/detail/en/ip_23_4328",
        "rationale": "European Commission formally designated these six gatekeepers under the DMA in September 2023."
    },
    {
        "id": "holdout-047",
        "claim_text": "The US Corporate Transparency Act requires reporting companies to file beneficial ownership information reports with FinCEN.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.fincen.gov/boi",
        "rationale": "The CTA beneficial ownership filing requirements took effect January 1, 2024."
    },
    {
        "id": "holdout-048",
        "claim_text": "The UK GDPR governs data protection compliance for UK businesses following the departure from the EU.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/",
        "rationale": "UK GDPR incorporated GDPR provisions into domestic law via the Data Protection Act 2018."
    },
    {
        "id": "holdout-049",
        "claim_text": "The US Securities and Exchange Commission approved the listing of spot Bitcoin exchange-traded products in January 2024.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.sec.gov/newsroom/press-releases/2024-4",
        "rationale": "The SEC approved 11 spot Bitcoin ETP applications on January 10, 2024."
    },
    {
        "id": "holdout-050",
        "claim_text": "The US SEC approved spot Ethereum exchange-traded products in 2024.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.sec.gov/",
        "rationale": "The SEC approved 19b-4 filings in May 2024 and final registration statements in July 2024."
    },
    {
        "id": "holdout-051",
        "claim_text": "The US Federal Trade Commission issued a final rule banning non-compete agreements nationwide in April 2024.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.ftc.gov/news-events/news/press-releases/2024/04/ftc-announces-rule-banning-noncompetes",
        "rationale": "The FTC issued its final Non-Compete Clause Rule on April 23, 2024 (facing federal court challenges)."
    },
    {
        "id": "holdout-052",
        "claim_text": "HIPAA privacy regulations apply strictly to console video game achievements and player scores.",
        "category": "regulation",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.hhs.gov/hipaa/for-professionals/privacy/index.html",
        "rationale": "HIPAA applies to covered health entities and business associates, not video game scores."
    },
    {
        "id": "holdout-053",
        "claim_text": "China's Personal Information Protection Law took effect on November 1, 2021.",
        "category": "regulation",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "http://www.npc.gov.cn/",
        "rationale": "PIPL was passed in August 2021 and became effective November 1, 2021."
    },
    {
        "id": "holdout-054",
        "claim_text": "The European Union permanently abolished all corporate income tax and VAT in all member nations in 2024.",
        "category": "regulation",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://taxation-customs.ec.europa.eu/taxation_en",
        "rationale": "Fabricated claim; VAT and corporate taxes remain fully active across all EU member states."
    },
    {
        "id": "holdout-055",
        "claim_text": "An upcoming secret international treaty will ban all private programming in Python starting next month.",
        "category": "regulation",
        "ground_truth_verdict": "UNVERIFIED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.un.org/",
        "rationale": "Fictitious, unverified regulatory prediction."
    },

    # ==========================================
    # 4. COMPANY INFORMATION & LEADERSHIP (15 Claims)
    # ==========================================
    {
        "id": "holdout-056",
        "claim_text": "Brian Niccol was appointed Chairman and CEO of Starbucks in September 2024.",
        "category": "company_info",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://stories.starbucks.com/press/2024/starbucks-names-brian-niccol-as-chairman-and-ceo/",
        "rationale": "Brian Niccol officially assumed the role of Chairman and CEO of Starbucks on September 9, 2024."
    },
    {
        "id": "holdout-057",
        "claim_text": "Laxman Narasimhan currently serves as the active Chief Executive Officer of Starbucks.",
        "category": "company_info",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://stories.starbucks.com/press/2024/starbucks-names-brian-niccol-as-chairman-and-ceo/",
        "rationale": "Laxman Narasimhan stepped down from Starbucks in August 2024."
    },
    {
        "id": "holdout-058",
        "claim_text": "Microsoft acquired Activision Blizzard in a $69 billion deal that closed in October 2023.",
        "category": "company_info",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://news.microsoft.com/2023/10/13/microsoft-completes-acquisition-of-activision-blizzard/",
        "rationale": "Microsoft officially closed its acquisition of Activision Blizzard on October 13, 2023."
    },
    {
        "id": "holdout-059",
        "claim_text": "Microsoft's planned acquisition of Activision Blizzard was permanently abandoned due to regulatory injunctions.",
        "category": "company_info",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://news.microsoft.com/2023/10/13/microsoft-completes-acquisition-of-activision-blizzard/",
        "rationale": "Contradicted by historical fact; the acquisition successfully closed in October 2023."
    },
    {
        "id": "holdout-060",
        "claim_text": "OpenAI was originally founded as a non-profit artificial intelligence research organization in December 2015.",
        "category": "company_info",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://openai.com/about/",
        "rationale": "OpenAI was founded in December 2015 by Sam Altman, Elon Musk, Greg Brockman, Ilya Sutskever, and others."
    },
    {
        "id": "holdout-061",
        "claim_text": "Alphabet Inc. was established in 2015 as the parent holding company of Google.",
        "category": "company_info",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://abc.xyz/",
        "rationale": "Larry Page announced Alphabet Inc. restructuring on August 10, 2015."
    },
    {
        "id": "holdout-062",
        "claim_text": "Satya Nadella is the Chairman and Chief Executive Officer of Microsoft.",
        "category": "company_info",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://news.microsoft.com/exec/satya-nadella/",
        "rationale": "Satya Nadella has been CEO since February 2014 and Chairman since June 2021."
    },
    {
        "id": "holdout-063",
        "claim_text": "Steve Ballmer currently serves as the active CEO of Microsoft managing daily software operations.",
        "category": "company_info",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://news.microsoft.com/",
        "rationale": "Steve Ballmer retired as Microsoft CEO in February 2014."
    },
    {
        "id": "holdout-064",
        "claim_text": "Jeff Bezos currently serves as the Chief Executive Officer of Amazon.",
        "category": "company_info",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.aboutamazon.com/news/company-news/andy-jassy-becomes-ceo-of-amazon",
        "rationale": "Jeff Bezos transitioned to Executive Chair in July 2021; Andy Jassy is CEO."
    },
    {
        "id": "holdout-065",
        "claim_text": "Andy Jassy is the Chief Executive Officer of Amazon.",
        "category": "company_info",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.aboutamazon.com/our-company/leadership/andy-jassy",
        "rationale": "Andy Jassy became President and CEO of Amazon on July 5, 2021."
    },
    {
        "id": "holdout-066",
        "claim_text": "Broadcom completed its acquisition of VMware in November 2023.",
        "category": "company_info",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.broadcom.com/company/news/financial-releases/61581",
        "rationale": "Broadcom closed its $69 billion acquisition of VMware on November 22, 2023."
    },
    {
        "id": "holdout-067",
        "claim_text": "Nvidia surpassed a $3 trillion market capitalization milestone during 2024.",
        "category": "company_info",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.reuters.com/technology/nvidia-hits-3-trillion-market-cap-2024-06-05/",
        "rationale": "Nvidia crossed the $3 trillion market cap milestone in June 2024."
    },
    {
        "id": "holdout-068",
        "claim_text": "Theranos is currently a publicly traded NASDAQ company manufacturing certified blood diagnostic hardware.",
        "category": "company_info",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.sec.gov/",
        "rationale": "Theranos collapsed into fraud, was dissolved in September 2018, and its founder was imprisoned."
    },
    {
        "id": "holdout-069",
        "claim_text": "Enron is currently the highest-earning Fortune 10 energy corporation in the United States.",
        "category": "company_info",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.sec.gov/",
        "rationale": "Enron collapsed into Chapter 11 bankruptcy in December 2001 and was liquidated."
    },
    {
        "id": "holdout-070",
        "claim_text": "Google and Apple will merge into a single joint company called Goopla tomorrow morning.",
        "category": "company_info",
        "ground_truth_verdict": "UNVERIFIED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://abc.xyz/",
        "rationale": "Fictitious rumor."
    },

    # ==========================================
    # 5. TECHNOLOGY & ARCHITECTURE (15 Claims)
    # ==========================================
    {
        "id": "holdout-071",
        "claim_text": "PostgreSQL utilizes Multi-Version Concurrency Control to handle concurrent database transactions.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.postgresql.org/docs/current/mvcc.html",
        "rationale": "MVCC is the foundational concurrency architecture of PostgreSQL."
    },
    {
        "id": "holdout-072",
        "claim_text": "Git uses cryptographic SHA hashes as object identifiers for commits, trees, and blobs.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://git-scm.com/book/en/v2/Git-Internals-Git-Objects",
        "rationale": "Git calculates SHA-1 (and optionally SHA-256) checksums as object IDs."
    },
    {
        "id": "holdout-073",
        "claim_text": "The HTTP/3 protocol uses QUIC over UDP rather than TCP for transport.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "MEDIUM",
        "reference_source": "https://datatracker.ietf.org/doc/html/rfc9114",
        "rationale": "RFC 9114 defines HTTP/3 running over QUIC using UDP."
    },
    {
        "id": "holdout-074",
        "claim_text": "HTTP/1.1 requires UDP socket connections exclusively for web browsing.",
        "category": "technology",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://datatracker.ietf.org/doc/html/rfc2616",
        "rationale": "HTTP/1.1 relies strictly on TCP connection transport."
    },
    {
        "id": "holdout-075",
        "claim_text": "Redis is an in-memory data store with optional persistence mechanisms like RDB and AOF.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://redis.io/docs/management/persistence/",
        "rationale": "Redis is fundamentally an in-memory key-value data structure store."
    },
    {
        "id": "holdout-076",
        "claim_text": "Apache Kafka stores partitioned commit logs sequentially on persistent disk.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://kafka.apache.org/documentation/",
        "rationale": "Kafka's architecture is based on partitioned append-only log files."
    },
    {
        "id": "holdout-077",
        "claim_text": "Docker containers share the host operating system kernel rather than hypervisor hardware virtualization.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://docs.docker.com/get-started/overview/",
        "rationale": "Containers run as isolated processes sharing the host OS kernel via cgroups and namespaces."
    },
    {
        "id": "holdout-078",
        "claim_text": "IPv4 network addresses are 32-bit numerical labels.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://datatracker.ietf.org/doc/html/rfc791",
        "rationale": "RFC 791 defines IPv4 addresses as 32 bits."
    },
    {
        "id": "holdout-079",
        "claim_text": "IPv4 network addresses have a theoretical maximum pool of over 900 trillion unique addresses.",
        "category": "technology",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://datatracker.ietf.org/doc/html/rfc791",
        "rationale": "The 32-bit address space provides exactly 2^32 = 4,294,967,296 addresses."
    },
    {
        "id": "holdout-080",
        "claim_text": "IPv6 addresses are 128-bit identifiers designed to succeed IPv4.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://datatracker.ietf.org/doc/html/rfc8200",
        "rationale": "RFC 8200 defines IPv6 as 128-bit addresses."
    },
    {
        "id": "holdout-081",
        "claim_text": "WebAssembly is a binary instruction format for a stack-based virtual machine.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://webassembly.org/",
        "rationale": "Official specification of WebAssembly."
    },
    {
        "id": "holdout-082",
        "claim_text": "TLS 1.3 removed support for insecure cryptographic algorithms like RC4, DES, and CBC-mode ciphers.",
        "category": "technology",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://datatracker.ietf.org/doc/html/rfc8446",
        "rationale": "RFC 8446 stripped out legacy cipher suites."
    },
    {
        "id": "holdout-083",
        "claim_text": "TLS 1.0 is the modern cryptographic protocol recommended by NIST for all banking transactions in 2026.",
        "category": "technology",
        "ground_truth_verdict": "OUTDATED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://datatracker.ietf.org/doc/html/rfc8996",
        "rationale": "RFC 8996 officially deprecated TLS 1.0 and TLS 1.1 in March 2021."
    },
    {
        "id": "holdout-084",
        "claim_text": "React components render exclusively through dedicated hardware GPUs and cannot execute within JavaScript engines.",
        "category": "technology",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://react.dev/",
        "rationale": "React is a JavaScript UI library executing in JS runtimes (V8, SpiderMonkey) manipulating the DOM."
    },
    {
        "id": "holdout-085",
        "claim_text": "Quantum computers have completely replaced all classical x86 CPU chips in all smartphones worldwide.",
        "category": "technology",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.nature.com/",
        "rationale": "Absurdly false assertion; smartphones utilize classical ARM processors."
    },

    # ==========================================
    # 6. GENERAL FACTUAL KNOWLEDGE (15 Claims)
    # ==========================================
    {
        "id": "holdout-086",
        "claim_text": "The speed of light in a vacuum is exactly 299,792,458 meters per second.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://physics.nist.gov/cuu/Constants/",
        "rationale": "SI standard definition of c."
    },
    {
        "id": "holdout-087",
        "claim_text": "Water at standard atmospheric pressure freezes at 0 degrees Celsius and boils at 100 degrees Celsius.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.bipm.org/en/committees/cc/cct",
        "rationale": "Standard metric physical property of water."
    },
    {
        "id": "holdout-088",
        "claim_text": "The Earth has three natural astronomical moons permanently orbiting in its gravitational field.",
        "category": "general_fact",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://solarsystem.nasa.gov/moons/earths-moon/overview/",
        "rationale": "Earth has one permanent natural moon."
    },
    {
        "id": "holdout-089",
        "claim_text": "Pluto was reclassified from a major planet to a dwarf planet by the International Astronomical Union in 2006.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.iau.org/news/pressreleases/detail/iau0603/",
        "rationale": "IAU Resolution B5 passed in Prague in August 2006."
    },
    {
        "id": "holdout-090",
        "claim_text": "Mount Everest is the highest mountain above sea level on Earth.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.nationalgeographic.org/",
        "rationale": "Geographical consensus at 8,848.86 meters."
    },
    {
        "id": "holdout-091",
        "claim_text": "The Pacific Ocean is the largest and deepest of the world's oceanic divisions.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://oceanservice.noaa.gov/",
        "rationale": "NOAA geographic standard."
    },
    {
        "id": "holdout-092",
        "claim_text": "The adult human skeletal structure typically consists of 206 bones.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.britannica.com/science/human-skeleton",
        "rationale": "Anatomical medical consensus."
    },
    {
        "id": "holdout-093",
        "claim_text": "Helium has an atomic number of 2 in the periodic table of elements.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.rsc.org/periodic-table/element/2/helium",
        "rationale": "IUPAC periodic table."
    },
    {
        "id": "holdout-094",
        "claim_text": "The Eiffel Tower is an iron lattice tower located in Tokyo, Japan.",
        "category": "general_fact",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.toureiffel.paris/en",
        "rationale": "The Eiffel Tower is located in Paris, France; Tokyo Tower is in Japan."
    },
    {
        "id": "holdout-095",
        "claim_text": "DNA stands for Deoxyribonucleic acid.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.genome.gov/genetics-glossary/Deoxyribonucleic-Acid",
        "rationale": "Standard biological definition."
    },
    {
        "id": "holdout-096",
        "claim_text": "A new continent will rise from the Indian Ocean next Tuesday at 3:00 PM.",
        "category": "general_fact",
        "ground_truth_verdict": "UNVERIFIED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.usgs.gov/",
        "rationale": "Physically impossible unverified prediction."
    },
    {
        "id": "holdout-097",
        "claim_text": "World War II in Europe formally concluded in May 1945.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.archives.gov/",
        "rationale": "Historical fact (V-E Day, May 8, 1945)."
    },
    {
        "id": "holdout-098",
        "claim_text": "The Apollo 11 lunar module landed on the Moon in July 1969.",
        "category": "general_fact",
        "ground_truth_verdict": "CURRENT",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.nasa.gov/mission/apollo-11/",
        "rationale": "Historical fact (July 20, 1969)."
    },
    {
        "id": "holdout-099",
        "claim_text": "The chemical symbol for Gold in the periodic table of elements is Fe.",
        "category": "general_fact",
        "ground_truth_verdict": "CONTRADICTED",
        "temporal_sensitivity": "LOW",
        "reference_source": "https://www.rsc.org/periodic-table/",
        "rationale": "Fe is the symbol for Iron; Gold is Au (Aurum)."
    },
    {
        "id": "holdout-100",
        "claim_text": "Total global human electricity consumption will reach zero watts for all countries next Friday.",
        "category": "general_fact",
        "ground_truth_verdict": "UNVERIFIED",
        "temporal_sensitivity": "HIGH",
        "reference_source": "https://www.iea.org/",
        "rationale": "Unverifiable speculation."
    }
]

out_dir = os.path.join(os.path.dirname(__file__), "..", "tests", "data")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "holdout_100_claims.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(HOLDOUT_CLAIMS, f, indent=2)

print(f"Successfully generated {len(HOLDOUT_CLAIMS)} independent holdout claims at {out_path}")

