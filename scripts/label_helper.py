"""Print hybrid_retrieve output for a fixed set of questions, for manual relevance labeling.

Run this, review each question's retrieved chunks by eye, and use what you see to
build a labeled test set (e.g. data/eval/test_questions.json) for evaluate_retrieval.py.
This script does not judge relevance or write labels itself.
"""
from query_rag import hybrid_retrieve

QUESTIONS = [
    "How does control-token-augmented Dense Passage Retrieval improve retrieval accuracy?",
    "What retrieval strategy does MultiRAG use to mitigate hallucination from inconsistent multi-source information?",
    "How does Blended RAG combine semantic search with hybrid query-based retrievers?",
    "What does Tree of Reviews propose for multi-hop question answering?",
    "How do multi-agent architectures coordinate retrieval across diverse data sources?",
    "What chunking strategies does the \"Reconstructing Context\" paper evaluate for RAG?",
    "How does R²AG incorporate retrieval information back into the generation process?",
    "What method does DeepCodeSeek use for real-time API retrieval in code generation?",
    "How does the TREC 2025 RAG Track evaluate retrieval-augmented systems?",
    "What challenges does industry face when deploying RAG systems, per the interview study?",
    "How does the Context Tuning approach improve retrieval-augmented generation?",
    "What does \"How Do LLMs Cite?\" find about attribution mechanisms in RAG-generated citations?",
    "How does RAC (Retrieval-Augmented Clarification) improve faithfulness in conversational search?",
    "What adaptive retrieval strategy is proposed for large reasoning models deciding when to retrieve?",
    "How does video-enriched RAG use aligned video captions for retrieval?",
    "What are common evaluation metrics used to measure RAG system quality across these papers?",
    "What approaches exist for improving retrieval accuracy beyond standard dense passage retrieval?",
    "How does BM25 handle typos and misspelled queries?",
    "What are the legal requirements for deploying AI systems in the EU under the AI Act?",
    "How does spatial augmented reality affect user locomotion in physical environments?",
]


def print_retrieval_report(questions: list[str]) -> None:
    for i, question in enumerate(questions, start=1):
        chunks = hybrid_retrieve(question)
        print(f"{'=' * 80}")
        print(f"Q{i}: {question}")
        print(f"{'=' * 80}")
        for rank, chunk in enumerate(chunks, start=1):
            meta = chunk["metadata"]
            snippet = chunk["text"][:150].replace("\n", " ")
            print(f"  [{rank}] chunk_id: {chunk['chunk_id']}")
            print(f"      paper: {meta['source_paper']}")
            print(f"      text:  {snippet}...")
        print()


if __name__ == "__main__":
    print_retrieval_report(QUESTIONS)
