function RecommendationsPanel({ recommendations, apiUrl, onPurchaseOrderCreated }) {
    function createPurchaseOrder(recommendation) {
      if (!recommendation.recommended_supplier_id) {
        alert("This recommendation does not have a supplier.");
        return;
      }

      fetch(`${apiUrl}/purchase-orders`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          product_id: recommendation.product_id,
          supplier_id: recommendation.recommended_supplier_id,
          quantity: recommendation.recommended_quantity,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to create purchase order");
          }

          return response.json();
        })
        .then(() => {
          alert("Purchase order created.");
          onPurchaseOrderCreated();
        })
        .catch(() => {
          alert("Could not create purchase order.");
        });
    }

    return (
      <section className="recommendations-panel">
        <div className="section-header">
          <h2>AI Recommendations</h2>
          <span>{recommendations.length} actions</span>
        </div>

        <div className="recommendation-list">
          {recommendations.map((recommendation) => (
            <article className="recommendation-item" key={recommendation.product_id}>
              <div>
                <strong>{recommendation.product_name}</strong>
                <p>{recommendation.reason}</p>
              </div>

              <div className="recommendation-meta">
                <span>{recommendation.recommended_quantity} units</span>
                <span>{recommendation.recommended_supplier_name || "No supplier"}</span>
                <span>
                  {recommendation.estimated_delivery_days
                    ? `${recommendation.estimated_delivery_days} days`
                    : "N/A"}
                </span>

                <button
                  className="small-action-button"
                  type="button"
                  onClick={() => createPurchaseOrder(recommendation)}
                >
                  Create order
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>
    );
  }

  export default RecommendationsPanel;