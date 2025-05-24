
# 📦 Inventory Management App (app_estoque)

This is a local inventory management application built using **Python** and **Tkinter**, ideal for environments without internet access.  
It allows registering, updating, tracking, and managing product stocks efficiently.

## 🧰 Requirements

Before running the app, make sure you have the following installed:

- **Python 3.10+**  
  Download: https://www.python.org/downloads/

- **Tkinter**  
  Already included with most Python distributions. If not, install via:

  ```bash
  sudo apt-get install python3-tk  # (Linux)
  ```

- **Pandas** (for data handling):

  ```bash
  pip install pandas
  ```

## 🚀 How to Run the Application

1. **Clone the repository** or download the ZIP:

   ```bash
   git clone https://github.com/Lucasyuki01/app_estoque.git
   cd app_estoque
   ```

2. **Run the main script**:

   ```bash
   python app.py
   ```

   This will open the graphical interface of the system.

---

## 🧭 Features

The app has a main menu with the following options:

### 1. 📊 Estoque (Stock Overview)
- View current stock
- Search by product name
- Withdraw product (with validation for quantity and existence)

### 2. 📝 Solicitar Produto (Request Product)
- Create a product request by entering:
  - Product name
  - Quantity
  - Importance
  - Responsible
  - Observation (optional)
- System generates a request number automatically

### 3. 📦 Acompanhar Solicitação (Track Request)
- View and filter all requests by:
  - Request number
  - Responsible
- Update status via dropdown (with password protection)

### 4. 🛠 Atualizar Status (Password Protected)
- Change the status of product requests:
  - Solicited
  - Under analysis
  - Approved
  - Rejected
  - Delivered

### 5. ➕ Gerenciar Estoque (Stock Management)
- **Add New Product**: Register product details and stock minimum
- **Add to Existing Product**: Select product by ID and increase quantity

### 6. 🕓 Histórico (History)
- Shows a table of all actions (additions, withdrawals, registrations)
- Filterable by:
  - Product Name
  - ID
  - Responsible

---

## 💾 Data Storage

- Product stock and history are saved in local `.csv` files:
  - `estoque.csv`
  - `historico.csv`
  - `solicitacoes.csv`

Make sure they are in the same directory as `app.py` when running the program.

---

## 👨‍💻 Author

Developed by [Lucas Yuki](https://github.com/Lucasyuki01)  
As a practical project to assist in inventory management without needing cloud services.

---

## 📜 License

This project is open-source and free to use under the MIT License.
