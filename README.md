# 🛒 Product Price Sorter

> 🛍️ Price comparison API for products in India.  
> Scrapes top e-commerce sites, matches similar products, and displays the best price.

![Build](https://img.shields.io/badge/build-MVP-informational?style=flat-square)
![Tech Stack](https://img.shields.io/badge/stack-FastAPI%2C%20Python-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## 🚀 Project Objective

**Product Price Sorter** is a price comparison tool tailored specifically for products in India.  
It enables users to **search** for a product, **compare prices** across platforms like Amazon, Flipkart, Myntra, Nykaa, etc.

---

## 🧱 Architecture & Workflow

1. **User Input** → Search Query  
2. **Backend Trigger** → Scrapes e-commerce platforms  
3. **Data Normalization** → Product Matching Engine  
4. **Response API** → Matched Products with Price Comparison  

---

## 📦 Tech Stack

| Layer       | Technology              |
|-------------|--------------------------|
| Backend     | Python, FastAPI          |
| Scraping    | `requests`, `playwright`, `lxml`, `fake_useragent`, `httpx` |
| Matching    | Sentence-Transformers, Fuzzy Matching |
| Deployment  | Docker / GitHub Actions / Prometheus |

---

## 🗂 Project Phases & Deliverables

### Phase 1: Planning & Architecture
- Define core features
- Setup GitHub repo & directory structure  
📁 Deliverables:  
`README.md`, `LICENSE`, base folder layout

---

### Phase 2: Web Scraping Modules

- Scrapers for:
  - Amazon
  - Flipkart
  - Ajio
  - Jiomart
  - Myntra
  - Nykaa
  - Snapdeal
- Data fields:
  - Title, Price, Discount, Rating, Delivery, Stock, Image, URL  
📁 Deliverables:  
`/backend/scrapers/*.py`, retry logic, user-agent rotation

---

### 🧠 Phase 3: Product Matching Engine

- Clean & normalize product titles  
- Match identical items across different sellers using NLP/heuristics  
📁 Deliverables:  
`/backend/utils/match_products.py`, test cases

---

### ⚙️ Phase 4: Backend API Layer

- Built with **FastAPI**  
- Key Endpoints:
  - `/search?q=product_name` → Raw results  
  - `/lowest?q=product_name` → Best match, lowest price  
📁 Deliverables:  
`/backend/main.py`, API testing via Postman

---

### 🔬 Phase 5: Testing & Optimization

- Full workflow testing (query → result)  
- Timeout handling, retries, invalid input support  
- Performance logging  
📁 Deliverables:  
Working MVP with logs, error states, test data

---

## 🧪 API Endpoint

### Product Search
`GET /api/search`

**Parameters**:
- `q` (required): Search query (e.g., "maybelline foundation")
- `platforms` (optional): Comma-separated platforms (e.g., "amazon,nykaa")
- `limit` (optional): Max results per platform (default: 5)

**Example**:
```bash
curl "http://localhost:8000/api/search?q=lakme+lips&platforms=amazon,myntra&limit=3"


