import { Navigate, Route, Routes } from 'react-router-dom';
import { Layout } from './components/Layout';
import { BoardPage } from './pages/BoardPage';
import { ClientsPage } from './pages/ClientsPage';
import { OrderPage } from './pages/OrderPage';
import { RequestsPage } from './pages/RequestsPage';
import { TrackingPage } from './pages/TrackingPage';

export function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Navigate to="/requests" replace />} />
        <Route path="requests" element={<RequestsPage />} />
        <Route path="orders" element={<BoardPage />} />
        <Route path="orders/:id" element={<OrderPage />} />
        <Route path="clients" element={<ClientsPage />} />
        <Route path="tracking" element={<TrackingPage />} />
        <Route path="*" element={<Navigate to="/requests" replace />} />
      </Route>
    </Routes>
  );
}
