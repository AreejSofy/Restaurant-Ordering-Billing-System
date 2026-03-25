The Mexican Flavor - POS System
A modern, light-themed Point of Sale (POS) application for a Mexican restaurant. This project is built using pure Python and the Tkinter library, focusing on clean code and Object-Oriented Programming (OOP) principles.

Features
Dynamic Menu Display: Categorized items (Tacos, Burritos, Drinks, etc.) with custom color coding for easy navigation.

Real-time Cart Management: Smart grouping logic that aggregates identical items (e.g., Taco x4) and calculates totals instantly.

Advanced Discount System: Supports multiple promo codes (SAVE20, FLAT50, WELCOME) using the Strategy Pattern.

Secure Payment Simulation: Supports both Cash and Credit Card payments with input validation (16-digit card check).

Responsive UI: Custom-built interface featuring scrollable menus, interactive cards, and centered windows.

Project Structure
To maintain high code quality and scalability, the project is organized into a modular structure:

Plaintext
mexican_flavor_project/
├── main.py                # Entry point to launch the application
├── requirements.txt       # Environment dependencies
├── README.md              # Project documentation
└── src/                   # Source code package
    ├── colors.py          # Theme configurations and UI constants
    ├── models.py          # Core data models (MenuItem, Order)
    ├── strategies.py      # Strategy Pattern implementation for discounts
    ├── payments.py        # Polymorphism logic for payment processing
    └── gui.py             # User interface components and windows

OOP Principles & Design Patterns
This project was developed to demonstrate core software engineering concepts:

Abstraction: Implemented using ABC (Abstract Base Classes) for DiscountStrategy and PaymentMethod models to define strict interfaces.

Inheritance: Specialized classes derived from abstract bases to handle unique behaviors for different payment methods and discount types.

Encapsulation: All business logic for orders and UI states is encapsulated within dedicated classes, protecting the internal data from direct external interference.

Polymorphism: The system processes various payment and discount objects through a unified interface, allowing the application to be easily extended with new methods in the future.

Getting Started
Prerequisites
Python 3.x (Tkinter is included in the standard library).

Installation & Running
Download or clone the project files.

Ensure your directory follows the structure mentioned above.

Run the application using the following command:

Bash
python main.py