function SuppliersPanel({ suppliers }) {
  return (
    <section className="suppliers-panel">
      <div className="section-header">
        <h2>Suppliers</h2>
        <span>{suppliers.length} partners</span>
      </div>

      <div className="supplier-list">
        {suppliers.length === 0 && (
          <p className="panel-message">No suppliers available yet.</p>
        )}

        {suppliers.map((supplier) => {
          const rating = Number(supplier.reliability_rating || 0);
          const isReliable = rating >= 4.5;

          return (
            <article className="supplier-item" key={supplier.id}>
              <div>
                <strong>{supplier.name}</strong>
                <p>Supplier ID {supplier.id}</p>
              </div>

              <div className="supplier-meta">
                <span>{rating.toFixed(1)} rating</span>
                <span className={isReliable ? "badge success" : "badge warning"}>
                  {isReliable ? "Preferred" : "Standard"}
                </span>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

export default SuppliersPanel;
