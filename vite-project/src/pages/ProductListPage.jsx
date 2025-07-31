import { useState, useEffect } from 'react';
import ProductGrid from '../components/ProductGrid';

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
        
        // --- ADD THIS LINE FOR DEBUGGING ---
        console.log("Data received from API:", data);
        // ------------------------------------

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
    <div>
      <div className="page-header">
        <h2>All Products</h2>
        <p>{products.length} Products</p>
      </div>
      <ProductGrid products={products} />
    </div>
  );
}

export default ProductListPage;