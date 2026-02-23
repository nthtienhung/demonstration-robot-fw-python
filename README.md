# Robot Framework Test Automation Project

A test automation framework using Robot Framework with Page Object Model (POM), custom libraries for visual validation, test data generation, and enhanced reporting.

## Quick Start

```bash
# Install Python 3.9+ (if not installed)
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run all tests
robot --outputdir robot-tests/results robot-tests/test-cases/

# Run specific test suites
robot --include api robot-tests/test-cases/
robot --include smoke robot-tests/test-cases/
robot --include visual robot-tests/test-cases/

# View report
open robot-tests/results/report.html
```

## Project Structure

```
demonstration-robot-fw-python/
├── pages/                      # Page Object Model (XPath locators)
├── api/                        # API test helpers
├── custom-libraries/           # Custom libraries
│   ├── TestDataGenerator/      # Test data generation (Faker)
│   ├── VisualValidator/        # Visual AI validation (OpenCV)
│   └── CustomReporter/         # Enhanced reporting
├── robot-tests/
│   ├── test-cases/
│   │   ├── ui/smoke/           # UI smoke tests
│   │   ├── ui/visual/          # Visual layout tests
│   │   └── api/                # API tests
│   └── results/                # Test reports
├── config/config.yaml          # Configuration
├── requirements.txt
```

## Features

- **Page Object Model** - Clean separation between tests and page interactions
- **XPath-Only Locators** - Consistent element identification
- **Custom Libraries** - TestDataGenerator, VisualValidator, CustomReporter
- **UI + API Testing** - Complete test coverage
- **10 Test Cases** - All passing (4 API + 4 UI + 2 Visual)

## Test Results

| Suite | Tests | Status |
|-------|-------|--------|
| API | 4 | ✅ Passing |
| UI Smoke | 4 | ✅ Passing |
| Visual | 2 | ✅ Passing |

## Target Websites

- **UI**: https://the-internet.herokuapp.com
- **API**: https://jsonplaceholder.typicode.com

## Configuration

Edit `config/config.yaml` to customize:

```yaml
ui:
  base_url: "https://the-internet.herokuapp.com"
  browser: "chrome"
  headless: true

api:
  base_url: "https://jsonplaceholder.typicode.com"

visual:
  threshold: 0.95
```

## Requirements

- Python 3.9+
- Chrome or Firefox
- See `requirements.txt` for full list

## Documentation

- **config/config.yaml** - Configuration reference
- **robot-tests/results/report.html** - Test execution report

## License

Educational and demonstration purposes.
