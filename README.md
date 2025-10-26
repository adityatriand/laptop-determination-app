# Laptop Selection Decision Support System

A web-based Decision Support System (DSS) for laptop selection using the Analytical Hierarchy Process (AHP) algorithm, built with Django framework and containerized with Docker.

## Features

- **AHP Algorithm Implementation**: Complete implementation of the Analytical Hierarchy Process for multi-criteria decision making
- **Laptop Database**: Comprehensive database of 573 unique laptops with specifications (CPU, RAM, Price, SSD, HDD)
- **Interactive Search**: User-friendly interface for setting criteria priorities with real-time validation
- **Ranking Results**: Detailed ranking results with consistency ratio validation and calculation details
- **Responsive Design**: Modern UI using AdminLTE template framework
- **Docker Support**: Fully containerized application with Docker Compose
- **Environment Configuration**: Secure environment variable management with `.env` files

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
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 4, AdminLTE
- **Containerization**: Docker & Docker Compose
- **Environment Management**: python-decouple for secure configuration
- **Data Processing**: Pandas for dataset processing and cleaning

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
   - Create a MySQL database named `db_spk`
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

### Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd laptop-determination-app
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file if needed (default values work for Docker)
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Web application: http://localhost:8000
   - MySQL database: localhost:3306
   - Database will be automatically initialized with 573 laptop records

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
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # URL routing
│   ├── views.py                 # Project-level views
│   ├── wsgi.py                  # WSGI configuration
│   ├── asgi.py                  # ASGI configuration
│   ├── laptop_selection/        # Main Django app
│   │   ├── models.py            # Database models
│   │   ├── views.py             # Business logic & AHP algorithm
│   │   ├── urls.py              # App URL patterns
│   │   ├── templates/           # HTML templates
│   │   └── templatetags/        # Custom template filters
│   ├── static/                  # Static assets (CSS, JS, images)
│   ├── templates/               # Base templates
│   └── manage.py               # Django management script
├── db_init/                     # Database initialization
│   └── init.sql                # SQL script with 573 laptop records
├── dataset/                     # Dataset processing (development only)
│   ├── laptopPrice.csv         # Indian laptop data
│   ├── laptop_price.csv        # European laptop data
│   └── processed_laptops.sql   # Processed SQL data
├── requirements.txt             # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## API Endpoints

- `/` - Home page
- `/laptop-selection/alternatives/` - View all laptop alternatives
- `/laptop-selection/search/` - Search interface
- `/laptop-selection/results/` - AHP ranking results

## Recent Improvements

### Code Refactoring
- **English Naming**: All variables, functions, and file names converted from Indonesian to English
- **Clean Architecture**: Removed redundant `config/` folder, moved files to proper Django structure
- **Modern JavaScript**: Refactored JavaScript code to use ES6+ features and clean architecture
- **Template Updates**: All HTML templates updated with consistent English naming conventions

### Environment & Configuration
- **Environment Variables**: Secure configuration management with `.env` files
- **Docker Optimization**: Streamlined Docker setup with proper environment variable handling
- **Database Initialization**: Automated database setup with 573 laptop records

### Code Quality
- **Clean Code**: Improved code readability and maintainability
- **Error Handling**: Enhanced error handling and validation
- **Template Filters**: Robust template filters with proper error handling
- **AHP Algorithm**: Fixed division by zero errors and improved algorithm robustness

## AHP Algorithm Details

The system implements a complete AHP workflow:

1. **Pairwise Comparison**: Creates comparison matrices for alternatives and criteria
2. **Weight Calculation**: Computes normalized weights using eigenvalue method
3. **Consistency Check**: Validates consistency ratio (CR < 0.1)
4. **Final Ranking**: Combines criteria weights with alternative weights

## Environment Variables

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```bash
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DATABASE_NAME=db_spk
DATABASE_USER=django_user
DATABASE_PASSWORD=django_password
DATABASE_HOST=db
DATABASE_PORT=3306

# MySQL Root Password
MYSQL_ROOT_PASSWORD=rootpassword
```

## Database Schema

### Laptops Table
- `id_laptop`: Primary key
- `company`: Laptop manufacturer
- `product`: Product name
- `cpu`: CPU performance score
- `ram`: RAM capacity (GB)
- `price`: Price in Indonesian Rupiah (IDR)
- `hdd`: HDD capacity (GB)
- `ssd`: SSD capacity (GB)

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running and accessible
   - Check database credentials in `.env` file
   - For Docker: Ensure containers are running with `docker-compose ps`

2. **Template Not Found Error**
   - Verify `BASE_DIR` in `settings.py` points to correct directory
   - Check template paths in `TEMPLATES` setting

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - For Docker: Rebuild containers with `docker-compose up --build`

4. **Database Not Initialized**
   - For Docker: Database initializes automatically on first run
   - For local: Run migrations and load data manually

### Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs web
docker-compose logs db

# Restart services
docker-compose restart

# Rebuild and start
docker-compose up --build

# Stop services
docker-compose down
```

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