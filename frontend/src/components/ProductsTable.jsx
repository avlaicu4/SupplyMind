function ProductsTable({ products, loading, error }) {
    if (loading) {
      return <p className="panel-message">Loading products...</p>;
    }

    if (error) {
      return <p className="panel-message error">{error}</p>;
    }

    return (
      <section className="table-section">
        <div className="section-header">
          <h2>Products</h2>
          <span>{products.length} items</span>
        </div>

        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Current Stock</th>
              <th>Minimum Stock</th>
              <th>Avg. Daily Sales</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {products.map((product) => {
              const isLowStock = product.current_stock < product.minimum_stock;

              return (
                <tr key={product.id}>
                  <td>{product.name}</td>
                  <td>{product.category}</td>
                  <td>{product.current_stock}</td>
                  <td>{product.minimum_stock}</td>
                  <td>{product.average_daily_sales}</td>
                  <td>
                    <span className={isLowStock ? "badge danger" : "badge success"}>
                      {isLowStock ? "Low stock" : "Healthy"}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </section>
    );
  }

  export default ProductsTable;