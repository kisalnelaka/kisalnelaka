# Kisal Nelaka
### Systems Architect & Senior Software Engineer

<div align="center">
  <a href="https://linkedin.com/in/kisalnelaka"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="mailto:kisalnelaka6@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="https://kisalnelaka.github.io"><img src="https://img.shields.io/badge/Portfolio-252525?style=for-the-badge&logo=app-store&logoColor=white" alt="Portfolio" /></a>
  <a href="https://medium.com/@kisalnelaka6"><img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium" /></a>
</div>

<br/>

<div align="center">
  <img src="tech-dashboard.svg" alt="Technical Dashboard" />
</div>

<br />

### Technical Profile
- **8+ Years Experience**: Full-stack engineering, systems architecture, and offensive security.
- **Specialty**: High-performance APIs, multi-tenant SaaS, and persistent memory frameworks.
- **Status**: Available for high-impact engineering roles. No fluff.

---

I build systems that work. I don't write bloat. 

8+ years across enterprise infrastructure, distributed systems, and security research. My background in cybersecurity means I assume everything is broken until I've audited the code. I build for performance, strict data isolation, and sub-millisecond latency. 

I solve technical problems. I don't care for corporate buzzwords or 'revolutionary' marketing. If a system is slow, it's poorly architected. I fix that.

---

### Technical Capabilities & Stack

- **Core Languages**: PHP (8.3+), TypeScript, Python, C#, Kotlin, C++.
- **Backend**: Laravel (Core/Internals), Node.js, Persistent Memory Architectures, Radix Tree Routing.
- **Frontend**: React, Vue, Native JS (No bloat), Tailwind.
- **Systems & Security**: Docker, Linux Kernel/PCNTL, Pentesting (OSCP-style), CI/CD Automation.
- **Focus**: Eliminating overhead, AOT compilation, and non-blocking I/O via Fibers.

---

### Certifications
- **[Palo Alto Networks Cybersecurity Professional Certificate](https://coursera.org/share/8b661cf253f9cd00f82c4f0a97505873)** - Palo Alto Networks
- **[Applied ChatGPT for Cybersecurity](https://coursera.org/share/ded5691396575d2b4d12418ebe61a13b)** - Infosec
- **[Introduction to SIEM (Splunk)](https://coursera.org/share/0e102acf787e47362780f8007c5284c9)** - EDUCBA

---

### Recently Active Repositories
<!-- RECENT-REPOS:START -->
- [nexusflow_erp](https://github.com/kisalnelaka/nexusflow_erp) - Multi-tenant ERP architected for high-performance inter-service communication.
- [path_setter](https://github.com/kisalnelaka/path_setter) - CLI utility for automated system path configuration and environment management.
- [thenet](https://github.com/kisalnelaka/thenet) - Decentralized mesh network for peer-to-peer file orchestration and media streaming.
- [noor](https://github.com/kisalnelaka/noor) - Asynchronous AI concierge system with complex state management.
- [Imladris](https://github.com/kisalnelaka/Imladris) - Offline-first knowledge engine utilizing a semantic neural graph.
<!-- RECENT-REPOS:END -->

---

### Engineering Showcase

#### [Aether](https://github.com/kisalnelaka/aether)
**Persistent Memory PHP Framework**
* **The Problem:** Modern frameworks are bloated, relying on regex routing and massive dependency trees that kill performance.
* **The Solution:** A zero-dependency framework built for speed. Uses a Radix Tree router (O(K) matching), Fibers for non-blocking I/O, and AOT attribute compilation.
* **Key Impact:** Sub-millisecond boot times. Runs in persistent memory (no reload on request). Zero external dependencies.
* **Tech Stack:** PHP 8.3+, Fibers, Radix Tree, PCNTL.

#### [Bunny](https://github.com/socialrabbit/bunny)
**Application Scaffolding Engine**
* **The Problem:** Standard boilerplates are either too generic or too bloated for rapid domain-specific deployment.
* **The Solution:** An automated scaffolding engine for Laravel that generates domain-specific architectures (E-commerce, LMS, Portfolio) with integrated CMS and RBAC.
* **Key Impact:** Reduced project initialization time from days to minutes. Clean, standardized code generation without the typical "package bloat."
* **Tech Stack:** PHP, Laravel, Vue/React, Tailwind.

#### [TenancyOS](https://github.com/kisalnelaka/TenancyOS)
**Multi-Tenant Infrastructure**
* **The Problem:** Most SaaS platforms leak data due to poor tenant scoping or over-complex RBAC.
* **The Solution:** Engineered a strict multi-tenant monolith with automated global scoping and hardware-level isolation concepts in the application layer.
* **Key Impact:** 100% data isolation guaranteed. Scalable tenant onboarding through automated provisioning.
* **Tech Stack:** Laravel, React, PostgreSQL.

#### [TheNet](https://github.com/kisalnelaka/thenet)
**Decentralized Mesh Architecture**
* **The Problem:** Cloud-dependency for local file sharing is a security risk and adds unnecessary latency.
* **The Solution:** Built a decentralized mesh network for secure, zero-latency local file management and media synchronization.
* **Key Impact:** Zero cloud reliance. High-speed local peer-to-peer transfers.
* **Tech Stack:** Node.js, WebSockets, React.

#### [NOOR Elite](https://github.com/kisalnelaka/noor)
**Asynchronous AI Orchestration**
* **The Problem:** Sequential AI processing is too slow for real-world concierge workflows.
* **The Solution:** Developed a non-blocking AI orchestration layer with complex state management for concurrent task execution across multiple LLM providers.
* **Key Impact:** 99.9% task reliability. Optimized token usage and response latency.
* **Tech Stack:** Dart, Flutter, Custom LLM Handlers.

#### [Imladris](https://github.com/kisalnelaka/Imladris)
**Graph-Based Knowledge Engine**
* **The Problem:** Hierarchical note-taking is primitive; it doesn't represent how humans link information.
* **The Solution:** Architected a spatial knowledge engine using a custom neural graph to map semantic connections between data points offline.
* **Key Impact:** High-speed semantic retrieval. 100% offline-first privacy.
* **Tech Stack:** Kotlin, Android SDK, Graph Theory.

#### [Vendetta 84](#)
**Performance-Optimized Game Engine Implementation**
* **The Problem:** Visual fidelity usually comes at the cost of high CPU/GPU overhead on mobile.
* **The Solution:** Custom Unity implementation focused on memory management, optimized AI state machines, and event-driven interaction scripts.
* **Key Impact:** 60FPS consistent performance on mid-range hardware without compromising the aesthetic.
* **Tech Stack:** Unity, C#, SDL2.

---

### Technical Writing & Publications
<!-- BLOG-POST-LIST:START -->
- [Building InfraFlow: A Production-Grade Multi-Tenant MSP Platform with Laravel 11 and Filament v3](https://medium.com/@kisalnelaka6/building-infraflow-a-production-grade-multi-tenant-msp-platform-with-laravel-11-and-filament-v3-b0070a377124?source=rss-3dd06b9e0f4------2)
- [Bunny: Revolutionizing Web Development with Laravel](https://medium.com/@kisalnelaka6/bunny-revolutionizing-web-development-with-laravel-12c1f26d14fc?source=rss-3dd06b9e0f4------2)
- [Bunny: The Laravel Scaffolding Package That Makes Web Development a Hop](https://medium.com/@kisalnelaka6/bunny-the-laravel-scaffolding-package-that-makes-web-development-a-hop-7276d4efdf57?source=rss-3dd06b9e0f4------2)
- [JavaScript for Clueless Newbies:Part 1 — Variables, Data Types, &amp; Operators](https://medium.com/@kisalnelaka6/javascript-for-clueless-newbies-part-1-variables-data-types-operators-ae71e4d01ce8?source=rss-3dd06b9e0f4------2)
- [Part 3: Lure Creation — The Art of Deception in Phishing Attacks](https://medium.com/@kisalnelaka6/part-3-lure-creation-the-art-of-deception-in-phishing-attacks-1f677e4eb613?source=rss-3dd06b9e0f4------2)
- [Part 2: The Reconnaissance Phase — Uncovering the Secrets of Phishing Preparation](https://medium.com/@kisalnelaka6/part-2-the-reconnaissance-phase-uncovering-the-secrets-of-phishing-preparation-05f34de00b7b?source=rss-3dd06b9e0f4------2)
- [The Lifecycle of a Phishing Attack: How Cybercriminals Bait, Hook, and Exploit](https://medium.com/@kisalnelaka6/the-lifecycle-of-a-phishing-attack-how-cybercriminals-bait-hook-and-exploit-e05cce7e4f5f?source=rss-3dd06b9e0f4------2)
- [PhishCatcher: Real-Time Phishing Detection with Chrome Extensions and Machine Learning](https://medium.com/@kisalnelaka6/phishcatcher-real-time-phishing-detection-with-chrome-extensions-and-machine-learning-450bf06e78c2?source=rss-3dd06b9e0f4------2)
- [Building a Blockchain-Powered, Encrypted Chat Application with Python](https://medium.com/@kisalnelaka6/building-a-blockchain-powered-encrypted-chat-application-with-python-103f116fad34?source=rss-3dd06b9e0f4------2)
- [Demystifying Shellcode Generation: A Guide for Beginners](https://medium.com/@kisalnelaka6/demystifying-shellcode-generation-a-guide-for-beginners-e8b536599296?source=rss-3dd06b9e0f4------2)
<!-- BLOG-POST-LIST:END -->

---

*If you have a technical problem that needs solving, contact me. If you want to talk about "synergy," don't.*
