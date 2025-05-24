# 📦 Inventory Management App (app_estoque)

This is a local inventory management application designed to run **without requiring Python installation**.  
The app helps manage product stock, requests, and history in environments without internet access.

## 🚀 How to Run the Application

1. **Download the repository** from GitHub:  
   [https://github.com/Lucasyuki01/app_estoque](https://github.com/Lucasyuki01/app_estoque)

2. Open the folder and **double-click the file `app.exe`** to launch the application.

> ⚠️ **Important:**  
> Windows might show a security warning the first time you open the app.  
> Click on **"More info"** and then **"Run anyway"**.  
> This is a common alert for apps not registered with Microsoft and does **not** mean the app is dangerous.

---

## 🧭 Features

### 1. 📊 Estoque (Stock Overview)
- View current stock
- Search by product name
- Withdraw products (with quantity validation)

### 2. 📝 Solicitar Produto (Request Product)
- Submit product requests with:
  - Name, Quantity, Importance, Responsible, Observation
- The system assigns a unique request number

### 3. 📦 Acompanhar Solicitação (Track Request)
- View all requests and filter by responsible or request number
- Update status (protected by password)

### 4. 🛠 Atualizar Status
- Change request status using a secure dropdown:
  - Solicited, Under Analysis, Approved, Rejected, Delivered

### 5. ➕ Gerenciar Estoque
- **Add New Product**
- **Add Quantity to Existing Product**

### 6. 🕓 Histórico
- Complete log of actions: additions, withdrawals, new registrations
- Filter by product, ID, or responsible

---

## 💾 Data Storage

The application stores data in local `.csv` files:
- `estoque.csv`
- `historico.csv`
- `solicitacoes.csv`

Make sure all files stay in the same folder as `app.exe` for everything to work correctly.

---

## 👨‍💻 Author

Developed by [Lucas Yuki](https://github.com/Lucasyuki01)  
As a practical project to assist in offline inventory management.

---

## 📜 License

This project is open-source and free to use under the MIT License.
