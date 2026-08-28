import { useEffect, useState } from "react";
import "./App.css";
import AddProductForm from "./components/AddProductForm";
import AiChat from "./components/AiChat";
import MetricCard from "./components/MetricCard";
import ProductsTable from "./components/ProductsTable";
import RecommendationsPanel from "./components/RecommendationsPanel";
import Sidebar from "./components/Sidebar";
import PurchaseOrdersPanel from "./components/PurchaseOrdersPanel";
import SuppliersPanel from "./components/SuppliersPanel";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [products, setProducts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [purchaseOrders, setPurchaseOrders] = useState([]);

  function loadDashboardData() {
    setLoading(true);
    setError("");

    fetch(`${API_URL}/products`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch products");
        }

        return response.json();
      })
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Could not load products from the backend.");
        setLoading(false);
      });

    fetch(`${API_URL}/ai/recommendations`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch recommendations");
        }

        return response.json();
      })
      .then((data) => {
        setRecommendations(data);
      })
      .catch(() => {
        setRecommendations([]);
      });

    fetch(`${API_URL}/suppliers`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch suppliers");
        }

        return response.json();
      })
      .then((data) => {
        setSuppliers(data);
      })
      .catch(() => {
        setSuppliers([]);
      });

    fetch(`${API_URL}/purchase-orders`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch purchase orders");
        }

        return response.json();
      })
      .then((data) => {
        setPurchaseOrders(data);
      })
      .catch(() => {
        setPurchaseOrders([]);
      });
  }

  useEffect(() => {
    loadDashboardData();
  }, []);

  useEffect(() => {
    const targetId = window.location.hash.replace("#", "");

    if (!targetId) {
      return;
    }

    setTimeout(() => {
      document.getElementById(targetId)?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 100);
  }, []);

  const lowStockCount = products.filter(
    (product) => product.current_stock < product.minimum_stock
  ).length;

  const healthyStockCount = products.filter(
    (product) => product.current_stock >= product.minimum_stock
  ).length;

  return (
    <div className="shell">
      <Sidebar />

      <main className="app" id="dashboard">
        <section className="page-header">
          <div>
            <p className="eyebrow">AI Procurement Command Center</p>
            <h1>Inventory Dashboard</h1>
            <p className="subtitle">
              Monitor stock risk, supplier coverage, and AI reorder decisions.
            </p>
          </div>

          <div className="api-status">
            <span />
            API online
          </div>
        </section>

        <section className="metrics-grid">
          <MetricCard
            label="Total products"
            value={products.length}
            detail="Tracked inventory items"
            tone="blue"
          />

          <MetricCard
            label="Low stock"
            value={lowStockCount}
            detail="Need procurement review"
            tone="red"
          />

          <MetricCard
            label="Healthy stock"
            value={healthyStockCount}
            detail="Above minimum threshold"
            tone="green"
          />

          <MetricCard
            label="Suppliers"
            value={suppliers.length}
            detail="Available procurement partners"
            tone="blue"
          />
        </section>

        <AddProductForm
          apiUrl={API_URL}
          onProductCreated={loadDashboardData}
        />

        <section id="products" className="scroll-section">
          <ProductsTable products={products} loading={loading} error={error} />
        </section>

        <section id="suppliers" className="scroll-section">
          <SuppliersPanel suppliers={suppliers} />
        </section>

        <section className="dashboard-grid" id="recommendations">
          <RecommendationsPanel
            recommendations={recommendations}
            apiUrl={API_URL}
            onPurchaseOrderCreated={loadDashboardData}
          />

          <div id="ai-assistant" className="scroll-section">
            <AiChat apiUrl={API_URL} />
          </div>
        </section>

        <section id="orders" className="scroll-section">
          <PurchaseOrdersPanel purchaseOrders={purchaseOrders} />
        </section>
      </main>
    </div>
  );
}

export default App;
