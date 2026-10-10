# Claims to label

For each claim, judge ONLY against the excerpts shown for its question (no outside knowledge),
and write one label per claim_id in `labels.csv`:

- `supported` - the excerpts state the claim or directly entail it
- `contradicted` - the excerpts state something incompatible with it
- `not_supported` - neither (including true-in-the-world facts the excerpts don't state)

---

## q001: What F1-scores did RATE and the BERT-based comparison model achieve for technology extraction, per RATE's evaluation on the gold-standard dataset of 70 articles?

<details><summary>Excerpts</summary>

**[C1]**

```
[RATE: An LLM-Powered Retrieval Augmented Generation Technology-Extraction Pipeline, chunk_14]
 weights of edges connected to a node.
Girvan-Newman modularity 0.44 A measure of the strength of division of a network into communities.
Louvain modularity 0.395 A measure of the strength of division of a network into communities.
III. R ESULTS
A. Performance Evaluation of RATE and BERT
To evaluate the performance of the RATE pipeline, three
gold-standard labeled lists were created by three domain
experts who independently reviewed 70 randomly selected
papers from the primary corpus. For each of these 70 papers,
the experts manually identified technologies based on the com-
bined title, abstract, and author keywords, this identification
and selection of technologies were based on the same defi-
nitions presented to the RATE. After discussing the potential
terms indicating technologies, a single gold standard list based
on the previous three were created. The technologies extracted
by RATE and BERT for these 70 papers were then compared
against the gold-standard list to identify True Positives (TP),
False Positives (FP), and False Negatives (FN) of both models.
Consequently, precision, recall, and F1-score were calculated
for RATE and BERT.
Calculated precision, recall, and F1-score for BERT were
39.16%, 85.50%, and 53.73% respectively. While the results
for RATE were significantly superior with 94.26% precision,
88.47% recall, and 91.27% F1-score. RATE’s superior F1-
score highlights its effectiveness in balancing high precision
with strong recall, without requiring annotated training data.
To the best of our knowledge, this F1-score represents a
state-of-the-art performance for technology extraction in a
general context from scientific literature, particularly in zero-
shot settings.
B. Descriptive Statistics of Extracted Technologies
The RATE pipeline was applied to the entire corpus of
678 scientific papers focusing on the intersection of XR and
BCI, published between 2000 and 2024. This comprehensive
analysis identified and validated a total of 3,181 unique tech-
nology terms across all documents. Regarding the distribution
of technologies per paper, the most frequently occurring counts
of unique technologies were 8 (observed in 78 papers), 7 (in
76 papers), and 9 (in 75 papers). On average, each paper
contained 
```

**[C2]**

```
[RATE: An LLM-Powered Retrieval Augmented Generation Technology-Extraction Pipeline, chunk_10]
 list is then checked against
a user-defined, domain-specific list of prohibited or overly
generic terms, allowing for user-defined exclusion of tech-
nologies. Subsequently, an acronym-priority deduplication was
performed to manage instances where both an acronym and its
full expanded form exists, retaining the more concise version
if they refer to the same base concept. The final remaining
technology terms are then sorted alphabetically, yielding the
refined list of technologies extracted from each paper.
D. Output Evaluation
To evaluate the performance of the RATE pipeline, a
ground truth dataset was established. First, 70 scientific papers
were randomly selected from the 678 collected documents.
Then, three domain experts independently reviewed the title,
abstract, and author keywords for each of these papers to
manually compile a gold-standard list of technologies. In the
next step, same technologies extracted by all experts were
added to the final list and the remaining technologies were
debated whether to be omitted or to be added to the final
list. The result was a final gold standard list approved by all
experts. Following this, the list of technologies extracted by
the RATE pipeline for these same 70 papers was presented
to each expert. They were then tasked with identifying True
Positives (TP), False Positives (FP), and False Negatives (FN)
by comparing RATE’s output against the final curated gold-
standard list. Based on experts’ assessment, Precision and
Recall were calculated. In the next step the comparison of
the proposed model with another state-of-the-art model was
required. Therefore, a supervised machine learning model has
been trained for the task of the technology extraction from text
so its results would be compared with RATE’s output and the
gold standard list of technologies.
E. BERT baseline for technology extraction
Bidirectional Encoder Representations from Transformers
(BERT) is a pretrained transformer with ability to achieve
exceptional results in many tasks including sequence classi-
fication [29], [30]. Using this model, we aimed to imply a
supervised machine learning model for the technology extrac-
tion task which then enabled us to quantify the precision and
F1-score of our model which did not benefit from a training
phase.
The BERT model was fine-tuned on a custom NER dataset
comprising approximately 2200 rows of tokenized scien-
tific sentences from domains
```

**[C3]**

```
[RATE: An LLM-Powered Retrieval Augmented Generation Technology-Extraction Pipeline, chunk_11]

F1-score of our model which did not benefit from a training
phase.
The BERT model was fine-tuned on a custom NER dataset
comprising approximately 2200 rows of tokenized scien-
tific sentences from domains like neuroscience, robotics, and
VR/AR, sourced from open-source publications. BIO tags
were used in the task of curating this dataset, B-TECH
indicating the beginning of a technology, I-TECH for inside
of a technology entity, and O for a non-technology token. The
dataset were split into training (80%), validation (10%), and
test (10%) sets.
”bert-base-cased” variant from Hugging Face Transform-
ers library were used as the base model, initialized with 3
output labels corresponding to the BIO tags [31]. The dataset
was preprocessed into a custom NERdataset class, handling
tokenization, padding/truncation to a maximum length of
128 tokens, and alignment of labels with subword tokens.
Training was conducted using the Trainer API with the fol-
lowing hyperparameters: 20 epochs, batch size of 16, learning
rate of 2e-5, AdamW optimizer with weight decay of 0.01,
and early stopping based on F1-score on the validation set.
Evaluation metrics included token-level accuracy and entity-
level F1-score, accounting for partial matches in multi-word
entities. This BERT baseline was trained on a GPU-enabled
environment, achieving convergence after 15 epochs. Post-
training, the model was used to predict technology entities
on unseen test texts by aggregating B-TECH and I-TECH
tokens into phrases, filtering out single-token noise through
post-processing.
F . Technology Mapping and Co-occurrence Analysis
Following the extraction and validation of technology terms
by the RATE pipeline for each of the 678 scientific papers, a
co-occurrence analysis was conducted to map and visualize the
relational structure of these technologies within the BCI-XR
research domain. This analysis aimed to identify prominent
technologies, understand their interconnections, and reveal
underlying thematic groupings. Two technologies were consid-
ered to co-occur if they both appeared in the final validated list
of extracted technologies for the same scientific paper. This co-
occurrence data was used to construct a network where each
unique validated technology
```

**[C4]**

```
[Subjective Question Answering: Deciphering the inner workings of Transformers in the realm of subjectivity, chunk_66]
 task, BERT Sbj(q,a), achieved an F1-score of 54.17%, when ﬁne-
tuned on Dsubj and 52.80% when ﬁne-tuned onDcombrespectively. There is, however, no statistically signiﬁcant
difference with respect to the F1-scores between BERT Sbj(q,a) and BERT Sbj(q,a)+ H IGHWAY according to
an independent t-test at α= .05. Whether the model was optimized to classify ( q,c) or (q,a), however, made
a notable impact on model performance. ¯ΘSbj(q,a) performed better than ¯ΘSbj(q,c) in both ﬁne-tuning set-ups.
The difference between the average models was even statistically signiﬁcant when trained on Dcomb at α= .05
(see Table 6.8). This is in line with training and evaluation curves displayed in Figure 6.2, where bothF1 scores
on the train and development set respectively are higher and the minimum evaluation loss lower for models that
were to classify (q,a) sequence pairs. For models that were optimized to classify (q,c) sequences it seems as if
the models were not learning anything at all during training (see Figure 6.2).
Interestingly, an additional recurrent neural model, namely BiLSTM, on top of BERT that takes into ac-
count temporal dependencies between timesteps in a sequence of tokens x, did not help on this task. It neither
deteriorated nor enhanced the model’s performance. Therefore, I did not report BERT + BiLSTM results in
Figures and Tables respectively.
MODEL \FINE -TUNING SUBJ QA C OMBINED
F1 F1
BERTSbj(q,c) 54.17 51.92
BERTSbj(q,c) + Highway 51.92 51.92
¯ΘSbj(q,c) 53.05 51.92
BERTSbj(q,a) 54.17 52.80
BERTSbj(q,a) + Highway 52.79 53.07
¯ΘSbj(q,a) 53.47 52.94 *
Table 6.8: Subjectivity classiﬁcation. Exclusively macro F1 scores reported due
```

**[C5]**

```
[RATE: An LLM-Powered Retrieval Augmented Generation Technology-Extraction Pipeline, chunk_1]
In an era of radical technology transformations,
technology maps play a crucial role in enhancing decision
making. These maps heavily rely on automated methods of tech-
nology extraction. This paper introduces Retrieval Augmented
Technology Extraction (RATE), a Large Language Model (LLM)
based pipeline for automated technology extraction from scien-
tific literature. RATE combines Retrieval Augmented Generation
(RAG) with multi-definition LLM-based validation. This hybrid
method results in high recall in candidate generation alongside
with high precision in candidate filtering. While the pipeline is
designed to be general and widely applicable, we demonstrate
its use on 678 research articles focused on Brain-Computer
Interfaces (BCIs) and Extended Reality (XR) as a case study.
Consequently, The validated technology terms by RATE were
mapped into a co-occurrence network, revealing thematic clusters
and structural features of the research landscape. For the purpose
of evaluation, a gold standard dataset of technologies in 70
selected random articles had been curated by the experts. In
addition, a technology extraction model based on Bidirectional
Encoder Representations of Transformers (BERT) was used as
a comparative method. RATE achieved F1-score of 91.27%,
Significantly outperforming BERT with F1-score of 53.73%. Our
findings highlight the promise of definition-driven LLM methods
for technology extraction and mapping. They also offer new
insights into emerging trends within the BCI-XR field. The source
code is available https://github.com/AryaAftab/RATE
Index Terms—Large Language Models, Retrieval Augmented
Generation, Technology Extraction, Co-occurrence Networks,
Technology Mapping, Brain-Computer Interface, Extended Re-
ality
I. I NTRODUCTION AND LITERATURE REVIEW
The early 21st century has been an era of acceleration in
the development of transformative digital technologies. Pow-
ered by advancements in computing power, high-resolution
displays, and artificial intelligence (AI), new ways of ex-
periencing reality have emerged, most notably Augmented
Reality (AR) and Virtual Reality (VR) [1]. AR enhances
users’ perception of their real world environment by overlaying
digital data onto their view [2], while VR immerses users
in a completely artificial, computer generated reality [1], the
umbrella term that brings these two immersive technologies

```

</details>

Claims:

- **c001** The BERT-based comparison model achieved a precision of 39.16% on the gold-standard dataset of 70 articles
- **c002** The BERT-based baseline achieved an F1-score of around 0.71 for technology extraction.
- **c003** RATE achieved an F1-score of approximately 0.84 for technology extraction.
- **c004** RATE incorporates stylistic alignment and retrieval feedback.
- **c005** The BERT-based comparison model achieved a recall of 85.50% on the gold-standard dataset of 70 articles
- **c006** RATE achieved an F1-score of 91.27% on the gold-standard dataset of 70 articles
---

## q002: Which sparse and dense retrieval methods does the zero-shot text classification paper use to retrieve supporting categories, and what toolkit/model implements each?

<details><summary>Excerpts</summary>

**[C1]**

```
[Domain-Adaptive and Scalable Dense Retrieval for Content-Based Recommendation, chunk_4]
2.1 Scope and positioning
Our work sits at the intersection of (i) dense retrieval for first-stage ranking and (ii) retrieval-based recommender
systems. Compared to generic sentence-embedding models used zero-shot, we emphasize domain-adaptive fine-tuning
on in-domain interactions. Compared to systems-only work on vector search, we report retrieval quality and end-to-end
serving trade-offs (accuracy vs. latency).
2.2 Sparse vs. Dense Retrieval
Information retrieval has historically been dominated by sparse retrieval methods, notably TF–IDF and Okapi
BM25[Robertson and Zaragoza(2009)]. These algorithms construct an inverted index based on bag-of-words rep-
resentations, scoring relevance via probabilistic functions of term frequency (tf) and inverse document frequency (idf).
The standard BM25 score for a queryqand documentdis given by:
BM25(q, d) =
X
t∈q
idf(t)· tf(t, d)(k1 + 1)
tf(t, d) +k1

1−b+b· |d|
avgdl
,(1)
where tf(t, d)is the term frequency of query term t in document d, |d| is the document length, avgdl is the average
document length in the collection, and k1, bare free parameters. While computationally efficient, sparse methods
suffer intrinsically from thevocabulary mismatchproblem, failing to retrieve relevant documents that use synonyms or
conceptual descriptions rather than exact keywords.
The advent of neural embeddings, starting with Word2Vec and advancing to Transformer-based models like
BERT[Devlin et al.(2019)Devlin, Chang, Lee, and Toutanova], facilitated the shift toward dense retrieval. In this
paradigm, queries and documents are mapped to continuous vectors q,d∈R m, enabling relevance scoring via
geometric proximity (e.g., cosine similarity) rather than lexical overlap.
2
APREPRINT- FEBRUARY3, 2026
2.3 Bi-Encoder Architectures
Neural retrieval architectures generally fall into two categories: cross-encoders and bi-encoders. Cross-encoders process
the query and document jointly, e.g., Enc([q;d]) , allowing full self-attention between query and document tokens;
however, this yields prohibitive inference cost at retrieval time since the model
```

**[C2]**

```
[Dense Text Retrieval based on Pretrained Language Models: A Survey, chunk_80]
-
ing the training of dense retrievers. After being trained on
large-scale synthetic training data, the zero-shot capabilities
of dense retrievers can be improved to some extent. Typi-
cally, a data generation model is employed for generating
large-scale query-text pairs in the target domain [99], [126],
[234], [235]. Recently, Promptagator [153] leverages a large
language model consisting of 137 billion parameters, i.e.,
FLAN [288], to generate large-scale query-text pairs by
using only a small number of labeled examples. It trains
a dense retriever with the set of generated query-text pairs,
and shows that the retriever trained on the generated data
(with consistency ﬁltering) signiﬁcantly outperforms Col-
BERTv2 [125] that is well-trained on manually annotated
dataset ( e.g., MS MARCO) on BEIR. As an alternative ap-
proach, knowledge distillation is commonly adopted for
tackling the scarcity of training data, which utilizes a more
capable teacher model to improve the student model [102],
[123], [126] in zero-shot retrieval scenarios. Besides, sev-
eral studies [130], [132] conduct unsupervised pretraining
by leveraging large-scale positive and negative pairs with
different data augmentation methods, e.g., ICT [92] and
SimCSE [229].
•Enhancing the term matching capability. Unlike sparse re-
trievers (e.g., BM25), dense retrievers no longer rely on exact
term matching for text retrieval, but instead learn semantic
matching for capturing the text relevance. While, empirical
studies show that the capability of exact term matching
is useful to improve zero-shot retrieval performance [72],
[289], since term overlapping is a strong indicator for text
relevance. Thus, sparse retrievers are easier to adapt to zero-
shot settings without training data. Inspired by this, several
studies propose to enhance the lexical matching capacity of
dense retrievers by leveraging sparse retrievers, such as the
fusion of rankings [289] or relevance scores [132] for both
sparse and dense retrievers. Besides, we can also employ
knowledge distillation for improving dense retrievers [123],
taking sparse retrievers as the teacher model.
•Scaling up the model capacity. In recent years, scaling
law for PLMs
```

**[C3]**

```
[Dense Text Retrieval based on Pretrained Language Models: A Survey, chunk_77]
 They propose two
training approaches by modeling the retrieved documents,
either individually or jointly.
7.3 Integration and Optimization in Other Applications
In the above subsection, we have discussed how to
optimize a retrieval pipeline that integrates a dense retriever
and reranker(s). Besides retrieval systems, dense retrievers
have been widely used in a variety of application systems
that require external knowledge resources, such as open-
domain question answering and entity linking. Typically,
these application systems contain two major parts, namely
knowledge retriever (the component provides necessary
supporting evidences) and task solver (the component rea-
sons over the retrieved evidences for prediction). Compared
with traditional sparse retrievers, dense retrievers are more
ﬂexible to be integrated into downstream tasks. It is concep-
tually simple, and can be effectively optimized according to
speciﬁc task goals.
To optimize a retrieval-augmented application system,
a typical approach [94] is to construct an embedding in-
dex for knowledge retriever and then utilize the retrieved
text embeddings for optimizing the task solver. During
the training of the whole system, a major difﬁculty lies in
the issue of index staleness : at each training step, when we
update the knowledge encoder, the indexed embeddings no
longer correspond to the latest parameters of the trainer.
To address this issue, REALM [94] proposes to use asyn-
chronous index update : the index builder is periodically ( e.g.,
each for several hundred training steps) updated, and the
trainer utilizes an existing index for optimization before it is
reconstructed24. Such an approach can be generally applied
to optimize downstream systems built on dense retrievers.
Other related studies [108], [286], [287] also discuss how
to optimize retrieval-augmented systems for open-domain
question answering.
In general, with dense retrieval techniques, it is easier to
develop retrieval based approaches for downstream tasks.
We will discuss the use of dense retrieval techniques for
speciﬁc applications in Section 9.
8 A DVANCED TOPICS
In this section, we discuss several important advanced
topics for dense retrieval, including zero-shot dense re-
trieval, model robustness to query variations, model based
retrieval and retrieval-augmented language model.
8.1 Zero-shot Dense Retrieval
The success of dense retrievers heavily relies on
```

**[C4]**

```
[Retrieval Augmented Zero-Shot Text Classification, chunk_17]
-small and TE-3-large are used
to denote text-embedding-3 small and large models, respectively,
throughout the manuscript. Unlike the All-mpnet base-v2 model,
with a 512-token limit, OpenAI models can handle longer inputs.
To ensure consistency and address the 512-token limit across all
models, we employed the GPT-2 tokenizer 9 when reformulating
queries.
4.3 Retrieval Models
To retrieve supporting categories, we explored two methods: a
dense and a sparse retriever. The sparse retriever utilized the BM25
[26] algorithm implemented in Pyterrier [19] with default settings.
For the dense retriever, we employed the Contriever [11] model,
trained speci/f_ically on Wikipedia passages. The BEIR [30] frame-
work enabled indexing and retrieval for the Contriever model.
5 RESULTS AND DISCUSSION
5.1 Eﬀect of Retrieval Augmentation on
Zero-shot Performance
Table 4 showcases the bene/f_its of the retrieval augmentation pipeline
(QZero), demonstrating performance improvements across all model
sizes, especially in News topic classi/f_ication datasets. In the TagMyNews
4https://www.kaggle.com/competitions/whats-cooking/data
5https://github.com/AIRobotZhang/STCKA
6https://disi.unitn.it/moschitti/corpora.htm
7https://platform.openai.com/docs/guides/embeddings
8https://huggingface.co/sentence-transformers/all-mpnet-base-v2
9https://huggingface.co/docs/transformers/en/model_doc/gpt2
ICTIR ’24, July 13, 2024, Washington DC, DC, USA Tassallah Abdullahi, Ritambhara Singh, and Carsten Eickhoﬀ
Table 2: Dataset Classi/f_ication Summary
Dataset Classi/f_ication Type # Classes # Test Class Labels
AG News News Topic 4 7.6K politics & government, sports, business & /f_inance, technology
DBPedia Wikipedia Topic 14 70K companies, schools & university, artists , athletes, politics, transportation
buildings & structures, mountains & rivers & lakes, villages, animals, plants &
trees, albums, /f_ilms, books & novels
```

**[C5]**

```
[Dense Text Retrieval based on Pretrained Language Models: A Survey, chunk_81]
sparse and dense retrievers. Besides, we can also employ
knowledge distillation for improving dense retrievers [123],
taking sparse retrievers as the teacher model.
•Scaling up the model capacity. In recent years, scaling
law for PLMs has been widely explored for raising the
performance bar of various tasks. It has been shown useful
to improve the zero-shot performance by increasing the
model size of dense retrievers. In [129], based on a T5-based
dense retriever trained on large-scale question-answer pairs,
scaling up the model size with multi-stage training can
signiﬁcantly improve the zero-shot retrieval performance on
the BEIR benchmark. Similarly, performance improvement
has been observed when the model size is increased from
0.1 billion to 2.4 billion in ERNIE-Search [141].
Besides, it is also useful to employ multi-task learn-
ing ( e.g., a joint training with self-supervised tasks, dense
retrieval and extractive question answering [290]) to im-
prove the zero-shot retrieval performance. As another re-
lated study, Zhan et al. [221] examine how dense retrievers
generalize to out-of-domain test queries, called extrapolation
capacity in their paper. They ﬁnd that cross-encoder can
extrapolate well, but not bi-encoder and sparse retriever.
This part can be extended to a more general topic low-
resourced dense retrieval , and readers can ﬁnd a comprehen-
sive discussion in a recent survey [222].
27
8.2 Improving the Robustness to Query Variations
Besides the out-of-distribution issue in zero-shot re-
trieval, it has been shown that dense retrieval models are
more sensitive to query variations than traditional lexical
matching methods [146], [291], [292]. Generally, query vari-
ations exist widely in real search behaviors, e.g., unexpected
query typos due to spelling errors and diverse query for-
mulations for the same information need. We next discuss
the effect of query variations on retrieval performance and
introduce several enhanced training methods.
Effect of query variations on retrieval. There are increasing
concerns on the robustness of dense retrieval models to
query variations. These studies typically create different
types of query variations and examine the performance
of dense retrieval models under different query variations.
Zhuang et al
```

</details>

Claims:

- **c007** One retrieval method is a sparse retriever.
- **c008** The combination of sparse and dense retrieval allows the system to retrieve supporting categories both through lexical overlap and semantic similarity.
- **c009** Dense retrieval is based on sentence embeddings or dual-encoder models.
- **c010** The dense retriever uses the Contriever model.
- **c011** The sparse retriever uses the BM25 algorithm.
- **c012** This combination improves coverage for zero-shot classification labels that may not share vocabulary with the input text.
---

## q003: In the BPIR converse proof, how is the set of non-user databases split into B1 and B2, and why does this construction lead to a decoding error?

<details><summary>Excerpts</summary>

**[C1]**

```
[The Capacity of Private Information Retrieval from Byzantine and Colluding Databases, chunk_43]
 problem. The proof in [28, 29] relies
on the fact that in the presence of an adversary controlling B nodes, and for any distinct
messages w1 ̸= w2, a necessary condition for the receiver to not make a decodin g error is to
have XU (w1) ̸= XU (w2).
24
Proof: Divide the set ¯U = {1, · · · , N } \ U into two sets B1, B2 such that |B1| = |B2| = B.
In the BPIR problem, we must guarantee correct decoding if the By zantine databases are
any subset B ⊂ { 1, · · · , N }, such that |B| = B, in particular, if the Byzantine databases are
either B1 or B2.
Now, assume for sake of contradiction, that there exists a valid re trieval scheme that
achieves correct decoding of Wi, and there exist two realizations of the message set W, ˜W
such that W ̸= ˜W, and
A[i]
U (W) = A[i]
U ( ˜W) (62)
Two scenarios can arise:
1. The true realization of the database contents is W. In this case, if the adversarial
nodes are the databases indexed by B2, and they ﬂip their contents Ω B2 into ˜W, the
user collects the answer strings
(
A[i]
B1 (W), A[i]
B2 ( ˜W), A[i]
U (W)
)
.
2. The true realization of the database contents is ˜W. In this case, if the adversarial
nodes are the databases indexed by B1, and they ﬂip their contents Ω B1 into W, the
user collects the answer strings
(
A[i]
B1 (W), A[i]
B2 ( ˜W), A[i]
U ( ˜W)
)
.
Since A[i]
U (W) = A[i]
U ( ˜W), there is no way for the user to diﬀerentiate between the two
scenarios. Hence, the user commits an error either directly (if W and ˜W diﬀer
```

**[C2]**

```
[The Capacity of Private Information Retrieval from Byzantine and Colluding Databases, chunk_38]
 ˜a[1:96], which is encoded by (96 , 64) outer MDS code. This code can correct up to
⌊96− 64
2 ⌋ = 16 errors. Hence, the user can decode W1 reliably.
For the privacy, from any 2 databases, the user asks for 16 symb ols from each message.
By the MDS property and Lemma 2, all these symbols are full-rank, a nd hence they are
independent and uniformly distributed. Therefore, the scheme is 2 -private.
The resilient achievable rate is R = 64
168 = 8
21 = 4
6 · 4
7 = N− 2B
N ·
1− T
N− 2B
1− ( T
N− 2B )
M = C.
Note that, for the same M, N, the achievable rate with T = 1, B = 2 in the previous
subsection, 4
21 , is smaller than the achievable rate with T = 2, B = 1 in this subsection, 8
21 ,
which signiﬁes that Byzantine behavior is a more severe adversarial behavior to cope with
compared to colluding behavior.
5 Converse Proof
In this section, we develop an upper bound for the BPIR problem. Weadapt the cut-set
upper bound proof in [28, 29] to the PIR setting. The upper bound c an be thought of as
a network version of the Singleton bound [30]. The upper bound intuit ively asserts that
22
Table 3: The query table for the case M = 3, N = 6, T = 2, B = 1.
DB 1 DB 2 DB 3 DB 4 DB 5 DB 6
a1, a2, a3, a4 a5, a6, a7, a8 a9, a10, a11, a12 a13, a14, a15, a16 a17, a18, a19, a20 a21, a22, a23, a24
b1, b2, b3, b4 b5, b6, b7, b8 b9, b10, b11, b12 b13, b14, b15
```

**[C3]**

```
[The Capacity of Private Information Retrieval from Byzantine and Colluding Databases, chunk_1]
We consider the problem of single-round private informatio n retrieval (PIR) from
N replicated databases. We consider the case when B databases are outdated (unsyn-
chronized), or even worse, adversarial (Byzantine), and th erefore, can return incorrect
answers. In the PIR problem with Byzantine databases (BPIR) , a user wishes to re-
trieve a speciﬁc message from a set of M messages with zero-error, irrespective of the
actions performed by the Byzantine databases. We consider t he T -privacy constraint
in this paper, where any T databases can collude, and exchange the queries submitted
by the user. We derive the information-theoretic capacity o f this problem, which is
the maximum number of correct symbolsthat can be retrieved privately (under the T -
privacy constraint) for every symbol of the downloaded data . We determine the exact
BPIR capacity to be C = N− 2B
N ·
1− T
N− 2B
1− ( T
N− 2B )M , if 2 B + T < N. This capacity expression
shows that the eﬀect of Byzantine databases on the retrieval r ate is equivalent to re-
moving 2 B databases from the system, with a penalty factor of N− 2B
N , which signiﬁes
that even though the number of databases needed for PIR is eﬀec tively N − 2B, the
user still needs to access the entire N databases. The result shows that for the unsyn-
chronized PIR problem, if the user does not have any knowledg e about the fraction
of the messages that are mis-synchronized, the single-roun d capacity is the same as
the BPIR capacity. Our achievable scheme extends the optima l achievable scheme for
the robust PIR (RPIR) problem to correct the errors introduced by the Byzantine
databases as opposed to erasures in the RPIR problem. Our converse proof uses the
idea of the cut-set bound in the network coding problem again st adversarial nodes.
∗ This work was supported by NSF Grants CNS 13-14733, CCF 14-221 11, and CNS 15-26608.
1
```

**[C4]**

```
[The Capacity of Private Information Retrieval from Byzantine and Colluding Databases, chunk_10]
 This
can be done by altering the contents of the databases to an erron eous version as in the
unsynchronized setting; or by altering the answering strings them selves, i.e., the nth
database returns the answer string ˜A[i]
n such that,
˜A[i]
n ̸= A[i]
n , n ∈ B , |B| = B (10)
or by doing both.
6
3 Main Result and Discussions
The main result of this paper is to characterize the capacity of the BPIR problem under T -
privacy constraint, where B databases are adversarial (Byzantine) and can return malicious
answers, and at the same time the privacy should be kept against an y T colluding databases.
Theorem 1 For the single-round BPIR problem with B Byzantine databases, and T collud-
ing databases, such that 2B + T < N , the capacity is given by,
C = N − 2B
N ·
1 − T
N− 2B
1 −
( T
N− 2B
) M (11)
= N − 2B
N ·
(
1 + T
N − 2B + T 2
(N − 2B)2 + · · · + T M− 1
(N − 2B)M− 1
) − 1
(12)
On the other hand, if 2B + 1 ≤ N ≤ 2B + T , then the user is forced to download the entire
database from at least from (2B + 1) diﬀerent databases, hence C = 1
(2B+1)M , which is the
trivial rate in the BPIR problem. Otherwise, the problem is i nfeasible and C = 0 .
The achievability proof for Theorem 1 is given in Section 4, and the con verse proof is
given in Section 5. We have a few remarks.
Remark 1The BPIR capacity in (11) is the same as the capacity of PIR wit h T colluding
databases if the number of databases is N − 2B with a penalty factor of N− 2B
N . This means
that the harm introduced by the B Byzantine databases is equivalent to removing a part
```

**[C5]**

```
[The Capacity of Private Information Retrieval from Byzantine and Colluding Databases, chunk_5]
 allowing for list decoding
instead of unique decoding enlarges the feasible set up to B < N − T − 1. Their achievable
scheme allows for a small failure probability. The scheme depends on S hamir’s secret sharing
algorithm [26] and Guruswami-Sudan decoding algorithm [27]. The unsy nchronized PIR
problem is investigated in [22], where they propose a two-round ret rieval scheme. The
scheme returns the desired record by ﬁrst identifying which recor ds are mis-synchronized,
and then by constructing a PIR scheme that avoids these problema tic records.
In this paper, we consider the single-round BPIR problem from N replicated databases
in the presence of B Byzantine databases that can introduce errors to the returned answer
strings. Other than the Byzantine databases, the remaining stor age nodes store the exact
copy of the message set which contains M diﬀerent messages, and respond truthfully with
the correct answer strings. We consider the T -privacy constraint, which permits colluding
3
between any T databases to exchange the queries submitted by the user. Our go al is to
characterize the single-round capacity of the BPIR problem under the zero-error reliability
constraint and the T -privacy constraint. To that end, we propose an achievable schem e that
is resilient to the worst-case errors that result from the Byzantin e databases. Our achievable
scheme extends the optimal scheme for the RPIR problem to corre ct the errors resulted
from the Byzantine databases, in contrast to the erasures introduced by the unresponsive
databases in RPIR. The new ingredients to the achievable scheme ar e: encoding the un-
desired symbols via a punctured MDS code, successive interferenc e cancellation of the side
information, and encoding the desired symbols by an outer-layer MD S code. For the con-
verse, we extend the converse arguments developed for the net work coding problem in [28]
and distributed storage systems in [29] to the PIR problem. This cut -set upper bound can
be thought of as a network version of the Singleton bound [30]. The upper bound intuitively
implies that a redundancy of 2 B nodes is needed in order to mitigate the errors introduced
by the B Byzantine databases.
We determine the exact capacity of the BPIR problem to be C = N− 2
```

</details>

Claims:

- **c013** B1 and B2 each have size B.
- **c014** In the BPIR converse proof, the set of non-user databases is partitioned into two blocks, B1 and B2.
- **c015** The remaining, less correlated databases fall into B2.
- **c016** In the second scenario, the Byzantine databases flip their contents from W̃ to W.
- **c017** In the second scenario, the user collects the answer strings (A[i]_B1(W), A[i]_B2(W̃), A[i]_U(W̃)).
- **c018** Because this bias is structural rather than random, it guarantees a nonzero probability of decoding error whenever B1 and B2 are constructed this way.
---

## q004: What NDCG@10 improvement does the UIA framework report from jointly modeling all three information access functionalities versus modeling them individually?

<details><summary>Excerpts</summary>

**[C1]**

```
[A Personalized Dense Retrieval Framework for Unified Information Access, chunk_5]
14 Pro ’). UIA uses
text description of each information access functionality, thus is
generic and extensible to a wide range of other information access
functionalities.
We evaluate our model on a real-world dataset collected from
user interactions with different information access systems on a
major e-commerce website.2 To improve reproducibility, we also
extend our experiments to a dataset constructed from the Amazon
ESCI data [25], recently released as part of KDD Cup 2022.3 Exten-
sive experiments demonstrate significant improvements compared
to a wide range of competitive baselines for all three information ac-
cess functionalities. We also demonstrate that up to 45% NDCG@10
improvements can be obtained by jointly modeling all information
access functionalities compared to their individual modeling using
the same dense retrieval architecture.
To summarize, the main contributions of this work include:
•Developing a generic and extensible dense retrieval framework
that performs multiple information access functionalities.
1In this paper, items refer to unstructured or semi-structured textual documents.
2Even though our both datasets are from the e-commerce domain, the proposed
approach is sufficiently generic to be applied to any domain. We are not aware of any
other publicly available dataset beyond e-commerce that can be used to evaluate our
task.
3KDD Cup 2022: https://amazonkddcup.github.io/
•Demonstrating the feasibility of learning a single model that can
perform a wide range of information access functionalities.
•Proposing an attentive personalized network with a two-stage
training process and negative sampling strategies from various
sources to improve personalized dense retrieval performance.
•Evaluating the proposed model on real-world data and demon-
strating substantial gain compared to competitive baselines.
We open-source our implementation of the UIA framework to
foster research towards developing universal information access.4
```

**[C2]**

```
[A Personalized Dense Retrieval Framework for Unified Information Access, chunk_27]
 benefit from joint optimization.
Row 3 shows that personalization (both content-based and col-
laborative) using APN has a significant impact on the models perfor-
mance. Using APN in UIA leads to 93%, 72%, and 145% NDCG@10
improvements in keyword search, query by example, and comple-
mentary item recommendation, respectively. These improvements
Figure 3: ΔNDCG (sorted) at user level between UIA and TS-
UIA (i.e., UIA without joint training) on the Lowe’s dataset.
Figure 4: ΔNDCG (sorted) at user level between UIA and UIA
without APN on the Lowe’s dataset.
are mostly coming from the content-based personalization. That
being said, in the following, we show that APN also benefits from
using the combination of all interaction history as well as collabo-
rative personalization.
Row 4 reports the results for UIA where for each information
access functionality, only the associated user history is used for
personalization. For example, only past search interactions of users
are used for the search functionality, as opposed to UIA that uses
all the past interactions combined. From this result, we observe that
UIA benefits from including historical user interactions from all
three information access functionalities. Again, query by example
and complementary item recommendation benefit the most, due
to their smaller training data size (and thus fewer historical user
interactions) compared to the search task.
Finally, Row 5 demonstrates the results for UIA without collab-
orative personalization, i.e., without user and relation embedding
in APN’s final layer (see Figure 2). We show that adding user and
relation embedding does not improve the model performance con-
sistently across information access functionalities. Collaborative
personalization is found to be helpful in keyword search and com-
plementary item recommendation but not in query by example.
The possible explanation might be that the structural informa-
tion provided by user-relation-item ids is conducive to identify
the item-item complementary and query-item relevance relations,
but content information which is important in query by example
(finding similar items) can be better distilled from content-based
personalization without using the user embeddings.
4.2.3 The Impact of Joint Training. Not all users benefit from
joint training, since
```

**[C3]**

```
[A Personalized Dense Retrieval Framework for Unified Information Access, chunk_26]
.
The improvements are generally smaller than the Lowe’s dataset
and it is due to the lack of personalization in UIA for this dataset.
We find a concurrent work [27] which aims to create a universal
encoder for all retrieval tasks. We utilized their publicly available
pre-trained checkpoint for zero-shot evaluation on the Amazon
ESCI dataset, however, its performance was inferior to BM25. As an
example, the MRR@10 in the complementary recommendation task
was 0.223 compared to 0.230 by BM25. We surmise that this disparity
could be due to the method being trained on datasets that prioritize
semantic text similarity [ 4, 6] and overlooks complementary or
subsititue item matching signals.
4.2.2 Ablation Study. To demonstrate the impact of each novel
component used in UIA, we conduct a thorough ablation study on
the Lowe’s dataset that contain temporal information as well as
anonymized user identifiers. For the sake of space, we only report
NDCG@10 values in Table 5. We make the following observations:
From Row 1, encoding the information access functionality (i.e.,
F) is found crucial. The reason is that the model does not know
what items are expected to be retrieved given the input request.
Thus, it behaves similarly across all information access functionali-
ties. The performance gain in query by example and complemen-
tary item recommendation is substantially higher than in keyword
search. There are two reasons: (1) the search data in Lowe’s dataset
is at least 300% larger than each of the other information access
functionalities (see Table 2); and (2) the input to both query by
example and complementary item recommendation are identical
From Row 2, we can conclude that all three information access
functionalities benefit from joint optimization. The improvement
observed in keyword search task is marginal, but 34% and 45%
relative improvements are observed in query by example and com-
plementary item recommendation, respectively. Note that Lowe’s
dataset contains fewer data points for these two tasks and thus they
can substantially benefit from joint optimization.
Row 3 shows that personalization (both content-based and col-
laborative) using APN has a significant impact on the models perfor-
mance. Using APN in UIA leads to 93%, 
```

**[C4]**

```
[A Personalized Dense Retrieval Framework for Unified Information Access, chunk_25]
4.2 Experimental Results
4.2.1 Main Results. The performance of UIA and the baselines
on the Lowe’s dataset for all the three information access function-
alities is reported in Table 3. The results demonstrate that BM25 and
NCF perform poorly compared to the deep learning based models.
Note that NCF cannot be used for the keyword search task, as it
is a collaborative filtering approach. We also observe that context-
aware variation of dense retrieval models substantially outperform
the original DPR and ANCE models. This demonstrates the im-
portance of personalization for information access in e-commerce.
Besides, BERT4Rec++ has better results than SASRec++, which
implies that BERT that is a stack of multiple Transformer layers is
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Hansi Zeng, Surya Kallumadi, Zaid Alibadi, Rodrigo Nogueira, and Hamed Zamani
capable of better capturing user history behaviors. Among models
that are trained on a corresponding single task, Context-Aware
ANCE achieves the best performance.
Table 3 also shows that joint training models perform better than
task-specific models, especially for query by example and comple-
mentary item recommendation tasks that have substantially smaller
training data compared to the keyword search task. All in all, UIA
outperforms all the baselines. The improvements are statistically
significant in nearly all cases, except for MRR in Keyword Search
which is only significant compared to the task-specific models.
We extend our experiments to the Amazon ESCI dataset and
report the result in Table 4. Note that ESCI does not contain user
identifiers, thus the baselines that cannot perform without person-
alization are omitted from Table 4. In this dataset, complementary
item recommendation benefit the most from joint training. The
reason is due to the size of the dataset for this information access
functionality. It is smaller than the other two functionalities, thus
it benefit the most from knowledge transfer across tasks. These
results suggest that UIA again performs better than all the baselines.
The improvements are generally smaller than the Lowe’s dataset
and it is due to the lack of personalization in UIA for this dataset.
We find a concurrent work [27] which aims to create a universal
encoder for all retrieval tasks.
```

**[C5]**

```
[A Personalized Dense Retrieval Framework for Unified Information Access, chunk_30]
is plotted in Figure 4 for all three information access functionalities.
According to the figure, not all users benefit from personalization.
This is expected especially for new and cold-start users and also
for situations where user’s information need is different from their
past interactions. The plots show that personalization has a neg-
ative impact on less than a quarter of users and a larger set of
users take advantage of personalization. These plots also show that
personalization has a larger impact on query by example and com-
plementary item recommendation compared to keyword search.
This is expected, as in keyword search, the user’s information need
is often clear from the query, while it is more difficult to infer user’s
need in query by example and complementary item recommenda-
tion. Predicting the need for personalization in future work can
substantially improve UIA.
4.2.5 Case Study. Our case study, which compares the top-1 re-
trieved item by UIA and its task-specific training counterpart TS-
UIA, is presented in Table 6. The results show that both models
struggle with partial attribute matching errors in the keyword
search task. For example, when searching for “6x6 privacy fence, ”
the top-1 item returned by TS-UIA is “outdoor privacy screens”
which only matches the “privacy” attribute but misses the “fence”
attribute. Similarly, UIA returns an irrelevant item for the query “ev
charger. ” In the query by example task, the top-1 retrieved item by
the task-specific training counterpart (TS-UIA) is often the same as
the query item. This may be due to high term overlap in the positive
training pairs, resulting in over-fitting of the model. Joint modeling
with other tasks can partially mitigate this issue as different tasks
serve as regularizers. In the complementary item recommenda-
tion task, UIA demonstrates superiority over TS-UIA by accurately
identifying complementary items, such as correctly matching “roof
ridge vents” with “roof shingle” despite the weak term matching
signal.
5 CONCLUSIONS AND FUTURE DIRECTIONS
This paper studied the feasibility of implementing universal infor-
mation access systems and proposed a generic and extensible dense
retrieval framework, called UIA, for this purpose. UIA encodes
each information access functionality in addition to
```

</details>

Claims:

- **c019** The paper presents this as evidence that unifying the three functionalities under a single architecture yields measurable retrieval quality gains.
- **c020** These complementary signals would otherwise remain isolated in single-task setups.
- **c021** The UIA framework stands for Unified Information Access.
- **c022** The Lowe's dataset contains fewer data points for query by example and complementary item recommendation tasks.
- **c023** An ablation study was conducted on the Lowe's dataset.
- **c024** Jointly modeling all information access functionalities in the UIA framework can yield up to 45% NDCG@10 improvement compared to individual (task-specific) modeling using the same dense retrieval architecture.
---

## q005: How does the adaptive passage combination retrieval method handle noisy retrieved documents differently from approaches that use LM confidence thresholds or preemptive document filtering?

<details><summary>Excerpts</summary>

**[C1]**

```
[Beyond Independent Passages: Adaptive Passage Combination Retrieval for Retrieval Augmented Open-Domain Question Answering, chunk_6]
Wang et al.,
2023; Asai et al., 2024; Yu et al., 2023), but overre-
liance on LM confidence can misidentify noisy doc-
uments. Other works attempt to preemptively re-
move known knowledge via LM prompting (Wang
et al., 2024), but these approaches risk inaccuracies
due to unfaithful internal reasoning of LMs (Lan-
ham et al., 2023). In contrast, our method avoids
document filtering during inference and instead di-
rectly optimizes the retriever distribution to align
with answer likelihood, assigning lower weights to
less useful documents without discarding them.
2.4 Overcoming Noisy Retrieved Result
Effective retrieval must address not only relevance
but also diversity and redundancy. This is particu-
larly critical when dealing with large, noisy corpora
like web-scale datasets (Piktus et al., 2021). To fix
this problem in RAG, some approaches incorporate
relevance thresholds and Maximal Marginal Rel-
evance (MMR) (Yasunaga et al., 2022; Vikraman
et al., 2021; Gao and Zhang, 2024), clustering-
based selection (Xu et al., 2024a), or identifying
diverse facets of the query before retrieval (Fromm
et al., 2021). Particularly, adaptive retrieval stop-
ping (Kratzwald and Feuerriegel, 2018) predicts
when sufficient information has been retrieved, to
which ours is similar in having a dynamic selec-
tion of retrieved documents but without requiring a
separate stopping classifier.
Rather than fixing retrieval alone, another strat-
egy is to make LM robust against noisy inputs.
Several works synthesize noisy contexts for LM
training (Yoran et al., 2023b; Lyu et al., 2023),
or use test-time adaptation to mitigate retrieval
errors (Hübotter et al., 2025). While these tech-
niques complement our work, our focus remains
on improving retriever quality to reduce noise at its
source.
```

**[C2]**

```
[Beyond Independent Passages: Adaptive Passage Combination Retrieval for Retrieval Augmented Open-Domain Question Answering, chunk_19]
We introduce AdaPCR, a retrieval framework that
adaptively selects and scores passage combinations
to improve open-domain QA with black-box LMs.
By modeling dependencies between passages and
aligning retriever scores with answer likelihood,
AdaPCR overcomes key limitations of traditional
RAG approaches—handling redundancy, promot-
ing diversity, and supporting multi-hop reasoning.
Experiments across multiple QA benchmarks show
that AdaPCR outperforms IC-RALM baselines, es-
pecially on complex questions, validating the bene-
fits of passage combination modeling and adaptive
retrieval.
Limitations
We explore and compare our methods to other meth-
ods that also train retriever in a black-box generator
setting. However, many work also explore concate-
nating answer probabilities produced by incorpo-
rating different passages in parallel or inference
multiple times (Yoran et al., 2023a; Jiapeng et al.,
2024). Also, while the current procedure involves
two rounds of retrieval, this iterative process could
be extended to more rounds to explore even more
complex passage combinations. Some strategies
for making LM robust against noisy inputs can also
be supplemented with our method. We leave these
extension for future work.
```

**[C3]**

```
[Beyond Independent Passages: Adaptive Passage Combination Retrieval for Retrieval Augmented Open-Domain Question Answering, chunk_7]
Our retriever framework addresses the challenge
of identifying optimal passage combinations that
maximize answer generation likelihood. Unlike
traditional approaches that select passages indepen-
dently, our method explicitly models dependencies
between passages to improve question answering
performance.
3.1 Adaptive Passage Combination Retrieval
(AdaPCR)
Given a question x, a large set of passages C =
{pi}, and a gold answer y, our goal is to find a
subset of passages d ⊂ Cthat enables a language
model (LM) to accurately generate the answer y
when conditioned on both x and d.
Prior methods typically assume that a fixed num-
ber k of passages are retrieved independently based
on their relevance to x. However, when answers
require combining information across passages, re-
trieving passages independently can be suboptimal.
Some passages may be individually unhelpful but
crucial when considered together.
Thus, we aim to retrieve passage combinations
that maximize the downstream answer generation
likelihood:
ˆd = arg max
d
PLM(y | [d; x]),
where
PLM(y|[d; x]) =PLM(y1, y2, . . . , yn|[d; x])
≜
nY
i=1
PLM (yi | [d; x; y<i]) . (1)
We propose explicitly modeling passage de-
pendencies by learning a combination retriever
Pret(d | x) that scores and selects groups of pas-
sages jointly rather than individually. We adopt
the common bi-encoder (Karpukhin et al., 2020)
structure as our retriever, including a query encoder
Eq and a passage encoder Ed.
Concretely, our framework proceeds in two
stages:
1. First-Stage Retrieval: We score all passages
and retrieve a small pool of top- k candidate
passages D1 = {p1, . . . , pk} based on their
relevance to the question x.
2. Combination Reranking: For each retrieved
document di from the first stage, we concate-
nated it with the input x to form a new query
di ⊕ x. Then, we again score and choose the
top k passages relevant to the new concate-
nated query. This form a new passage combi-
nation candidate set D2 = {pij|1 ≤ i,
```

**[C4]**

```
[Beyond Independent Passages: Adaptive Passage Combination Retrieval for Retrieval Augmented Open-Domain Question Answering, chunk_5]
 work improves retriever optimization by
explicitly modeling document dependencies and
introducing a new training objective with stabilized
sampling, leading to enhanced open-domain QA
performance.
Reranking techniques are employed to enhance
retrieval quality for QA (Glass et al., 2022; Ren
et al., 2023; Iyer et al., 2021; Wang et al., 2021;
Kruit et al., 2024). These methods calculate a gran-
ular score representing the relationship between the
query and each individual passage, utilizing these
scores for subsequent re-ordering. Nevertheless,
a limitation is that as each passage is scored inde-
pendently, it overlooks the potentially important
interactions between passages, which can be impor-
tant for multi-hop QA or in noisy corpus scenarios.
To address this by explicitly modeling relationships
between documents, alternative retrieval architec-
tures, such as tree-structured indices (Sarthi et al.,
2024) or graph-neural-network-enhanced retrievers
(Li et al., 2024) has been explored. Our AdaPCR
similarly models these inter-passage relationships
via its combination retrieval framework.
2.3 LLM Guided Pre- and Post-Retrieval
Techniques
In addition to directly improving the retrievers and
rerankers, some pre- and post-retrieval techniques
are also used to improve the quality of the retrieval.
Pre-retrieval techniques include query rewrit-
ing and expansion using LLMs (Xu et al., 2024b;
Jiang et al., 2025; Su et al., 2022; Trivedi et al.,
2023; Kim et al., 2024; Sarthi et al., 2024), en-
abling broader and more context-aware document
retrieval. On the other hand, post-retrieval tech-
niques refine retrieved documents. For example,
2
Re2G (Glass et al., 2022) combines and reranks
dense and sparse retrieval results to improve gen-
eration quality. Some approaches use LM confi-
dence to filter retrieved documents (Wang et al.,
2023; Asai et al., 2024; Yu et al., 2023), but overre-
liance on LM confidence can misidentify noisy doc-
uments. Other works attempt to preemptively re-

```

**[C5]**

```
[Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers, chunk_9]
 to proceed with generation, re-trigger retrieval, or
decompose the input into simpler sub-queries. This corrective mechanism positions CRAG within the hybrid class, as it
tightly coordinates retrieval assessment with adaptive generation pathways under uncertainty.
These architectures reflect a broader trend toward treating retrieval as a controllable, contextualized act rather than
a fixed preprocessing step. Their strength lies in adaptivity, coordination, and the capacity to handle under-specified
or evolving queries. However, they introduce new challenges in training stability, latency, and system transparency—
especially when retrieval is performed mid-decoding. These trade-offs, as well as efficiency-oriented enhancements like
pipelining and reranking, are further explored in Section 4.
3.4 Robustness and Security-Oriented RAG Systems
Robustness- and security-oriented RAG systems are designed to preserve output quality in the face of noisy, irrelevant,
or adversarially manipulated retrieval contexts. Unlike models that optimize retrieval or generation under ideal
assumptions, these systems explicitly address worst-case scenarios—such as hallucination under misleading evidence,
retrieval failures, or corpus poisoning. We identify three major design strategies in this category: noise-adaptive training,
hallucination-aware decoding constraints, and adversarial robustness.
Noise-Adaptive Training Objectives: These systems aim to make RAG outputs resilient to degraded or spurious
input evidence by training under perturbed, irrelevant, or misleading contexts. RAAT [18] classifies retrieved passages
into relevant, irrelevant, or counterfactual categories and introduces an adversarial training objective to maximize worst-
case performance. Bottleneck Noise Filtering [89] applies information bottleneck theory to identify the intersection
of useful and noisy information, compressing retrieved context into minimal, high-utility representations. These
approaches are particularly effective in retrieval-heavy pipelines where context precision cannot be guaranteed.
Hallucination-Aware Decoding Constraints: To mitigate factual inaccuracies in generation, several systems in-
troduce decoding-time constraints or architectures designed to enforce grounding. RAGTruth [46] provides benchmarks
and evaluation protocols for hallucination detection, guiding system-level design. Structured retrieval-based approaches
have also been explored: one method [24] retrieves executable templates (e.g., JSON workflows) to constrain output
generation, minimizing reliance on generative interpolation and reducing domain-specific hallucination. RAG-Ex [62]
simulates retrieval variability by injecting perturbed documents
```

</details>

Claims:

- **c025** AdaPCR avoids document filtering during inference.
- **c026** Some methods try to make the language model robust against noisy inputs through synthesized noisy training contexts.
- **c027** The MOEBQA routing strategy is end-to-end learned.
- **c028** In MOEBQA, each example is assigned to only a few experts based on its underlying question type.
- **c029** Modeling dependencies between passages helps address redundancy and diversity issues that arise from noisy, large-scale corpora.
- **c030** The adaptive combination technique has only a tolerable computational overhead.
---

## q006: What recent techniques does this paper list as ways researchers have improved dense retriever effectiveness (e.g., hard negative mining, late interaction)?

<details><summary>Excerpts</summary>

**[C1]**

```
[CharacterBERT and Self-Teaching for Improving the Robustness of Dense Retrievers on Queries with Typos, chunk_7]
Effectiveness of Dense Retrievers. Pre-trained transformer-based
language models (PLMs) [5, 24, 43] from NLP have been adapted
to IR tasks such as passage retrieval and have demonstrated much
higher effectiveness than traditional bag-of-words methods (e.g.,
BM25) [21]. Among the retrieval methods that exploit PLMs, dense
retrievers have attracted the most attention. Karpukhin et al. [17]
first demonstrated that simply leveraging hard negatives sampled
from BM25 top retrieved passages is sufficient for learning a fairly
effective BERT-based DR. Follow up work has focused on designing
more complex hard negative mining strategies to further improve
effectiveness [31, 42, 44]. Xiong et al. [42] proposed to sample hard
negatives from an asynchronously updated Approximate Nearest
Neighbor (ANN) index, giving rise to the ANCE model. Similar to
ANCE, Zhan et al. [44] suggested that static hard negative sampling
is risky and leads to learning a suboptimal DR. They then proposed
to dynamically update the query encoder so that hard negatives
are sampled according to the latest query embeddings: this is the
ADORE method. Training dense retrievers with hard negatives is
however computationally expensive. To maximise the GPUs com-
putational power, Qu et al . [31] proposed to leverages negative
samples across different GPUs, thus greatly enlarging the negatives
samples per training data while maintaining training efficiency as
GPU memory locality is exploited: this is the training pipeline of the
RocketQA model. The availability of such a large number of nega-
tive samples significantly improves ranking effectiveness. However,
this training pipeline still requires a large number of GPUs and
memory. As an alternative, Gao et al. [11] introduced a gradient
caching technique that allows the RocketQA training pipeline to be
run within a single GPU. In this paper, we adopt the hard negative
training approach of Karpukhin et al . [17] to efficiently train an
effective dense retriever, and leave the application of our methods
on more complex dense retrievers training pipelines to future work.
Another widely used technique used to improve the effectiveness
of dense retrievers is Knowledge Distillation (KD) [14, 15, 22, 23, 33],
where a DR is obtained by learning from
```

**[C2]**

```
[Boosted Dense Retriever, chunk_24]
 gold
pairs (Yih et al., 2011) has recently shown to
be effective in several settings (Lee et al., 2019;
Karpukhin et al., 2020; Reimers and Gurevych,
2019; Hofst ¨atter et al., 2021b). See Yates et al.
(2021) for a survey. The success of Dense Re-
trieval has led to many recent papers proposing
schemes to improve dense retriever training by in-
novating on how negatives are sampled (Xiong
et al., 2020; Qu et al., 2021; Zhan et al., 2021c;
Lin et al., 2021, inter alia.), and/or proposing pre-
training objectives (O˘guz et al., 2021; Guu et al.,
2020; Chang et al., 2020; Sachan et al., 2021; Gao
and Callan, 2021). Our work also innovates on
how dense retrievers are trained, but is arguably
orthogonal to most of these training innovations,
since these could still be employed when training
each component weak learner.
Distillation We leverage a simple distillation
technique to make DrBoost more efﬁcient at test
time. Distillation for dense retrievers is an active
area, and more complex schemes exist which could
improve results further (Izacard and Grave, 2021;
Qu et al., 2021; Yang and Seo, 2020; Lin et al.,
2021; Hofst¨atter et al., 2021a; Barkan et al., 2020;
Gao et al., 2020).
Multi-vector Retrievers Several approaches
represent passages with multiple vectors. Humeau
et al. (2020) represent queries with multiple vec-
tors, but retrieval is comparatively slow as rele-
vance cannot be calculated with a single MIPS call.
ME-BERT (Luan et al., 2021) index a ﬁxed number
of vectors for each passage and ColBERT (Khattab
and Zaharia, 2020) index a vector for every word.
Both can perform retrieval with a single MIPS
call (although ColBERT requires reranking) but
produce very large indices, which, in turn, slows
down search
```

**[C3]**

```
[I^3 Retriever: Incorporating Implicit Interaction in Pre-trained Language Models for Passage Retrieval, chunk_7]
 methods are subsequently
proposed to improve the effectiveness. In particular, most of the ex-
isting PLM-based retrievers improve the model performance from
the following aspects. (1) By introducing late-interactions after
encoding: ColBERT [25], COIL [16] and ME-BERT [35] are three
representative studies that explicitly model the interactions after
query/passage encodings. The performance is largely boosted by the
interactions compared with DPR (i.e., vanilla dual-encoder), while
the late interaction also brings significant computational overhead.
(2) By designing effective fine-tuning processes: For example,
ANCE [63] proposes to a hard negative sampling technique that
greatly improve the effectiveness. Moreover, RocketQAv1 [46] and
RocketQAv2 [49] boost the performance of dense retrieval models
by leveraging the power of cross-encoder. The relevance features
captured through sufficient interaction by the cross-encoder could
be properly transferred to retrievers in a cascade or joint train-
ing manner. ERNIE-Search [34] narrows the divide between cross-
encoder and dual-encoder models through on-the-fly distillation
in the process of fine-tuning. ColBERTv2 [ 52] further improves
ColBERT by employing fine-tuning with distillation. (3) By de-
signing pre-training tasks tailored for retrieval: A handful of
studies focused on constructing pseudo-training data for retrieval-
oriented pre-training, such as ICT [2], COSTA [37], DCE [29], etc.
Besides, several studies [ 27, 32, 33, 58–60, 60, 67] employ weak
generative modules (i.e. decoder) to enhance the query/passage en-
coding through pre-training. Notably, after pre-training, the weak
decoder is discarded and only the enhanced encoder is employed
as the backbone of retriever. In this work, we propose a novel ap-
proach that incorporates implicit interaction modeling into the
dual-encoder architecture by introducing a generative module. To
the best of our knowledge, this is the first attempt to introduce a
generative module as a backbone in a retriever.
PLM-based reranker. PLM-based rerankers usually take the con-
catenated query and passage as input and perform full interaction
between query and passage via self
```

**[C4]**

```
[Dense Text Retrieval based on Pretrained Language Models: A Survey, chunk_97]
replace sparse retrieval is still being under explored by the
research community, and there are also some studies that
devise new framework consisting of multiple effectiveness
measurements for examining this problem [350].
Training approach . Compared with previous neural IR
methods, PLM-based dense retrieval models are more dif-
ﬁcult to be optimized given the huge number of parame-
ters. Even with the ever-increasing labeled dataset, it still
requires speciﬁc training techniques to effectively optimize
large retrieval models. We summarize three major issues to
address for improving dense retrieval systems, i.e., large-
scale candidate space, limited relevance judgements, and
pretraining discrepancy. Focused on the three issues, the
researchers have made extensive efforts by designing var-
ious effective training strategies, including negative selec-
tion, data augmentation and speciﬁc pretraining techniques.
These studies have signiﬁcantly improved the retrieval per-
formance of dense retrievers on benchmark datasets [1],
[36], [98], [112]. In particular, negative selection is a key
step in the training approach, and using more negatives (e.g.,
in- and cross-batch negatives) or more high-quality negatives
(e.g., sampling static or dynamic hard negatives) typically
lead to a better retrieval performance. Besides, in order
to enhance the capacity of bi-encoder, it is very useful to
distill a more capable teacher model ( e.g., cross-encoder)
and design suitable pretraining tasks ( e.g., representation-
enhanced pretraining). More recently, auto-encoder and
contrastive learning based pretraining methods have been
widely adopted to enhance the semantic representations
of texts. As an improvement direction, it is important to
design data- and parameter-efﬁcient training approaches
32
for enhancing the retrieval capacity under low-resourced
setting (e.g., zero-shot retrieval).
Dense vector index. Although the idea of representing texts
by dense vectors is intuitive, it is not easy to construct large-
scale dense vector index for efﬁcient search. Without the
support of a suitable index structure, the retrieval process
(i.e., ﬁnding the most close text vectors w.r.t. query vectors)
would be extremely slow. For this issue, a popular solution
is the use of Approximate Nearest Neighbor Search (ANNS) al-
gorithms [84
```

**[C5]**

```
[DESIRE-ME: Domain-Enhanced Supervised Information REtrieval using Mixture-of-Experts, chunk_3]
. Even in
this case, we observe a significant performance boost over the underlying dense
retriever.
The paper is organized as follows. Section 2 discusses the relevant related
work. Section 3 formally introduces the DESIRE-ME architecture and method-
ology while Section 4 discusses the results of our experimental analysis on public
datasets. Finally, Section 5 concludes the work and drafts some future work.
```

</details>

Claims:

- **c031** Knowledge distillation from cross-encoder rerankers improves the bi-encoder's ranking quality.
- **c032** Karpukhin et al. first showed that using hard negatives sampled from BM25 top retrieved passages is sufficient for learning an effective BERT-based dense retriever.
- **c033** Late interaction architectures, such as ColBERT, preserve token-level embeddings.
- **c034** A gradient caching technique proposed by Gao et al. later enabled the RocketQA pipeline to run on a single GPU.
- **c035** Auto-encoder and contrastive learning-based pretraining methods are increasingly adopted to enhance semantic representations.
- **c036** Better negative sampling strategies have contributed to stronger dense retrievers.
---

## q007: What multi-hop question example does the GeAR paper use to illustrate why a base retriever cannot answer complex questions in a single step?

<details><summary>Excerpts</summary>

**[C1]**

```
[GeAR: Graph-enhanced Agent for Retrieval-augmented Generation, chunk_2]
Retrieval-augmented Generation (RAG) has en-
hanced the performance of Large Language Models
(LLMs) (OpenAI, 2023) in Question Answering
(QA) tasks (Lewis et al., 2020). While effective for
simple queries, multi-hop QA presents a more com-
plex challenge, requiring reasoning across several
passages or documents. Consider the example in
Table 1, where finding the correct answer requires
building a 3-hop reasoning chain starting from the
question’s main entity (i.e. “Stephen Curry”). A
base retriever cannot, by design, retrieve all neces-
sary information in a single step.
To address these complex reasoning require-
ments, researchers have increasingly turned to
graph-based approaches (Fang et al., 2024; Li et al.,
2024; Edge et al., 2024; Gutierrez et al., 2024;
†The authors contributed equally to this work.
In what year did Stephen Curry’s father join the team
from which he started his college basketball career?
Table 1: A motivating example of a multi-hop question
where a base retriever cannot, by design, retrieve all
necessary information in a single step. Graph expansion
(see §4.2), which we incorporate within GEAR, enables
retrieval of subsequent hops and guides the system to-
ward the correct answer without using an LLM.
Liang et al., 2024). By extracting entities, atomic
facts, or semantic triples (Li et al., 2024; Fang et al.,
2024; Gutierrez et al., 2024), these graphs can es-
tablish more direct pathways for multi-hop reason-
ing. For instance, HippoRAG extracts triples from
passages to form a knowledge graphs and employs
a variant of PageRank for passage retrieval (Gutier-
rez et al., 2024). GraphReader uses an LLM agent
with graph-navigating operations to explore the re-
sulting graph structure (Li et al., 2024). TRACE
relies on an LLM to iteratively select triples for
constructing reasoning chains, which then either
ground answer generation, or filter irrelevant doc-
uments from initially retrieved results (Fang et al.,
2024). However, recursively prompting LLMs to
traverse graphs remains computationally expensive,
particularly as
```

**[C2]**

```
[GeAR: Graph-enhanced Agent for Retrieval-augmented Generation, chunk_1]
Retrieval-augmented Generation (RAG) relies
on effective retrieval capabilities, yet tradi-
tional sparse and dense retrievers inherently
struggle with multi-hop retrieval scenarios. In
this paper, we introduce GEAR, a system
that advances RAG performance through two
key innovations: (i) an efficient graph expan-
sion mechanism that augments any conven-
tional base retriever, such as BM25, and (ii) an
agent framework that incorporates the result-
ing graph-based retrieval into a multi-step re-
trieval framework. Our evaluation demon-
strates GEAR’s superior retrieval capabilities
across three multi-hop question answering
datasets. Notably, our system achieves state-
of-the-art results with improvements exceed-
ing 10% on the challenging MuSiQue dataset,
while consuming fewer tokens and requiring
fewer iterations than existing multi-step re-
trieval systems. The project page is available at
https://gear-rag.github.io.
```

**[C3]**

```
[Do Multi-Hop Question Answering Systems Know How to Answer the Single-Hop Sub-Questions?, chunk_3]
 sim-
pler questions. Figure 1 presents an illustrating
example. A successful complex QA model should
be able to answer the two sub-questions “ Which
movie stars Arnold Schwarzenegger as a former
New York Police detective” and “What year did
Guns N Roses perform a promo for End of Days”
if it understands the underlying reasoning process
for the original multi-hop question.
We focus on the HotpotQA (Yang et al., 2018)
dataset under the distractor setting, in which multi-
hop questions are asked over several Wikipedia
paragraphs. We create the evaluation dataset by
generating the sub-questions and then extracting
their answers automatically. The candidate sub-
questions and intermediate answers are then man-
ually veriﬁed, which results in 1,000 sub-question
arXiv:2002.09919v2  [cs.CL]  27 Jan 2021
Figure 1: An illustrating example from the HotpotQA dataset in the distractor setting, with our construction pro-
cedure to generate an evaluation example. We only show one out of eight distracting paragraphs provided in the
context due to paper length constraint.
evaluation examples. It is surprising to ﬁnd that all
three top-performing models which we experiment
with fail to answer a large portion of sub-questions
(49.8% to 60.4%), although their corresponding
multi-hop questions are correctly answered.
Previous work has investigated the necessity of
multi-hop reasoning on HotpotQA dataset. Jiang
and Bansal (2019) construct distracting paragraphs
adversarially to demonstrate that models learn to
exploit reasoning shortcuts to locate the answer
rather than performing multi-hop reasoning. Chen
and Durrett (2019) show that a sentence-factored
model can solve a large number of questions in Hot-
potQA, suggesting multi-hop reasoning is not re-
ally needed. Min et al. (2019a) also achieve similar
result using a single-hop BERT-based model. Our
sub-question evaluation is complementary to these
approaches. While existing work shows the lack
of multi-hop reasoning by limiting or adding text
input to QA models, we provide sub-questions and
intermediate answers explicitly to interpret model
behavior on each hop of the reasoning process. It
can be used as a complementary metric to ensure
that models which can correctly
```

**[C4]**

```
[GeAR: Graph-enhanced Agent for Retrieval-augmented Generation, chunk_7]
 from R in descending order, according
to a retrieval score. BM25 or a conventional dense
retriever can serve as a base retrieval function, with-
out requiring any multi-hop capabilities.
Our goal is to retrieve relevant passages from C
that enable a retrieval-augmented model to answer
multi-hop queries (Lewis et al., 2020). To this end,
we introduce GEAR, which is a graph-enhanced
framework of retrieval agent (see Figure 1).
4 Retrieval with Synchronised Graph
Expansion
Given an input query q, let C′
q = hk
base (q, C) be
a list of passages returned by the base retriever.
Given this list, C′
q, our goal is to derive relevant
multi-hop contexts (passages) by retrieving a sub-
graph of triples that interconnect their source pas-
sages. Two challenges arise in materialising such
sub-graph retrieval: (i) locating initial triples (i.e.
starting nodes) Tq, and (ii) expanding the graph
from these initial triples while reducing the search
Figure 1: System Architecture. The left section (blue)
depicts SyncGE (detailed in §4), while the the right sec-
tion (orange), completes the GEAR system (described
in §5). A visual step-by-step walk-through of the system
is presented in Appendix C.
space. The following sections address these chal-
lenges within GEAR.
4.1 Knowledge Synchronisation
We describe a knowledge Synchronisation (Sync)
process to locate initial nodes for graph expan-
sion. We first employ an LLM to read C′
q (see
Appendix K.2) and summarise knowledge triples
that can support answering the current query q:
T′
q = read
 
C′
q, q

. (1)
T′
q is a collection of triples to which we refer
as proximal triples. Initial nodes Tq for graph
expansion are identified by linking each triple in
T′
q to a triple inT, using the tripleLink function:
Tq =

ti|ti = tripleLink(t′
i) ∀t′
i ∈ T′
q
	
. (2)
The implementation oftripleLink can vary. How-
ever, in this paper we consider
```

**[C5]**

```
[GeAR: Graph-enhanced Agent for Retrieval-augmented Generation, chunk_22]
We propose GEAR, a novel framework that incor-
porates a graph-based retriever within a multi-step
retrieval agent to model the information-seeking
process for multi-hop question answering.
We showcase the synergy between our proposed
graph retriever (i.e. SyncGE) and the LLM within
the GEAR framework. SyncGE leverages the LLM
to synchronise information from passages with
triples and expands the graph by exploring diverse
beams of triples that link multi-hop contexts. Our
experiments reveal that this strategy improves over
more naive implementations, demonstrating the
LLM’s capability to guide the exploration of initial
nodes for graph expansion. Furthermore, GEAR
utilises multi-hop contexts returned by SyncGE and
constructs a gist memory which is used for effec-
tively summarising information across iterations.
GEAR achieves superior performance compared to
other multi-step retrieval methods while requiring
fewer iterations and LLM tokens.
Limitations
The scope of this paper is limited to retrieval using
a graph of triples that bridge corresponding pas-
sages. While we demonstrate the effectiveness of
our graph expansion approach and GEAR, several
components could be further refined. More so-
phisticated graph construction methods addressing
challenges such as entity disambiguation (Dredze
et al., 2010) and knowledge graph completion (Lin
et al., 2015) may yield further improvements, as
discussed in Appendix E. Similarly, our choice of a
dense embedding model for the scoring function in
the diverse triple beam search could be replaced by
alternatives, such as formulating this as a natural
language inference task (Wang et al., 2021).
Beyond the core graph and scoring mecha-
nisms, our design choices for other agent com-
ponents—such as the gist memory, reasoner, and
query rewriter—adopt commonly validated prac-
tices from prior research (Trivedi et al., 2022; Li
et al., 2024; Fang et al., 2024). While effective,
exploring more sophisticated designs specifically
tailored for these functions presents an opportunity
for future performance gains.
```

</details>

Claims:

- **c037** The 3-hop reasoning chain starts from the question's main entity, Stephen Curry.
- **c038** The paper makes a broader point that complex, multi-step reasoning chains require sequential retrieval rather than a single-pass lookup
- **c039** all-mpnet-base-v2 is an example of a suitable dense retriever for SciDocs and FiQA
- **c040** The GeAR paper notes that a base retriever cannot, by design, retrieve all necessary information in a single step for multi-hop questions.
- **c041** The multi-hop retrieval scenario is similar to the dense retriever selection problem described by Khramtsova et al.
- **c042** The GeAR paper illustrates the limitation of a base retriever with the example question: "In what year did Stephen Curry's father join the team from which he started his college basketball career?"
---

## q008: What accuracy did the typed-dependency-based question classification method achieve on the UIUC and FPT question datasets using unigram plus typed dependency features?

<details><summary>Excerpts</summary>

**[C1]**

```
[A Factoid Question Answering System for Vietnamese, chunk_12]
 for the UIUC and FPT question dataset re-
spectively. It is worth noting that the best question classi ﬁcation
accuracy on the UIUC dataset is 89.00% by [6], where importan t
features like head words and their hypernyms are included. S uch
semantic features are not readily available for less-resou rced lan-
guages such as Vietnamese, where a WordNet is still in its ﬁrs t
stage of construction.
3.6 Textual Question to Cypher Query
Transformation
An important module of our knowledge-based QA system is the
module that transforms textual questions in Vietnamese int o equiv-
alent Cypher queries. The queries are then executed to searc h for
answers to the questions. This section describes the main pr ocess-
ing steps of this module.
First, a textual question is processed by the NLP chain prese nted
above, ranging from word segmentation to part-of-speech ta gging
and question classiﬁcation. For example a question such as “ Thành
viên chủ chốt của tập đoàn FPT là những ai?” (“Who are the
most important people of FPT Corporation?”) will be analyse d as
follows:
Word Segmentation: The output is a sequence of words: [Thành_viên,
chủ_chốt, của, tập_đoàn, FPT, là_những_ai] . Here
the underscore character is used to connect the syllables of
a word and words are separated by commas.
Part-of-speech Tagging: The output is a sequence of tagged
words: [Thành_viên/ N , chủ_chốt/ N, của/ E, tập_đoàn/ N,
FPT/ Np, là_những_ai?/ QW] . In this step, each word
of the question is tagged as a part-of-speech, where N de-
notes a common noun, Np denotes a proper noun, E denotes
a preposition and so on.
Key Word Extraction: In this step stop words or unimpor-
tant words are stripped out of the question. Only key words
are retained. In the example above, the wordcủa/ E is re-
moved.
Question Classiﬁcation: This step determines the answer
```

**[C2]**

```
[A Factoid Question Answering System for Vietnamese, chunk_11]
,
while “ What is the Internet of things? ” is of deﬁnition type. Con-
sider also these examples: (1) What tourist attractions are there in
Reims? (2) What do most tourists visit in Reims? (3) What are t he
names of the tourist attractions in Reims? (4) What attracts tourists
to Reims? (5) What is worth seeing in Reims? [14]; all these ques-
tions are of the same answer type: location. Diﬀerent wordin g and
syntactic structures classiﬁcation diﬃcult [6].
With the increasing popularity of statistical approaches t o nat-
ural language processing in general and to question classiﬁ cation
in particular, recent years have seen many machine learning ap-
proaches which have been applied to the problem of question c las-
siﬁcation. The main advantage of machine learning approach es
is that one can learn a statistical model using useful featur es ex-
tracted from a suﬃciently large set of labeled questions and then
use it to automatically classify new questions.
We use the method proposed by [12] in our question classiﬁca-
tion module. In contrast to many existing approaches for que stion
classiﬁcation which make use of very rich feature spaces or h and-
crafted rules, this method proposes a compact yet eﬀective f eature
set. In particular it uses typed dependencies as semantic fe atures. It
has been shown that by integrating only two simple dependenc ies
of types nominal subject and prepositional object, one can i mprove
the accuracy of question classiﬁcation by over 8.0% using co m-
mon statistical classiﬁers over two benchmark datasets, th e UIUC
dataset for English and a recently introduced FPT question d ataset
for Vietnamese. With unigram feature and typed dependency f ea-
ture, one can obtain accuracy of 87.6% and 80.5% using maximu m
entropy classiﬁcation for the UIUC and FPT question dataset re-
spectively. It is worth noting that the best question classi ﬁcation
accuracy on the UIUC dataset is 89.00% by [6], where importan t
features
```

**[C3]**

```
[A Survey on non-English Question Answering Dataset, chunk_23]
50 negative, unanswerable questions. 
Those question -answers pairs were posed by 
general users and physicians. The QA system built 
by the author, which combine d both information 
retrieval and natural language processing methods 
has a performance of F1 score at 83.7%. 
After the release of the first dataset, in the same 
year, ParsiNLU  (Khashabi et al., 2021)  was 
released. Compared to the first one, ParsiNLU is a 
more complete dataset that covers various NLU 
tasks. Regarding the question -answering task, 
ParsiNLU includes datasets for machine reading 
comprehension (MRC) and multiple -choice 
question answers (MCQA). The author generates 
the MRC dataset using google search queries as the 
questions feeder. Then, the results of the queries 
will be used as the contexts to answer the questions. 
To get the MCQA data, ParsiNLU utilizes general 
paper-based tests for students and employees that 
have multiple choice questions i n there. Those 
exams were then scanned and converted to text 
using OCR techniques and annotated afterward by 
Persian speakers. In ParsiNLU, there are 800 
examples of MRC data and 2460 examples of 
MCQA. The best performing model on the MRC 
dataset is the mT5-XL model with an F1 score of 
70.4% compared to an 86.2% F1 score of human 
performance. For the MCQA dataset, the author 
divided the evaluation based on the three question 
topics: literature, common knowledge, and math 
and logic. The best performing models based on the 
accuracy score for each topic are WikiBERT-base 
(36.9%), WikiBERT-base (30.2%), and mt5-small 
(39.1%) respectively. 
Not long after ParsiNLU, PeCoQ (Etezadi and 
Shamsfard, 2020) was released. The author used a 
different technique from the previous two where 
they utilize FarsBase  (Asgari-Bidhendi et al., 
2019), a Persian knowledge graph, to build the 
dataset. From all nodes and edges in the knowledge 
graphs which acts as an entity or relationship, the 
authors extracted questions and answers using 

```

**[C4]**

```
[Question Analysis for Arabic Question Answering Systems, chunk_11]
In this paper, we have developed a question analysi s module for analyzing a natural language  
question. Our Question analysis module is mainly co ncerned with the identiﬁcation of four 
important factors , namely, focus, question expansi on, Question Classiﬁcation, and Q terms 
extraction . This is a comprehensive analysis of qu estion which extracts all the necessary 
information that will be used as inputs for the oth er question answering components. We have 
evaluated our implementation of our module in terms  of its performance based  on the  focus 
identification  and Question Classiﬁcation tasks, b y evaluating  its impact on our QA system 
accuracy. Our proposed  method achieved average accuracy of 65% for the five types of questions 
with total 250 questions submitted to the system.
```

**[C5]**

```
[Answering Complicated Question Intents Expressed in Decomposed Question Sequences, chunk_11]
ifying assumption
that each question in a sequence can be solved with
just a single operation. Another major difference is
that we use a character-level LSTM , as the training
and test vocabulary are radically different.7
4.3 Results
Table 1 shows the results of both FP and NEURAL
on the test set of SQA. We present both the overall
accuracy and the accuracy of answers to questions
at each position. Although the accuracy of FP on
position-1 questions (48.7%) is much higher than its
performance on WTQ (37.0%), the overall accuracy
(32.8%) is still lower, which indicates that our SQA
dataset remains difﬁcult. In addition, the NEURAL
model signiﬁcantly underperforms FP, suggesting
that it requires more data or more sophisticated archi-
6We did not design more speciﬁc modules to handle arith-
metic or aggregation like those of Neelakantan et al. (2015),
although this is a potentially interesting direction for larger
datasets.
7Due to the fact that much of our vocabulary (e.g., numbers,
entities) is not included in a regular corpus, we suspect that the
alternative of leveraging publicly-available word embeddings
will not be effective.
answer to previous question: 
What actresses have completed an EGOT?
Which of 
them won a 
Tony after 
1960?
Name EGOT 
complete
Years to 
complete Emmy Grammy Oscar Tony
Helen 
Hayes 1977 45 1953 1977 1932 1941
Rita 
Moreno 1977 16 1977 1972 1961 1975
Audrey 
Hepburn 1994 41 1993 1994 1953 1954
Whoopi 
Goldberg 2002 17 2002 1985 1990 2002
select_row
0.05
0.87
0.13
0.94
select_col
 0.71
 0.14
 0.03
 0.02
 0.03
 0.06
 0.01
select_cell
a
Figure 2:Diagram of NEURAL architecture. Small colored rect-
angles represent the output of the character-level LSTM decoder.
The question, column header, and cell
```

</details>

Claims:

- **c043** Syntactic typed dependencies help capture relationships between question words that indicate the expected answer type.
- **c044** The question classification method achieved an accuracy of 87.6% on the UIUC dataset.
- **c045** The question classification method used maximum entropy classification.
- **c046** The FPT dataset is smaller in size than the UIUC dataset.
- **c047** The question classification method used unigram features combined with typed dependency features.
- **c048** Incorporating syntactic typed dependencies alongside simple unigram features improved classification performance over using unigrams alone.
---

## q009: What does the ChatDoctor system, referenced in this paper's related work, detail, and what does it emphasize?

<details><summary>Excerpts</summary>

**[C1]**

```
[TabMCQ: A Dataset of General Knowledge Tables and Multiple-choice Questions, chunk_3]
In related recent work Pasupat and Liang (2015) create a
dataset of QA pairs over tables. However, their annotation
setup does not impose structural constraints from tables,
and produces simple QA pairs rather than MCQs. (Yin et
al., 2015) and (Neelakantan et al., 2015) use tables in the
context of question answering, but deal with synthetically
generated query data for those tables. More generally ta-
bles have been related to QA in the context of queries over
relational databases (Cafarella et al., 2008; Pimplikar and
Sarawagi, 2012). Regarding crowd-sourcing for question
creation, Aydin et al. (2014) harvest MCQs via a gamiﬁed
app. However their work does not involve tables. Monolin-
gual alignment datasets have also been explored separately,
for example by Brockett (2007) in the context of Textual
Entailment.
3. Motivation for the Dataset
Our motivation for constructing and releasing this data
stems from promising preliminary results on using tables
and their alignments to MCQs for solving AI2’s Aristo
challenge. We manually annotated 77 of the 108 4th grade
science exam questions in the Regents dataset 2 for align-
ment to tables. The resulting data was exactly like the one
in this paper, but at a fraction of the scale. Even with this
small amount of data we were able to build a system that
rivaled our best in-house solvers of the Aristo challenge. A
larger dataset will enable us to exceed this performance,
and also allow us to explore models that require greater
amounts of data (such as Neural Networks).
A detailed description of our system is beyond the scope of
this paper, but in summary it uses a feature-rich log-linear
model to score table cells on their relevance to answering a
2http://allenai.org/content/data/Regents.
zip
arXiv:1602.03960v1  [cs.CL]  12 Feb 2016
question. A combination of structural and textual features
are used to capitalize on the semi-structured format of ta-
bles.
4. General Knowledge Tables
In this section we present the set of tables of curated natural
language facts. We discuss
```

**[C2]**

```
[Neural Approaches to Conversational Information Retrieval, chunk_202]
-domain social chatbots (Sec-
tion 7.3.1) and target-guided conversation systems (Section 7.3.2). Although there is little research on
topic shifting for CIR, the works described here provide useful lessons and lay a good foundation for
the development of future CIR systems.
7.3.1 Topic Shifting in Social Chatbots
As shown in Figure 7.6, humans commonly shift topics during conversations. Therefore, ﬂuent topic
shifts are crucial for social chatbots to be able to mimic human conversational patterns.
The Topic Manager in XiaoIce. The Topic Manager in XiaoIce, one the most popular social
chatbots, is designed to simulate human behavior of changing topics during conversations [Zhou
et al., 2020]. It consists of (1) atopic shift detectorfor deciding at each dialogue turn whether or not
to shift topics, and (2) atopic recommenderfor suggesting a new topic.
Topic shifting is triggered if XiaoIce does not have suﬃcient knowledge about the topic to engage in
a meaningful conversation, or the user is getting bored. Speciﬁcally, the detector monitors a set of
pre-deﬁned indicative signals to determine whether to it is necessary to change the topic to keep a
user engaged. Some examples of these signals are
• whether an editorial response is used due to the bot failing to generate any valid response
candidate;
• whether the bot-generated response simply repeats the user inputs, or contains no new
information; and
• whether the user inputs are getting bland, for example, “OK”, “I see”, “go on”.
Thetopicrecommenderconsistsofatopicranker,andatopicdatabasethatisconstructedbycollecting
popular topics and related comments and discussions from high-quality Internet forums, such as
Instagram in the United States and douban.com in China. The topic database is updated periodically.
When topic shifting is triggered, a list of topic candidates is retrieved from the database using the
on-goingdialogasquery. Thetop-rankedcandidatetopicischosenasthenewtopic. Thetopicranker
is implemented as a boosted tree [Wu et al., 2010] that uses the following features:
• Contextual relevance: The topic needs to be related to the dialogue, but has not been
discussed
```

**[C3]**

```
[Neural Approaches to Conversational Information Retrieval, chunk_218]
 see XiaoIce’s response in Turn
1). Figure credit: Zhou et al. [2020].
Modern Chatbots
We now turn from a more historical perspective on chatbots to more modern chatbots. In contrast to
the origin of chatbots, most modern chatbots provide a blend of information seeking and retrieval
support, task completion, and chit-chat functionalities. To demonstrate this trend in evolution of
chatbots, we now dive into XiaoIce (“Little Ice”) [Zhou et al., 2020] as an example of the modern
class of chatbots. After its release in 2014, XiaoIce became one of the most popular social chatbots in
the world reaching more than 660 million active users.
WhileXiaoIceblendsmultiplefunctionalities,thedesignfocusesoncreatinganengagingconversation.
This is predicated on the philosophy that the primary reason we have a conversation is because it is
enjoyableratherthantogetsomethingoutofit. Thisisincontrasttothebotsthatsimplyfocusontask
completion where the goal is typically to get the task completed with as few conversational turns as
possible. Themainmetricformeasuringlong-termuserengagementinXiaoIceisconversational-turns
per session (CPS). That is, a longer engaging conversation will be considered typically better in
XiaoIce. This is similar to a viewpoint taken in other settings such as the Alexa Challenge [Ram
et al., 2018a] which considered conversation length as a signal for positive engagement while also
consideringotherfactorssuchascoherence,topicdiversity,etc. Inordertopreventsimplemethodsof
extending a conversation that fail to provide much depth (e.g. like the ELIZA system above), XiaoIce
also considers the number of active users (NAU) to compute theexpectedCPS. This is analogous
to information systems which consider sessions per unique user as a sign of long-term engagement
while the short-term engagement signal is the number of turns per session. As reported in Zhou et al.
[2020] XiaoIce ultimately reached an average of 23 CPS across – one of the highest reported lengths
of engagement for chatbots.
To demonstrate how XiaoIce achieves such deep engagement, we provide several examples taken
from diﬀerent sessions of the same user as reported by Zhou et al. [202
```

**[C4]**

```
[Neural Approaches to Conversational Information Retrieval, chunk_222]
. To help ensure that topics
are extended based on the topic, XiaoIce’s topic selection model (see Section 7.3) takes into account
ﬁve factors: (1) contextual relevance: novel information that is still related to the discussion thus far;
(2) freshness: trending in the news or other external sources; (3) personal interests: likely of interest
to the user based on engagement in past sessions; (4) popularity: high overall attention online; (5)
acceptance: past interaction with the topic from other users has been high. These dimensions of
topicality provide ﬁve broad ways in which XiaoIce can bring new information into the conversation.
In terms of more general functionality, XiaoIce like other modern chatbots has a large extensive
skillset where speciﬁc “skills” or modes can be engaged through contextual triggers. Focusing simply
on the chat capabilities itself, XiaoIce fuses two common modern styles of chatbot systems: (1)
information retrieval based chat which uses retrieval from past conversations across users ﬁltered for
appropriateness; (2) a neural based chat model which is trained on ﬁltered query-context-response
pairs. While the complexity of the dialog policy and mitigation go beyond the scope of this article,
XiaoIce can be seen more generally as how chatbots have evolved from social chit-chat to include
social chit-chat as simply one capability within personalized and extensible capabilities for search,
recommendation, and task completion.
8.2.2 Conversational Search Engine
WiththeadvancesinCIR,evenstandardGUIinterfacestosearchhavebecome“moreconversational”.
These changes can be seen as part of a broader trend acknowledging that a search engine site will
continue to be useful in many contexts where voice-based search is inconvenient; however, it may still
be desirable to introduce analogous aﬀordances on a Search Engine site for conversational techniques
fordisambiguation,suggestingnewtopics,etc. Suchtrendsareevidencedonanumberofmajorsearch
engines including Google and Bing as well as other search engines. Since some of the technology
behind these capabilities have been discussed in earlier chapters. We focus on how these capabilities
present in the user experience and how the capabilities relate to a conversational style.
Figure 8.8 shows a screenshot of Microsoft’s
```

**[C5]**

```
[Neural Approaches to Conversational Information Retrieval, chunk_214]
 mother.
Tell me more about your family.
My mother takes care of me.
Who else in your family takes care of you?
My father.
Your father.
You are like my father in some ways.
What resemblance do you see?
Figure 8.2: Example of actual interaction with ELIZA excerpted from Weizenbaum [1966]. ELIZA
simulated a Rogerian psychotherapist that primarily echoes back statements as questions. Conversa-
tional input turns by the human user of the system are in normal font. Responses from ELIZA are
indented and in teletype font.
8.2 Commercial Applications
8.2.1 Chatbots
As mentioned in early chapters, the focus of this book is primarily oninformation-seeking. However,
because chatbots were one of the ﬁrst domains where signiﬁcant progress was made to a more
open-domain NL interaction, we brieﬂy review several popular chatbots whose primary goal was
to serve as AI companions. Overall, the literature and industry demonstrate a trend toward bots
that blend together various functions of retrieval, recommendation, chit-chat, and task-completion.
Increasingly, there is a belief among practitioners that conversational systems most demonstrate both
EQ (emotional quotient) and IQ (intelligent quotient). The demonstration of a “personality” can play
a critical role in user acceptance of the system – our discussion of Microsofts’s XiaoIce [Zhou et al.,
2020] highlights some of the reasons why this belief is gaining popularity. Thus, understanding the
history of diﬀerent chatbots can help current designers and researchers regardless of the primary
goals of the system. In this section we review a brief history of well-known chatbots over time as
further background for making design decisions.
Inﬂuential Historical Chatbots
Wereviewthreewell-knownhistoricalchatbots: ELIZA[Weizenbaum,1966], PARRY[Colby,1975],
and ALICE [Wallace, 2009]. ELIZA was a chatbot based on a model of Rogerian psychotherapy.
Figure 8.2 shows an example excerpt of an interaction with ELIZA originally published in 1966.
ELIZA relied on very simplistic dialog management – canned phrases and simple re-write rules
of the user’s input with catch-all fallback responses to
```

</details>

Claims:

- **c049** The dual-encoder architecture follows Karpukhin et al. (2020).
- **c050** The ChatDoctor system builds on the pre-training paradigm pioneered by Lee et al. (2019) with the Inverse Cloze Task.
- **c051** The Condenser-style pre-training architecture was proposed by Gao and Callan (2021b).
---

## q010: What two difficult issues in Information Retrieval does this paper identify as needing to be addressed?

<details><summary>Excerpts</summary>

**[C1]**

```
[Annotation of Scientific Summaries for Information Retrieval, chunk_2]
The question of assisting information seekers in locating a specific category (facet) of information has  
rarely been addressed in the IR community due to the inherent difficulty of such a task. Indeed, efficiency and  
effectiveness have been the main guiding principles in building IR models and tools. Our aim here is to delve into  
the problem of how to assist a researcher or a specialist in rapidly accessing a specific category or class of  
information in scientific texts. For this, we need annotated corpora where relevant sentences are marked up with  
the type of information they are purportedly carrying. We identified eight categories of information in abstracts  
which can be useful in the framework of information-category driven IR: OBJECTIVE, RESULT, NEWTHING,  
HYPOTHESIS, FINDINGS, RELATED WORK, CONCLUSION, FUTUREWORK. These categories enable the  
user to identify what a paper is all about and what the contribution of the author is to his/her field. We adopted a  
surface linguistic analysis using lexico-syntactic patterns that are generic to a given language and rely on surface  
cues to perform sentence annotation from scientific abstracts. Once annotated, the corpus is fed into an automatic  
summarizer which takes into account the different semantic annotations for query-oriented document ranking and  
automatic  summarization.  The  automatic  summarizer  used  here  is  Enertex   developed  by  LIA team  at  the 
University of Avignon (Fernández et al, 2007a). Enertex is based on neural networks (NN), inspired by statistical  
physics, to study fundamental problems in Natural Language Processing, like automatic summarization and topic  
segmentation.
In  this  paper,  we  will  present  some  preliminary  experiments  on  abstract  ranking  and  automatic 
summarization using the semantic annotations resulting from our sentence categorization scheme.
The plan of this paper is as follows: section 2 recalls relevant related work ; section 3 describes the sentence  
categorization method. Section  4 describes the query-oriented abstract ranking and automatic summarization  
experiments using the semantic annotations. Section 5 discusses difficulties inherent in this task as well as earlier  
unsuccessful experiments which we had attempted.
```

**[C2]**

```
[Retrieval Augmented Generation-Based Incident Resolution Recommendation System for IT Support, chunk_8]
 in their metadata.
In many cases, this allows us to identify identical links. The
two issues with documentation evolution between versions
are addressed with Rouge-1 scores, using a threshold of 0.90
as sufficiently similar to count as identical.
For retrieval, a dedicated team is already responsible for
maintaining indexed collections of the software product doc-
umentation. This saves our project from gathering, maintain-
ing, and indexing all of these documents, and its base Slate-
30M embedding returns a good first set of results.
Re-ranking this first set allows us to use fine-tuning to
improve performance without maintaining a parallel set of
indexes. For this final task-specific fine-tuning stage, we
used training data based on 1,430 questions with up to three
matching passages per question extracted from documents
identified in user interactions, together with negative exam-
ples found using BM25 search. The resulting IBM Slate-
125M model was then distilled into the deployed IBM Slate-
30M model. To evaluate its effectiveness, we present recall
before and after re-ranking with Google Search as a baseline
in Figure 2.
0 - Completely 1 - somewhat 2 - Solution
Rating irrelevant relevant/helpful in link
Product A
SME 58% (11) 0% (0) 42% (8)
Tool 26% (5) 5% (1) 68% (13)
Product B
SME 20% (12) 48% (28) 28% (17)
Tool 48% (29) 37% (22) 12% (7)
Table 3: AB testing human evaluation of retrieved links
We also conducted an AB test in which support agents of
two products were provided with a link retrieved by the tool
Figure 2: Retriever recall for top x (log scale), compar-
ing with (yellow) and without (orange) re-ranking vs. direct
Google search via SerpApi (grey) for 1729 customer issues
over six products
and a link provided by a subject matter expert. The source
of the link was randomized as Source A or Source B so that,
for example, Source A could be either our tool or an SME
for any given case. The support agents were asked to rate
each link as shown in Table 3 and to pick the better of the
two solutions
```

**[C3]**

```
[Text mining policy: Classifying forest and landscape restoration policy agenda with neural information retrieval, chunk_13]
 use agenda,
integrated and multi-sectoral analyses that prioritize interventions
that balance societal, economic, and environmental trade offs are
required [5]. This paper’s results indicate that text mining can be
used to identify gaps in policy, and to subset relevant passages
of policies to quickly summarize how the social, economic, and
environmental trade-offs of restoration are framed and where they
are missing from the conversation.
While the present research establishes the utility of analyzing
restoration policy with neural information retrieval, a number of
challenges remain that may be addressed by future research. Two
primary limitations of this study are its focus on national-level
policies and on policy agenda rather than specific incentives and
disincentives for restoration. As such, the next steps for research
include analyzing local-level policies and analyzing the sentiment
around policy agenda and specific financial incentives. Addition-
ally, text mining models based on Word2vec have difficulty disam-
biguating word meanings in different contexts and must be trained
specifically on texts from the application domain [ 23]. This im-
plies that models such as the one presented in this paper should be
Text mining policy: Classifying forest and landscape restoration policy agenda with neural information retrieval FEED ’19 KDD 2019
trained individually for each policy domain to achieve maximum
interpretability. Although this paper demonstrated fairly accurate
results on cross-domain applications, models which can learn to
disambiguate word meanings based on the domain context would
likely fare better. Word embedding based approaches also struggle
to differentiate synonyms and antonyms, and require word-level
features to be aggregated to the sentence or paragraph level [17].
Although the approach presented in this paper effectively identifies
passages pertaining to specific policy agenda, these drawbacks con-
tribute to the method’s inability to differentiate between ambitions,
discussions of agenda, and actual implementation strategies and
targets. Recent embedding approaches which learn word sense dis-
ambiguation, such as ELMo embeddings [23], or explicitly model
variable length passages, such as Doc2Vec [15] or skip-thoughts
[14], may be useful in extending the generalizability and specificity
of this approach. Finally, the utility of this approach may be ex-
tended by training light-weight classification algorithms on top
of the results to automate query expansion and cosine similarity
threshold selection or to classify the sentiment and subjectivity of
passages.

```

**[C4]**

```
[A Retrieval-Augmented Generation Framework for Academic Literature Navigation in Data Science, chunk_5]
 information in
academic literature for data scientists. The other metrics, such as Faithfulness and Answer
Relevance, assess the quality of answers generated using the retrieved context, but since
the language model used for answer generation remained unchanged, these metrics are less
indicative of improvements brought by the fine-tuning process and other retrieval enhance-
ments. Therefore, Context Relevance serves as the most appropriate measure to demonstrate
advancements in retrieval capabilities across different configurations.
This paper makes two primary contributions. First, it introduces an enhanced RAG ar-
chitecture and systematically evaluates the impact of each component on performance using
key metrics within the RAGAS framework, based on a specially prepared test set of relevant
questions. Second, it provides a focused analysis of the fine-tuning process, characterized by
its experimental flexibility and diverse potential approaches. This analysis involves exploring
various alternative configurations by altering data sources and preprocessing techniques to
allow for a detailed assessment of how different fine-tuning strategies influence the metrics.
The most effective configurations are then integrated into the overall evaluation of the pro-
posed architecture, which contributes to a comprehensive understanding of each component’s
role in system performance.
The remainder of the paper is organized as follows: The next section reviews the literature
on RAG and outlines the components of the five-stage enhancement process, highlighting
existing research gaps. In Section 3, we introduce the enhanced RAG architecture and
the metrics used to evaluate the performance of various alternatives. Section 4 presents a
3
detailed overview of the key findings from the experimental analysis. In the following section,
we provide an in-depth discussion and analysis of these findings. Finally, the paper concludes
with final thoughts and a discussion of potential avenues for future research in Section 6.
2. Literature Review
Academic guidance is an essential element in the work of a data scientist, providing
a framework for grasping existing research and directing new, creative project directions.
Engaging with scholarly articles allows data scientists to identify established methodologies,
discern gaps in current research, and draw connections between their specific challenges
and those addressed in prior studies. This process is essential for both refining research
questions and selecting or adjusting methods for data analysis and model development.
As noted by [24], data scientists heavily depend on the literature to assess what has been
accomplished, determine whether similar problems have been addressed, and find solutions
to related challenges.
In recent years, the volume of
```

**[C5]**

```
[Modeling Diverse Relevance Patterns in Ad-hoc Retrieval, chunk_3]
A central question in ad-hoc retrieval is how to learn a generalizable
function that can well assess relevance between a query and a doc-
ument. One of the major difficulties for relevance assessment lies in
that there might be diverse relevance patterns between a query and
a document. As revealed by the evaluation policy in TREC ad-hoc
task [6, 32], “a document is judged relevant if any piece of it is
relevant (regardless of how small the piece is in relation to the rest
of the document)1”. In other words, a document could be relevant
to a query as a whole or partially as long as it provides sufficient
information for users’ needs. Such diverse relevance patterns might
be highly related to the heterogeneity of long documents in ad-hoc
retrieval. As discussed by Robertson and Walker [30], there are two
underlying hypotheses concerning document structures in relev-
ance judgement, i.e. verbosity hypothesis and scope hypothesis [30].
With the Verbosity Hypothesis a long document might be relevant
to a query as a whole, while with the Scope Hypothesis the relevant
parts could be in any position of a long document, and thus it could
be partially relevant to a query.
The diverse relevance patterns call for a retrieval model to be
able to assess relevance at the right granularity adaptively in ad-hoc
retrieval. Unfortunately, most existing retrieval models operate at a
single granularity, either document-wide or passage-level. Specific-
ally, document-wide approaches compare a document as a whole
to a query. For example, most probabilistic retrieval methods (e.g.,
BM25 or language models) and learning-to-rank models [ 8, 15]
rely on document-wide feature statistics for relevance computation.
Obviously, such document-wide approaches are difficult to model
finer-granularity relevance signals, leading to potential biases on
the competition between long and short documents [25]. On the
other hand, Passage-level approaches segment a document into
passages and aggregate passage-level signals for relevance compu-
tation [4, 20, 31]. However, the performance of existing passage-
based approaches is mixed when applied to a variety of test beds
[35] by only using simple manually designed operations over the
passage-level signals. There have been a few efforts [2, 35] trying
to combine both document-wide and
```

</details>

Claims:

- **c052** The main guiding principles traditionally used in building IR models and tools have been efficiency and effectiveness.
- **c053** Addressing vocabulary mismatch and difficulty representing user information needs typically requires techniques such as query expansion.
- **c054** The reason assisting information seekers in locating a specific facet of information has rarely been addressed is due to the inherent difficulty of such a task.
- **c055** The second issue concerns accurately capturing and modeling a user's true information need.
- **c056** The paper is titled "Annotation of Scientific Summaries for Information Retrieval".
- **c057** Sophisticated ranking algorithms cannot compensate for a fundamental mismatch between query representation and document representation.
---

## q011: What two existing query-rewriting datasets does the ReFeed paper cite as supporting supervised learning for semantic reformulation, and what limitation do they share?

<details><summary>Excerpts</summary>

**[C1]**

```
[ReFeed: Retrieval Feedback-Guided Dataset Construction for Style-Aware Query Rewriting, chunk_4]
Query Rewriting for Information Retrieval.Query
rewriting aims to reformulate user queries into more effec-
tive forms for retrieval or generation tasks. Recent works
have explored explicit rewriting mechanisms optimized for
retrieval, including structured rewriting frameworks (Baek
et al. 2024) and generative reformulation approaches (Dhole
et al. 2024). These studies show that leveraging large lan-
arXiv:2603.01417v1  [cs.IR]  2 Mar 2026
Figure 1: Overview of the retrieval feedback–driven dataset generation framework. Missed queries are rewritten via LLMs to
match the style of the correct documents and validated through re-retrieval before being assembled into a style-aware corpus.
guage models for rewriting can improve recall and ranking
quality, but they primarily emphasize semantic reformula-
tion or expansion rather than aligning rewritten queries with
the stylistic patterns of target domain documents.
Feedback-Driven Query Reformulation.Another line of
research integrates retrieval or ranking feedback into the
rewriting process. For example, Mao et al. (2024) lever-
age reranker-derived ranking signals to fine-tune rewrit-
ers, and Wang et al. (2024) incorporate multi-aspect feed-
back—including retrieval, generation, and document simi-
larity—to optimize rewriting for RAG systems. Similarly,
Shi et al. (2023) augment black-box language models with
retrieval feedback to enhance evidence grounding. While
these methods demonstrate that feedback can guide rewriter
optimization, they typically employ reinforcement learning
or reward modeling to train models directly. In contrast, our
framework uses retrieval feedback as adata curation sig-
nal, constructing reusable (original, rewritten) query pairs
that encode both retrieval success and document-style align-
ment.
Existing Query Rewriting Datasets.Large-scale rewrit-
ing datasets such asCANARD(Elgohary, Peskov, and
Boyd-Graber 2019) andQReCC(Anantha et al. 2021) sup-
port supervised learning for semantic reformulation, provid-
ing pairs of conversational and standalone queries. However,
these datasets do not capture retrieval feedback or stylis-
tic variation. Our proposed dataset complements these re-
sources by leveraging retrieval outcomes to ensure effective-
ness and by explicitly conditioning rewrites on the
```

**[C2]**

```
[ReFeed: Retrieval Feedback-Guided Dataset Construction for Style-Aware Query Rewriting, chunk_2]
Information retrieval (IR) systems often fail when user
queries differ stylistically or semantically from the lan-
guage used in domain documents. In many real-world appli-
cations—such as technical manuals, customer-service chat
logs, and enterprise knowledge bases—users express prob-
lems or requests in informal, context-rich ways, whereas
documents are written in formal and domain-specific styles.
This stylistic mismatch leads to retrieval failures even when
the underlying intent of the query is correct, limiting the re-
liability of retrieval-augmented generation (RAG) systems
and conversational assistants.
Query rewriting has emerged as a promising approach to
bridge this gap. By reformulating user queries into semanti-
cally equivalent forms, rewriting helps retrievers locate rel-
evant documents more effectively. However, most existing
rewriting approaches remain semantic rather than stylistic:
they focus on preserving meaning while ignoring how in-
*This work was conducted independently and does not repre-
sent the views of the affiliated organizations.
Copyright © 2026, Association for the Advancement of Artificial
Intelligence (www.aaai.org). All rights reserved.
formation is actually phrased in the target corpus. As a re-
sult, rewritten queries may still deviate from the linguistic
and structural patterns found in domain-specific documents,
leaving retrieval performance suboptimal.
Recent advances in feedback-driven query rewriting have
shown that retrieval signals can guide better reformulation
and ranking. However, most approaches integrate such feed-
back onlyduringmodel training, using it to fine-tune rewrit-
ers via reinforcement objectives. In contrast, we investigate
how retrieval outcomes can be leveragedbeforetraining—to
automatically curate high-quality supervision data for style-
aware query rewriting.
To address these gaps, we proposeReFeed, a retrieval
feedback–guided dataset generation framework for style-
aware query rewriting. Our method automatically identi-
fies failed retrieval cases from existing QA datasets, lever-
ages large language models (LLMs) to rewrite queries in
the style of relevant documents, and validates improvement
through re-retrieval. Only rewritten queries that successfully
retrieve the correct document are retained, resulting in a
high-precision corpus of (original, rewritten) query pairs that
naturally encode both retrieval feedback and document-style
adaptation. This corpus can be used for few-shot prompt-
ing or supervised fine-tuning (SFT
```

**[C3]**

```
[DiSCo: LLM Knowledge Distillation for Efficient Sparse Retrieval in Conversational Search, chunk_16]
 consisting of query rewriting, supervised fine-tuned, and
distillation-based methods, which we list below.
Table 2: One-shot prompt used for rewriting with the LLMs
teachers. The example is taken out of the QReCC dataset.
# Instruction: I will give you a conversation between a
user and a system. You should rewrite the last question
of the user into a self-contained query.
# Example 1:
# Context:
user: Tell me about the benefit of Yoga?
system: Increased flexibility, muscle strength.
# Please rewrite the following user question:
Does it help in reducing stress?
# Re-written query:
Does Yoga help in reducing stress?
# Example 2:
# Context:
<ctx>
# Please rewrite the following user question:
<utterance>
# Re-written query:
Query rewriting methods. SPLADE-[T5/Llama/Mistral/Human]QR
does retrieval using the SPLADE ad-hoc retrieval model trained
on MS MARCO [ 47]. As input, we pass the rewritten query us-
ing T5 [55], Llama 3.1 [13], Mistral [23], or gold human rewrites2.
SPLADE no rewrite is the same ad-hoc retrieval model without
rewrite, on the original conversation.IterCQR [21], CHIQ-Fusion [43],
and LLM4CS [41] are state-of-the-art query rewriting baselines;
however, they require multiple LLM calls at inference, which puts
them under a high disadvantage. For LLM4CS, we reproduced their
best setting (RAR, Mean aggregation from 𝑁 = 5, CoT, GPT-4).
Supervised fine-tuned methods. convSPLADE [42] and convA-
NCE [42] are two methods fine-tuned using the InfoNCE loss on
the conversational contrastive labels. Their input is the whole con-
versational context. We reproduce convSPLADE for out-of-domain
retrieval using the same hyperparameters as in the original paper.
Distillation-based method. LeCoRe [42], QRACDR [46] and Con-
vDR [65]3 all learn to distill the gold human rewrite representations
and usually combine the distillation loss with an InfoNCE. Like
our DiSCo, these models do not rely on LLM calls either, making
them comparable
```

**[C4]**

```
[ReFeed: Retrieval Feedback-Guided Dataset Construction for Style-Aware Query Rewriting, chunk_1]
Retrieval systems often fail when user queries differ stylis-
tically or semantically from the language used in domain
documents. Query rewriting has been proposed to bridge
this gap, improving retrieval by reformulating user queries
into semantically equivalent forms. However, most exist-
ing approaches overlook the stylistic characteristics of target
documents—their domain-specific phrasing, tone, and struc-
ture—which are crucial for matching real-world data distribu-
tions. We introduce a retrieval feedback–driven dataset gener-
ation framework that automatically identifies failed retrieval
cases, leverages large language models to rewrite queries in
the style of relevant documents, and verifies improvement
through re-retrieval. The resulting corpus of (original, rewrit-
ten) query pairs enables the training of rewriter models that
are explicitly aware of document style and retrieval feed-
back. This work highlights a new direction in data-centric
information retrieval, emphasizing how feedback loops and
document-style alignment can enhance the reasoning and
adaptability of RAG systems in real-world, domain-specific
contexts.
```

**[C5]**

```
[ReFeed: Retrieval Feedback-Guided Dataset Construction for Style-Aware Query Rewriting, chunk_6]
Our goal is to construct aretrieval feedback–driven dataset
forstyle-aware query rewriting—a corpus of (original,
rewritten) query pairs that reflect both retrieval outcomes
and the stylistic characteristics of domain documents. The
overall framework, illustrated in Figure 1, consists of four
stages: (1) Initial Retrieval, (2) LLM-Guided Rewriting, (3)
Verification via Re-Retrieval, and (4) Dataset Assembly.
Initial Retrieval
We begin with an existing QA datasetD={(q i, ai)}, where
each queryq i is paired with its relevant document or passage
ai. Each query is embedded and used to retrieve the top-k
documents from the corpus using a dense retriever (e.g., E5-
base or BGE-large). If the ground-truth documenta i is not
included in the retrieved top-k, the instance is marked as a
miss case. These failure cases serve as informative starting
points for generating retrieval-aware rewrites.
LLM-Guided Rewriting
For each miss case, we prompt a large language model
(LLM) to rewrite the query so that it better matches the lan-
guage and style of the relevant document. The input prompt
includes (1) the original queryq i, (2) the top-kretrieved but
incorrect documentsD neg, and (3) the ground-truth docu-
ment or its summaryD pos. A simplified prompt template is
shown below:
Your goal is to refine the given query
so that it successfully retrieves
the correct document among multiple
embedded candidates.
Original query: [q i]
Correct document: [D pos]
Retrieved but irrelevant documents:
[D neg 1 ... D neg k]
Rewrite the query to better match
the style and phrasing of the correct
document, so that it can be retrieved
within the top-k results.
Do not copy or use any specific
information from the correct document.
Revise the query only based on the
content and intent of the original
query itself.
The LLM then produces one or more rewritten queries
q′
i. By conditioning on both negative and positive contexts,
the model implicitly learns to align the query with the tar-
get document’s linguistic and stylistic properties rather than
performing purely semantic paraphrasing.
Verification via Re-Retrieval
Each rewritten queryq ′
```

</details>

Claims:

- **c058** ReFeed notes that both datasets suffer from insufficient annotated examples.
- **c059** CANARD and QReCC do not account for the stylistic alignment between queries and target documents.
- **c060** The ReFeed paper draws on the RATE pipeline's experimental setup to benchmark its query-rewriting approach.
- **c061** The ReFeed paper cites the gold-standard dataset of 70 annotated papers as one of two supervised learning resources supporting semantic reformulation.
- **c062** CANARD and QReCC provide pairs of conversational and standalone queries.
- **c063** QReCC is by Anantha et al., published in 2021.
---

## q012: According to the MAGMaR 2026 shared task findings, which retrieval system achieved the highest retrieval scores, and how does it index its content?

<details><summary>Excerpts</summary>

**[C1]**

```
[Findings of the MAGMaR 2026 Shared Task, chunk_13]
The shared task at the second workshop on Mul-
timodal Augmented Generation via Multimodal
Retrieval (MAGMaR 2026) attracted two retrieval
teams and four generation teams. Text-based rea-
soning dominates both tracks: C2F-RAG achieves
the highest retrieval scores by indexing summaries
and captions rather than operating on video directly,
and every generation system converts videos to
text before reasoning. Given this shared substrate,
inference-time reasoning proves more important
than the choice of first-stage model. Reranking
transforms OmniEmbed from the weakest retrieval
baseline into a competitive first stage, and iterative
QA generation produces noticeably better articles
than single-shot variants. On the generation side,
human preference and automatic metrics also di-
verge: systems that appropriately abstain when evi-
dence is insufficient are rewarded by annotators but
penalized by MiRAGE, which treats all omissions
as failures.
These results point to several directions for fu-
ture work. Evaluation frameworks need to account
for appropriate refusal and persona-relevant cov-
erage beyond factual completeness. No submitted
system uses task-specific fine-tuning in either track,
and the strong performance of QA-based gener-
ation suggests that models trained for grounded,
persona-conditioned multi-video question answer-
ing could improve further. All current systems also
discard visual information by converting videos
to text before reasoning; architectures for direct
multi-video visual reasoning remain unexplored.
```

**[C2]**

```
[Findings of the MAGMaR 2026 Shared Task, chunk_2]
The second workshop on Multimodal Augmented
Generation via Multimodal Retrieval (MAGMaR
2026) was located at ACL in San Diego and hosted
a shared task focused on video retrieval and gen-
eration. Increasingly, information seeking needs
require solutions that span modalities, yet much of
the literature, and open shared tasks, continue to
focus on one modality (i.e., text). The focus of this
shared task is aimed at addressing this deficiency.
The task built upon the success of last year’s shared
task of retrieving videos given a query. This year
the task expanded the test collection of videos and
introduced a new generation track:
• Retrieval Track:Systems provide a ranked
list of videos in the collection ordered by rele-
vance to the query.
• Generation Track:Systems produce a text
article that answers the information need and
grounds its content in the retrieved videos.
This shared task focuses on retrieving relevant
videos and generating grounded articles that re-
*Subsequent authors listed alphabetically
spond to information needs. Given a query de-
scribing a real-world current event, participating
systems must identify pertinent videos from a large
multilingual, multimodal collection and use that ev-
idence to produce a coherent and informative writ-
ten article. Our retrieval collection comprised over
110,000 multilingual, event-centric videos. The
generation task had 19 queries for which systems
needed to produce an article that met the infor-
mation seeking needs of a specific persona. The
summaries were judged by 3 human participants.
Overall, this was a very successful shared task
garnering multiple submissions with all teams beat-
ing very strong baselines in both tracks. Teams
made meaningful improvements and explored
cutting-edge solutions to an open-problem. We
are delighted with the results and suggest you read
the system descriptions. That being said, here are
some of the highlights across submissions:
Findings of the 2026 MAGMaR Shared Task
• Text-based reasoning dominated both tracks.
Converting videos into summaries and cap-
tions rather than operating on video directly
helps in both retrieval and generation.
• Complex, persona-constrained queries issued
against a large video corpus do not perform
well for retrieval methods using only a single
dense embedding. However, more expressive
retrieval architectures can do substantially bet-
ter.
•
```

**[C3]**

```
[Findings of the MAGMaR 2026 Shared Task, chunk_8]
832
2 MARQUIS-2 0.759 0.771 0.811 0.652 0.730 0.832
1 C2F-RAG 0.848 0.851 0.853 0.773 0.832 0.837
Table 1: MAGMaR 2026 — Retrieval track leaderboard (sorted by nDCG@10). Baselines shown in italics above
the rule. Note that we received 17 submission and all of them beat a strong baseline based on the winner of last
year’s shared task. As many submitted systems were slight variants of each other, we are only showing the top 6
systems from the leaderboard.
results point to a gap in multimodal embedding
models and rerankers for complex retrieval over
long-form video.
4 Generation Task
Task.The generation task requires systems
to produce a cited, persona-consistent article
grounded in a set of relevant videos. In theoracle
setting, systems receive the ground-truth relevant
videos for each query, isolating generation quality
from upstream retrieval variance. Generated arti-
cles are evaluated both by human annotators and
by MiRAGE (Martin et al., 2026), an automatic
framework that measures factuality, information
coverage, groundedness, and citation attribution.
Each MiRAGE entailment judgment is produced
by CLUE (Zhang et al., 2026), a calibrated multi-
modal uncertain-inference model. Full results are
in Table 2.
4.1 Systems
We provide Collaborative Article Generation
(CAG) (Martin et al., 2025) as a baseline with
Qwen3.5 as the backbone (Qwen Team, 2026).
CAG achieves a human score of 3.088 with strong
precision on both information (0.76) and citation
(0.62) metrics, but low recall.
Four teams submitted 16 predictions to the
leaderboard: TRACE (Yan et al., 2026), CRAFT
(Bhosale et al., 2026), C2F-RAG (Dai et al., 2026),
and MARQUIS (Chakraborty et al., 2026). TRACE
builds a structured text timeline for each video via
OCR and object detection, then uses a text-only
LL
```

**[C4]**

```
[Findings of the MAGMaR 2026 Shared Task, chunk_0]
Findings of the MAGMaR 2026 Shared Task
Alexander Martin1 Dengjia Zhang1 Joel Brogan2* Francis Ferraro3
Jeremy Gwinnup4 Reno Kriz5 Teng Long6
Kenton Murray5 Andrew Yates5 Xiang Xiang7
1Johns Hopkins University 2OpenAI
3University of Maryland, Baltimore County 4Air Force Research Laboratory
5Human Language Technology Center of Excellence, Johns Hopkins University
6University of Amsterdam 7Huazhong University of Science and Technology
{amart233, kenton, rkriz1}@jhu.edu
```

**[C5]**

```
[Decoupling Semantics and Logic: A Training-Free Coarse-to-Fine Pipeline for Video Retrieval-Augmented Generation, chunk_11]
To demonstrate the robustness and precision of
C2F-RAG, we evaluate the system on the MAG-
MaR Full RAG track. Our experiments are de-
signed to answer two core questions:
1. Can the two-stage cognitive filtering archi-
tecture effectively isolate true evidence from
massive background noise compared to stan-
dard retrieval baselines?
2. Does the system maintain high-fidelity per-
sona constraints and temporal grounding
when scaling to real-world corpus sizes?
3.1 Experimental Setup
DatasetWe evaluate on the MAGMaR2026 Test
Set. The data is based on WikiVideo (Martin et al.,
2025a). For the retrieval and RAG settings, we
retrieve relevant videos from a combination of the
MAGMaR data and MultiVENT2.0 test (Kriz et al.,
2025). The background collection comprises ∼
110,000multilingual, event-centric videos.
Retrieval Evaluation SetupRetrieval results are
evaluated with nDCG and Recall for 10, 20, and
100. We use ir-measures (MacAvaney et al., 2022)
to calculate these scores.
Generation Evaluation SetupPredictions are
evaluated using an automatic evaluation framework.
Specifically, the systems are evaluated by MiRAGE
(Martin et al., 2025b), which captures the factuality,
information coverage, groundedness, and proper
attribution of citations. Each MiRAGE entailment
judgment is judged by CLUE (Zhang et al., 2026).
BaselinesTo benchmark the effectiveness of our
retrieval pipeline, we compare C2F-RAG against
several official and industry-standard baselines pro-
vided in the MAGMaR leaderboard:
• OmniEmbed(Ma et al., 2025): A founda-
tional zero-shot multimodal embedding base-
line that relies purely on single-stage dense
vector similarity.
• OmniEmbed + RankVideo(Skow et al.,
2026): A traditional two-stage pipeline that
employs OmniEmbed for initial recall and a
standard RankVideo module for re-ranking.
• Mixedbread(Lee et al., 2024; Li and Li,
2023): A highly competitive, commercial
state-of-the-art dense retrieval system known
for its robust semantic matching capabilities.
3.2 Retrieval Performance: The Power of
Cognitive Filtering

```

</details>

Claims:

- **c064** C2F-RAG topped the leaderboard with the best nDCG@10 among all submissions
- **c065** Text-based reasoning involves converting videos into summaries and captions instead of processing raw video
- **c066** C2F-RAG topped the leaderboard with the best related metrics among all submissions
---

## q013: How does MS MARCO/ORCAS training leakage affect retrieval effectiveness differently on the Robust04 track versus the Common Core tracks?

<details><summary>Excerpts</summary>

**[C1]**

```
[How Train-Test Leakage Affects Zero-shot Retrieval, chunk_18]
iveness on the TREC 2018
CommonCore track fortheﬁvemodelswhenoptimizing eachfold fornDCG@10,
MFR, or Precision@1 in a grid search. In contrast to Robust04 and the 2017 edi-
tion of the Common Core track, training with MSM leakage improves the eﬀec-
tiveness in all cases for all three measures. While most of the leakage-induced
eﬀectiveness improvements are not statistically signiﬁcant, the model order even
changes on the top MFR position, where PACRR with MSM leakage would
overtake monoT5 without leakage.
Discussion. The results in Tables 3–5 show that leakage from MS MARCO /
ORCAS(MSM)canhaveanimpactontheretrievaleﬀectiveness,evenwhenonly
a small number of instances are leaked, as in our experiments. While the changes
on Robust04 are rather negligible, the impact is larger for the Common Core
tracks with document publication dates closer to the ones from MS MARCO. In-
terestingly, MSM leakage-induced nDCG@10 improvements sometimes can lead
to swaps in model ordering despite the improvements not being signiﬁcant in
most cases. This exempliﬁes that experimental eﬀectiveness comparisons might
be invalid when some models had access to leaked instances during training.
Memorization of Leaked Instances.To analyze whether the models memorize
leaked instances, we compare the retrieval scores and resulting ranks of leaked
documents in the test rankings when training includes or does not include leak-
age.Forleakeddocumentsnotreturnedinthetop-100BM25results—themodels
only re-rank these—, we determine a hypothetical rank by calculating the score
of this document for the query and inserting the document at the correspond-
ing rank in the to-be-re-ranked 100 documents (including breaking score-ties by
document ID). Each leaked document thus has a maximal rank of 101.
How Train–Test Leakage Aﬀects Zero-shot Retrieval 11
Table 7.Mean retrieval score of the (leaked) relevant training documents (±standard
deviation; higher scores = “more relevant”) for models trained with / without leakage
from MS MARCO / ORCAS (MSM) or the test data (Test).
```

**[C2]**

```
[How Train-Test Leakage Affects Zero-shot Retrieval, chunk_4]
 leaks are unintentional.
The TREC 2017 and 2018 Common Core tracks [1] intentionally reused topics
from Robust04 to allow participants to use the relevance judgments for training.
Indeed, approaches trained on the Robust04 judgments were more eﬀective than
others [1]. In this paper, we study whether a similar eﬀect can be observed for
unintentional leakage from the large MS MARCO and ORCAS datasets.
Training retrieval models on MS MARCO and applying them to another
corpus is a form of transfer learning [34]. Transfer learning is susceptible to
train–test leakage since the train and test data are often generated indepen-
dently without precautions to prevent leaks [6]. Research on leakage in transfer
learning focuses on membership inference [35, 41] (predicting if a model has seen
an instance during training) and property inference [2, 17] (predicting properties
of the training data). Both inferences rely on the observation that neural models
may memorize some training instances to generalize through interpolation [5, 7]
and to similar test instances [15, 16]. It is unclear whether and how neural re-
trieval models in a transfer learning scenario are aﬀected by leakage. Memorized
relevant instances might reduce eﬀectiveness for diﬀerent test queries while im-
proving it for similar queries, like the examples in Figure 1. We take the ﬁrst
steps to investigate the eﬀects of such a train–test leakage.
When the target corpus contains only few training instances, transferred
retrieval models are often more eﬀective without ﬁne-tuning, in a zero-shot set-
ting [47]; for instance, when training on MS MARCO and testing on TREC
datasets [34, 36, 47]. A frequently used target TREC dataset is Robust04 [42]
with 250 topics and a collection of 528,155 documents published between 1989
and 1996 by the Financial Times, the Federal Register, the Foreign Broad-
cast Information Service, and the LA Times.5 Later, the TREC Common Core
track 2017 [1] reused 50 of the 250 Robust04 topics on the New York Times An-
notated Corpus [39]6 (1
```

**[C3]**

```
[How Train-Test Leakage Affects Zero-shot Retrieval, chunk_16]
-fold cross-validated eﬀectiveness on the TREC 2017
CommonCore track fortheﬁvemodelswhenoptimizing eachfold fornDCG@10,
MFR, or Precision@1 in a grid search. In contrast to Robust04, more models
improve their eﬀectiveness when trained with MSM leakage as the time gap
between the New York Times Annotated Corpus and MS MARCO is smaller
than for Robust04. MonoT5 with actual test leakage is the most eﬀective model
for all three measures, and monoT5 trained on MSM leakage is more eﬀective
than the no-leakage counterpart in nDCG@10 and MFR. MSM leakage also may
cause model order swaps at higher positions in the systems’ nDCG@10 ordering:
monoBERT with MSM leakage would slightly overtake PACRR. Still, most of
the eﬀectiveness improvements on this dataset caused by MSM leakage or test
leakagearenotsigniﬁcant(exception:thenDCG@10diﬀerencesformonoT5with
test leakage and KNRM with MSM leakage to the no-leakage counterparts).
10 Fröbe et al.
Table 6.Meanrankofthe(leaked)relevanttrainingdocuments( ±standarddeviation)
for models trained with and without leakage from MS MARCO / ORCAS (MSM leak-
age) or from the test data (test leakage). Ranks macro-averaged over all topics for test
leakage and over all topics with leaking queries for MSM leakage.
Model Robust04 Common Core 17 Common Core 18
With Without With Without With Without
MSM leak.
Duet 41.70 ±45.88 46.79±46.51 34.52±32.67 35.98±32.93 43.39±33.52 45.67±32.99
KNRM 82.36 ±31.88 84.74±30.15 43.24±31.74 43.68±31.50 53.12±32.14 53.45±32.14
monoBERT 23.08±28.71 23.58±28.22 46.97±34.95 47.11±35
```

**[C4]**

```
[How Train-Test Leakage Affects Zero-shot Retrieval, chunk_1]
Training transformer-based retrieval models requires large amounts of data un-
available in many traditional retrieval benchmarks [34]. Data-hungry training
regimes became possible with the 2019 release of MS MARCO [10] and its
367,013 queries that were subsequently enriched by the ORCAS click log [8]
with 10 million queries. Fine-tuning models trained on MS MARCO to other
benchmarks or using them without ﬁne-tuning in zero-shot scenarios is often
very eﬀective [34, 36, 47]. For example, monoT5 [36], which has been trained
only on MS MARCO data, is currently the most eﬀective model for the Ro-
bust04 document ranking task.3 Furthermore, the reference implementations of
monoT5 and monoBERT [37] in retrieval frameworks such as PyTerrier [32] or
Pyserini / PyGaggle [26] all use models trained only on MS MARCO by default.
However, when MS MARCO was oﬃcially split into train and test data, cross-
benchmark use was not anticipated, so that MS MARCO’s training queries may
overlap with the test queries of other much smaller datasets (e.g., Robust04).
In this paper, we investigate the impact of such a train–test leakage by training
neural models on MS MARCO document ranking data with diﬀerent propor-
tions of controlled leakage to Robust04 and the TREC 2017 and 2018 Common
Core tracks as test datasets.
3 https://paperswithcode.com/sota/ad-hoc-information-retrieval-on-trec-robust04
arXiv:2206.14759v2  [cs.IR]  30 Aug 2022
2 Fröbe et al.
Robust04 Topic 441
Title: lyme disease
Description: How do you
prevent and treat Lyme disease?
Narrative: Documents that
discuss current prevention
and treatment techniques for
Lyme disease are relevant.
Reports of research on new
treatments of the disease are
also relevant.
Query variants:
lyme disease treatments
prevent lyme disease
...
MS MARCO + ORCAS
lyme disease
how to treat lyme disease
how to prevent lyme disease
lyme disease treatment
prevent lyme disease

```

**[C5]**

```
[How Train-Test Leakage Affects Zero-shot Retrieval, chunk_6]
 leaks from MS MARCO / ORCAS to the
TREC datasets Robust04 and Common Core 2017 and 2018, we compare the for-
mer’s queries (367,013 plus 10 million) to the 275 topics of the latter three. Since
lexical similarity may not be suﬃcient, as indicated by the ELI5 issue [24] men-
tioned above, we compute semantic similarity scores using Sentence-BERT [38].8
WestoretheSentence-BERTembeddingsofallMSMARCOandORCASqueries
in two Faiss indexes [23] and query them for the 100 nearest neighbors (exact;
cosine similarity) of each topic’s title, description, and query variants.
To determine the threshold for the Sentence-BERT similarity score beyond
which we consider a query a source of leakage for a topic, one human annotator
assessed whether a query is leaking for a TREC topic (title, description, query
variants)forastratiﬁedsampleof100pairsofqueriesandtopicswithasimilarity
above 0.8. Against these manual judgments, a similarity threshold of 0.91 is the
lowest that yields a 0.9 precision for deciding that a query is leaking for a topic.
Table 1 shows the number of topics for which queries above this threshold can
be found. From MS MARCO and ORCAS combined, 3,960 queries are leakage
candidates for one of 181 Robust04 topics (72% of the 250 topics). From the
two Common Core tracks, 37 and 38 topics have leakage candidates (76% of the
50 topics, respectively)—high similarities mostly against the query variants.
7 https://trec.nist.gov/data/wapost/
8 Of the available pre-trained Sentence-BERT models, we use the para-
phrase detection model: https://huggingface.co/sentence-transformers/
paraphrase-MiniLM-L6-v2
How Train–Test Leakage Aﬀects Zero-shot Retrieval 5
Table 1.Number of topics (T) in Robust04 and the TREC 2017 and 2018 Common
Core tracks for which similar queries (number as Q) in MS MARCO (MSM) and the
union of MSM and ORCAS (+ORC) exist in terms of the query having a Sentence-
BERT score
```

</details>

Claims:

- **c067** The impact of MSM leakage on Robust04 is described as rather negligible or minimal.
- **c068** The different sensitivities to training leakage are largely due to how retrieval redundancy is handled across the two collections.
- **c069** In Robust04-style setups, the full training corpus is still used despite the penalty factor.
- **c070** An example of a model order swap is monoBERT with MSM leakage slightly overtaking PACRR.
- **c071** For Common Core 2017, more models improve their effectiveness when trained with MSM leakage because the time gap between the New York Times Annotated Corpus and MS MARCO is smaller than for Robust04.
- **c072** In Robust04-style setups, leakage acts like reducing the effective number of clean training signals by 2B.
---

## q014: What retrieval latency and index storage reduction does ConAE achieve on MS MARCO when compressing embeddings to 128 dimensions while matching ANCE teacher performance?

<details><summary>Excerpts</summary>

**[C1]**

```
[Dimension Reduction for Efficient Dense Retrieval via Conditional Autoencoder, chunk_9]
trievers ANCE (Xiong et al., 2021a) and build
document index with exact matching (ﬂat index),
which is implemented by FAISS (Johnson et al.,
2019). During training ConAE, we set the hyper-
parameter λas 0.1 and search Top100 documents
using vanilla ANCE to construct the Dtop collec-
tion for each query. For our CE and ANCE models,
we sample 7 negative documents for each query to
contrastively train these models and sample 1 nega-
tive document to train ConAE. In our experiments,
we set the batch size to 2 and accumulate step to
8 for ANCE. The batch size and accumulate step
are 128 and 1 for other models. All models are
implemented with PyTorch and tuned with Adam
optimizer. The learning rates of ANCE and other
models are set to 2e−6 and 0.001, respectively.
5 Evaluation Result
Four experiments are conducted in this section to
study the effectiveness of ConAE in reducing em-
bedding dimensions for dense retrieval.
5.1 Overall Performance
The performance of different dimension reduction
models is shown in Table 2. PCA, CE and ConAE
are based on ANCE (Teacher), which freezes the
teacher model and only optimizes the dimension
projection layers. ANCE starts from CE and con-
tinuously tunes all parameters in the model.
Compared with PCA and CE (Ma et al., 2021),
ConAE achieves the best performance on almost
of datasets, which shows its effectiveness in com-
pressing dense retrieval embeddings. ConAE
can achieve comparable performance with ANCE
(Teacher) using 128-dimensional embeddings to
build the document index on MS MARCO, which
reduces the retrieval latency (from 17.152 ms to
3.942 ms per query) and saves the index storage
(from 26.0G to 4.3G) signiﬁcantly. It demonstrates
that ConAE is effective to alleviate the redundancy
of the embeddings learned by dense retrievers.
Among all baselines, PCA shows signiﬁcantly
Method MS MARCO NQ TREC DL TREC-COVID
Latency(ms) MRR@10 NDCG@10 Rec@1000 Top20 Top100 NDCG@
```

**[C2]**

```
[Dimension Reduction for Efficient Dense Retrieval via Conditional Autoencoder, chunk_15]
This paper presents ConAE, which reduces the em-
bedding dimension of dense retrievers. Our experi-
ments show that ConAE can achieve comparable
retrieval performance with the teacher model, sig-
niﬁcantly reduce the index storage and accelerate
the searching process. Our further analyses show
that the high-dimensional embeddings of dense re-
trievers are usually redundant and ConAE helps to
alleviate such redundancy and visualize the embed-
ding space more intuitively and effectively.
Limitations
In this paper, we mainly focus on compressing the
embeddings of dense retrievers in an additional
stage between query/document encoding and index
building. As a result, we ﬁx query and document
embeddings of dense retrievers and project high-
dimensional embeddings to low-dimensional ones
using only one linear layer. Thus, the effectiveness
of ConAE is limited by the number of learnable pa-
rameters. Even though ConAE shows comparable
performance with ANCE (Teacher), joint modeling
the query/document encoder, dimension reduction
module and index building still show strong poten-
tial to achieve better retrieval performance.
Acknowledgments
This work is mainly supported by Beijing Academy
of Artiﬁcial Intelligence (BAAI) as well as sup-
ported in part by the Natural Science Foundation
of China under Grant No. 62206042 and No.
62006129, the Fundamental Research Funds for
the Central Universities under Grant N2216013,
China Postdoctoral Science Foundation under
Grant 2022M710022 and National Science and
Technology Major Project (J2019-IV-0002-0069).
```

**[C3]**

```
[Dimension Reduction for Efficient Dense Retrieval via Conditional Autoencoder, chunk_11]
3.041 0.2773 0.3295 0.9217 0.7687 0.8474 0.6003 0.4731
PCA-64 2.627 0.1855 0.2259 0.8540 0.6698 0.7928 0.3788 0.2174
CE-64 3.046 0.2551 0.3036 0.9042 0.7404 0.8341 0.5561 0.3968
ConAE-64 3.087 0.2862 0.3376 0.9222 0.7604 0.8460 0.5877 0.5006
Table 2: Performance of Different Dimension Reduction Models. We start from ANCE (Teacher), reduce the
embedding dimension and evaluate their retrieval effectiveness. The document indices are built with ﬂat index
and the sizes of MS MARCO indices are 26.0G, 8.5G, 4.3G and 2.2G for 768, 256, 128 and 64 dimensional
embeddings.
(a) Teacher (t-SNE).
 (b) ConAE-128 (t-SNE).
 (c) ConAE-64 (t-SNE).
 (d) Teacher (ConAE).
Figure 1: Embedding Visualization of Different Dense Retrievers. Figure 1(a), 1(b) and 1(c) are plotted with t-SNE
with 768, 128 and 64 dimensional embeddings. In Figure 1(d), we directly use ConAE w/o Decoder to visualize
the document embedding space of ANCE. The “•” in “dark orange” color denotes the golden document that ranked
2nd by ConAE-64 and 1st by other models. For other documents, darker blue ones are more relevant to the query.
worse ranking performance on MS MARCO, in-
dicating that embedding dimensions of dense
retrievers are usually nonorthogonal. ConAE-
128 achieves more than 11% improvements than
CE and performs much better on TREC-COVID,
demonstrating its ranking effectiveness and gener-
alization ability. ANCE can further improve the
retrieval performance of CE by continuously train
```

**[C4]**

```
[Dimension Reduction for Efficient Dense Retrieval via Conditional Autoencoder, chunk_14]
 KL
divergence to optimize the 2-dimensional embed-
dings to mimic the relevance score distribution of
teacher models. As shown in Figure 1(d), the dis-
tributions of documents are distinguishable, which
provides an intuitive way to analyze the ranking-
oriented document distribution. In addition, the
query is usually far away from the documents. The
main reason lies that the relevance scores are calcu-
lated by dot product and the embedding norms are
meaningful to distinguish the relevant documents.
5.4 Retrieval Performance with HNSW
Besides exact searching, we also show retrieval
results of different dimension reduction methods
in Table 4, which are implemented by the approxi-
mate nearest neighbor (ANN) search, Hierarchical
Navigable Small World (HNSW). Using HNSW,
Dim. Method Latency MS MARCO
(ms) MRR@10 NDCG@10
768 ANCE 2.056 0.3295 0.3869
256
PCA 1.016 0.2427 0.2924
CE 1.646 0.2948 0.3461
ConAE 1.478 0.3257 0.3818
128
PCA 0.702 0.2340 0.2829
CE 1.047 0.2906 0.3424
ConAE 0.978 0.3209 0.3770
64
PCA 0.616 0.1844 0.2246
CE 0.860 0.2545 0.3030
ConAE 0.983 0.2837 0.3344
Table 4: ANN Retrieval Effectiveness of Different
Models. The ANN index is built with HNSW.
the retrieval efﬁciency can be further improved, es-
pecially for high-dimensional embeddings. ConAE
keeps its advanced retrieval performance again with
less than 1ms retrieval latency.
```

**[C5]**

```
[Dimension Reduction for Efficient Dense Retrieval via Conditional Autoencoder, chunk_13]
 shows stronger generalization ability by
outperforming ConAE w/o KL on TREC-COVID,
which belongs to a different domain. The source of
the generalization ability of ConAE w/o Decoder
may come from ﬁner-grained training signals from
our teacher model. The annotated training signals
usually face the hole rate problem (Xiong et al.,
2020) and using neural IR models to denoise the
training signals has shown strong effectiveness in
training neural IR models (Qu et al., 2021).
ConAE combines both KL and autoencoder ar-
chitectures to fully use training signals and regulate
the distribution of compressed embedding, which
usually achieves better retrieval performance.
5.3 Embedding Visualization with ConAE
We randomly sample one case from MS MARCO
and visualize the embedding space of query and
retrieved documents in Figure 1.
We ﬁrst employ t-SNE (van der Maaten and Hin-
ton, 2008) to visualize the embedding spaces of
ANCE (Teacher) and ConAE. As shown in Fig-
ure 1(b), ConAE-128 conducts a more meaningful
visualization results: the related query-document
pair is closer and the other documents are dis-
tributed around the golden document according
to their relevance to the query. The visualization
of ANCE (Teacher) is slightly distorted and dif-
ferent from our expectations, which is mainly due
to its redundancy. The redundant features usually
mislead t-SNE to overﬁt these ranking features,
thus reducing the embedding dimension of dense
retrievers to 128 provides a possible way to alle-
viate redundant features and better visualize the
embedding space of dense retrievers using t-SNE.
Besides, ConAE-64 shows decreased retrieval per-
formance than ConAE-128 (Sec. 5.1). As shown
in Figure 1(c), it mainly derives from that ConAE-
64 loses some ranking features with the limited
embedding dimensions.
The other way to visualize the embedding space
is using ConAE w/o Decoder to project the em-
bedding to a 2-dimensional coordinate. It uses KL
divergence to optimize the 2-dimensional embed-
dings to mimic the relevance score distribution of
teacher models. As shown in Figure 1(d), the dis-
tributions of documents are distinguishable, which
provides an intuitive
```

</details>

Claims:

- **c073** ConAE shrinks the index storage from 26.0G to 4.3G on MS MARCO
- **c074** Latency reductions in dense retrieval compression approaches typically range from 2x to 5x
- **c075** ConAE reduces retrieval latency from 17.152 ms to 3.942 ms per query on MS MARCO
- **c076** ANCE embeddings are high-dimensional vectors of 768 dimensions
- **c077** Latency reductions in such compression approaches occur due to reduced vector comparison costs and improved cache efficiency
- **c078** ConAE achieves comparable retrieval performance to the ANCE (Teacher) model on MS MARCO when compressing embeddings to 128 dimensions
---

## q015: What problem does the Mixture-of-Experts based MOEBQA method aim to alleviate in biomedical question answering, and how does it split the Transformer model to do so?

<details><summary>Excerpts</summary>

**[C1]**

```
[Mixture of Experts for Biomedical Question Answering, chunk_1]
Biomedical Question Answering (BQA) has attracted increasing attention in recent years due to
its promising application prospect. It is a challenging task because the biomedical questions are
professional and usually vary widely. Existing question answering methods answer all questions
with a homogeneous model, leading to various types of questions competing for the shared pa-
rameters, which will confuse the model decision for each single type of questions. In this paper,
in order to alleviate the parameter competition problem, we propose a Mixture-of-Expert (MoE)
based question answering method called MOEBQA that decouples the computation for different
types of questions by sparse routing. To be speciﬁc, we split a pretrained Transformer model
into bottom and top blocks. The bottom blocks are shared by all the examples, aiming to capture
the general features. The top blocks are extended to an MoE version that consists of a series
of independent experts, where each example is assigned to a few experts according to its un-
derlying question type. M OEBQA automatically learns the routing strategy in an end-to-end
manner so that each expert tends to deal with the question types it is expert in. We evaluate
MOEBQA on three BQA datasets constructed based on real examinations. The results show
that our MoE extension signiﬁcantly boosts the performance of question answering models and
achieves new state-of-the-art performance. In addition, we elaborately analyze our MoE mod-
ules to reveal how M OEBQA works and ﬁnd that it can automatically group the questions into
human-readable clusters.
```

**[C2]**

```
[Mixture of Experts for Biomedical Question Answering, chunk_19]
In this paper, we point out the parameter competition problem among different types of questions in
BQA. In order to alleviate this problem, we propose a Mixture-of-Expert (MoE) based question answer-
ing method called M OEBQA that decouples the computation for different types of questions by sparse
routing. We evaluate M OEBQA on three BQA datasets constructed based on real examinations and
achieve new state-of-the-art performance. In addition, we elaborately analyze our MoE modules to re-
veal how MOEBQA works. Note that our MoE extension is neither limited to Transformer models nor
limited to question answering tasks, so it has the potential to be generalized to other models and tasks in
the future. Also, although we conduct experiments on only BQA, we encourage to try the idea of MoE
extension on other question answering tasks as long as they also need to decouple the computation for
different types of questions.
```

**[C3]**

```
[Mixture of Experts for Biomedical Question Answering, chunk_2]
In recent years, Biomedical Question Answering (BQA) has attracted increasing attention due to its
promising application prospect, e.g., supporting the clinical decision for doctors, or being integrated into
search engines and chatbots. Compared with general domain question answering, BQA is more chal-
lenging because the biomedical questions are professional and usually vary widely. Existing question
answering methods usually answer all questions with a homogeneous model, even if different types of
biomedical questions have different focuses and need different problem-solving processes. In this man-
ner, different types of questions will compete for the shared model parameters, which makes a model
more confused about each single type of questions and thus negatively affects the performance. There-
fore, existing general domain question answering methods may not be the best choice for BQA.
In this paper, we aim to alleviate the parameter competition problem via a Mixture-of-Expert (MoE)
based question answering method called MOEBQA that decouples the computation for different types of
questions by sparse routing. To be speciﬁc, we split a pretrained Transformer model into bottom and top
blocks. The bottom blocks are shared by all the examples, aiming to capture the general features among
them. By contrast, the top blocks are extended to an MoE version that consists of a series of independent
experts. In the MoE-extended top blocks, each example is assigned to a few experts according to its
question representation, which implies its underlying question type. MOEBQA automatically learns the
routing strategy in an end-to-end manner so that the questions will be grouped into clusters and each
expert tends to answer several types of questions it is expert in.
∗Joint work of Peking University and Baidu Inc.
arXiv:2204.07469v1  [cs.CL]  15 Apr 2022
We evaluate M OEBQA on three BQA datasets constructed based on real examinations, including
MedQA (Jin et al., 2020), HEAD-QA (Vilares and G ´omez-Rodr´ıguez, 2019), and NLPEC (Li et al.,
2020). The experimental results show that M OEBQA signiﬁcantly boosts the performance of ques-
tion answering models and achieves new state-of-the-art performance within a tolerable computational
overhead. In addition, we elaborately
```

**[C4]**

```
[Mixture of Experts for Biomedical Question Answering, chunk_3]
2020). The experimental results show that M OEBQA signiﬁcantly boosts the performance of ques-
tion answering models and achieves new state-of-the-art performance within a tolerable computational
overhead. In addition, we elaborately analyze our MoE modules to validate our design and reveal how
MOEBQA groups the questions into human-readable clusters.
Our contributions are summarized as follows: (1) We point out the parameter competition problem in
BQA, which limits the performance of BQA models. (2) We propose an MoE-based question answering
method called MOEBQA to alleviate the parameter competition problem by decoupling the computation
for different types of questions. (3) We evaluate M OEBQA on three BQA datasets and show that it
achieves new state-of-the-art performance. We also perform quantitative and qualitative analysis on
MOEBQA to reveal how it works.
2 Multiple Choice Question Answering
In this section, we formulate the multiple choice question answering task, which is used to evaluate our
method in this paper. In addition, we describe a typical paradigm for this task that utilizes pretrained
Transformer models such as BERT (Devlin et al., 2019).
Given a context C, a question Q, and a set of candidate options O= {O1,O2,...,O n}, the multiple
choice question answering task requires a model to select the correct optionOa from the candidate setO.
In the typical paradigm, for each option, we ﬁrst jointly encode the context C, the question Q, and the
option Oi to obtain an overall representation. Taking BERT as an example encoder, we concatenate C,
Q, Oi, and the special tokens for BERT to form the input sequence I = “[CLS] C Q[SEP] Oi [SEP]”
and feed it into BERT to obtain the overall representation pi:
H = BERT(I), (1)
pi = Pooling(H), (2)
where H is the hidden states computed by BERT, and Pooling(·) pools the hidden states into a single
vector pi (e.g., taking the hidden state of the [CLS] token as pi). After this, we project each pi into a
scalar score ei, and determine the predicted answer as follows:
ei = qT pi, (3)
P(Oi|C,Q) =αi = exp(ei
```

**[C5]**

```
[Mixture of Experts for Biomedical Question Answering, chunk_18]
Biomedical Question Answering In recent years, many efforts in constructing BQA datasets are paid
to facilitate the BQA research. BioASQ (Tsatsaronis et al., 2012) is a cornerstone challenge that spans
several years and has various types of task types. emrQA (Pampari et al., 2018) is a large-scale reading
comprehension dataset generated by an automatic algorithm. Considering that the question-answer pairs
in real examinations usually have a considerable scale and high quality, MedQA (Jin et al., 2020), HEAD-
QA (Vilares and G´omez-Rodr´ıguez, 2019), and NLPEC (Li et al., 2020) are constructed based on medical
examinations in different countries and districts. These examination-based datasets can reﬂect the ability
of a model to solve problems in real-world scenarios, so we focus on them to validate the effectiveness
of our method.
Mixture of Experts Jacobs et al. (1991) ﬁrst propose the MoE technique to compute different examples
with independent experts. Shazeer et al. (2017) ﬁrst apply MoE to build large-scale LSTM language
models. Recently, MoE-version feed-forward networks has been designed for MoE-based Transformers.
GShard (Lepikhin et al., 2021), Switch Transformer (Fedus et al., 2021), and BASE Layer (Lewis et al.,
2021) dynamically learn to route each input token to experts. Hash Layer (Roller et al., 2021) propose to
use a pre-designed token-level hash table as the routing strategy. StableMoE (Dai et al., 2022) ﬁrst learns
to route and then ﬁxes the learned routing strategy for more stable training. Our work applies MoE to
BQA at an example granularity, aiming to decouple the computation for different types of questions.
```

</details>

Claims:

- **c079** MOEBQA builds on the AdaPCR framework's insight that passages scored independently overlook important inter-passage dependencies
- **c080** MOEBQA aligns retriever scores with answer likelihood as in Equation 1 of the AdaPCR formulation
- **c081** MOEBQA's expert-partitioned Transformer architecture improves robustness on complex, multi-hop biomedical questions
- **c082** The bottom blocks in MOEBQA are designed to capture general features common across question types.
- **c083** MOEBQA splits a pretrained Transformer model into bottom and top blocks.
- **c084** In Biomedical Question Answering, different types of biomedical questions must compete for shared model parameters when answered by a single homogeneous model.
---

## q016: What is the 'cold start' problem in course recommender systems, and how did Wu et al. propose to address it, per RAMO's related work?

<details><summary>Excerpts</summary>

**[C1]**

```
[RAMO: Retrieval-Augmented Generation for Enhancing MOOCs Recommendations, chunk_1]
Massive Open Online Courses (MOOCs) have significantly
enhanced educational accessibility by offering a wide vari-
ety of courses and breaking down traditional barriers re-
lated to geography, finance, and time. However, students of-
ten face difficulties navigating the vast selection of courses,
especially when exploring new fields of study. Driven by
this challenge, researchers have been exploring course rec-
ommender systems to offer tailored guidance that aligns
with individual learning preferences and career aspirations.
These systems face particular challenges in effectively ad-
dressing the “cold start” problem for new users. Recent
advancements in recommender systems suggest integrating
large language models (LLMs) into the recommendation pro-
cess to enhance personalized recommendations and address
the “cold start” problem. Motivated by these advancements,
our study introduces RAMO (Retrieval-Augmented Genera-
tion for MOOCs), a system specifically designed to overcome
the“cold start”challenges of traditional course recommender
systems. The RAMO system leverages the capabilities of
LLMs, along with Retrieval-Augmented Generation (RAG)-
facilitated contextual understanding, to provide course rec-
ommendations through a conversational interface, aiming to
enhance the e-learning experience.
Keywords
Retrieval-Augmented Generation (RAG), Personalized Learn-
ing, Recommender Systems, Artificial Intelligence
```

**[C2]**

```
[RAMO: Retrieval-Augmented Generation for Enhancing MOOCs Recommendations, chunk_10]
4.1 LLM vs. Non-LLM
We compared RAMO with a traditional course recommenda-
tion system built by the content-based and collaborative fil-
Figure 3: Sample output for a cold-start question on LLM vs RAG-LLM system
tering using the same dataset2. During this comparison, we
focused on the “cold start ” problem. The “cold start ” prob-
lem is especially pertinent in the context of an e-learning
platform for tutor training, such as tutor training platform
[24]. When new tutors join the platform, they are encour-
aged to complete various training courses to enhance their
tutoring skills. Given the wide range of courses available,
new tutors may feel overwhelmed when deciding where to
begin their learning journey. In such scenarios, they may
ask general questions such as, “What can I learn today since
I am a new tutor onboarding to this platform? ” They do
not have prior course completions or specific learning pref-
erences logged in the system, making it challenging for the
recommendation system to personalize suggestions based on
historical data. When prompted with“I am a new user ”, the
traditional recommender system failed to generate a recom-
mendation because its algorithm relies on the cosine simi-
larity of the descriptive texts of the user’s desired learning
topic and the database items, and there are no courses with
similar title or description as the phrase ‘ new user ’. In con-
trast, both our standard LLM and the RAG-enhanced LLM
system can provide relevant course suggestions for the new
user, with the LLM offering more detailed descriptions based
on its internal knowledge base and RAG offering more cus-
tomized outputs based on its external knowledge base and
the prompt template we designed. The comparative results
for both the standard and RAG-based recommender systems
are displayed in Figure 3.
Regarding system performance, the traditional system typi-
cally took about 0.02 seconds longer than RAMO to gener-
ate responses according to the same user interest—a certain
topic the user wants to learn, and this delay increased with
the complexity of the user’s input regarding relevant skills.
4.2 LLM vs. LLM with RAG
To explore how well our LLMs can provide personalized
course recommendations, we used prompts that specified a
2https://www
```

**[C3]**

```
[RAMO: Retrieval-Augmented Generation for Enhancing MOOCs Recommendations, chunk_4]
2.1 Course Recommender Systems
Course recommender systems are essential in educational
technology, helping students choose courses that align with
their interests and academic goals. Many prior studies have
employed collaborative filtering methods to build course rec-
ommender systems [2, 31, 19]. For instance, Schafer et al.
[31] proposed a recommender system that suggested courses
based on the preferences of similar users. A more recent ex-
ample by Koren et al. [19] developed advanced collaborative
filtering techniques to enhance course recommendation accu-
racy. However, a significant issue arises when recommending
courses for new users, as there is no historical data available
for these individuals—this is known as the “cold start” prob-
lem [35]. To address this challenge, a recent study by Wu
et al. [35] leveraged large language models (LLMs), which
utilize extensive pre-trained knowledge from web datasets,
demonstrating potential in overcoming the cold start prob-
lem. Despite the advancements in LLMs, their integration
into course recommendation systems remains largely unex-
plored, presenting an opportunity for future research to in-
novate and improve student course selection processes.
2.2 Large Language Models in Education
Large language models (LLMs) like ChatGPT, trained on
extensive datasets, have the ability to generate human-like
text and respond to questions with exceptional precision [12,
36]. Many studies have highlighted the potential of LLMs
in educational applications, leveraging their capabilities to
enhance various aspects of teaching and learning. For ex-
ample, Kabir and Lin [16] developed an adaptive practicing
system utilizing ChatGPT to generate personalized ques-
tions and feedback, demonstrating LLMs’ potential in facil-
itating tailored educational interactions. Researchers inves-
tigated multiple GPT models on their ability to generate
tailored learning materials and provide instant feedback on
student errors, enhancing personalized learning experiences
[34]. Huber et al. [13] demonstrated the use of LLMs in
creating interactive, conversational systems that assist both
students and teachers by providing adaptive learning sup-
port and resources. Moreover, LLMs are also used in gener-
ating automatic feedback for students [5, 6], handling sparse
learner performance data [37] from intelligent tutoring sys-
tems, predicting learning performance [38], and
```

**[C4]**

```
[RAMO: Retrieval-Augmented Generation for Enhancing MOOCs Recommendations, chunk_3]
] and Chat-Rec [9] demonstrated the
potential of LLMs in improving course alignment with learn-
ers’ interests and interaction. However, LLMs can some-
times generate misleading or outdated information. To coun-
teract these shortcomings, one possible solution is the in-
tegration of Retrieval-Augmented Generation (RAG) with
LLMs [26].
RAG [10] is a process that optimizes the output of LLMs
by extending their robust capabilities to cater specifically
to distinct domains or an organization’s internal knowledge
base, eliminating the need for retraining the model [8]. The
use of RAG in recommendation systems enhances the adapt-
ability of LLMs, ensuring that recommendations remain cur-
arXiv:2407.04925v1  [cs.IR]  6 Jul 2024
Figure 1: Interface of the Retrieval-Augmented Generation for MOOCs (RAMO) system
rent and contextually relevant [26]. This advancement paves
the way for more precise and targeted course recommen-
dations that adapt to changes in educational content and
learner preferences. Despite these improvements, there is
a noticeable gap in research specifically focused on using
LLMs in course recommender systems, particularly in ad-
dressing the “cold start ” problem where the system lacks a
user’s profile. Thus, our study aims to investigate the poten-
tial of LLMs, particularly those enhanced by RAG, in pro-
viding course recommendations tailored to individual user
needs. We introduce a course recommender system, RAMO
(Retrieval-Augmented Generation for MOOCs), which em-
ploys a RAG-based LLM model (refer to Figure 1). RAMO
leverages RAG’s advantage to improve the quality of course
recommendations, addressing and mitigating common issues
associated with LLMs especially in “ cold start” problem.
```

**[C5]**

```
[Federated Recommendation via Hybrid Retrieval Augmented Generation, chunk_2]
Recommendation systems play a vital role in aiding
users to discover pertinent content of their interests,
such as online commerce (Ying et al., 2018), social
media (Fan et al., 2019). The prevailing strategy in
developing recommendation systems involves ex-
tracting users’ personalized preferences from their
historical data. However, the concerns on data pri-
vacy have prompted strict regulations on data gov-
Client 1
Server 
Q: I’ve watched these 
movies, any 
recommendations?
A:            11   
Poor generalization on 
cold-start users. 
Federated RecSys
Client 2
User: query with unseen 
movie IDs?
Data:
Data:
😔
Figure 1: Under data heterogeneity and data sparsity,
traditional ID-based recommenders fail to recommend
correct items to the cold-start users.
ernance (e.g., GDPR 1). Such regulations limit the
development of modern recommendation systems.
To address this issue, federated recommenda-
tion (FR) emerges as a new paradigm facilitating
privacy-preserving recommendations (Ammad-Ud-
Din et al., 2019; Zhang et al., 2024). In FR, a cen-
tral server stores a global recommendation model,
while a set of clients contain local private data.
These clients collaboratively train the global model
without sharing their private data. Note that the
concept "client" does not necessarily refer to a sin-
gle human user, but can also represent a local data
server with a small dataset. For clarity, we con-
sistently use "client" to represent a federated
client, and use "user" to denote a human user
of a recommender system.
However, traditional FR systems usually rep-
resent users/items with discrete identities (Zhang
et al., 2024). As such, they may suffer from de-
graded performance, due to the data sparsity and
heterogeneity in the federated setting (Wu et al.,
2022; Zhang et al., 2024). In FR, the clients might
only contain the data of a few or even a single user
(data sparsity). Training an ID-based recommender
on such sparse data is prone to overfitting (Zhang
1General Data Protection Regulation:https://gdpr-info.eu/
arXiv:2403.04256v
```

</details>

Claims:

- **c085** Wu et al. proposed addressing the cold start issue by incorporating auxiliary information beyond interaction history.
- **c086** The fact that integration of LLMs into course recommendation systems remains largely unexplored presented an opportunity for the RAMO study
- **c087** The cold start problem arises because there is no historical data available for new users
- **c088** The cold start problem is especially problematic in educational settings where new courses are frequently introduced.
- **c089** Wu et al.'s approach leveraged content-based features and side information such as course descriptions, prerequisites, and learner profiles to bridge the data sparsity gap.
- **c090** Traditional recommender systems often rely on collaborative filtering methods based on preferences of similar users or historical course completions
---

## q017: What is the task of 'dense retriever selection', and why is it challenging according to this paper?

<details><summary>Excerpts</summary>

**[C1]**

```
[Leveraging LLMs for Unsupervised Dense Retriever Ranking, chunk_37]
This paper introduces a novel LLM-based approach for dense re-
triever selection, the Large Language Model Assisted Retrieval
Model Ranking (LARMOR). Dense retriever selection is a crucial
task in many applications of search engines technologies. Dense
retrievers are an effective and increasingly popular component of
a search engine. Search engine practitioners are often faced with
the choice of which dense retriever to deploy on a specific target
collection. However, it is challenging to predict a DR’s effective-
ness on a target collection that contains data different from that
in the collection used for training the DR. This is even more so if
the practitioners do not have access to user queries and relevance
judgements from the target collection, as it is often the case in many
applications, e.g., in small-medium enterprises and in domains like
health and legal, due to the cost and time required to collect these
signals, or the impossibility to access this data for privacy reasons.
Notably, LARMOR stands out as the only available method that
does not require any post-deployment data but instead relies on
minimal prior knowledge about the target collection to design
prompts to guide LLMs in generating synthetic queries, pseudo-
relevant judgments, and reference lists. These in turn are used
within LARMOR to rank dense retriever systems.
We comprehensively evaluate LARMOR across 13 different BEIR
collections, considering a large pool of state-of-the-art dense retriev-
ers. Our results demonstrate that LARMOR accurately ranks DRs
based on their effectiveness in a zero-shot manner, outperforming
all previous DR selection methods and adapted QPP methods.
Notably, unlike many existing baselines (e.g., score-based QPP,
Query Alteration, Binary Entropy), our method is model-agnostic
and can be extended to choose among any type of IR models.
For future work, we are interested in applying advanced auto-
matic prompt optimization methods [18, 61] to further enhance the
domain-specific prompts used by LARMOR. Additionally, we are
also interested in incorporating into LARMOR and study recent
advanced open-source LLMs, such as Mistral [26] and Llama3 [1].
Another promising avenue for future work is reducing the compu-
tational overhead of LLM-related computations in our pipeline.
SIGIR ’24, July 14–18
```

**[C2]**

```
[Leveraging LLMs for Unsupervised Dense Retriever Ranking, chunk_13]
truth ranking for the dense retriever selection task, defined below,
since the DRs are evaluated and ranked based on the ground truth
relevance judgments.
Dense retriever selection task : The problem of dense retriever
selection consists of predicting the ranking O(R,T,E,J)without
accessing the relevance judgments J𝑄T,𝐷T, as well as the target
queries 𝑄T. This is equivalent to producing a ranking ˆ𝑂(R,𝐷T,E)
of the rankers in Rfor the target collection Tand evaluation mea-
sure E, such that ˆ𝑂(R,𝐷T,E)corresponds to the true ranking
O(R,T,E,J). Note that ˆ𝑂(R,𝐷T,E)does not include the rele-
vance assessments J𝑄T,𝐷T and target queries 𝑄T as input. Our
goal is to develop a dense retriever selection method 𝑀(R,𝐷T)
that produces the ranking ˆ𝑂(R,𝐷T,E).
4Multiple training collections could also be used to derive a dense retriever: this does
not change the setup discussed here.
```

**[C3]**

```
[Leveraging LLMs for Unsupervised Dense Retriever Ranking, chunk_1]
In this paper we present Large Language Model Assisted Retrieval
Model Ranking (LARMOR), an effective unsupervised approach
that leverages LLMs for selecting which dense retriever to use on a
test corpus (target). Dense retriever selection is crucial for many IR
applications that rely on using dense retrievers trained on public
corpora to encode or search a new, private target corpus. This is
because when confronted with domain shift, where the downstream
corpora, domains, or tasks of the target corpus differ from the
domain/task the dense retriever was trained on, its performance
often drops. Furthermore, when the target corpus is unlabeled,
e.g., in a zero-shot scenario, the direct evaluation of the model
on the target corpus becomes unfeasible. Unsupervised selection
of the most effective pre-trained dense retriever becomes then a
crucial challenge. Current methods for dense retriever selection are
insufficient in handling scenarios with domain shift.
Our proposed solution leverages LLMs to generate pseudo-relevant
queries, labels and reference lists based on a set of documents sam-
pled from the target corpus. Dense retrievers are then ranked based
on their effectiveness on these generated pseudo-relevant signals.
Notably, our method is the first approach that relies solely on the
target corpus, eliminating the need for both training corpora and
test labels. To evaluate the effectiveness of our method, we con-
struct a large pool of state-of-the-art dense retrievers. The proposed
approach outperforms existing baselines with respect to both dense
retriever selection and ranking. We make our code and results
publicly available at https://github.com/ielab/larmor/.
CCS CONCEPTS
• Information systems →Evaluation of retrieval results .
KEYWORDS
Model selection, Dense retrievers, Zero Shot Model Evaluation
ACM Reference Format:
Ekaterina Khramtsova, Shengyao Zhuang, Mahsa Baktashmotlagh, and Guido
Zuccon. 2024. Leveraging LLMs for Unsupervised Dense Retriever Rank-
ing. In Proceedings of the 47th International ACM SIGIR Conference on Re-
search and Development in Information Retrieval (SIGIR ’24), July 14–18,
2024, Washington, DC, USA. ACM, New York, NY, USA, 
```

**[C4]**

```
[Leveraging LLMs for Unsupervised Dense Retriever Ranking, chunk_21]

the rankings of dense retrievers11 and create our final ranking of
DRs used as solution to the dense retrievers selection task.
5 EXPERIMENTAL SETUP
We aim to comprehensively evaluate our proposed DR selection
approach against a large pool of state-of-the-art DRs across a wide
range of corpora from different domains. In this section, we outline
the details of the criteria for selecting DRs from the MTEB leader-
board, along with the corpora used in our experiments. Finally, we
provide the implementation and evaluation details of our approach.
5.1 Dense Retriever Pool and Target Corpora
We assembled a large collection of state-of-the-art dense retrievers
through the following steps:
We began by examining the MTEB leaderboard, selecting the
top 30 retrievers based on their average performance across all
corpora featured in the MTEB benchmark. Next, we assessed the
performance of the retrievers on each individual corpus, expanding
our set to include any retrievers that ranked in the top 30 for a
specific corpus but were not part of our initial overall selection.
This approach naturally led to overlapping models, as those most
effective on one corpus often performed well on others. However,
certain models demonstrated unique strengths in specific corpora.
For instance, the all-mpnet-base-v2 model is ranked the best for
both SciDocs and FiQa corpora, yet it is 48th overall. Following
the selection of leading models for each corpus, we refined our
pool to align with our budgetary and computational constraints.
This entailed removing API-based retrievers, e.g. Cohere, and any
models with more than 6B parameters.
This process ultimately resulted in a carefully curated pool of
47 state-of-the-art dense retrieval models, which we will be using
for all the experiments throughout the paper. Note that the num-
ber of models in our study substantially exceeds those utilized by
Khramtsova et al. [28], thereby increasing the complexity of the
task and enhancing the credibility of our results.
For evaluation corpora, we follow Khramtsova et al. [28] who
utilized the corpora from the BEIR benchmark [54], which is widely
employed for zero-shot dense retriever evaluation. This benchmark
includes 18 collections across 9 diverse tasks. In accordance with
standard
```

**[C5]**

```
[Leveraging LLMs for Unsupervised Dense Retriever Ranking, chunk_3]
With the rapid advancements in natural language processing and
information retrieval, a multitude of diverse dense retrievers (DRs)
has emerged, demonstrating impressive effectiveness in various text
retrieval tasks [56, 63]. For example, over 100 dense retrievers are
featured in the Massive Text Embedding Benchmark1 (MTEB [41]).
A typical situation in practical application settings is that a dense
retriever trained on one or more corpora (the training corpus ) is
to be applied to a new corpus (the target corpus ). Often queries
and relevance judgements (labels) for the target corpus are not
available, or they are prohibitive to collect due to costs or data access
restrictions (this is often the case in domain specific settings like in
health, legal and patent search). In this situation, then, search engine
practitioners are faced with the question — Which dense retriever
should I use? This is the task ofdense retriever selection [28]: identify
the most suitable DR for a target corpus. This is a challenging
task because no queries and associated relevance judgements are
available for the target corpus, and thus the prediction task is to be
performed in an unsupervised manner.
A reasonable choice for dense retriever selection would be to
select the DR that performs overall best on a comprehensive leader-
board like MTEB. However, recent studies have shown that the
effectiveness of DRs is often dependent on the similarity between
the training corpus and the target corpus; in particular, the effec-
tiveness becomes varying and unpredictable when DRs are applied
to data that differs from that at training (e.g., from a new domain,
see Figure 1) [32, 35, 47, 54, 69, 70]. This issue is evident for instance
in the MTEB benchmark. There, results show that the overall top-
performing DRs may not necessarily be the most suitable for each
1https://huggingface.co/spaces/mteb/leaderboard
arXiv:2402.04853v2  [cs.IR]  23 May 2024
SIGIR ’24, July 14–18, 2024, Washington, DC, USA Ekaterina Khramtsova, Shengyao Zhuang, Mahsa Baktashmotlagh,
```

</details>

Claims:

- **c091** Queries and relevance judgments for the target corpus are sometimes prohibitively costly or restricted to collect.
- **c092** GEAR does not require a specially engineered retriever architecture.
- **c093** Dense retriever selection refers to the process by which GEAR chooses among conventional dense retrieval models to serve as the base retriever h_base.
- **c094** Simply choosing the dense retriever that performs best overall on a comprehensive leaderboard like MTEB is not a reliable strategy.
- **c095** These challenges motivate the development of methods like LARMOR.
- **c096** Dense retrievers, like sparse counterparts, inherently struggle with multi-hop retrieval scenarios.
---

## q018: What hardware and training configuration did the NEWSKVQA experiments use (GPUs, batch size, epochs)?

<details><summary>Excerpts</summary>

**[C1]**

```
[Enhancing Visual Question Answering through Ranking-Based Hybrid Training and Multimodal Fusion, chunk_18]
 software configurations used for training and evaluating 
the RankVQA model. The detailed configurations are shown in table 1. 
Table 1. Experimental Environment 
Parameter Configuration 
GPU NVIDIA Tesla V100 (32GB) 
CPU Intel Xeon E5-2698 v4 
Memory 256GB DDR4 
Storage 2TB SSD 
Operating System Ubuntu 20.04 LTS 
Deep Learning Framework PyTorch 1.10.0 
CUDA Version 11.2 
cuDNN Version 8.1 
Python Version 3.8.10 
 
4.3 Experimental Details 
4.3.1. Data preprocessing  
During the data preprocessing stage, we applied several steps to the VQA v2.0 and COCO -QA 
datasets to ensure the quality and consistency of the input data. First, for the image data, we resized 
all images to a uniform size of 224x224 pixels to meet the input requirements of the model. 
Additionally, we normalized the images by scaling the pixel values to the range of 0 to 1, which helps 
to accelerate the training process and improve the model's convergence. Second, for the text data, we 
 Journal of Intelligence Technology and Innovation (JITI), 2024, 2(3), 1-27. 
  16  
 
tokenized the questions into sequences of words or subwords, enabling the model to better understand 
the semantics of the questions. We also removed common stopwords such as "the" and "is" to reduce 
noise and extract key information. These preprocessing steps ensured high-quality and consistent data, 
thereby enhancing the performance of the RankVQA model during training and testing. 
4.3.2. Model training 
In terms of network parameter settings, we chose a configuration suitable for the visual question 
answering task. The specific configuration is shown in the table2. 
Table 2. Network parameter settings for training the RankVQA model. 
Parameter value 
Learning Rate 0.001 
Batch Size 64 
Epochs 50 
Optimizer Adam 
β1 0.9 
β2 0.999 
Early Stopping 5 consecutive epochs 
 
During training, we used a combined loss function of classification loss and ranking loss. The 
classification loss employed the cross- entropy loss function to optimize the model's classification 
accuracy, while the ranking loss used the contrastive loss
```

**[C2]**

```
[Transformer Module Networks for Systematic Generalization in Visual Question Answering, chunk_14]
4e-5 for
GQA. We search best learning rates for each model. We train all the models with batch size of 128
on 4 Tesla V100 GPUs for 20 epochs except standard Transformer on CLEVR, where we use 30
epochs to achieve convergence. Training of standard Transformers and TMNs ﬁnished in 3 and 4
days, respectively. We use this experimental setup and hyperparameter tuning for all experiments.
–Other methods: We also experiment with other state-of-the-art methods, including Vector-
NMN (Bahdanau et al., 2020), MDETR (Kamath et al., 2021) and MMN (Chen et al., 2021)
(LXMERT (Tan & Bansal, 2019) in Appendix G). We use the hyperparamters described in the orig-
inal papers. For a fair comparison, we train Vector-NMN and MMN using their publicly available
code on the same training set as the rest of the methods. We also use the ground-truth programs as
in TMN. MDETR was already trained on the same training set as the rest of the methods, and hence,
we use the publicly available trained model. Also, we report the performance of NS-VQA (Yi et al.,
2018) from its original paper and Akula et al. (2021).
5 Results and Analysis
In this section, we ﬁrst report the systematic generalization performance to novel combinations of vi-
sual attributes or linguistic constructs with synthetic images (CLEVR-CoGenT and CLOSURE) and
complex natural images (GQA-SGL). Then, we analyze the effect of module composition, module
specialization, and pre-training.
5.1 Systematic Generalization Performance
Tables 1 and 2 show the mean and standard deviation accuracy of TMNs and the rest of approaches
for both in-distribution and systematic generalization (see Appendix B, C, D and J for further de-
tails). In the following, we ﬁrst introduce the results in the three datasets, and then, we discuss
them:
CLEVR-CoGenT. It evaluates the systematic generalization performance to novel combinations
of known visual attributes. All models are trained on CLEVR-CoGenT condition A. Our results
show that both standard Transformers and TMNs largely outperform the state-of-the
```

**[C3]**

```
[Hyperlink-induced Pre-training for Passage Retrieval in Open-domain Question Answering, chunk_11]
 to Reddy et al.
(2021)’s work. For HotpotQA and MS MARCO,
we use the ofﬁcial corpus.
4.3 Implementation Details
During the pre-training, we train the bi-encoder for
5 epochs with parameters shared, using a batch size
of 400 and an Adam optimizer (Kingma and Ba,
2014) with a learning rate 2 ×10−5, linear schedul-
ing with 10% warm-up steps. Our HLP and all
the reproduced baselines are trained on 20 million
Q-P pairs with in-batch negative sampling, and the
best checkpoints are selected based on the average
rank of gold passages evaluated on the NQ dev set.
The pre-training takes around 3 days using eight
NVIDIA V100 32GB GPUs.
For the downstream, we use the same hyper-
parameters for all experiments. Speciﬁcally, we
ﬁne-tune the pre-trained models for 40 epochs with
a batch size of 256 and the same optimizer and
learning rate settings to the pre-training. We con-
duct evaluation on respective dev sets to select best
checkpoints, and we use the last checkpoint if there
is no dev set or test set (e.g. HotpotQA). More
details can be found in the Appendix A.
4.4 Baselines
Most existing baselines have been implemented un-
der different experimental settings, which have a
substantial effect on the retrieval performance. To
ensure fairness, we reproduce several pre-training
methods (ICT, WLP, BFS, and their combina-
tion) under the same experimental setting, such
as batch size, base model, amount of pre-training
data, and so on. The only difference between our
method and the re-implemented baselines is the
self-supervision signal derived from the respective
pre-training samples. Our reproduced BM25 base-
line is better than that reported in Karpukhin et al.
(2020), and the re-implemented pre-training meth-
ods also perform better than those reported by the
recent work3. In addition, we include the work
REALM (Guu et al., 2020) as a baseline which has
recently been reproduced by Sachan et al. (2021)
using 240 GPUs and is named masked salient spans
(MSS
```

**[C4]**

```
[Domain-Adaptive and Scalable Dense Retrieval for Content-Based Recommendation, chunk_19]
 ONNX Runtime 1.17.0.
• CPU instructions: A VX2 supported; A VX-512/VNNI not supported.
• Training configuration: epochs = 1; effective batch size = 32 (batch size 8 with gradient accumulation 4); max
sequence length = 500; seed = 42.
• Hardware and timing: training time = 3 h 40 min (single run; no distributed training). Threads pinned to 1 core;
dynamic INT8 quantization for CPU.
• Evaluation: the candidate set is the full catalog of 826,402 items (no filtering).
11
APREPRINT- FEBRUARY3, 2026
7.2 Ethical Considerations
This study uses the Amazon Reviews 2023 (Fashion) dataset, which consists of publicly available user reviews paired
with item metadata. The model is trained and evaluated only for retrieval (embedding and nearest-neighbor search) and
does not generate text.
7.3 Artifacts
For transparency, we provide access to the main artifacts used in this study:
• Data:https://huggingface.co/datasets/Pandeymp29/Amazon-Fashion-Training-Data-2023.
• Model artifacts:https://huggingface.co/Pandeymp29/Amazon-Fashion-Semantic-Search.
• Demo:https://huggingface.co/spaces/Pandeymp29/Optimised-Amazon-RecSys.
• Code:https://www.kaggle.com/code/pandeymritunjay/recommendation-system-optimised.
• Benchmarking notebook:https://www.kaggle.com/code/pandeymritunjay/comparision.
```

**[C5]**

```
[Questions Are All You Need to Train a Dense Passage Retriever, chunk_11]
 or instruction-tuned T0 (Sanh et al.,
2022) language models, which have been shown
to be effective zero-shot re-rankers for information
retrieval tasks (Sachan et al., 2022).
Compute Hardware We perform training on in-
stances containing 8 or 16 A100 GPUs, each con-
taining 40 GB RAM.
Passage Retrieval To perform fast top- K pas-
sage retrieval at every training step, we pre-
compute the embeddings of all the evidence pas-
sages. Computing embeddings of 21M passages
takes roughly 10 minutes on 16 GPUs. The total
size of these embeddings is around 30 GB (768-
dimensional vectors in FP16 format). For scalable
retrieval, we shard these embeddings across all the
GPUs and perform exact maximum inner product
search using distributed matrix multiplication.
3We use the open-source MSS retriever checkpoint from
https://github.com/DevSinghSachan/emdr2.
Training Details When training with T0 (3B)
PLM, for all the datasets except WebQ, we per-
form training for 10 epochs using Adam with a
batch size of 64, 32 retrieved passages, dropout
value of 0.1, peak learning rate of 2 ×10−5 with
warmup and linear scheduling. Due to the smaller
size of WebQ, we train for 20 epochs with a batch
size of 16. When training with the T5-lm-adapted
(11B) PLM, we use a smaller batch size of 32 with
16 retrieved passages. We save the retriever check-
point every 500 steps and perform model selection
by evaluating it on the development set. We use
mixed precision training to train the retriever and
perform inference over the PLM using bﬂoat16
format. We set the value of the temperature hy-
perparameter (τ) using cross-validation.
3.3 Baselines
We compare ART to both unsupervised and super-
vised models. Unsupervised models train a single
retriever using unlabeled text corpus from the In-
ternet while supervised models train a separate re-
triever for each dataset. We report the performance
numbers from the original papers when the results
are available or run their open-source implemen-
t
```

</details>

Claims:

- **c097** Mixed-precision training was used to optimize memory usage and computational efficiency.
- **c098** The training pipeline utilized mixed-precision training in some configurations.
- **c099** The NEWSKVQA experiments were conducted using NVIDIA GPUs.
---

## q019: What are the Inverse Cloze Task, Body First Selection, and Wiki Link Prediction pre-training tasks for dense retrieval, as described in this survey?

<details><summary>Excerpts</summary>

**[C1]**

```
[Pre-training Methods in Information Retrieval, chunk_80]
 stage. Leeet al.(2019b) proposed a new pre-training task
for passage retrieval in open domain question answering (openQA), i.e.,
Inverse Cloze Task (ICT), where one sentence is randomly sampled from
a given passage as pseudo query and the rest sentences are treated as its
positive context. Inspired by ICT, Changet al.(2020) proposed another
two tasks to better take advantage of Wikipedia documents. The ﬁrst
is Body First Selection (BFS) where one sentence from the ﬁrst section
of a Wikipedia page is randomly sampled and another passage from the
same page is considered as its positive context. The other is Wiki Link
Prediction (WLP) where the sentence is sampled the same way as in
BFS, but the passage is sampled from another hyperlinked Wikipedia
page. These paragraph-level pre-training tasks are pre-trained with a
bi-encoder architecture to support the embedding-based dense retrieval.
Experiments on several QA datasets showed that the pre-trained model
signiﬁcantly outperform the widely used BM25 algorithm and the MLM
pre-trained models when ﬁne-tuning with a limited number of labeled
data. However, BFS and WLP heavily rely on the special structures of
web documents (e.g., multiple paragraph segmentation and hyperlinks),
which may hinder their application on a general text corpus.
Anotheroneborrowstheideaofinformationbottlenecktheory(Tishby
6.1. Pre-training Embeddings/Representation Models for IR 71
and Zaslavsky, 2015) which says a good representation is a maximally
compressed mapping of the input on the output. The autoencoder ar-
chitecture, which performs the compress-then-reconstruct operation
to the input, naturally conforms the information bottleneck principle.
Speciﬁcally, the general autoencoder consists of an encoder and a de-
coder, where the encoder maps the input text to representations and
the decoder is trained to reconstruct the input text from the represen-
tations. Luet al.(2021) found that the decoder may take shortcuts by
exploiting language patterns using its access to previous tokens. Thus,
the vanilla autoencoder is not able to provide high-quality sequence
representations. They proposed SEED which pre-trains autoencoder-
based language model with a weak decoder to avoid the bypass eﬀect.
By restricting the model
```

**[C2]**

```
[Hyperlink-induced Pre-training for Passage Retrieval in Open-domain Question Answering, chunk_5]
Dense Retriever Pre-training Previous works
have attempted to conduct additional pre-training
for dense retrievers on various weakly supervised
data. Borisov et al. (2016) and Dehghani et al.
(2017) pre-trained ranking models on click-logs
and BM25-induced signals respectively for web
search. Lee et al. (2019) proposed the inverse
cloze task (ICT) to pre-train a dense retrieval
model, which randomly selects sentences as pseudo
queries, and matched them to the passages that
they originate from. Besides, Chang et al. (2019)
proposed the pre-training task of wiki link predic-
tion (WLP) and body ﬁrst selection (BFS) tasks.
Similar to our work, the WLP task also leveraged
the hyperlinks within Wikipedia to construct rel-
evant text pairs. However, as shown in ﬁgure 1,
the WLP pseudo query can only ensure the weak
doc-wise contextual relationship with the passage.
Guu et al. (2020) proposed the masked-salient-span
pre-training task which optimizes a retrieval model
by the distant supervision of language model objec-
tive. As a follow-up, Sachan et al. (2021) combined
ICT with the masked-salient-span task and further
improved the pre-training effectiveness.
Data Augmentation via Question Generation
Ma et al. (2021), Reddy et al. (2021) and O ˘guz
et al. (2021) all investigate training a dense retriever
on questions synthesized by large question gen-
erative (QG) models. Targeting on the zero-shot
setting, Ma et al. (2021) trained a question gen-
erator on general-domain question passage pairs
from community platforms and publicly available
academic datasets. Reddy et al. (2021) focused
more on domain transfer and trained the QG model
on QA datasets of Wikipedia articles. O ˘guz et al.
(2021) uses the synthetically generated questions
from PAQ dataset (Lewis et al., 2021) and the post-
comment pairs from dataset of Reddit conversa-
tions for retrieval pre-training. Recently, Shinoda
et al. (2021) reveals that the QG models tend to
generate questions with
```

**[C3]**

```
[Pre-training Methods in Information Retrieval, chunk_98]
 pioneer studies (Leeet al., 2019b; Changet al., 2020;
Guu et al., 2020; Maet al., 2021b; Maet al., 2021c; Liuet al., 2021g; Ma
et al., 2021d) on the pre-training objectives tailored for IR. For example,
Lee et al.(2019b) proposed to pre-train with a large-scale document
collection with the Inverse Cloze Task (ICT) for retrieval tasks. Besides
ICT, Changet al.(2020) also proposed to capture the inner-page and
88
8.1. New Objectives & Architectures Tailored for IR 89
inter-page semantic relations with Body First Selection (BFS) and Wiki
Link Prediction (WLP) for passage retrieval in QA tasks. For the re-
ranking component, Maet al.(2021b) and Maet al.(2021c) proposed
the Representative Words Prediction (ROP) objective for pre-training,
which achieves signiﬁcant improvement. In addition to constructing
pseudo query-document pairs from the raw text, some researches turned
to relying on certain corpus structures. For example, Maet al.(2021d)
proposed to leverage the large-scale hyperlinks and anchor texts for
pre-training. Experimental results show that pre-training with four
objectives based on the hyperlinks (i.e., RQP, QDM, RDP, and ACM)
and the MLM objective jointly achieves state-of-the-art performance on
two ad-hoc retrieval datasets. On the whole, the underlying idea of all
these pre-training objectives tailored for IR is to simulate the relevance
relationship between queries and documents. However, it is still in the
preliminary stage to design more suitable pre-training objectives for IR.
New Architectures.Beyond designing new pre-training tasks for
IR, another research line is to design novel architectures according
to speciﬁc downstream tasks. For example, towards the dual-encoder
architecture for dense retrieval, Gao and Callan (2021b) argued that
language models like BERT have a non-optimal attention structure to
aggregate sophisticated information into a single dense representation
for retrieval tasks. Based on these observations, they introduced a
novel Transformer pre-training architecture, Condenser, to address
structural readiness during pre-training. Experimental results
```

**[C4]**

```
[Dense Text Retrieval based on Pretrained Language Models: A Survey, chunk_52]
 to the student model, yielding
a better distillation performance.
The above two approaches can directly produce pseudo
supervision signals for ﬁne-tuning the underlying PLMs for
dense retrieval. Besides, there are also other augmentation
related methods for dense retrieval, such as synthetic data
generation [116], [227], [228] and contrastive learning [132],
[229], [230], which are more related to pretraining. We leave
the discussion of these topics in Section 5.4.
5.4 Pretraining for Dense Retrieval Models
The original purpose of PLMs is to learn universal
semantic representations that can generalize across different
tasks. However, such representations often lead to sub-
optimal performance on downstream applications due to
the lack of task-speciﬁc optimization [92], [93], [127], [211].
Considering this issue, recent studies employ task-related
pretraining strategies for dense retrieval. Besides reducing
the pretraining discrepancy (Issue 2), these approaches can
also alleviate the scarcity of labeled relevance data (Issue
3)11. Next, we describe the pretraining approaches for dense
retrieval in detail.
5.4.1 Task Adaptive Pretraining
This line of pretraining tasks essentially follow what
have been used in BERT [28], but try to mimic the retrieval
task in a self-supervised way. Below, we list several repre-
sentative pretraining tasks for dense retrieval.
• Inverse Cloze Task (ICT) [92]: ICT randomly selects
a sentence of a given text as the query, and the
rest sentences are considered as gold matching text.
This task aims to capture the semantic context of a
sentence and enhance the matching capacity between
query and relevant contexts.
• Body First Selection (BFS) [93]: BFS utilizes the sen-
tences from the ﬁrst section of a Wikipedia article as
anchors to the rest sections of texts. It considers a
randomly sampled sentence from the ﬁrst section as
the query and a randomly sampled passage in the
following sections as a matched text.
• Wiki Link Prediction (WLP) [93]: WLP utilizes the
hyperlink to associate the query with text, where
a sampled sentence of the ﬁrst section from a
Wikipedia page is considered as the query and a pas-
sage from another article containing the hyperlink
link to the
```

**[C5]**

```
[Improving Biomedical Information Retrieval with Neural Retrievers, chunk_6]
Neural Retrieversaim to retrieve relevant context from a
large corpus given a query. NRs can be clubbed into two
architectural families – cross-attention models (Nogueira and
Cho 2019; MacAvaney et al. 2019; Yang et al. 2019), and
dual-encoder models which employ separate encoders to en-
code the query and context (Karpukhin et al. 2020; Chang
et al. 2020). The cross-attention model requires heavy com-
putation and can not be directly used in a large corpus setting,
while dual-models can allow pre-computation of context rep-
resentations and the application of efﬁcient search methods
such as MIPS (Shrivastava and Li 2014) during inference. To
take advantage of both models, Poly-Encoder (Humeau et al.
2020) uses K representations for each query and an attention
mechanism to get context-speciﬁc query representations. Col-
BERT (Khattab and Zaharia 2020) extends the dual-encoder
architecture by performing a token-level interaction step over
the query and context representations, but requires signiﬁcant
memory for large corpora (Thakur et al. 2021).
Pre-training Tasks for NR.Masked language model-
ing (MLM) and next-sentence prediction introduced in
BERT (Devlin et al. 2019) have led to a paradigm shift in the
training of neural network models for multiple NLP tasks. For
text retrieval, pre-training tasks that are more aligned with the
retrieval task have been developed. Chang et al. (2020) pro-
pose Body First Selection (BFS), and Wiki Link Prediction
(WLP) for document retrieval. Lee, Chang, and Toutanova
(2019) propose an Inverse Cloze Task (ICT) task in which a
random sentence drawn from a passage acts as a query and
the remaining passage as a relevant answer. Guu et al. (2020)
show that ICT effectively avoids the cold-start problem.
Question Generation (QG)methods have become sophis-
ticated due to the advances in sequence-to-sequence mod-
eling (Sutskever, Vinyals, and Le 2014); QG is considered
an auxiliary pre-training
```

</details>

Claims:

- **c100** The Inverse Cloze Task is implemented through XiaoIce's topic shift detector
- **c101** Body First Selection (BFS) uses sentences from the first section of a Wikipedia article as anchors to the rest of the text
- **c102** XiaoIce's topic shift detector monitors dialogue signals like bland user inputs such as 'OK' or 'I see' to determine when retrieval should be re-triggered
- **c103** Inverse Cloze Task, Body First Selection, and Wiki Link Prediction collectively feed into a five-factor topic selection model used by XiaoIce
- **c104** In Body First Selection (BFS), a randomly sampled passage from later sections is considered the matched text
- **c105** Body First Selection (BFS) randomly samples one sentence from the first section of a Wikipedia page to act as a pseudo query
---

## q020: On the DL19 dataset, which lexical perturbation (misspelling, synonym, paraphrase, or reordering) causes the largest Stage 2 NDCG drop?

<details><summary>Excerpts</summary>

**[C1]**

```
[Lost in Decoding? Reproducing and Stress-Testing the Look-Ahead Prior in Generative Retrieval, chunk_28]
ordering is near-
invariant. On DL19, Stage 2 drops by 0.217 NDCG (misspelling),
0.143 (synonym), and 0.073 (paraphrase), versus 0.014 for reorder-
ing; DL20 shows the same ranking (0.161/0.114/0.109 vs. 0.014).
These effectiveness gaps align with plan stability in Table 7: re-
ordering has the highest overlap (CandOverlap@100 ≈0.80; TokJac-
card@100 ≈0.68 on DL19/20), whereas misspelling and synonym
sharply reduce overlap (e.g., DL19 CandOverlap 0.374/0.439; Tok-
Jaccard 0.352/0.422; DL20 CandOverlap 0.348/0.498; TokJaccard
0.363/0.485), and the boxplots (Fig. 2–3) show pronounced lower
tails under lexical corruption, indicating that a non-trivial subset of
queries undergoes near-replacement of the planned set. A plausible
contributor to plan collapse under typos issubword fragmentation:
small edits can change SentencePiece segmentation, producing
rare/mismatched units that fail to fire the lexical planner’s sparse
triggers and sharply reduce planned-set overlap. Consistent with
PAG’s mechanism, this instability limits Stage 2 because the look-
ahead bonus is computed from a shifted candidate pool, reducing
coverage of relevant docid prefixes and increasing pruning risk.
Stage 2 improvements are therefore conditional: SeqGain is pos-
itive for most Dev conditions (0.043–0.048) and for DL19 under
misspelling/synonym/paraphrase (0.045/0.071/0.039 NDCG), but
becomes negative in several DL20 settings despite relatively high
SIGIR ’26, July 20–24, 2026, Melbourne, VIC, Australia Kidist Amde Mekonnen, Yongkang Li, Yubao Tang, Simon Lupart, and Maarten de Rijke
Table 7: Planner stability and plan swapping (defined in §3.4). Mean ±std over five seeds; PlanSwapDrop < 0implies the clean
plan helps.
Plan Stability(↑)Plan Sensitivity /
```

**[C2]**

```
[Lost in Decoding? Reproducing and Stress-Testing the Look-Ahead Prior in Generative Retrieval, chunk_31]
 Synonymizing Paraphrasing Naturalizing
0.00
0.25
0.50
0.75
1.00CandOverlap@100
DL19 DL20 Dev Mean ± std
Figure 2: Candidate-set stability (CandOverlap@100). Can-
dOverlap@100 compares the planner top-100 candidate sets
for clean 𝑞 vs. perturbed ˜𝑞. Line styles denote splits (DL19
solid, DL20 dashed, Dev dotted). Across five seeds: whiskers
𝑝10–𝑝90, boxes 𝑝25–𝑝75, median line, mean ±std marker (Nat-
urality: std=0).
Misspelling Ordering Synonymizing Paraphrasing Naturalizing
0.00
0.25
0.50
0.75
1.00T oken Jaccard@100
DL19 DL20 Dev Mean ± std
Figure 3: Planner-token stability (TokJaccard@100). TokJac-
card@100 compares top-100 planner tokens for clean 𝑞vs.
perturbed ˜𝑞; same plotting convention as Fig. 2.
overlap (e.g., Reordering CandOverlap 0.801 and TokJaccard 0.684,
yet SeqGain =−0.020NDCG), indicating residual sensitivity in the
sequential component beyond plan membership.
Finally, plan swapping isolates causality: PlanSwapDrop is typically
negative under harder variations (e.g., DL19 misspelling −0.058
NDCG and −0.070MRR), showing that reusing the clean bonus par-
tially recovers performance, but the magnitude is smaller than the
total losses in Table 6, implying that robustness is bounded by both
planning instability (especially tail events) and sequential-decoding
sensitivity under perturbed inputs.
Table 8: Plan collapse analysis. Collapse rate (mean ±std over
five seeds) under the criterion from §3.4 ( 𝛿= 0.05, 𝜏= p10of
CandOverlap@100 per seed-condition). We also report the
seed-mean thresholdE[𝜏](std. omitted for brevity).
Split Variation Collapse Rate (%) Threshold (𝜏)
MS MARCO Dev
Misspelling5.2
```

**[C3]**

```
[Lost in Decoding? Reproducing and Stress-Testing the Look-Ahead Prior in Generative Retrieval, chunk_33]
DL, indicating tail events where planning becomes both unstable
and planning-only effectiveness degrades.
Comparison with dense and GR baselines.Fig. 4 shows that
robustness is primarily limited bylexical disruptionrather than
benign rewrites: misspellings and synonym substitutions strongly
affect both PAG/RIPOR and the dense baseline TAS-B, while recent
Lost inDecoding? Reproducing and Stress-Testing the Look-Ahead Prior in Generative Retrieval SIGIR ’26, July 20–24, 2026, Melbourne, VIC, Australia
dense retrievers are typically less impacted across MS MARCO Dev
and TREC-DL 2019/2020. Under misspellings, RIPOR/TAS-B/PAG
drop by ∼48%/44%/41% on MS MARCO Dev, versus ∼18–26% for
recent dense models, and the same ordering holds on DL19/20.
Reordering is near-invariant for all methods (single-digit drops),
indicating brittleness is driven by surface-form mismatch rather
than word order. Synonym substitution shows a similar pattern:
recent dense models drop ∼16–22%, while RIPOR/PAG typically
drop ∼18–30%, placing PAG closer to RIPOR than to recent dense
retrievers under lexical perturbations. Overall, this comparison
aligns with RQ2–RQ3: robustness failures concentrate on lexical
surface-form shifts, which in RQ2 coincide with planner drift and
reduced candidate stability that can limit Stage 2 gains under finite-
beam decoding. RQ3 confirms the same sensitivity under stronger
surface-form mismatch (cross-lingual queries) with a fixed index
and evaluates query-side mitigations.
5.3 RQ3: Cross-lingual query shift
RQ2 showed that lexical surface-form variation can destabilize the
planning signal and weaken downstream decoding. RQ3 tests this
failure mode under a more extreme setting:cross-lingual query shift,
where query surface form diverges sharply from the English plan-
ning vocabulary on which PAG was trained, while the document
collection and all document-side artifacts remain fixed to the re-
leased English index (set-based identifiers𝑡𝑑, sequential docids𝑐𝑑,
and the trie). This setting isnotstudied in the original paper, so
```

**[C4]**

```
[Lost in Decoding? Reproducing and Stress-Testing the Look-Ahead Prior in Generative Retrieval, chunk_27]
002 (0.125±0.002) 0.245±0.003 (0.165±0.003) 0.215±0.003 (0.147±0.003)
Reordering 0.355±0.001 (0.009±0.001) 0.307±0.001 (0.008±0.001) 0.399±0.001 (0.011±0.001) 0.350±0.001 (0.012±0.001)
Synonymizing 0.260±0.001 (0.104±0.001) 0.225±0.001 (0.090±0.001) 0.305±0.002 (0.105±0.002) 0.268±0.002 (0.094±0.002)
Paraphrasing 0.297±0.001 (0.068±0.001) 0.257±0.001 (0.059±0.001) 0.342±0.003 (0.069±0.003) 0.300±0.002 (0.062±0.002)
Naturalizing 0.341±0.000 (0.023±0.000) 0.294±0.000 (0.021±0.000) 0.388±0.000 (0.022±0.000) 0.342±0.000 (0.020±0.000)
5.2 RQ2: Robustness stress test
RQ2 stress-tests PAG under intent-preserving query variation while
holding the released checkpoint, docids, trie, and decoding configu-
ration fixed. This isolates query-side sensitivity in Stage 1 planning
(SimulOnly, ranking by 𝑠simul) and in Stage 2 planning-guided de-
coding.
Query-variation evaluation.We evaluate five intent-preserving
variations of each clean query 𝑞. Table 6 shows that lexical varia-
tions cause large end-to-end degradation, while reordering is near-
invariant. On DL19, Stage 2 drops by 0.217 NDCG (misspelling),
0.143 (synonym), and 0.073 (paraphrase), versus 0.014
```

**[C5]**

```
[Lost in Decoding? Reproducing and Stress-Testing the Look-Ahead Prior in Generative Retrieval, chunk_32]
@100 per seed-condition). We also report the
seed-mean thresholdE[𝜏](std. omitted for brevity).
Split Variation Collapse Rate (%) Threshold (𝜏)
MS MARCO Dev
Misspelling5.2±0.10.015
Ordering3.2±0.80.531
Synonym5.7±0.10.032
Paraphrase6.2±0.10.078
Naturality4.5±0.00.333
TREC-DL 2019
Misspelling11.2±1.00.015
Ordering7.4±3.00.580
Synonym11.6±0.00.040
Paraphrase10.7±1.30.152
Naturality2.3±0.00.427
TREC-DL 2020
Misspelling9.6±1.50.063
Ordering10.0±1.70.617
Synonym10.4±2.50.144
Paraphrase11.1±0.00.126
Naturality11.1±0.00.392
Plan-collapse.Table 8 reports seed-aggregated collapse rates over
75 (split, variation, seed) conditions (176,925 query instances). Col-
lapse is infrequent on MS MARCO Dev (3.2–6.2%) but higher on
TREC-DL (2.3–11.6% on DL19; 9.6–11.1% on DL20), indicating a
non-trivial subset of queries with both low stability and a planning-
only drop ( Δ𝑀SimulOnly ≤−0.05). Ordering exhibits a large low-
stability tail (19.0–33.3%; Table 7) yet comparatively lower collapse,
suggesting that overlap deviations under ordering often do not
coincide with large planning-only drops at 𝛿= 0.05. By contrast,
misspelling/synonym/paraphrase yield 9.6–11.6% collapse on TREC-
DL, indicating tail events where planning becomes both unstable
and planning-only effectiveness degrades.
Comparison with dense and GR baselines.Fig. 4 shows that
robustness is primarily limited bylexical disruptionrather than
benign rewrites:
```

</details>

Claims:

- **c106** On the DL19 dataset, synonym substitution causes a decrease of 0.143 NDCG in Stage 2.
- **c107** The sensitivity to misspellings highlights a persistent weakness in reranker robustness to noisy, real-world query formulations compared to clean, well-formed text.
- **c108** On the DL19 dataset, reordering causes a decrease of 0.014 NDCG in Stage 2.
- **c109** Reordering tends to preserve more of the original semantic and lexical content, including key entities and terms.
- **c110** On the DL19 dataset, misspelling causes a decrease of 0.217 NDCG in Stage 2.
- **c111** Paraphrasing tends to preserve more of the original semantic and lexical content, including key entities and terms.
