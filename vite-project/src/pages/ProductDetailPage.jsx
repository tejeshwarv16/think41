import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function ProductDetailPage() {
  const { productId } = useParams(); // Hook to get URL parameters
  const [product, setProduct] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/products/${productId}`);
        if (!response.ok) throw new Error('Product not found');
        const data = await response.json();
        setProduct(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchProduct();
  }, [productId]); // Re-run effect if productId changes

  if (isLoading) return <div>Loading product details...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <Link to="/" className="back-link">← Back to Products</Link>
      <div className="product-detail">
        <img src={`https://picsum.photos/seed/${product.id}/600/400`} alt={product.name} />
        <div className="product-info">
          <h2>{product.name}</h2>
          <p className="price">${product.retail_price.toFixed(2)}</p>
          <p><strong>Brand:</strong> {product.brand}</p>
          <p><strong>Category:</strong> {product.category}</p>
          <p><strong>Department:</strong> {product.department}</p>
          <p className="sku">SKU: {product.sku}</p>
        </div>
      </div>
    </div>
  );
}

export default ProductDetailPage;