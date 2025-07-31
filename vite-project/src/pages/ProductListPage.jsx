import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function ProductListPage() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/products');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchProducts();
  }, []);

  if (isLoading) return <div>Loading products...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="product-grid">
      {products.map((product) => (
        <Link to={`/products/${product.id}`} key={product.id} className="product-card-link">
          <div className="product-card">
            {/* Reverted to picsum.photos for placeholder images */}
            <img src={`https://picsum.photos/seed/${product.id}/400/400`} alt={product.name} />
            <h2>{product.name}</h2>
            <p>${product.retail_price.toFixed(2)}</p>
          </div>
        </Link>
      ))}
    </div>
  );
}
export default ProductListPage;