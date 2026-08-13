# LLM-query — Text-to-SQL Assistant

An interactive command-line assistant that turns plain-English questions into SQLite queries using the Google Gemini API, runs them against a local database, and prints the results.

Ask *"Which customers from Greece placed a completed order?"* and get back both the generated SQL and the actual rows from the database.

## How it works

1. Your question is sent to `gemini-2.5-flash` together with a hardcoded description of the database schema.
2. The model is constrained by a Pydantic schema (`response_schema=SQLResponse`), so it must return structured JSON containing an `sql_query` and a short `explanation` — never free-form text.
3. The generated query is executed against `ecommerce.db` and the results are printed as a table.

Temperature is fixed at `0.0` for deterministic output. The system prompt instructs the model to produce `SELECT` statements only.

## Requirements

- Python 3.10+
- A Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

## Setup

Clone the repository and install the dependencies:

```bash
git clone https://github.com/michalisklk/LLM-query.git
cd LLM-query
pip install -r requirements.txt
```

Create a `.env` file in the project root (see `.env.example`) and add your key:

```
API_KEY=your_gemini_api_key_here
```

Build the sample database:

```bash
python create_db.py
```

## Usage

```bash
python app.py
```

Then type your questions at the prompt. Type `exit`, `quit` or `q` to leave.

```
Ask a question about your DB > How many orders were placed by each country?

AI Generated SQL : SELECT u.country, COUNT(o.order_id) FROM users u
                   JOIN orders o ON u.user_id = o.user_id GROUP BY u.country
Explanation      : Counts the number of orders grouped by the customer's country.

Query Results from DB:
   country  COUNT(o.order_id)
   Greece  3
   Portugal  1
   UK  1
   USA  1
```

Other questions to try:

- What is the total revenue from completed orders?
- Which product category sold the most items?
- List all users who signed up in March 2024.
- Show me the highest-value order and who placed it.

## Database

`create_db.py` creates and seeds three related tables:

| Table | Contents |
|---|---|
| `users` | Customer details — name, email, signup date, country |
| `orders` | Orders linked to users — date, total amount, status |
| `order_items` | Line items linked to orders — product, category, price, quantity |

Re-running `create_db.py` drops and recreates everything from the same fixed sample data.

## Project structure

```
app.py            Main CLI loop — prompt, LLM call, query execution
create_db.py      Creates and seeds ecommerce.db
requirements.txt  Python dependencies
.env.example      Template for the required environment variable
```

## Notes and limitations

- The schema is described twice: as `DB_SCHEMA` in `app.py` and as `CREATE TABLE` statements in `create_db.py`. Nothing keeps them in sync — if you change the tables, update both.
- Restricting the model to `SELECT` queries is a prompt-level convention, not an enforced guard. `execute_sql` will run whatever SQL string it is given. Do not point this at a database you care about without adding a real check.
- `ecommerce.db` is gitignored. It is generated locally by `create_db.py`, so there is no need to track it.

## License

MIT