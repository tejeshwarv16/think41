import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ProductGrid from '../components/ProductGrid';

function DepartmentProductsPage() {
  const { departmentId } = useParams();
  const [departmentData, setDepartmentData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDepartmentProducts = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/departments/${departmentId}/products`);
        if (!response.ok) throw new Error('Could not fetch department products');
        const data = await response.json();
        setDepartmentData(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchDepartmentProducts();
  }, [departmentId]);

  if (isLoading) return <div>Loading products...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <div className="page-header">
        <h2>{departmentData.department}</h2>
        <p>{departmentData.products.length} Products</p>
      </div>
      <ProductGrid products={departmentData.products} />
    </div>
  );
}

export default DepartmentProductsPage;