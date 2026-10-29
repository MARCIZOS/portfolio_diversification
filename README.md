# ARAIA — Portfolio Diversification Under Macroeconomic Stress

A full-stack risk analytics platform that answers one question: **when correlations converge in a crisis, how much of your diversification is real — and what single reallocation would help most?**

Most portfolio tools measure diversification in calm markets. That is exactly when it looks best. ARAIA re-prices a portfolio inside a simulated macroeconomic stress scenario, finds the correlation cluster carrying the most concentrated risk, retrieves behavioural diversifiers with FAISS vector search, and proposes a bounded reallocation — then *measures* the resulting change in stressed drawdown rather than asserting it.

Every number in the API is computed deterministically. The language model is an explainability layer on top; it never calculates risk and never chooses allocations.

---

## Table of contents

- [Architecture](#architecture)
- [How the analysis works](#how-the-analysis-works)
- [Measured results](#measured-results)
- [API](#api)
- [Running locally](#running-locally)
- [Configuration](#configuration)
- [Tests](#tests)
- [Deployment](#deployment)
- [Project layout](#project-layout)
- [Limitations](#limitations)

---

## Architecture

```
                       ┌──────────────────────────────┐
                       │  React + Vite frontend       │
                       │  Landing / Auth / Dashboard  │
                       └───────────────┬──────────────┘
                                       │  JSON over HTTPS
                       ┌───────────────▼──────────────┐
                       │  FastAPI  (api/)             │
                       │  /api/v1/analyze             │
                       │  /api/v1/stress              │
                       │  /api/v1/recommend           │
                       │  /api/auth/*   (JWT)         │
                       └───────────────┬──────────────┘
                                       │
                       ┌───────────────▼──────────────┐
                       │  analysis_service            │
                       │  (orchestration)             │
                       └───────────────┬──────────────┘
         ┌──────────────┬──────────────┼───────────────┬───────────────┐
         │              │              │               │               │
 ┌───────▼──────┐┌──────▼──────┐┌──────▼──────┐┌───────▼──────┐┌───────▼──────┐
 │ data_service ││ correlation ││   stress    ││    risk /    ││recommendation│
 │  yfinance    ││ clustering  ││  service    ││diversification│    service   │
 │  cache+retry ││ Ward / SciPy││  Cholesky   ││ VaR CVaR ENB ││ FAISS search │
 └──────────────┘└─────────────┘└─────────────┘└──────────────┘└──────┬───────┘
                                                                      │
                                                       ┌──────────────▼───────┐
                                                       │  ai_service          │
                                                       │  RAG (FAISS +        │
                                                       │  MiniLM) → Groq LLM  │
                                                       │  explanation only    │
                                                       └──────────────────────┘
```
