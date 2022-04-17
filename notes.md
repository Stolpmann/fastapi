Create venv in project Directory

    virtualenv <name>
    
Activate venv

    source venv/bin/activate

Deactivate venv

    deactivate

Install Dependencies

    pip install fastapi[all]

Start Server

    uvicorn main:app --reload
    
