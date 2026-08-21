import { useState } from "react";

const initialFormData = {
  name: "",
  category: "",
  current_stock: "",
  minimum_stock: "",
  average_daily_sales: "",
};

function AddProductForm({ apiUrl, onProductCreated }) {
  const [formData, setFormData] = useState(initialFormData);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  function handleSubmit(event) {
    event.preventDefault();

    setSaving(true);
    setMessage("");

    fetch(`${apiUrl}/products`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: formData.name,
        category: formData.category,
        current_stock: Number(formData.current_stock),
        minimum_stock: Number(formData.minimum_stock),
        average_daily_sales: Number(formData.average_daily_sales),
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to create product");
        }

        return response.json();
      })
      .then(() => {
        setFormData(initialFormData);
        setMessage("Product added successfully.");
        setSaving(false);
        onProductCreated();
      })
      .catch(() => {
        setMessage("Could not add product.");
        setSaving(false);
      });
  }

  return (
    <section className="add-product-panel">
      <div className="section-header">
        <h2>Add Product</h2>
        <span>Inventory input</span>
      </div>

      <form className="product-form" onSubmit={handleSubmit}>
        <input
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Product name"
          required
        />

        <input
          name="category"
          value={formData.category}
          onChange={handleChange}
          placeholder="Category"
          required
        />

        <input
          name="current_stock"
          value={formData.current_stock}
          onChange={handleChange}
          placeholder="Current stock"
          type="number"
          required
        />

        <input
          name="minimum_stock"
          value={formData.minimum_stock}
          onChange={handleChange}
          placeholder="Minimum stock"
          type="number"
          required
        />

        <input
          name="average_daily_sales"
          value={formData.average_daily_sales}
          onChange={handleChange}
          placeholder="Average daily sales"
          type="number"
          step="0.1"
          required
        />

        <button type="submit" disabled={saving}>
          {saving ? "Saving..." : "Add product"}
        </button>
      </form>

      {message && <p className="form-message">{message}</p>}
    </section>
  );
}

export default AddProductForm;