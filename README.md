# KPB — POP Contract Generator

Dynamic PDF generator for the KPB Supports Solutions Pay-on-Performance Agreement.

## Folder Structure

```
contract_generator/
├── app.py                   # Flask backend
├── requirements.txt
├── README.md
└── templates/
    ├── form.html            # Frontend UI form
    └── contract.html        # Jinja2 contract template (PDF layout)
```

## Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **WeasyPrint** also requires system libraries:
> - **Ubuntu/Debian:** `sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0`
> - **macOS:** `brew install pango`
> - **Windows:** Install GTK3 runtime from https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

### 2. Run the server

```bash
python app.py
```

### 3. Open in browser

```
http://localhost:5000
```

## Dynamic Fields

| Field | Location in Contract |
|---|---|
| **Service Provider Name** | Opening para, Section 11 signature |
| **Agreement Date** | Opening paragraph |
| **Effective From Date** | Section 1 |
| **Commission %** | Section 3 & Section 4 |
| **Jurisdiction City** | Section 9 |
| **Provider Designation** | Section 11 signature block |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Render the form UI |
| `POST` | `/preview` | Preview contract in browser tab |
| `POST` | `/generate-pdf` | Generate and download PDF |

### POST `/generate-pdf` — Form fields

```
provider_name        string   e.g. "Samiksha Dubey"
provider_designation string   e.g. "Freelance Consultant"
agreement_date       date     YYYY-MM-DD format
effective_date       date     YYYY-MM-DD format
commission           string   e.g. "20"
city                 string   e.g. "Greater Noida"
```
