function PurchaseOrdersPanel({ purchaseOrders }) {
    return (
      <section className="purchase-orders-panel">
        <div className="section-header">
          <h2>Purchase Orders</h2>
          <span>{purchaseOrders.length} orders</span>
        </div>

        <div className="orders-list">
          {purchaseOrders.length === 0 && (
            <p className="panel-message">No purchase orders created yet.</p>
          )}

          {purchaseOrders.map((order) => (
            <article className="order-item" key={order.id}>
              <div>
                <strong>Order #{order.id}</strong>
                <p>
                  Product ID {order.product_id} · Supplier ID {order.supplier_id}
                </p>
              </div>

              <div className="order-meta">
                <span>{order.quantity} units</span>
                <span>{order.status}</span>
              </div>
            </article>
          ))}
        </div>
      </section>
    );
  }

  export default PurchaseOrdersPanel;