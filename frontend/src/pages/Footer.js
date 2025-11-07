import React from 'react';

export default function Footer() {
  return (
    <footer className="footer bg-white mt-4 shadow-sm">
      <div className="container">
        <small>© {new Date().getFullYear()} SmartSpend — Built for demo purposes</small>
      </div>
    </footer>
  );
}