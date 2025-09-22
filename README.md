# Toy Project

Đây chỉ là một đồ chơi, đừng có đánh giá người khác qua đồ chơi!

This is just a toy, don't judge a person by his toys!

## Installation

1. Clone the repository

2. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1 # Windows/PowerShell
.venv\Scripts\activate.bat # Windows/CMD
source .venv/bin/activate  # Linux
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the development server:
```bash
uvicorn app.main:app --reload
```

Access the application at `http://localhost:8000`