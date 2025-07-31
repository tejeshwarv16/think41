import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ProductListPage from './pages/ProductListPage';
import ProductDetailPage from './pages/ProductDetailPage';
import DepartmentProductsPage from './pages/DepartmentProductsPage';

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<ProductListPage />} />
        <Route path="/departments/:departmentId" element={<DepartmentProductsPage />} />
      </Route>
      <Route path="/products/:productId" element={<ProductDetailPage />} />
    </Routes>
  );
}

export default App;