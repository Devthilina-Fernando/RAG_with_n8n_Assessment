## 1. Document Processing Architecture

The document processing layer needed to handle diverse content (PDFs, DOCX, HTML, etc.), languages (English, Sinhala, Tamil), and formatting styles (tables, bullet lists, etc.). The goal was to create context preserving and semantically coherent chunks for embedding.

### Approach

- **Parsing**  
  To ensure robust content extraction, we can utilized a combination of tools
  - **LangChain’s document loaders** (e.g., `PDFLoader`, `TextLoader`) for seamless integration with the pipeline.
  - **Apache Tika** for handling a wide variety of file formats with strong language detection and content extraction.
  - **Unstructured.io** to extract and standardize content from complex layouts including tables, lists, and headers.

- **Chunking Strategy**
  - **Sliding Window with Overlap**  
    LangChain’s `RecursiveCharacterTextSplitter` with domain specific tuning can be used. Default was 512 token chunks with 20% overlap (~100 tokens), balancing context retention and vector dimensionality.

    chunk size can be vary depends on the size and the content of the document.
  

- **Metadata Enrichment**  
  Each chunk can be annotated with metadata such as
  - Source
  - Author
  - Timestamp
  - Language

  This supports hybrid search, traceability, and filtered query refinement.

---

## 2. Production Monitoring and Observability

Ensuring system observability was essential due to the asynchronous nature of components (e.g., n8n for ingestion, LangChain for retrieval).

### Monitoring Stack

- **Metrics & Logs**
  - **Prometheus + Grafana**: Metrics collection and dashboard visualization
  - **Loki**: Log aggregation
  - **LangSmith**:
    - Deep integration with LangChain for tracing, debugging, and prompt/version management
    - Visualizes full execution paths (retriever > LLM > output)
    - Supports dataset evaluation, agent runs, and model comparisons
  - **Langfuse**:
    - More general purpose observability for LLM applications
    - Works with any LLM (including OpenAI GPT-4) and frameworks beyond LangChain
    - Supports self hosting, custom metrics, user session tracking, and manual event logging

### Key Performance Indicators (KPIs)

- Embedding latency (per document/chunk)
- Vector store ingestion success rate
- Retrieval latency and accuracy (via synthetic QA evaluation or user feedback)
- LLM API call latency and failure rates
- Token consumption (to monitor usage and control costs)
- RAG response accuracy and hallucination rate (tracked via LangSmith or Langfuse)

### Alerting Mechanisms

- **PagerDuty**: For critical failures (e.g., pipeline crash, vector DB unavailable)
- **Slack Integrations**: For warning thresholds and performance degradation alerts
- **LangSmith**: Trigger alerts on specific run failures, token overuse, or model drift
- **Langfuse**: Define custom alert rules (e.g., error rates, latency spikes)

### Debugging Tools

- **n8n Logs**: Payload inspection using JSON-formatted execution logs
- **LangChain Verbose Mode**: Step-by-step visibility into prompt chaining and retriever use
- **LangSmith**:
  - Explore execution graphs of chains and agents
  - Compare different prompt versions and runs
  - Built-in evaluation datasets for QA performance benchmarking
- **Langfuse**:
  - End-to-end trace visualization (prompt → LLM → output)
  - Attach user session context for debugging real-world flows
  - Use with or without LangChain

### Performance Optimization

- Periodic batch profiling of queries with known answers
- Analyzed latency spikes and optimized bottlenecks (e.g., DB connection pooling, embedding queue throughput)
- Indexed slow query logs for correlation with load and latency
- **LangSmith**:
  - Built-in evaluation tools and structured run comparison for regression testing
  - Track performance over time with dataset accuracy tracking
- **Langfuse**:
  - User behavior analytics and prompt effectiveness
  - Custom dashboards for identifying latency trends and cost hotspots


---

## 3. LLM Selection Strategy

### Model Strategy

The system needs a balance between **answer quality**, **cost-effectiveness**, and **ease of maintenance**.

- **Primary Model (API-Based)**  
  **OpenAI GPT-4-turbo**  
  - Best suited for high quality answers in production due to superior instruction following, long context (128k tokens), and strong support/documentation.  
  - Reliable uptime and minimal operational overhead.  
  - Ideal for critical customer facing use cases where trust and completeness matter.

- **Fallback/Cost-Optimized Model (Self-Hosted)**:  
  **Mistral 7B** via **vLLM** or **Ollama**  
  - Suitable for internal or budget constrained use cases.  
  - Can be containerized for on premise or GPU backed cloud environments.  
  - Lower inference cost, though quality may degrade on nuanced tasks.

---

### Context Window Considerations

- **GPT-4-turbo**
  - 128k context window allows entire document sections to be passed without chunking, reducing hallucination risk.

- **Mistral 7B**
  - Limited to ~32k tokens (when optimized with vLLM).
  - Requires chunk merging strategies and careful retrieval logic (e.g., windowed retrieval or re-ranking).

---

### Model Evaluation & Quality

- Each candidate LLM was benchmarked on internal domain specific QA datasets.
- **GPT-4-turbo** consistently outperformed in accuracy, coherence, and factual correctness.
- **Mistral 7B** performed reasonably well on factual retrieval but struggled with long-context reasoning and ambiguous queries.

---

### Multimodal Handling (Optional)

- If image heavy or scanned PDFs are included,
  - Use **GPT-4V (Vision-enabled)** for native OCR and layout comprehension.
---

### Hosting Strategy

- **API-Based (Recommended)**:
  - OpenAI provides a fully managed service with,
    - Low maintenance
    - Automatic scaling
    - Minimal infrastructure burden
    - Built-in observability and access controls
  - No GPU setup or DevOps team required.

- **Self-Hosted**,
  - Models like **Mixtral** or **Mistral** can be deployed using **vLLM** or **Ollama**, but
    - Require GPU infrastructure
    - Need monitoring (e.g., Prometheus/Grafana)
    - Maintenance and security overhead
    - Skilled engineers for deployment and updates

---

### Final Recommendation

For the current RAG system built using **n8n** and **LangChain**, the most **suitable LLM** is:

> **OpenAI GPT-4-turbo** via API

**Why**
- 128k token context is ideal for chunk heavy RAG pipelines.
- High quality, reliable answers.
- Fast integration with LangChain.
- No DevOps/GPU burden—ideal for rapid production.

Self hosted models like **Mistral 7B** are best used for fallback or internal testing environments where cost is a stronger constraint than precision or uptime.


---

## 4. Security and Privacy Architecture

Security practices must be concidered due to sensitive nature of documents and user interactions.

### Data Protection

- **Data Masking**  
  Can apply regex masking for sensitive fields like,
  - Emails
  - Phone numbers
  - National IDs  
  Replace with placeholder tokens (e.g., `[EMAIL]`) before embedding

- **Access Control**
  - Enforced RBAC across UI and API
  - Each chunk stored with permission metadata

- **Audit Logging**
  - Can log every user interaction with,
    - User ID
    - Timestamp
    - Response metadata
    - Document tracebacks  
  - Encrypted logs at rest and rotated weekly

### Compliance

- Can follow GDPR-aligned practices,
  - Right to deletion
  - Consent-based ingestion
  - Data portability

- Encryption
  - AES-256 at rest
  - TLS 1.3 in transit



---

## 5. Scalability Architecture

Designed the pipeline to handle increasing ingestion and query traffic via horizontal scaling.

### Vector Store

- **Backend**:  
  Qdrant with HNSW indexing and sharding

- **Deployment**:  
  Kubernetes with autoscaling, tenants segmented by department/project

### Caching Strategy

- Redis caching server can be used for,
  - Query result caching (based on embedding hash)
  - Pre-computed summaries of high-frequency documents


### Load Balancing

- Ingress Routing with NGINX - Direct traffic to specific services (API, retriever, LLM) based on path or headers using NGINX ingress.
- Weighted reverse proxy - Route requests to LLM worker nodes based on custom weights (e.g., GPU capacity), allowing dynamic load distribution.
- Round-Robin Load Balancing - NGINX's default round-robin method to evenly distribute incoming requests across multiple backend pods, ensuring simple and effective load spreading.

### Database Scalability (Pinecone)

- **Tenant-based Sharding**  
  Used Pinecone namespaces or metadata filters to isolate data by tenant ID.

- **Indexed Metadata**  
  Metadata fields are indexed for fast and filtered document vector retrieval.

- **Auto-Scaling Vector Store**  
  Pinecone handles scaling and partitioning automatically based on load and data volume.

- **High-Concurrency Support**  
  Built-in support for concurrent vector queries—no need for connection pooling tools like PgBouncer.

- **Optimized Retrievals**  
  Tuned top-k search and pre-filtering for low-latency, accurate responses.


---

