1. Create venv:
>python3 -m venv venv
>source venv/bin/activate

2. Install:
>pip install -r requirements.txt

3. Update .env:
>OPENAI_API_KEY="sk-..."

4. Run:
>uvicorn main:app --reload --port 8000
