import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';

function Sidebar({ isCollapsed, onToggle }) {
  const [departments, setDepartments] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/departments');
        if (!response.ok) throw new Error('Could not fetch departments');
        const data = await response.json();
        setDepartments(data.departments);
      } catch (error) {
        setError(error.message);
      }
    };
    fetchDepartments();
  }, []);

  if (error) return <aside className="sidebar">Error: {error}</aside>;

  return (
    <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-content">
        <h3>Departments</h3>
        <nav>
          <ul>
            <li>
              <NavLink to="/" end>
                <span className="nav-icon">🏠</span>
                <span className="nav-text">All Products</span>
              </NavLink>
            </li>
            {departments.map(dept => (
              <li key={dept.id}>
                <NavLink to={`/departments/${dept.id}`}>
                  <span className="nav-icon">{dept.name === 'Men' ? '👨' : '👩'}</span>
                  <span className="nav-text">{dept.name} <span>({dept.product_count})</span></span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </div>
      <button onClick={onToggle} className="sidebar-toggle">
        {isCollapsed ? '→' : '←'}
      </button>
    </aside>
  );
}

export default Sidebar;