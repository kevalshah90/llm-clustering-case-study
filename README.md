# Overview
In this assignment you will build a prototype of a cluster analysis tool to navigate financial statements.

Each company has a unique CIK (Central Index Key) that is used to identify it in the data. The CIK is a 10 digit number, and is the prefix of the file name for each company's 10-K report.

There are three main tasks in this assignment:
* To construct a CIK -> Company Name mapping from the provided data.
* To summarize each company's report into a few sentences.
* To cluster the companies into similar groups based on their financial statements.

The goal of this assignment is to demonstrate your ability to build a data pipeline to process unstructured data, and to use that data to build a simple clustering and summarizing tool whose output could be built into a more complex application. What we expect you to build are proofs of concept, and not production-ready models.

If you decide to use a paid API to solve the exercise, we will reimburse you for usage up to $10.

## Instructions
1. Clone (**please, don't fork!**) this repository and create a new branch for your development work
1. Create your implementation following the [Specification](#specification) below
1. Add instructions on how to run your implementation to the [Getting Started](#getting-started) section.
1. In the [follow-up questions](#follow-up-questions) section below, respond inline to each of the questions.
1. Commit your implementation and answers to a new repo in your personal GH and give `@avyfain` access to the repo.

**Guidelines:**
- Do not spend longer than four hours on your implementation, a perfect implementation is not required or expected. Please move on to the [follow-up questions](#follow-up-questions) after that.
- You may use any language or tools you like to complete this assignment. You can use any libraries or frameworks you like, including any existing clustering libraries. You can use any pre-trained language models you like.
- Ask questions if you have them. The business problem is intentionally vague, so you will need to make some assumptions. Document your assumptions in your code and in the follow-up questions.
- It's fine to use Google or StackOverflow to look up syntax or documentation. If you use ChatGPT or similar tools, please share the prompts you used in the follow-up questions.

## Exercise Data

You can find a zip file with the required data in [this HuggingFace repo](https://huggingface.co/datasets/inscopehq/SEC-10K).

In the provided data zip file, you will find over 3000+ recent 10-K reports from publicly traded companies. These reports are HTML containing the financial statements for each company.

If you have a CIK, you can use it to access the corresponding company's data in the SEC's EDGAR database. For example, the CIK for Apple Inc. is 0000320193. You can find Apple's reports here: https://www.sec.gov/edgar/browse/?CIK=000320193.

We do not expect you to download any additional data from the SEC's database, but you can find the full documentation for the EDGAR database here: https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm

## Specification

We expect you to build the following functionality:
  - [ ] You will filter down the dataset to cluster companies that are in the S&P 500 index. You can find a recent list of CIKs for companies in the S&P 500 in the `SP500.txt` file.
  - [ ] You will create a script that given a directory with report files can produce a `CIK -> Company Name` mapping in the shape of a CSV file with two columns: CIK and Company Name. Each row in this file will represent each file in the provided data. (hint: you don't need to throw an LLM at this problem)
  - [ ] You will run your mapping script on the provided data, and include it in your response.
  - [ ] You will write a data pipeline to process the provided HTML into an intermediate representation that can be used for clustering. One of the features in your intermediate representation should be a 1-paragraph summary of the report. You can use any pre-trained language model you like to generate the summary.
  - [ ] You will use your pipeline to assign every company in the dataset into similar groups based on their financial statements.
  - [ ] You will provide a Jupyter Notebook, a Streamlit app, or equivalent for users to inspect and interact with the results of your clustering and summarization. The visualization should allow the user to select a company and show other similar companies in the same cluster.


## Getting Started

The `inscope-take-home.ipynb` is the primary file that references the data files and performs read, write, cluster and summarize operations. The notebook is divided into roughly 3 sections, 1) Mapping CIK-Company task 2) Summarization 3) Clustering. 

Set the working directory as the directory that includes the `inscope-take-home.ipynb` file. The `.html` 10k files are saved in the `\data` folder and read from there.

The intermediary files are saved in the working directory and can be found here in this HF repo because of the large file limits: https://huggingface.co/datasets/keval-sha/inscope-case-study

Add the open AI API key: `os.environ['OPENAI_API_KEY'] = "xxx"`

You will run through the script and save a final dataframe in the `/App` folder. From this folder, you can launch the streamlit App by running command `streamlit run app.py`. 

## Follow-Up Questions

  1. Describe which task you found most difficult in the implementation, and why.

     > Parsing text from the `.html` files and subsequently generating summaries of the document text was challenging. Given the layout of the document, different structure containing disclaimers, table of content, it was tricky to extract clean text / information that we are interested in. 

     > Upon parsing the html, the document text is fairly length and exceeds the context window allowed LLMs for summarization. We are not able to pass the complete text for summarization and need to experiment with different chunking strategies, extractive, abstractive outputs and so on.
     
  2. What led you to choose the libraries or frameworks you used in your implementation?

     > I ended up choosing `langchain's chatOpenAI` module given it's simplicity to to work with openAI models. `AWS SageMaker` for compute and processing power. `gpt-3.5-turbo-16k` for larger context window. `FAISS` for vector storage and search functionality and support for clustering algorithm.
     
  3. How did you evaluate whether the clusters and summaries created by your system were good or not?

     > In the absence of ground-truth data, one way to evaluate is randomly sample companies from the list and compare the system-generated summaries against human-generated ones. 

     > For clustering, I compared the companies within each cluster based on their industry / sector, financial performance, regulations and so on. For example; cluster #3 includes financial companies like Morgan Stanley, BlackRock, PayPal, Bank of America, Goldman Sachs and JPMorgan Chase.
     
  4. If there were no time or budget restrictions for this exercise, what improvements would you make in the following areas:
     
      > Implementation
    
       I'd spend more time dealing with unstructured data and extracting relevant text from the 10k's. I'd experiment with different chunking strategies and summarization methods based on the use-case. For example, chunk based on sections in the report or each paragraph? Generate summaries of the each chunk of the document and then combine them for a more cohesive summary. Try out a few different models with larger context window. 
        
        Try an domain specific model or Fine-tune one on financial data and utilize that for generating summaries. Example, https://huggingface.co/ProsusAI/finbert.   
    
      > User Experience
    
       I'd work on generating more meaningful clusters. The improvements here would be from extracting relevant texts, generating embeddings and then trying out different clustering / similarity algorithms. In the streamlit App UI, instead of showing all the companies in the same cluster as the selected company, I'd limit the list to top 5 or 10 companies for better UX. 
    
      > Data Quality
    
       Improvements in how we process unstructured textual data. Using Beautiful soup to parse text, identify and clean up irrelevant texts, piping in factual data such as financials, sector, market cap and so on and using them for either feature engineering for classical ML or into the embeddings for LLMs. 
       
  5. If you built this using classic ML models, how would approach it if you had to build it with LLMs? Similarly, if you used LLMs, what are some things you would try if you had to build it with classic ML models?

     > For classical ML model, I'd attempt to process unstructured text into structured data by extracting relevant data points for each company for feature engineering. Data points could include financial information such as revenue, profits, expenses, operational costs, assets, liabilities, employees, market / sector, competition and so on. I'd then train an unsupervised clustering algorithm based on features.
     
  6. If you had to build this as part of a production system, providing an inference API for previously unseen reports, how would you do it? What would you change in your implementation?

     > For production systems, I'd implement some the improvements around data quality, UX and evaluations outlined above. Once we have satisfactory results, I'd productionize using a service like `AWS SageMaker` for deploying the model to production and creating an inference endpoint. I'd consider different inference options (batch, real-time, async), costs, latency, throughput, other metrics for running a production system. I'd ensure proper configuration to manage LLM pipelines. This includes setup for logs, tracking model versioning, data changes. Depending on the usage and for scalability, I'd consider using CI/CD tools, kubernetes. 

     > For model performance, I'd employ model evaluation metrics for summarization tasks such as BLEU, Perplexity to monitor model performance and identify potential biases or drift. 
     

ChatGPT / Bard helper Prompts: 

1. LLM model evaluation metrics for summarization tasks
2. How to deal with BadRequestError: Error code: 400 - {'error': {'message': "This model's maximum context length is 16385 tokens. However, your messages resulted in 16412 tokens. Please reduce the length of the messages.", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}


# Evaluation Criteria

You will be evaluated out of a total of 50 points based on the following criteria.

  - Learning Exercise (30 points total)
    - **Functionality (20 points)**: is the requested functionality implemented as described?
    - **Code Quality (10 points)**: is the code well structured and easily read?
    - **Bonus (3 maximum)**: bonus points are awarded for anything that goes above and beyond the items in the specification.  For example, additional .
  - Follow Up Questions (20 points total)
    - Question 1 (2 points)
    - Question 2 (2 points)
    - Question 3 (3 points)
    - Question 4 (3 points)
    - Question 5 (5 points)
    - Question 6 (5 points)
