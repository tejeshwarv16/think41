import { Routes, Route } from 'react-router-dom';
import ProductListPage from './pages/ProductListPage';
import ProductDetailPage from './pages/ProductDetailPage';

function App() {
  return (
    <div className="container">
      <h1>Our Products</h1>
      <Routes>
        {/* Route for the main product list */}
        <Route path="/" element={<ProductListPage />} />
        
        {/* Route for a single product's detail page */}
        <Route path="/products/:productId" element={<ProductDetailPage />} />
      </Routes>
    </div>
  );
}

export default App;