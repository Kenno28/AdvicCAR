## LLM Choice

For the current version of AdviCAR, I selected **OpenAI GPT-5 Nano**.

This decision is mainly pragmatic. At this stage, the goal of the project is not to run extensive cross-model benchmarks, but to build a working end-to-end system with a reliable and lightweight language model.

In AdviCAR, the LLM is responsible for:
- combining structured vehicle comparison results with retrieved domain knowledge
- generating a readable price assessment
- providing short buying advice
- explaining the reasoning in a clear and understandable format

The focus of V1 is on validating the system design and workflow first.  
Model comparison and deeper evaluation against other LLMs can be added in later iterations if needed.