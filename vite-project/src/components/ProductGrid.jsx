import { Link } from 'react-router-dom';

function ProductGrid({ products }) {
  if (products.length === 0) {
    return <p>No products found in this department.</p>;
  }

  return (
    <div className="product-grid">
      {products.map((product) => (
        <Link to={`/products/${product.id}`} key={product.id} className="product-card-link">
          <div className="product-card">
            <img src={product.image_url} alt={product.name} />
            <h2>{product.name}</h2>
            <p>${product.retail_price.toFixed(2)}</p>
          </div>
        </Link>
      ))}
    </div>
  );
}

export default ProductGrid;