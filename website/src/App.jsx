import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HomePage, ExtensionPage, TermsPage, PolicyPage, NotFoundPage } from './pages/common';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/extension" element={<ExtensionPage />} />
        <Route path="/terms" element={<TermsPage />} />
        <Route path="/policy" element={<PolicyPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
