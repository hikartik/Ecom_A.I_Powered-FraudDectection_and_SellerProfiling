# AI-Powered E-Commerce Marketplace

Welcome to the comprehensive **AI-Powered E-Commerce Marketplace**, a full-stack solution that empowers consumers, sellers, and administrators with seamless AI-driven tools for product discovery, listing validation, and marketplace oversight.

---

## 🚀 Product Overview

Our platform offers a unified marketplace experience where:

- **Consumers** browse products annotated with AI-generated trust indicators—image authenticity, description quality, and multimodal consistency.
- **Sellers** list new items through an intuitive interface that provides real-time AI feedback and quality scores before a listing goes live.
- **Administrators** oversee platform health via aggregated risk analytics and seller profiling, all built into the same product suite.

This end-to-end solution combines real-time inference, batch analysis, and graph-based modeling into a single, cohesive product.

---

## 🔧 Key Features

1. **Real-Time Listing Validation**

   - **Image Authenticity**: Detect manipulated or low-quality images using CLIP vision embeddings and a lightweight classification head.
   - **Description Quality**: Identify exaggeration, policy violations, or keyword stuffing via a fine-tuned BERT model.
   - **Multimodal Consistency**: Score alignment between visuals and text with CLIP multimodal embeddings.
   - **Unified Risk Score**: Aggregate vision, text, and consistency metrics through a weighted ensemble to generate a real-time risk indicator.

2. **Seller Onboarding & Feedback**

   - **Interactive Listing Form**: Image uploader, rich-text description editor, and live AI scoring dashboard.
   - **Quality Recommendations**: AI-driven suggestions to improve image quality and text clarity before publishing.
   - **Audit Trail**: Track historical listing revisions, AI score changes, and publication status.

3. **Batch Review Analysis & Seller Profiling**

   - **Review Semantics**: Generate sentence-level embeddings (SentenceTransformers) and sentiment scores (BERT) for each review.
   - **Coherence Score**: Compute consistency across multiple reviews using combined semantic similarity and sentiment agreement.
   - **Heterogeneous Graph Risk Engine**: Build a seller–product–review multimodal graph and apply a GAT-based GNN (PyTorch Geometric) to produce a comprehensive Seller Risk Score.

4. **Unified Administrative Insights**

   - **Aggregate Dashboards**: Searchable tables and charts for flagged listings, seller risk distribution, and marketplace trends.
   - **Actionable Alerts**: Automated notifications for high-risk listings and sellers requiring review.
   - **Data Export**: CSV/JSON downloads of risk reports and seller profiles.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn, Pydantic, MongoDB
- **Frontend**: React (Vite), Tailwind CSS, component-based UI
- **AI & ML**: PyTorch, PyTorch Geometric, CLIP, Hugging Face Transformers (BERT), SentenceTransformers
- **Storage & Media**: Cloudinary
- **Authentication**: JWT

---

## ⚙️ Deployment & Setup

1. **Clone & Install**

   ```bash
   git clone https://github.com/your-org/ai-commerce.git
   cd ai-commerce
   ```

2. **Backend**

   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   - Configure `.env` with `MONGO_URI`, `CLOUDINARY_*`, and `SECRET_KEY`.
   - Start API: `uvicorn app.main:app --reload --port 8000`

3. **Frontend**

   ```bash
   cd ../frontend
   npm install
   npm run dev  # http://localhost:3000
   ```

4. **Optional**: Seed sample data:

   ```bash
   cd backend
   python scripts/seed.py
   ```

---

## 📄 API Summary

**Users**

- `POST /users/register` – Register a new user (consumer, seller, or admin)
- `POST /users/login` – Authenticate and obtain JWT

**Products**

- `POST   /products/add` – Add a new product listing (seller)
- `GET    /products/my` – List all products created by the authenticated seller
- `GET    /products/` – Retrieve all product listings (consumers)

**Reviews**

- `POST /products/{product_id}/reviews/` – Post a review for a specific product
- `GET  /products/{product_id}/reviews/` – Get all reviews for a specific product

**Admin**

- `GET    /admin/sellers` – List all sellers
- `GET    /admin/sellers/{seller_id}` – Get details for a specific seller
- `GET    /admin/products` – List all products across the platform
- `PATCH  /admin/products/{product_id}` – Update product details (e.g., flag, amend scores)
- `DELETE /admin/products/{product_id}` – Delete a product listing
- `POST   /admin/sellers/{seller_id}/ban` – Ban a seller from the marketplace

---

## 🤝 Contributing

We welcome your contributions:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/xyz`).
3. Commit your changes (`git commit -m "feat: ..."`).
4. Push and submit a Pull Request.

Please follow code style guidelines and include tests for new features.

---

## 📄 License

MIT License. See `LICENSE` for details.

---

_Built with ❤️ by Team Titans_
