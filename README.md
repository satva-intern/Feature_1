# AI-Powered Chart Generator

A Streamlit app that turns your CSV data and natural language prompts into beautiful, AI-generated charts.

## Features

- Upload any CSV file
- Describe your desired chart in plain English
- Groq LLM generates Python code for the chart
- Secure, sandboxed code execution (Plotly/Matplotlib)
- Interactive chart display
- Edit and re-run generated code
- Model selection for speed/accuracy tradeoff

## Usage

1. Clone this repo and install requirements:
    ```
    pip install -r requirements.txt
    ```

2. Run the app:
    ```
    streamlit run app.py
    ```

3. Enter your [Groq API key](https://console.groq.com/keys) in the sidebar.

4. Upload your CSV file.

5. (Current) App samples 20 random rows for context.  
   *(Future: Will use a vector database for large datasets and smarter context retrieval.)*

6. Enter your chart description (e.g., "Show a bar chart of sales by region").

7. Click **Generate Chart**.

8. Review, edit, and re-run the generated code as needed.

## Security

- All AI-generated code is executed in a restricted environment.
- Only safe built-ins and whitelisted libraries are available.
- No file system or network access.

## Model Selection

- **llama-3.3-70b-versatile:** Best for complex queries.
- **llama-3.1-8b-instant:** Fastest for simple charts.
- **gemma2-9b-it:** Balanced.

Choose the model that fits your needs in the sidebar.

## Advanced (Planned)

- **Vector Database Integration:**  
  For large datasets, will embed and store your data in a vector DB, retrieving relevant rows for each prompt.

## Contributing

Pull requests welcome! Please open an issue to discuss your ideas.

## License

MIT

## Credits

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Groq](https://groq.com/)
