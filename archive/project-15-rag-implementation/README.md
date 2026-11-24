# Project 15 — Chunking Experiment: RAG on the FAA Pilot's Handbook

Every RAG system cuts its documents into chunks before embedding them, and the settings are usually a guess
("1,000 characters, 200 overlap"). This project measures the choice instead, on a corpus I can check by hand:
three chapters of the FAA *Pilot's Handbook of Aeronautical Knowledge* (public domain).

## What it does

1. **Corpus** (`src/phak.py`): downloads chapters 11 (Aircraft Performance), 12 (Weather Theory) and 15 (Airspace)
   from faa.gov, extracts the text with pypdf, rejoins hyphenated and wrapped lines, and drops page numbers.
2. **Labelled questions** (`eval/questions.csv`): 20 questions, each tagged with its chapter and the words a correct
   passage must contain. The notebook checks every keyword appears in its chapter (no impossible questions) and
   doesn't appear in most chunks (no free hits).
3. **Sweep** (`src/chunking.py`): 2 strategies (fixed-size windows that never cut a word; whole sentences packed to
   a size) × 4 sizes (300–1,600 characters) × 3 overlaps (0, 15%, 30%) = 24 settings. Each one is scored on
   - **keyword hit@5**: share of questions with a correct passage in the top 5,
   - **MRR**: how high the first correct passage ranks,
   - **context characters**: how much text the LLM would have to read, the cost side of the trade-off.
   Embeddings are BGE-small (sentence-transformers), cached so each distinct chunk is embedded once.
4. **Answers** (`src/answer.py`): with the best setting and with a setting at least twice as large, a local LLM (Qwen in LM Studio) answers with passage
   citations like `[P2]`, and must reply exactly *"Not in the handbook passages."* to questions the handbook
   doesn't cover (`eval/out_of_scope.csv`: binary heaps, the World Series, radix sort, sourdough). Every answer is
   checked for citations to passages that don't exist.

## Results

Recorded run: 16 November 2026, Qwen3.6-35B-A3B in LM Studio, BGE-small embeddings, k = 5
(`outputs/chunking_sweep.csv`, `outputs/answers_run.json`, `outputs/answer_review.csv`).

**Retrieval (24 settings, 20 questions).** Fixed 300-character chunks with no overlap scored best: keyword hit@5 0.95,
MRR 0.78, about 1,500 characters of context. Fixed 600 with 15% overlap tied on hit@5 (0.95, MRR 0.78) at twice the
context. Most settings sit within one or two questions of each other, so on 20 questions these are tendencies, not a ranking:

- Bigger chunks bought nothing in retrieval: 1,600-character chunks sent the model 5× more text for 0.85–0.90 hit@5.
- Overlap didn't help consistently. It improved some sizes and hurt others.
- Packing whole sentences was clearly worst at 300 characters (0.70–0.75), likely because the chunks come out shorter
  (about 1,150 characters across the top 5, against 1,480 for fixed windows), so a definition and its context rarely fit together.

**Answers: the retrieval winner wasn't the answer winner.** Each of the 20 questions was answered twice: once with the
winning 300-character chunks and once with the best setting at least twice as large (fixed 600, 15% overlap). I then
checked all 40 answers by hand against the handbook text (`outputs/answer_review.csv`):

| | 300 chars, no overlap | 600 chars, 15% overlap |
|---|---|---|
| Correct answers | 17 / 20 | 18 / 20 |
| Correctly declined (question asks for more than the chapter holds) | 1 | 1 |
| Missed | 2 | 1 |
| Out-of-scope questions declined | 4 / 4 | – |

- The 300-character chunks lost two answers to chunk boundaries. The service ceiling definition and the sentence about
  wind flowing from high to low pressure were both cut off just before the answer. The larger chunks fixed both.
- The larger chunks lost one: for the 250-knot speed limit they retrieved "250 knots" from the military training routes
  paragraph, not the speed limit rule. The model declined to use it rather than guessing.
- Every answer cited passages that exist, every number traced to its cited passage, and all four off-topic questions
  (binary heaps, the World Series, radix sort, sourdough) got exactly "Not in the handbook passages."

**What I'd take from it.** A keyword-in-top-5 metric is a useful first pass, but on its own it picks chunks too small
to hold a complete answer. It also has false positives ("250 knots" in the wrong paragraph) and false negatives (an
answer saying "upsloping" doesn't match the keyword "upslope"). For a handbook like this I'd use ~600-character chunks
with some overlap and judge the choice on answers, not retrieval alone. One labelled question was also flawed: it asks
for the types of hydroplaning, and this edition of the chapter only describes dynamic hydroplaning. Both settings
correctly declined it, but its keyword still counts as a retrieval hit, so hit@5 is slightly generous.

## Run it

```bash
uv sync
uv run pytest -q tests          # offline: chunkers, the sweep, answer checks (toy embedding, scripted model)
uv run jupyter lab notebooks/chunking_experiment.ipynb
```

Step 4 needs LM Studio's server running with the model named in `LLM_MODEL` (see the repo's `.env.example`).
Any OpenAI-compatible endpoint works.

## Files

- `notebooks/chunking_experiment.ipynb` — corpus, keyword audit, sweep, chart, answers
- `src/phak.py`, `src/chunking.py`, `src/answer.py` — the code the notebook calls
- `corpus/phak_ch*.txt` — the cleaned chapter text
- `outputs/chunking_sweep.csv`, `outputs/chunking_sweep.png`, `outputs/answers_run.json` — recorded run
- `outputs/answer_review.csv` — my hand check of all 40 in-scope answers against the handbook

## Earlier version

The first version was two course notebooks (LangChain + ChromaDB with OpenAI, and llama-index with Ollama). One
needed a PDF that wasn't in the repo, and neither measured whether retrieval was right, so this rebuild replaces them.
