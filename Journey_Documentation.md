# Building an AI Chart Generator: Our Story & Technical Insights

---

## 🌱 The Journey: Why and How

It all started with a simple frustration: creating charts from data always felt harder than it should be. What if you could just upload your CSV and *describe* the chart you want, and the app would build it for you? That vision led to this project.

---

## 🏗️ Our Approach: Making Charting Effortless

We wanted users to:
- Upload a CSV file
- Describe their desired chart in plain English
- Instantly get a ready-to-use visualization

**How did we do it?**
- **Streamlit** for the web interface
- **Groq LLMs** (like Llama-3 and Gemma) to turn text into chart code
- **Plotly/Matplotlib** for rendering charts
- **Python’s `exec()`** to run the generated code

---

## ⚡ Prototyping Fast: Why 20 Random Rows?

During early development, we realized:
- Sending the *whole* dataset to the AI was slow and sometimes unnecessary
- Privacy matters—less data sent means less risk
- Quick feedback is key for a good user experience

**So, we decided to sample 20 random rows** from the uploaded CSV for each chart request. This made the app snappy, safe, and perfect for prototyping.

---

## 🤖 Model Quirks: Not All AIs Are Created Equal

One challenge: not every AI model is equally reliable for code generation.

- Some models (like Qwen) sometimes returned explanations or thoughts instead of just the code we needed.
    - Example:  
      *"First, import pandas. Then create a bar chart..."*  
      instead of  
      `fig = px.bar(sample_data, x='Region', y='Sales')`
- We solved this by:
    - Writing very clear prompts: *"Return only Python code. No explanations."*
    - Preferring models like **Llama-3-70B** and **Gemma** for their consistency.

---

## 🛡️ Safety First: Running Code Securely

Letting an AI write code that runs on your computer is risky!  
We needed to make sure nothing dangerous could happen.

**Our solution: Restricted Globals**
- Only allow access to safe libraries (`pandas`, `numpy`, `plotly`, `matplotlib`)
- Only expose the sampled data (`sample_data`)
- Block dangerous functions (like `open`, `os`, `import`, etc.)

This means:
- ✅ The AI can create charts from your data
- ❌ The AI cannot access your files, the internet, or your system

---

## 🚀 Scaling Up: How Vector Databases Can Help

Sampling 20 rows is great for quick demos, but what about *huge* datasets?  
That’s where **vector databases** come in.

### **How Vector Databases Work**

- **What is it?**  
  A vector database stores data as *vectors* (lists of numbers) that capture the meaning or features of your data (like text, images, or rows from your CSV)[1][3][5][7].
- **Why use it?**  
  Instead of searching for exact matches, vector databases find *similar* data using mathematical distance (like “find me rows most similar to this question”)[3][5][7].
- **How does it help here?**  
  For large datasets, we could:
    - Convert each row to a vector (using embeddings)
    - Store these vectors in a vector database (like Pinecone, Weaviate, or ChromaDB)
    - When a user asks for a chart, retrieve the most relevant rows (not just random ones)
    - Send those to the AI for chart generation

This approach is **faster**, **smarter**, and **scales** to millions of rows.

---

## 🔗 Further Reading: Learn More About Vector Databases

| Title & Description | Link |
|---------------------|------|
| An Introduction to Vector Databases For Machine Learning (DataCamp) | [Read here](https://www.datacamp.com/tutorial/introduction-to-vector-databases-for-machine-learning) |
| An Introduction to Vector Databases for Beginners (Xomnia) | [Read here](https://xomnia.com/post/an-introduction-to-vector-databases-for-beginners/) |
| What is a Vector Database & How Does it Work? (Pinecone) | [Read here](https://www.pinecone.io/learn/vector-database/) |
| A Gentle Introduction to Vector Databases (Weaviate) | [Read here](https://weaviate.io/blog/what-is-a-vector-database) |
| Complete Tutorial on Vector Database (YouTube, Entbappy) | [Watch here](https://www.youtube.com/watch?v=8KrTO9bS91s) |

---

## 💡 Lessons Learned

- **Clear instructions for AI models** make a huge difference.
- **Sampling data** is great for prototyping, but vector search is the future for scale.
- **Security is non-negotiable** when running generated code.

---

**Thanks for reading our journey! If you want to dig deeper into vector databases or chart automation, check out the links above. Happy building!**
