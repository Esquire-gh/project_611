# Amazon Review Summarization Tool

---

## Project Scope
This project aims to create a tool that simplifies understanding Amazon product reviews by summarizing them into clear, topic-based insights. As Amazon reviews can be overwhelming due to their volume and detail, the tool will help users by scraping product information and reviews from Amazon and then summarizing these reviews by different topics using machine learning. The goal is to simplify shopping by giving users straightforward summaries of what people say about a product rather than just relying on star ratings.

---

## Architecture and Environment

### Architecture
- **Data Collection**: Utilize the Unwrangle Amazon Scraping API to extract product details and reviews.
- **NLP Pipeline**: Conduct aspect-based sentiment analysis using Apache Spark NLP, leveraging pretrained models.
- **Frontend & Backend**: Integrate the processing pipeline with a Django-based web application.

### Environment
- **Development Tools**:
  - Apache Spark NLP.
  - Git for version control.
  - Docker for containerization.
- **Libraries and Frameworks**:
  - Apache Spark ML for machine learning tasks.
  - Django for application development.
- **Pretrained Models**:
  - `glove_6B_300` for word embeddings.
  - `NerDLModel` for named entity recognition.
  - `tfhub_use` for universal sentence encoding.
  - `sentimentdl_use_imdb` for sentiment analysis.

---

## Methodology

### Data Collection
- **Unwrangle Amazon Scraping API**: Fetch product data and customer reviews directly from Amazon.

### Aspect-Based Sentiment Analysis
Aspect-based sentiment analysis examines specific aspects (e.g., quality, price) mentioned in customer reviews and determines the sentiment (positive, negative, or neutral) associated with each aspect.

#### Example:
- **Customer Review**: "The battery life is excellent, but the screen quality is poor."
- **Analysis**:
  - Aspect: *Battery life*, Sentiment: *Positive*
  - Aspect: *Screen quality*, Sentiment: *Negative*

Pipeline Components:
- Pretrained Models:
  - `glove_6B_300` for extracting word embeddings.
  - `NerDLModel` for recognizing aspects in text.
  - `sentimentdl_use_imdb` for classifying sentiment.

[Aspect Based Sentiment Analysis Pipeline![](https://app.eraser.io/workspace/WZ2JNt9iwIseKceK3jS8/preview?elements=da9_2yxJPNu1PyKpYVGD5Q&type=embed)](https://app.eraser.io/workspace/WZ2JNt9iwIseKceK3jS8?elements=da9_2yxJPNu1PyKpYVGD5Q)

---

### Topic Modeling
- **Objective**: Group customer reviews into high-level topics for better insights.
- **Technique**: Latent Dirichlet Allocation (LDA), which clusters reviews into topics based on word frequency and co-occurrence patterns.

#### Example:
- **Topics**:
  - *Battery Performance*: 75% Positive, 25% Negative
  - *Build Quality*: 60% Positive, 40% Negative

[LDA Topic Modelling Process![](https://app.eraser.io/workspace/WZ2JNt9iwIseKceK3jS8/preview?elements=9JZJPgvY0UL-AETv7Ost3g&type=embed)](https://app.eraser.io/workspace/WZ2JNt9iwIseKceK3jS8?elements=9JZJPgvY0UL-AETv7Ost3g)

---

### Application Workflow
The application flow combines data scraping, sentiment analysis, topic modeling, and user-facing results.  

[Application flowchart![](https://app.eraser.io/workspace/WZ2JNt9iwIseKceK3jS8/preview?elements=HAq16rAkGPGWBo91NeaW9w&type=embed)](https://app.eraser.io/workspace/WZ2JNt9iwIseKceK3jS8?elements=HAq16rAkGPGWBo91NeaW9w)
---

## Challenges
1. **Amazon Review Limitations**:
   - Amazon blocks access to the customer reviews page for logged-in users, making it difficult to scrape data.
2. **Topic Modeling Issues**:
   - LDA topics lacked meaningful labels, necessitating the use of OpenAI for better topic naming.
3. **Aspect Sentiment Integration**:
   - Creating concise, sentiment-based summaries from reviews was challenging.

---

## Improvements
- Refine the sentiment distribution for each topic to include only one dominant sentiment (e.g., purely positive or negative).
- Enhance topic modeling to produce more intuitive and actionable insights without external tools like OpenAI.
- Focus on scraping directly from the customer reviews page instead of the product page.

---

## How to Run the Application
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Esquire-gh/project_611.git
2. **Build docker images**:
   ```bash
   docker compose up --build

---

## User Interface
![Product Url from amazon](/docs_images/Shot1.png)
![Paste Product Url](/docs_images/Shot2.png)
![Get output](/docs_images/Shot3.png)