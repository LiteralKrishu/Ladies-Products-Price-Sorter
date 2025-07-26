# 💄 Ladies Product Price Sorter

> 🛍️ An intelligent price comparison platform for women’s products in India.  
> Scrapes top e-commerce sites, matches similar products, and displays the best price in real-time.

![Build](https://img.shields.io/badge/build-MVP-informational?style=flat-square)
![Tech Stack](https://img.shields.io/badge/stack-FastAPI%2C%20Python-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## 🚀 Project Objective

**Ladies Product Price Sorter** is a smart price comparison tool tailored specifically for fashion and cosmetic products for women in India.  
It enables users to **search** for a product, **compare prices** across platforms like Amazon, Flipkart, Myntra, Nykaa, etc., and **redirect** to the best deal with a click.

---

## 🧱 Architecture & Workflow

1. **User Input** → Search Query  
2. **Backend Trigger** → Scrapes e-commerce platforms  
3. **Data Normalization** → Product Matching Engine  
4. **Response API** → Matched Products with Price Comparison  
5. **Frontend UI** → Interactive sortable display  

---

## 📦 Tech Stack

| Layer       | Technology              |
|-------------|--------------------------|
| Frontend    | HTML, CSS, JavaScript    |
| Backend     | Python, FastAPI          |
| Scraping    | `requests`, `selenium`, `lxml`, `fake_useragent`, `httpx` |
| Matching    | NLP / Regex / String Similarity |
| Deployment  | Vercel / Render / Heroku |

---

## 🗂 Project Phases & Deliverables

### ✅ Phase 1: Planning & Architecture
- Define core features
- Setup GitHub repo & directory structure  
📁 Deliverables:  
`README.md`, `LICENSE`, base folder layout

---

### ✅ Phase 2: Web Scraping Modules

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

### 🎨 Phase 5: Frontend UI

- Clean, responsive interface  
- Search bar → Results in card/grid layout  
- Price comparison with highlights  
- "Buy Now" button opens product in new tab  
📁 Deliverables:  
`/frontend/index.html`, `main.js`, `styles.css`

---

### 🔬 Phase 6: Testing & Optimization

- Full workflow testing (query → result)  
- Timeout handling, retries, invalid input support  
- Performance logging  
📁 Deliverables:  
Working MVP with logs, error states, test data

---

### 🚢 Phase 7: Deployment & Docs

- Deploy full-stack project  
- Setup CORS, domain routing  
- Write final documentation  
📁 Deliverables:  
Live link, `README.md`, contribution guide, `requirements.txt`

---

## 🌟 Optional Enhancements (Post-MVP)

- 🔔 **Alerts**: Price drop SMS/Email alerts  
- 📲 **Mobile-first UI**  
- 💼 **User Dashboard** with history  
- 🕒 **Scheduler**: Periodic scraping via Celery/CRON  
- 📊 **Analytics**: Product trends, price patterns  
- 📈 **Historical Graphs** (price over time)

---

## 🧪 Sample API Response

```json
[
  {
    "title": "Maybelline Fit Me Foundation - 120 Classic Ivory",
    "price": 449,
    "discount": "10%",
    "rating": 4.4,
    "platform": "Amazon",
    "image_url": "https://...",
    "product_link": "https://..."
  },
  ...
]
