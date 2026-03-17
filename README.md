# AdviCAR

AdviCAR is an early-stage AI project that analyzes a car listing and provides a **rough price assessment**, **buying advice**, and **model-specific risk hints**.

The goal of this project is **not** to build a perfect automotive valuation system from day one.  
Instead, the goal is to build a small but meaningful system that combines:

- structured vehicle comparison
- Retrieval-Augmented Generation (RAG)
- LLM-based reasoning and explanation

AdviCAR starts as a focused mini-project and is designed to grow step by step into a more advanced production-ready system later.

---

## Project Goal

The main purpose of AdviCAR is to answer questions like:

- Is this car listing **fairly priced**?
- Is it **too expensive** or a potential **good deal**?
- What are the **typical weaknesses** of this model?
- What should a buyer **pay attention to before purchasing**?

This project is intentionally built as a learning project with real substance.  
It should be useful, realistic, and extendable - not a perfect end product from the start.

---

## Why This Project?

I wanted to build something that is:

- personally interesting
- practical enough to be used
- technically expandable
- strong enough to become portfolio material later

Instead of building a generic chatbot, AdviCAR focuses on a concrete use case:
**car listing analysis with structured comparison + RAG-based domain knowledge**.

---

## Scope of V1

Version 1 is intentionally narrow.

### Input
- A car listing link  
  **or**
- Manually entered vehicle data

### Extraction / Normalization
The system should extract or normalize the relevant vehicle information into a structured format, such as:

- brand
- model
- generation
- engine / variant
- year
- mileage
- price
- equipment
- condition
- location
- notes from the free-text description

### Structured Store
A structured dataset of comparable vehicles, including:

- price
- mileage
- year
- equipment
- condition

This store is used for rough market comparison.

### RAG Store
A separate knowledge base containing model-specific information such as:

- common weaknesses
- strengths
- known issues
- buying advice
- red flags
- variant-specific risks

This store is used for retrieval and grounding.

### Price Assessment Logic
The system should compare the input listing to similar vehicles and apply simple rules to estimate whether the listing is:

- rather cheap
- rather fair
- rather expensive

### LLM Output
The LLM should generate a response that includes:

- a price judgment
- a short explanation
- buying advice
- model-specific risks
- sources, if available

### Uncertainty / Fallback
If the system cannot find enough comparable vehicles or relevant model knowledge, it should explicitly communicate that the confidence is low.

---

## Why RAG Is Used

RAG is not used to calculate the price directly.

RAG is used to retrieve **domain knowledge** such as:

- common model weaknesses
- known reliability issues
- purchase warnings
- strengths and weaknesses of specific variants

The pricing logic should mainly rely on **structured comparison data**, while RAG provides additional expert-like context and grounding.

This separation is important because:

- structured data is better for comparison
- RAG is better for unstructured domain knowledge
- the LLM is better for combining both into a readable explanation

---

## High-Level Architecture

AdviCAR is currently planned as a system with the following conceptual flow:

1. **User Input**
   - listing link or manual car data

2. **Extraction / Normalization**
   - convert raw input into structured vehicle attributes

3. **Structured Retrieval**
   - find similar vehicles from the structured comparison dataset

4. **RAG Retrieval**
   - retrieve relevant model knowledge from the knowledge base

5. **Assessment Logic**
   - compare price-related factors such as mileage, year, condition, and equipment

6. **LLM Explanation**
   - generate final output with reasoning and buying advice

---

## Current Design Principles

This project follows a few important principles:

- start small
- keep the first version narrow
- avoid overengineering
- learn by building and making mistakes
- grow the project step by step

The first version is **not** intended to be a polished production product.  
It is intended to be a solid and honest first version with room to improve.

---

## Evaluation Goals

AdviCAR should not only “sound good” - it should also be testable.

### RAG Evaluation
Possible retrieval-focused evaluation metrics:

- Recall@K
- Precision@K
- Context relevance
- retrieval correctness for the right model / variant

### LLM Output Evaluation
Possible response-focused evaluation criteria:

- price judgment plausibility
- explanation completeness
- groundedness
- uncertainty handling
- output consistency

In early versions, evaluation will likely be based on **manual test cases** and small custom benchmarks.

---

## Planned Limitations of V1

Version 1 will **not** try to solve everything.

### Out of Scope for V1
- multiple brands at once
- large-scale live scraping
- full production deployment
- image-based vehicle analysis
- alerts / watchlists
- advanced valuation models
- perfect market price prediction

---

## Roadmap

### V1
- single brand or narrow model family
- listing input
- structured comparison
- RAG-based model knowledge
- simple LLM output
- basic manual evaluation

### V2
- stronger comparison logic
- cleaner data extraction
- improved retrieval quality
- more robust evaluation
- better output formatting

### Future Flagship Version
- API layer
- persistent storage
- monitoring
- logging
- CI/CD
- deployment
- more brands / models
- stronger valuation logic
- optional image-based inspection support


## Main Learning Objectives

This project is also a personal learning project.  
The main learning goals are:

- understanding how to combine LLMs with RAG in a meaningful way
- designing a system around both structured and unstructured data
- learning from real implementation mistakes
- building something that can later evolve into a stronger portfolio project

---

## Project Philosophy

AdviCAR is not meant to be the “perfect project”.  
It is meant to be a project with real substance that starts small and improves over time.

The goal is simple:

> build something real, make mistakes, learn from them, and gradually turn it into something stronger.