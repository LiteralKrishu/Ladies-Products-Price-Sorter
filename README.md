# Project Plan: Ladies Product Price Sorter

## Project Title  
**Ladies Product Price Sorter** – An Intelligent Price Comparison Platform for Women’s Products in India.

## Objective  
Develop a web application that scrapes multiple e-commerce sites (Amazon, Flipkart, etc.), matches similar products, and displays the cheapest price for each item in a user-friendly interface.

---

## Phases & Deliverables

### Phase 1: Planning & Architecture ✅
- Define core use cases and MVP scope
- Finalize tech stack and tool selection
- Create repository and initialize code structure

**Deliverables:** 
- Project repository with directory structure
- Initial documentation (`README.md`)

---

### Phase 2: Web Scraping Modules ✅ 
- Write individual scrapers for:
  - Amazon
  - Flipkart
  - Ajio
  - Jiomart
  - Myntra
  - Nykaa
  - Snapdeal
- Implement retry and proxy support
- Extract: Title, Price, Discount, Rating, Delivery time, Stock Status, Image, Product Link

**Deliverables:**
- `/backend/scrapers/*.py` modules
- Unified product data schema

---

### Phase 3: Product Matching Engine
- Use NLP to associate same products across sites
- Build utilities to clean and normalize product names

**Deliverables:**
- `/backend/utils/match_products.py`
- Sample matched results with test cases

---

### Phase 4: Backend API Layer
- Create REST API endpoints using FastAPI:
  - `/search?q=product_name`
  - `/lowest?q=product_name`
- Integrate scrapers and matching engine

**Deliverables:**
- `/backend/main.py`
- JSON API responses tested via Postman or browser

---

### Phase 5: Frontend UI
- Design clean interface to:
  - Input product query
  - Display products in a sortable table/grid
  - Highlight the lowest price
- Add “Buy Now” buttons linking to product pages

**Deliverables:**
- `/frontend/index.html`, JS and CSS
- Working user interface

---

### Phase 6: Testing & Optimization
- Test full workflow end-to-end
- Add basic error handling and timeouts
- Optimize scraping for speed and accuracy
- Optional: Setup caching with Redis or local DB

**Deliverables:**
- Working MVP
- Sample test cases and performance logs

---

### Phase 7: Deployment & Documentation
- Deploy to Render, Vercel, or Heroku
- Finalize documentation (usage, setup)
- Add license and contribution guidelines

**Deliverables:**
- Live website URL
- Complete GitHub documentation

---

## Optional Enhancements (Post-MVP)
- Add user registration and product watchlist
- Email/SMS alerts for price drops
- Mobile-friendly or app version
- Support for more sites
- Real-time scraping scheduler via Celery or CRON
