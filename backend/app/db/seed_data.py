"""75 legal FAQ pairs across 6 categories."""

SEED_FAQS = [
    # ── Contracts (13) ──────────────────────────────────────────────────────────
    {
        "title": "What makes a contract legally binding?",
        "question": "What elements are required to make a contract legally binding?",
        "answer": (
            "A legally binding contract requires four essential elements: (1) Offer — one party "
            "proposes specific terms; (2) Acceptance — the other party agrees to those exact terms; "
            "(3) Consideration — something of value is exchanged by both parties (money, services, "
            "a promise to act or refrain from acting); and (4) Mutual assent — both parties must "
            "have the legal capacity to contract and genuinely agree (no fraud, duress, or "
            "misrepresentation). Some contracts also require a written form to be enforceable, "
            "such as contracts for real estate or agreements lasting more than one year."
        ),
        "category": "Contracts",
    },
    {
        "title": "Can a verbal agreement be enforced?",
        "question": "Is a verbal contract legally enforceable?",
        "answer": (
            "Verbal contracts are generally enforceable, but proving their existence and terms can "
            "be difficult. Certain types of contracts must be in writing under the Statute of "
            "Frauds, including agreements for the sale of real property, contracts that cannot be "
            "performed within one year, contracts for goods over $500 (under the UCC), and "
            "prenuptial agreements. If a verbal contract dispute arises, courts look at witness "
            "testimony, emails, texts, and conduct to determine what was agreed."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is a breach of contract?",
        "question": "What constitutes a breach of contract and what remedies are available?",
        "answer": (
            "A breach of contract occurs when one party fails to fulfill their contractual "
            "obligations without a legally valid excuse. Breaches may be material (significant, "
            "defeating the contract's purpose) or minor (partial performance). Remedies include: "
            "compensatory damages (to put the injured party in the position they would have been "
            "in), consequential damages (foreseeable losses flowing from the breach), specific "
            "performance (court order to complete the contract), rescission (cancellation), and "
            "restitution (recovering the value of benefits conferred)."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is an indemnification clause?",
        "question": "What does an indemnification clause mean in a contract?",
        "answer": (
            "An indemnification clause requires one party to compensate the other for certain "
            "losses, damages, or legal costs that arise from specified events. For example, a "
            "vendor contract might require the vendor to indemnify the client for any third-party "
            "claims resulting from the vendor's negligence. Broad indemnification clauses can "
            "shift significant financial risk; always review the scope, triggers, and any "
            "limitations (caps, exclusions) before signing."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is a non-disclosure agreement (NDA)?",
        "question": "What is an NDA and when should I use one?",
        "answer": (
            "A non-disclosure agreement (NDA) is a contract where one or both parties agree to "
            "keep certain information confidential. Use an NDA before sharing proprietary business "
            "information, trade secrets, or sensitive data with potential partners, employees, or "
            "contractors. Key provisions include: the definition of confidential information, the "
            "obligations of the receiving party, permitted disclosures, and the duration of the "
            "confidentiality obligation. Unilateral NDAs protect one party's information; mutual "
            "NDAs protect both."
        ),
        "category": "Contracts",
    },
    {
        "title": "Can I cancel a contract after signing?",
        "question": "How can I cancel or get out of a contract I already signed?",
        "answer": (
            "Options for cancelling a contract depend on its terms and applicable law. Look for: "
            "a rescission or cancellation clause, a cooling-off period (federally mandated for "
            "certain door-to-door and telemarketing sales), or grounds for voidability such as "
            "fraud, misrepresentation, duress, undue influence, or mutual mistake. If none apply, "
            "you may negotiate a mutual release with the other party or argue that the contract "
            "is unenforceable. Acting without a valid basis exposes you to a breach of contract "
            "claim."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is a force majeure clause?",
        "question": "What does force majeure mean in a contract?",
        "answer": (
            "A force majeure clause excuses a party's non-performance when an extraordinary event "
            "beyond their control — such as natural disasters, wars, pandemics, or government "
            "actions — prevents fulfillment of contractual obligations. Whether an event qualifies "
            "depends on the clause's language; courts interpret these provisions narrowly. Parties "
            "typically must notify the other side promptly, mitigate where possible, and resume "
            "performance once the event ends."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is a limitation of liability clause?",
        "question": "What does a limitation of liability clause do?",
        "answer": (
            "A limitation of liability clause caps the amount one party can recover from the other "
            "in the event of a breach or other claim. Common caps are the fees paid under the "
            "contract or a fixed dollar amount. These clauses may also exclude certain types of "
            "damages (e.g., consequential or punitive). Courts generally enforce them unless they "
            "are unconscionable, the result of unequal bargaining power, or prohibited by statute."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is the difference between void and voidable contracts?",
        "question": "What is the difference between a void contract and a voidable contract?",
        "answer": (
            "A void contract has no legal effect from the outset — it cannot be enforced by either "
            "party (e.g., a contract to commit a crime). A voidable contract is valid and "
            "enforceable unless the party with the right to cancel chooses to do so. Grounds for "
            "voidability include: lack of capacity (minor or mental incapacity), fraud, "
            "misrepresentation, duress, undue influence, or mutual mistake. The injured party can "
            "ratify (keep) or rescind (cancel) a voidable contract."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is an arbitration clause?",
        "question": "What is an arbitration clause and does it affect my rights?",
        "answer": (
            "An arbitration clause requires disputes to be resolved through arbitration rather than "
            "court litigation. It typically waives your right to a jury trial and may restrict "
            "class-action participation. Arbitration can be faster and cheaper than litigation, "
            "but the process is usually private, discovery is limited, and awards are difficult "
            "to appeal. Always read whether arbitration is binding, who selects the arbitrator, "
            "who pays fees, and where proceedings occur."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is the statute of limitations on contract claims?",
        "question": "How long do I have to sue for breach of contract?",
        "answer": (
            "Statutes of limitations for breach of contract vary by state and contract type. "
            "Written contracts typically have longer periods (4–6 years in most states) than oral "
            "contracts (2–4 years). The UCC sets a 4-year limit for contracts for the sale of "
            "goods. The clock generally starts when the breach occurs or is discovered. Missing "
            "the deadline bars your claim, so consult an attorney promptly if you believe a breach "
            "has occurred."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is liquidated damages?",
        "question": "What are liquidated damages in a contract?",
        "answer": (
            "Liquidated damages are a pre-agreed amount that one party will pay the other if a "
            "specific breach occurs. They are enforceable when: (1) actual damages would be "
            "difficult to calculate at the time of contracting, and (2) the amount is a reasonable "
            "estimate of likely harm (not a penalty). Courts will void a liquidated damages clause "
            "deemed punitive. Common in construction, event planning, and software development "
            "contracts."
        ),
        "category": "Contracts",
    },
    {
        "title": "What is a non-compete agreement?",
        "question": "Are non-compete agreements enforceable?",
        "answer": (
            "Non-compete agreements restrict an employee or contractor from working for competitors "
            "or starting a competing business for a defined period and geographic area after "
            "leaving. Enforceability varies widely by state — California, Minnesota, and a few "
            "others ban them almost entirely; most states enforce reasonable restrictions. Courts "
            "consider whether the scope (duration, geography, activity) is no broader than "
            "necessary to protect legitimate business interests such as trade secrets or "
            "customer relationships."
        ),
        "category": "Contracts",
    },

    # ── Employment Law (13) ─────────────────────────────────────────────────────
    {
        "title": "What is at-will employment?",
        "question": "What does at-will employment mean?",
        "answer": (
            "At-will employment means either the employer or the employee can end the employment "
            "relationship at any time, for any reason (or no reason), with or without notice, "
            "subject to exceptions. Employers cannot terminate for illegal reasons such as "
            "discrimination, retaliation for protected activity, or violation of an implied "
            "contract. Most U.S. states follow at-will employment, with Montana being the "
            "primary exception requiring just cause after a probationary period."
        ),
        "category": "Employment",
    },
    {
        "title": "What qualifies as wrongful termination?",
        "question": "Was I wrongfully terminated from my job?",
        "answer": (
            "Wrongful termination occurs when an employer fires an employee for illegal reasons. "
            "Common grounds include: discrimination based on race, sex, age, disability, religion, "
            "or national origin; retaliation for whistleblowing, filing a workers' comp claim, or "
            "taking FMLA leave; violation of an employment contract; or violation of public policy "
            "(e.g., firing someone for serving on jury duty). At-will employees can be dismissed "
            "for any lawful reason, but not for these protected reasons."
        ),
        "category": "Employment",
    },
    {
        "title": "What is workplace harassment?",
        "question": "What constitutes illegal workplace harassment?",
        "answer": (
            "Illegal workplace harassment under federal law (Title VII, ADA, ADEA) involves "
            "unwelcome conduct based on a protected characteristic (race, sex, age, disability, "
            "religion, etc.) that is severe or pervasive enough to create a hostile work "
            "environment, or that results in a tangible employment action. Sexual harassment "
            "includes quid pro quo (submission to conduct tied to job benefits) and hostile "
            "environment claims. Isolated minor incidents generally do not meet the legal "
            "threshold, but patterns of behavior do."
        ),
        "category": "Employment",
    },
    {
        "title": "Am I entitled to overtime pay?",
        "question": "When am I legally entitled to overtime pay?",
        "answer": (
            "Under the federal Fair Labor Standards Act (FLSA), non-exempt employees must receive "
            "1.5× their regular pay for hours worked beyond 40 in a workweek. Exemptions apply to "
            "executive, administrative, and professional employees who are paid a salary above the "
            "threshold (currently $684/week) and meet duties tests. Some states have stricter "
            "overtime rules (e.g., California requires daily overtime after 8 hours). "
            "Misclassification as exempt is a common wage-and-hour violation."
        ),
        "category": "Employment",
    },
    {
        "title": "What is the FMLA?",
        "question": "What rights does the Family and Medical Leave Act give me?",
        "answer": (
            "The FMLA entitles eligible employees of covered employers (50+ employees) to up to "
            "12 weeks of unpaid, job-protected leave per year for: the birth or adoption of a "
            "child, a serious health condition of the employee or immediate family member, or "
            "qualifying military exigencies. To be eligible, you must have worked for the employer "
            "for at least 12 months and 1,250 hours in the past year. Your employer must restore "
            "you to the same or an equivalent position when you return."
        ),
        "category": "Employment",
    },
    {
        "title": "What is an independent contractor vs. employee?",
        "question": "What is the difference between being an employee and an independent contractor?",
        "answer": (
            "The distinction affects taxes, benefits, and legal protections. Key factors courts "
            "and agencies examine include: behavioral control (does the company control how work "
            "is done?), financial control (who provides tools, sets pay, bears risk?), and the "
            "type of relationship (written contracts, permanency, integral to business?). "
            "Misclassification denies workers minimum wage, overtime, workers' comp, and "
            "unemployment benefits. The IRS, DOL, and states each have their own tests."
        ),
        "category": "Employment",
    },
    {
        "title": "What protections exist against workplace discrimination?",
        "question": "What federal laws protect me from workplace discrimination?",
        "answer": (
            "Key federal anti-discrimination laws include: Title VII of the Civil Rights Act (race, "
            "color, religion, sex, national origin), the Age Discrimination in Employment Act "
            "(workers 40+), the Americans with Disabilities Act (disability), the Equal Pay Act "
            "(sex-based wage discrimination), the Pregnancy Discrimination Act, and Title II of "
            "GINA (genetic information). These laws are enforced by the EEOC. Many states provide "
            "broader protections and cover smaller employers."
        ),
        "category": "Employment",
    },
    {
        "title": "What is a severance agreement?",
        "question": "Do I have to sign a severance agreement and what rights does it affect?",
        "answer": (
            "Severance agreements are generally voluntary — you cannot be compelled to sign one. "
            "In exchange for severance pay, employers typically require you to release all claims "
            "against them. Before signing: review what claims you are waiving, check whether it "
            "complies with the OWBPA (for workers 40+ you must have 21–45 days to consider and "
            "7 days to revoke), confirm any non-disparagement, non-compete, or cooperation "
            "obligations, and consult an employment attorney if the amount or claims are "
            "significant."
        ),
        "category": "Employment",
    },
    {
        "title": "What are my rights if my employer doesn't pay me?",
        "question": "What can I do if my employer withholds or refuses to pay my wages?",
        "answer": (
            "You have the right to all earned wages under the FLSA and state wage payment laws. "
            "Steps to take: first, raise it with HR or payroll in writing; if unresolved, file a "
            "wage claim with your state's labor board or the U.S. Department of Labor Wage and "
            "Hour Division; or file a private lawsuit. Many states allow recovery of unpaid wages "
            "plus penalties, interest, and attorneys' fees. Retaliation for filing a wage claim "
            "is illegal."
        ),
        "category": "Employment",
    },
    {
        "title": "What is workers' compensation?",
        "question": "How does workers' compensation work and what does it cover?",
        "answer": (
            "Workers' compensation is a state-mandated insurance program providing benefits to "
            "employees injured on the job or who develop occupational illnesses. Benefits typically "
            "include medical treatment, temporary disability pay (a portion of lost wages), "
            "permanent disability benefits, and vocational rehabilitation. In exchange, employees "
            "generally cannot sue their employer for negligence. Deadlines for reporting injuries "
            "and filing claims vary by state; missing them can forfeit your benefits."
        ),
        "category": "Employment",
    },
    {
        "title": "Can my employer monitor my work communications?",
        "question": "Is it legal for my employer to monitor my emails or computer activity at work?",
        "answer": (
            "Generally yes. Employers have broad rights to monitor activity on company-owned "
            "devices and networks, and courts have upheld this consistently. Employees have a "
            "reduced expectation of privacy when using employer equipment or systems. Many "
            "employers include monitoring disclosures in their acceptable-use policies. Personal "
            "devices and accounts may receive stronger protection, but if you use personal accounts "
            "on work systems, that protection may be reduced."
        ),
        "category": "Employment",
    },
    {
        "title": "What is a hostile work environment?",
        "question": "What is a hostile work environment claim?",
        "answer": (
            "A hostile work environment claim arises when harassment based on a protected "
            "characteristic (race, sex, religion, etc.) is so severe or pervasive that it alters "
            "the conditions of employment and creates an abusive work environment. A single "
            "incident can be sufficient if severe enough (e.g., physical assault). You generally "
            "must report internally first (giving the employer a chance to correct it) before "
            "bringing an EEOC charge, unless reporting would be futile or cause retaliation."
        ),
        "category": "Employment",
    },
    {
        "title": "What is COBRA health insurance continuation?",
        "question": "What is COBRA and am I eligible for it after losing my job?",
        "answer": (
            "COBRA (Consolidated Omnibus Budget Reconciliation Act) allows you to continue your "
            "employer-sponsored health insurance for up to 18 months (36 in some cases) after "
            "losing coverage due to job loss, reduced hours, divorce, or other qualifying events. "
            "Employers with 20+ employees are covered. You must pay the full premium (including "
            "the employer's share) plus a 2% administrative fee, making it expensive. You have "
            "60 days from your loss of coverage to elect COBRA coverage."
        ),
        "category": "Employment",
    },

    # ── Intellectual Property (13) ──────────────────────────────────────────────
    {
        "title": "How do I protect my business name?",
        "question": "How do I protect my business name or brand?",
        "answer": (
            "Trademark registration with the USPTO provides nationwide protection for your brand "
            "name, logo, or slogan used in commerce. Common law trademark rights arise from actual "
            "use, but only in the geographic area of use. Before adopting a name, search the USPTO "
            "database and state databases for conflicts. Registration gives you the right to use ®, "
            "the presumption of ownership, and the ability to bring a federal infringement lawsuit. "
            "Domain names and business name registrations do not confer trademark rights."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "What does copyright protect?",
        "question": "What types of works are protected by copyright?",
        "answer": (
            "Copyright protects original works of authorship fixed in a tangible medium: literary "
            "works, music, art, photographs, software code, films, architectural works, and more. "
            "Copyright does not protect ideas, facts, titles, short phrases, or methods — only the "
            "specific expression. Rights arise automatically upon creation; registration with the "
            "U.S. Copyright Office is not required but is necessary to sue for infringement and "
            "allows recovery of statutory damages and attorneys' fees."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "What is a patent?",
        "question": "What can be patented and how long does a patent last?",
        "answer": (
            "A patent grants the inventor exclusive rights to make, use, sell, or import an "
            "invention for a limited period. Utility patents (new and useful processes, machines, "
            "manufactures, or compositions of matter) last 20 years from the filing date. Design "
            "patents (ornamental appearance) last 15 years. Plant patents last 20 years. To be "
            "patentable, an invention must be novel, non-obvious, and useful. Abstract ideas, "
            "laws of nature, and natural phenomena are not patentable."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "What is a trade secret?",
        "question": "What qualifies as a trade secret and how is it protected?",
        "answer": (
            "A trade secret is information that derives economic value from being secret and is "
            "subject to reasonable efforts to maintain secrecy — for example, formulas, algorithms, "
            "customer lists, or business processes. Protection arises automatically (no "
            "registration). Under the Defend Trade Secrets Act and state laws, misappropriation "
            "can result in injunctive relief, damages, and in willful cases, exemplary damages and "
            "attorneys' fees. Maintain trade secrets through NDAs, access controls, and security "
            "policies."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "What is fair use?",
        "question": "When can I use copyrighted material without permission under fair use?",
        "answer": (
            "Fair use is a defense to copyright infringement evaluated on four factors: (1) the "
            "purpose and character of use (commercial vs. educational, transformative vs. "
            "reproductive); (2) the nature of the copyrighted work; (3) the amount and "
            "substantiality of the portion used; and (4) the effect on the market for the original. "
            "No single factor is determinative. Commentary, criticism, parody, news reporting, and "
            "teaching are common fair use contexts, but commercial use weighs against the defense."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "Who owns IP created by employees?",
        "question": "Does my employer own intellectual property I create on the job?",
        "answer": (
            "Under the work-for-hire doctrine, IP created by an employee within the scope of "
            "employment generally belongs to the employer. Employment agreements often include "
            "IP assignment clauses that broadly assign inventions and creative works. However, "
            "many states (California, Delaware, Minnesota, etc.) limit assignments to inventions "
            "related to the employer's business or created with employer resources. Inventions "
            "made entirely on personal time without employer resources and unrelated to the "
            "employer's business usually remain the employee's."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "What is trademark infringement?",
        "question": "What constitutes trademark infringement?",
        "answer": (
            "Trademark infringement occurs when someone uses a mark that is likely to cause "
            "consumer confusion about the source, sponsorship, or affiliation of goods or services. "
            "Courts examine: the similarity of the marks, the proximity of the goods/services, "
            "the strength of the plaintiff's mark, evidence of actual confusion, and the "
            "defendant's intent. The standard is likelihood of confusion, not actual confusion. "
            "Remedies include injunctions, profits, actual damages, and in exceptional cases "
            "(willful infringement), treble damages and attorneys' fees."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "How do I register a copyright?",
        "question": "How do I register a copyright with the U.S. Copyright Office?",
        "answer": (
            "Register online at copyright.gov by submitting: the application form, the filing fee "
            "(currently $45–$65 for online single-work registration), and a deposit copy of the "
            "work. Registration is not required for copyright to exist, but it must be registered "
            "before filing an infringement suit (for U.S. works), and registration within 3 months "
            "of publication (or before infringement) enables recovery of statutory damages "
            "($750–$30,000 per work, up to $150,000 for willful infringement) and attorneys' fees."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "What is a licensing agreement?",
        "question": "What is an IP licensing agreement and what should it include?",
        "answer": (
            "A licensing agreement grants another party (licensee) permission to use IP owned by "
            "the licensor under defined conditions. Key terms include: the scope of the license "
            "(exclusive or non-exclusive, field of use, territory), royalty rates and payment "
            "structure, sublicensing rights, quality control standards, audit rights, term and "
            "termination triggers, and representations about ownership. Exclusive licenses in "
            "patent contexts may need to be in writing and signed to transfer standing to sue."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "What is the DMCA takedown process?",
        "question": "How do I issue a DMCA takedown notice for infringing content?",
        "answer": (
            "Under the Digital Millennium Copyright Act (DMCA), you can send a takedown notice "
            "to an online service provider's designated DMCA agent. The notice must include: your "
            "contact information, identification of the copyrighted work, identification of the "
            "infringing material and its URL, a good-faith belief statement, and your signature. "
            "The provider must promptly remove the content to maintain its safe harbor protection. "
            "The alleged infringer can submit a counter-notice; if they do, you have 10–14 days "
            "to file suit or the content is restored."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "What is a provisional patent application?",
        "question": "What is a provisional patent application and is it worth filing?",
        "answer": (
            "A provisional patent application (PPA) establishes an early filing date and allows "
            "you to use 'Patent Pending' for 12 months while you prepare a full non-provisional "
            "application. It is not examined and never becomes a patent on its own. Benefits: "
            "lower initial cost, time to assess commercial viability, and priority date protection. "
            "The non-provisional must be filed within 12 months or the priority date is lost. "
            "Draft the PPA thoroughly — you can only claim what is disclosed in the provisional."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "What is the difference between ™ and ®?",
        "question": "What is the difference between the TM and R symbols?",
        "answer": (
            "™ (TM) indicates that you are claiming trademark rights in a mark but have not yet "
            "obtained a federal registration from the USPTO. Anyone can use ™ regardless of "
            "registration. ® (registered) may only be used once the USPTO has approved your "
            "trademark registration. Using ® on an unregistered mark is a federal violation and "
            "can result in loss of rights. SM (service mark) functions like ™ but for services "
            "rather than goods."
        ),
        "category": "Intellectual Property",
    },
    {
        "title": "Can I patent software?",
        "question": "Is software patentable in the United States?",
        "answer": (
            "Software can be patentable if it is tied to a specific machine or transforms an "
            "article into a different state, and if it does more than apply an abstract idea on "
            "a computer. After Alice Corp. v. CLS Bank (2014), abstract ideas implemented in "
            "software face heightened scrutiny under the two-step Alice/Mayo framework. Claims "
            "must be directed to a specific technical improvement with inventive concept beyond "
            "the abstract idea itself. Prosecution strategy and claim drafting are critical — "
            "consult a patent attorney."
        ),
        "category": "Intellectual Property",
    },

    # ── Liability & Torts (12) ──────────────────────────────────────────────────
    {
        "title": "What is negligence?",
        "question": "What do I need to prove to win a negligence lawsuit?",
        "answer": (
            "To succeed in a negligence claim you must prove four elements: (1) Duty — the "
            "defendant owed you a legal duty of care; (2) Breach — the defendant failed to meet "
            "that standard of care; (3) Causation — the breach actually and proximately caused "
            "your injury; and (4) Damages — you suffered actual harm. The standard of care is "
            "generally what a reasonably prudent person would do under the same circumstances. "
            "Special duties apply to professionals (doctors, lawyers, architects)."
        ),
        "category": "Liability",
    },
    {
        "title": "What is a personal injury claim?",
        "question": "What types of damages can I recover in a personal injury lawsuit?",
        "answer": (
            "Personal injury damages fall into two categories. Economic damages are quantifiable "
            "losses: medical expenses (past and future), lost wages, property damage, and "
            "rehabilitation costs. Non-economic damages compensate for intangible harms: pain and "
            "suffering, emotional distress, loss of enjoyment of life, and loss of consortium. "
            "Some states cap non-economic damages in certain cases. Punitive damages may be "
            "available for egregious misconduct to punish and deter."
        ),
        "category": "Liability",
    },
    {
        "title": "What is product liability?",
        "question": "When can I sue a manufacturer for a defective product?",
        "answer": (
            "Product liability claims arise from: (1) manufacturing defects (a specific unit "
            "deviates from its intended design); (2) design defects (the entire product line is "
            "unreasonably dangerous); or (3) failure to warn (inadequate instructions or safety "
            "warnings). Claims may be brought in negligence or strict liability (no need to prove "
            "fault). Defendants in the chain of distribution — manufacturer, distributor, "
            "retailer — may all be liable. Statutes of limitations and repose vary by state."
        ),
        "category": "Liability",
    },
    {
        "title": "What is premises liability?",
        "question": "When is a property owner liable for injuries on their property?",
        "answer": (
            "Premises liability holds property owners and occupiers responsible for injuries caused "
            "by unsafe conditions. The duty owed depends on the visitor's status in most states: "
            "invitees (customers, guests) are owed the highest duty — reasonable care to inspect "
            "and fix dangers; licensees (social guests) — duty to warn of known hazards; "
            "trespassers — no duty except to avoid willful/wanton harm (with exceptions for "
            "children under the attractive nuisance doctrine). Some states use a general "
            "reasonable care standard for all lawful visitors."
        ),
        "category": "Liability",
    },
    {
        "title": "What is comparative negligence?",
        "question": "Can I still recover if I was partially at fault for my injury?",
        "answer": (
            "Under comparative negligence (adopted by most states), your recovery is reduced by "
            "your percentage of fault. Pure comparative negligence allows recovery even if you are "
            "99% at fault. Modified comparative negligence (the majority rule) bars recovery if "
            "you are 50% or 51% or more at fault (varies by state). A few states still use "
            "contributory negligence, which completely bars recovery if you are even 1% at fault. "
            "Understand your state's rule before evaluating a claim's value."
        ),
        "category": "Liability",
    },
    {
        "title": "What is defamation?",
        "question": "What is defamation and what do I need to prove?",
        "answer": (
            "Defamation is a false statement of fact published to a third party that harms someone's "
            "reputation. Libel is written/recorded; slander is spoken. To prevail you must show: "
            "a false statement of fact (not opinion), publication, identification of the plaintiff, "
            "and fault. Public figures must prove actual malice (knowledge of falsity or reckless "
            "disregard for truth). Private figures typically need only show negligence. Truth is "
            "an absolute defense. Online statements are subject to Section 230 immunity for "
            "platforms (not for the original poster)."
        ),
        "category": "Liability",
    },
    {
        "title": "What is strict liability?",
        "question": "What is strict liability and when does it apply?",
        "answer": (
            "Strict liability imposes responsibility for harm regardless of fault or intent. It "
            "applies when someone engages in abnormally dangerous activities (blasting, storing "
            "explosives, keeping wild animals) or when a product is defective. The plaintiff "
            "need not prove the defendant was negligent — only that the activity or product caused "
            "the harm. Strict liability encourages businesses and individuals to take maximum "
            "precautions and efficiently internalize the cost of dangerous activities."
        ),
        "category": "Liability",
    },
    {
        "title": "What is vicarious liability?",
        "question": "When is an employer liable for an employee's wrongful acts?",
        "answer": (
            "Under the doctrine of respondeat superior, employers are vicariously liable for torts "
            "committed by employees acting within the scope of employment. 'Scope of employment' "
            "includes acts authorized by the employer and acts closely connected to authorized "
            "tasks, even if the specific act was prohibited. Employers are generally not liable "
            "for independent contractors' torts unless the employer controls the work method. "
            "Direct liability may arise from negligent hiring, retention, or supervision."
        ),
        "category": "Liability",
    },
    {
        "title": "What is a statute of limitations for personal injury?",
        "question": "How long do I have to file a personal injury lawsuit?",
        "answer": (
            "Personal injury statutes of limitations typically range from 1 to 6 years, varying "
            "by state and injury type. Most states allow 2–3 years from the date of injury or "
            "discovery (under the discovery rule, the clock starts when you knew or should have "
            "known of the injury). Special rules apply for: minors (tolling until majority), "
            "claims against government entities (often 6-month notice requirements), medical "
            "malpractice, and latent diseases. Missing the deadline usually bars your claim "
            "entirely."
        ),
        "category": "Liability",
    },
    {
        "title": "What is an LLC and does it protect me from liability?",
        "question": "Does forming an LLC protect my personal assets from business liability?",
        "answer": (
            "A limited liability company (LLC) generally shields members' personal assets from "
            "business debts and judgments, limiting liability to the member's investment. However, "
            "courts will 'pierce the corporate veil' if: members comingle personal and business "
            "funds, the LLC is inadequately capitalized, corporate formalities are not observed, "
            "or the LLC is used fraudulently. Members remain personally liable for their own "
            "torts and acts, even those committed in the LLC's name. Obtain adequate insurance "
            "alongside your LLC formation."
        ),
        "category": "Liability",
    },
    {
        "title": "What is an assumption of risk defense?",
        "question": "What is the assumption of risk doctrine in personal injury cases?",
        "answer": (
            "Assumption of risk is a defense arguing that the plaintiff voluntarily and knowingly "
            "accepted the risk that caused their injury. Express assumption of risk arises from "
            "a signed waiver or release. Implied assumption of risk arises from voluntary "
            "participation in an activity with known risks (e.g., contact sports). Many states "
            "have merged implied assumption of risk into comparative negligence analysis. Courts "
            "scrutinize waivers signed under duress or for essential services, and waivers "
            "generally cannot excuse intentional misconduct or gross negligence."
        ),
        "category": "Liability",
    },
    {
        "title": "What is intentional infliction of emotional distress?",
        "question": "Can I sue for emotional distress caused by someone's extreme behavior?",
        "answer": (
            "Intentional infliction of emotional distress (IIED) requires: (1) extreme and "
            "outrageous conduct by the defendant (beyond all bounds of decency); (2) intent or "
            "reckless disregard for causing emotional harm; (3) severe emotional distress suffered "
            "by the plaintiff. Simple insults, threats, or rude behavior typically do not meet "
            "the threshold. Courts look at the relationship between parties and any power "
            "imbalance. Physical injury is not required, but medical evidence of distress "
            "strengthens the claim."
        ),
        "category": "Liability",
    },

    # ── Privacy & Data (12) ─────────────────────────────────────────────────────
    {
        "title": "What is GDPR and does it apply to my business?",
        "question": "What is the GDPR and does it apply to U.S. businesses?",
        "answer": (
            "The General Data Protection Regulation (GDPR) is EU law governing the collection and "
            "processing of personal data of EU residents. It applies to any organization — "
            "regardless of location — that processes EU residents' data when offering goods/services "
            "to them or monitoring their behavior. Key obligations: lawful basis for processing, "
            "transparency, data subject rights (access, erasure, portability), breach notification "
            "within 72 hours, and data protection by design. Penalties up to 4% of global annual "
            "revenue or €20 million."
        ),
        "category": "Privacy",
    },
    {
        "title": "What is CCPA?",
        "question": "What rights does the California Consumer Privacy Act give California residents?",
        "answer": (
            "The CCPA (as amended by the CPRA) gives California residents the right to: know what "
            "personal information is collected and how it's used; delete personal information "
            "(with exceptions); opt out of the sale or sharing of their information; correct "
            "inaccurate information; and limit the use of sensitive personal information. It "
            "applies to businesses that meet certain thresholds (annual revenue over $25M, or "
            "processing data of 100,000+ consumers/households, or deriving 50%+ revenue from "
            "selling data). Non-compliance can result in civil penalties up to $7,500 per "
            "intentional violation."
        ),
        "category": "Privacy",
    },
    {
        "title": "What is HIPAA?",
        "question": "Who must comply with HIPAA and what does it require?",
        "answer": (
            "HIPAA (Health Insurance Portability and Accountability Act) applies to covered "
            "entities (health care providers, health plans, clearinghouses) and their business "
            "associates that handle protected health information (PHI). It requires: safeguarding "
            "PHI through administrative, physical, and technical safeguards (Security Rule); "
            "limiting disclosures to the minimum necessary; providing patients access to their "
            "records; breach notification within 60 days (Breach Notification Rule); and privacy "
            "notices. Penalties range from $100 to $50,000 per violation."
        ),
        "category": "Privacy",
    },
    {
        "title": "What constitutes a data breach?",
        "question": "What is a data breach and when must it be reported?",
        "answer": (
            "A data breach is unauthorized access to, acquisition, or disclosure of personal "
            "information. Reporting obligations vary by jurisdiction. Under most U.S. state laws, "
            "businesses must notify affected individuals and regulators within a specified period "
            "(often 30–72 hours for state AG notification, up to 90 days for individuals). GDPR "
            "requires supervisory authority notification within 72 hours. HIPAA requires "
            "notification within 60 days. Incident response plans, forensic investigation, and "
            "legal counsel involvement are critical from day one."
        ),
        "category": "Privacy",
    },
    {
        "title": "What is a privacy policy?",
        "question": "Do I legally need a privacy policy for my website?",
        "answer": (
            "A privacy policy is legally required if you collect personal information from: "
            "California residents (CCPA/CalOPPA), EU/UK residents (GDPR/UK GDPR), children "
            "under 13 (COPPA), or if you operate in states with comprehensive privacy laws "
            "(Virginia, Colorado, Texas, etc.). Even absent a specific law, many third-party "
            "services (Google, Apple App Store) contractually require one. The policy must "
            "accurately disclose: what data is collected, how it's used and shared, user rights, "
            "and how to contact you. Deceptive policies violate FTC Act Section 5."
        ),
        "category": "Privacy",
    },
    {
        "title": "What is COPPA?",
        "question": "What is COPPA and how does it affect my website or app?",
        "answer": (
            "The Children's Online Privacy Protection Act (COPPA) applies to websites, apps, and "
            "online services directed to children under 13, or that knowingly collect personal "
            "information from children under 13. Operators must: post a clear privacy policy, "
            "obtain verifiable parental consent before collecting information, allow parents to "
            "review and delete data, and maintain data security. The FTC enforces COPPA with "
            "civil penalties up to $51,744 per violation. Age-gating must be genuinely effective, "
            "not nominal."
        ),
        "category": "Privacy",
    },
    {
        "title": "What are employee privacy rights at work?",
        "question": "What privacy rights do employees have in the workplace?",
        "answer": (
            "Employee privacy rights are limited, particularly regarding company resources. "
            "Employers may lawfully monitor: company email and internet usage, work phones, "
            "workplace video surveillance (with notice in many states), and company-issued "
            "devices. Employees retain stronger privacy rights in: personal devices, private "
            "communications on personal accounts, medical information, off-duty conduct (in many "
            "states), and union activity. California, Connecticut, Delaware, and New York require "
            "employers to notify employees of electronic monitoring. Drug testing is regulated "
            "by state law."
        ),
        "category": "Privacy",
    },
    {
        "title": "What is the right to be forgotten?",
        "question": "Do I have a right to have my personal data deleted?",
        "answer": (
            "The 'right to erasure' (GDPR Article 17) allows EU/UK residents to request deletion "
            "of their personal data when it is no longer needed for its original purpose, when "
            "consent is withdrawn, or when data was unlawfully processed. Exceptions apply for "
            "legal obligations, public interest, or freedom of expression. Under the CCPA/CPRA, "
            "California residents can request deletion with similar exceptions. Most U.S. states "
            "with comprehensive privacy laws include a deletion right. Businesses must respond "
            "within 45–30 days depending on the law."
        ),
        "category": "Privacy",
    },
    {
        "title": "What is biometric data privacy?",
        "question": "What laws protect biometric data like fingerprints and facial recognition?",
        "answer": (
            "Illinois' Biometric Information Privacy Act (BIPA) is the most stringent in the U.S. "
            "It requires: written notice and consent before collecting biometric data (fingerprints, "
            "facial scans, retinal scans, voiceprints), a retention and destruction schedule, "
            "restrictions on sale or profit from biometrics, and data security safeguards. BIPA "
            "provides a private right of action with statutory damages of $1,000–$5,000 per "
            "violation. Texas, Washington, and other states have similar laws. GDPR treats "
            "biometric data as a special category requiring explicit consent."
        ),
        "category": "Privacy",
    },
    {
        "title": "What is FERPA?",
        "question": "What does FERPA protect and who does it apply to?",
        "answer": (
            "The Family Educational Rights and Privacy Act (FERPA) protects the privacy of "
            "students' education records at schools receiving federal funding. It gives eligible "
            "students (or parents of students under 18) the right to: inspect records, request "
            "corrections, and consent to disclosures. Schools may not disclose education records "
            "without consent except in defined circumstances (school officials with legitimate "
            "interest, transfers, financial aid, judicial orders). Enforcement is through the "
            "Department of Education; there is no private right of action under FERPA."
        ),
        "category": "Privacy",
    },
    {
        "title": "What is GLBA financial privacy?",
        "question": "What privacy obligations does the Gramm-Leach-Bliley Act impose on financial companies?",
        "answer": (
            "The Gramm-Leach-Bliley Act (GLBA) requires financial institutions to: provide "
            "customers with clear privacy notices explaining information-sharing practices, offer "
            "opt-out rights for sharing with non-affiliated third parties, and implement "
            "administrative, technical, and physical safeguards (Safeguards Rule). 'Financial "
            "institutions' broadly includes banks, insurers, securities firms, tax preparers, "
            "mortgage brokers, and payday lenders. The FTC Safeguards Rule requires a written "
            "information security program and annual risk assessments."
        ),
        "category": "Privacy",
    },
    {
        "title": "Can employers ask about criminal history?",
        "question": "Can a potential employer ask about my criminal record?",
        "answer": (
            "Many states and cities have 'ban the box' laws that prohibit employers from asking "
            "about criminal history on job applications or before a conditional offer is made. "
            "Federal law (EEOC guidance) cautions against blanket exclusions of applicants with "
            "convictions, as it may have disparate impact. Employers conducting background checks "
            "must comply with the Fair Credit Reporting Act (FCRA): provide notice, obtain "
            "consent, and follow adverse action procedures. Certain positions (working with "
            "children, financial roles) may permit broader inquiries by statute."
        ),
        "category": "Privacy",
    },

    # ── Business Law (12) ───────────────────────────────────────────────────────
    {
        "title": "What business structure should I choose?",
        "question": "What are the main business structures and how do I choose the right one?",
        "answer": (
            "Common structures: Sole proprietorship — simplest, no liability protection, "
            "pass-through taxation. Partnership — shared control, partners personally liable. "
            "LLC — liability protection, flexible taxation (pass-through or corporate), less "
            "formality. S-Corporation — pass-through taxation, avoids self-employment tax on "
            "distributions, but restricted to 100 U.S. shareholders. C-Corporation — full "
            "liability protection, unlimited shareholders, eligible for institutional investment, "
            "but double taxation. Consider liability exposure, tax strategy, funding needs, "
            "and administrative burden when choosing."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is the duty of fiduciary?",
        "question": "What are fiduciary duties owed by corporate directors and officers?",
        "answer": (
            "Corporate directors and officers owe two primary fiduciary duties to the corporation "
            "and its shareholders: (1) Duty of Care — act with the care a reasonably prudent person "
            "in a similar position would exercise, make informed decisions; (2) Duty of Loyalty — "
            "act in the best interest of the corporation, not personal interests, avoid "
            "self-dealing and conflicts of interest. The business judgment rule protects decisions "
            "made in good faith, with due care, and without conflict of interest from shareholder "
            "challenge."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is a shareholder agreement?",
        "question": "What should a shareholder agreement include?",
        "answer": (
            "A shareholder agreement governs the relationship among shareholders and the company. "
            "Key provisions: share transfer restrictions (rights of first refusal, drag-along, "
            "tag-along rights), buy-sell provisions (what happens when a shareholder dies, "
            "becomes disabled, or wants to exit), voting rights and deadlock resolution, "
            "anti-dilution protections, confidentiality and non-compete obligations, dividend "
            "policy, and dispute resolution. Without one, default state corporate law governs, "
            "which may not reflect the parties' intentions."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is securities fraud?",
        "question": "What constitutes securities fraud?",
        "answer": (
            "Securities fraud involves deception in connection with the purchase or sale of "
            "securities. Under SEC Rule 10b-5, it is unlawful to: make a material misstatement "
            "or omission in connection with a securities transaction, with scienter (intent to "
            "defraud or recklessness), that causes investor reliance and loss. Insider trading "
            "(trading on material non-public information) is a form of securities fraud. "
            "Penalties include SEC enforcement, disgorgement, civil penalties, and criminal "
            "prosecution (up to 20 years imprisonment)."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is a merger vs. acquisition?",
        "question": "What is the legal difference between a merger and an acquisition?",
        "answer": (
            "In a merger, two companies combine into a single surviving entity — one or both "
            "companies cease to exist as separate legal entities. In an acquisition, one company "
            "purchases another, which may continue to operate as a subsidiary or be absorbed. "
            "Asset acquisitions (buying specific assets) differ from stock acquisitions (buying "
            "ownership shares). Key legal considerations: due diligence, representations and "
            "warranties, indemnification obligations, antitrust approval (Hart-Scott-Rodino for "
            "large transactions), and regulatory approvals in regulated industries."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is antitrust law?",
        "question": "What business practices violate antitrust law?",
        "answer": (
            "Antitrust laws (Sherman Act, Clayton Act, FTC Act) prohibit: per se illegal practices "
            "(price-fixing, bid-rigging, market allocation among competitors — no justification "
            "accepted); monopolization or attempted monopolization through anticompetitive conduct; "
            "mergers that substantially lessen competition; and exclusive dealing or tying "
            "arrangements analyzed under the rule of reason. The DOJ and FTC enforce federal "
            "antitrust law; private plaintiffs can recover treble damages plus attorneys' fees."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is due diligence in a business transaction?",
        "question": "What does due diligence involve in a business acquisition?",
        "answer": (
            "Due diligence is the investigation a buyer conducts before closing a transaction. "
            "It covers: legal (corporate structure, contracts, litigation, IP ownership, regulatory "
            "compliance), financial (audited financials, tax returns, debt obligations), "
            "operational (key employees, customer concentration, supply chain), technical "
            "(IT systems, cybersecurity, software), and environmental. Findings inform purchase "
            "price adjustments, indemnification escrows, and deal-breaker determinations. Sellers "
            "typically provide a data room; buyers respond with follow-up questions."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is a term sheet?",
        "question": "What is a term sheet and is it binding?",
        "answer": (
            "A term sheet (or letter of intent) outlines the proposed terms of a deal before "
            "definitive agreements are drafted. Most provisions are non-binding — they express "
            "intent rather than create legal obligations. However, certain provisions are typically "
            "binding: exclusivity/no-shop (seller can't negotiate with others for a set period), "
            "confidentiality, and governing law. Breaching binding provisions can result in "
            "liability. Term sheets speed negotiation by aligning parties on key economic and "
            "governance terms before costly legal drafting begins."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is Chapter 11 bankruptcy?",
        "question": "What is Chapter 11 bankruptcy and when should a business consider it?",
        "answer": (
            "Chapter 11 allows a financially distressed business to reorganize its debts while "
            "continuing operations. The debtor (or a trustee) proposes a reorganization plan "
            "to restructure debt, reject burdensome contracts and leases, and emerge as a viable "
            "enterprise. An automatic stay stops all collection actions upon filing. Creditors "
            "vote on the plan; court confirmation binds all creditors. Small businesses may use "
            "the streamlined Subchapter V process. Chapter 11 is expensive and time-consuming; "
            "consider it when the business has a viable core but unsustainable debt load."
        ),
        "category": "Business Law",
    },
    {
        "title": "What are SOX compliance requirements?",
        "question": "What does the Sarbanes-Oxley Act require of public companies?",
        "answer": (
            "The Sarbanes-Oxley Act (SOX) applies to public companies and establishes: CEO and CFO "
            "certification of financial statements (Section 302), management assessment of "
            "internal controls over financial reporting and auditor attestation (Section 404), "
            "prohibition on personal loans to executives, whistleblower protections, enhanced "
            "financial disclosure, auditor independence rules, and document retention requirements. "
            "Violations can result in criminal penalties (up to 20 years for willful violations). "
            "Many private companies voluntarily implement SOX-like controls in preparation for "
            "an IPO."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is a regulatory compliance program?",
        "question": "What elements does an effective corporate compliance program include?",
        "answer": (
            "An effective compliance program (per DOJ guidelines) includes: written policies and "
            "a code of conduct, a designated compliance officer with adequate resources, risk "
            "assessments tailored to the company's industry and operations, training and "
            "communication, confidential reporting mechanisms (hotlines), investigation procedures "
            "for reported issues, disciplinary mechanisms, due diligence on third parties, "
            "periodic program evaluation, and continuous improvement after detected violations. "
            "A well-designed and genuinely implemented program can reduce penalties in enforcement "
            "actions."
        ),
        "category": "Business Law",
    },
    {
        "title": "What is a UCC financing statement?",
        "question": "What is a UCC-1 financing statement and why does it matter?",
        "answer": (
            "A UCC-1 financing statement is filed under the Uniform Commercial Code to publicly "
            "notice a secured creditor's interest in a debtor's personal property (collateral). "
            "Filing perfects the security interest and establishes priority against other creditors "
            "and bankruptcy trustees. It is filed with the Secretary of State in the debtor's "
            "state of organization. Financing statements are effective for 5 years and must be "
            "continued before expiration. Lenders, landlords, and equipment financers routinely "
            "search UCC filings during due diligence."
        ),
        "category": "Business Law",
    },
]
