# Laptop Selection Decision Support System

A web-based Decision Support System (DSS) for laptop selection using the Analytical Hierarchy Process (AHP) algorithm, built with Django framework.

## Features

- **AHP Algorithm Implementation**: Complete implementation of the Analytical Hierarchy Process for multi-criteria decision making
- **Laptop Database**: Comprehensive database of 573 unique laptops with specifications (CPU, RAM, Price, SSD, HDD)
- **Interactive Search**: User-friendly interface for setting criteria priorities
- **Ranking Results**: Detailed ranking results with consistency ratio validation
- **Responsive Design**: Modern UI using AdminLTE template framework

## Dataset

The laptop database contains 573 unique laptop records processed from two datasets:

1. **laptopPrice.csv** (823 records) - Indian laptop market data
   - Source: [Kaggle - Laptop Price Prediction](https://www.kaggle.com/code/anubhavgoyal10/laptop-price-prediction/input)
   - Prices converted from Indian Rupees to Indonesian Rupiah (1 INR = 200 IDR)

2. **laptop_price.csv** (1,303 records) - European laptop market data  
   - Source: [Kaggle - Laptop Price Dataset](https://www.kaggle.com/datasets/muhammetvarl/laptop-price/)
   - Prices converted from Euros to Indonesian Rupiah (1 EUR = 16,000 IDR)

**Total processed records**: 2,126 → **573 unique laptops** after deduplication

## Criteria Evaluation

The system evaluates laptops based on five key criteria:
- **CPU Performance**: Processor specifications and performance metrics
- **RAM Capacity**: Memory specifications
- **Price**: Cost considerations
- **SSD Storage**: Solid State Drive capacity
- **HDD Storage**: Hard Disk Drive capacity

## Technology Stack

- **Backend**: Django 3.2.8 (Python 3.8+)
- **Database**: MySQL 8.0
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 4, AdminLTE
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Docker and Docker Compose (optional)

## Installation

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd laptop-determination-app
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your database credentials
   ```

5. **Set up MySQL database**
   - Create a MySQL database named `db-spk`
   - Update database credentials in `.env` file

6. **Run migrations**
   ```bash
   cd laptop_determination
   python manage.py migrate
   ```

7. **Load sample data** (if available)
   ```bash
   python manage.py loaddata fixtures/sample_data.json
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Docker Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd laptop-determination-app
   ```

2. **Start services with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Web application: http://localhost:8000
   - MySQL database: localhost:3306

## Usage

1. **View Alternatives**: Browse all available laptops in the database
2. **Search Interface**: 
   - Select preferred laptop brand (or "All" for all brands)
   - Set priority levels for each criteria (1-5, where 1 is most important)
3. **Results**: View detailed AHP analysis and ranking results

## Project Structure

```
laptop-determination-app/
├── laptop_determination/          # Main project directory
│   ├── config/                   # Django project settings
│   │   ├── settings.py          # Main configuration
│   │   ├── urls.py              # URL routing
│   │   └── views.py             # Project-level views
│   ├── laptop_selection/        # Main Django app
│   │   ├── models.py            # Database models
│   │   ├── views.py             # Business logic & AHP algorithm
│   │   ├── urls.py              # App URL patterns
│   │   ├── templates/           # HTML templates
│   │   └── templatetags/        # Custom template filters
│   ├── static/                  # Static assets (CSS, JS, images)
│   ├── templates/               # Base templates
│   └── manage.py               # Django management script
├── requirements.txt             # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # This file
```

## API Endpoints

- `/` - Home page
- `/laptop-selection/alternatives/` - View all laptop alternatives
- `/laptop-selection/search/` - Search interface
- `/laptop-selection/results/` - AHP ranking results

## AHP Algorithm Details

The system implements a complete AHP workflow:

1. **Pairwise Comparison**: Creates comparison matrices for alternatives and criteria
2. **Weight Calculation**: Computes normalized weights using eigenvalue method
3. **Consistency Check**: Validates consistency ratio (CR < 0.1)
4. **Final Ranking**: Combines criteria weights with alternative weights

## Database Schema

### Laptops Table
- `id_laptop`: Primary key
- `company`: Laptop manufacturer
- `product`: Product name
- `cpu`: CPU performance score
- `ram`: RAM capacity (GB)
- `price`: Price in local currency
- `hdd`: HDD capacity (GB)
- `ssd`: SSD capacity (GB)

## Development

### Running Tests
```bash
cd laptop_determination
python manage.py test
```

### Code Style
The project follows PEP 8 guidelines. Use a code formatter like `black` for consistent formatting.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Django framework for the web framework
- AdminLTE for the UI template
- AHP methodology for decision support algorithms