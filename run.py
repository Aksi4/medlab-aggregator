from database import create_app

# Створення екземпляра додатка
app = create_app()

if __name__ == "__main__":
    # Запуск додатка
    app.run(debug=True)
