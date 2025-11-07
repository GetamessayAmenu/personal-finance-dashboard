import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import toast from 'react-hot-toast';
import axios from 'axios';
import { format } from 'date-fns';

const schema = yup.object({
  category: yup.string().required('Category is required'),
  amount: yup.number().positive('Amount must be positive').required('Amount is required'),
  month: yup.number().min(1).max(12).required('Month is required'),
  year: yup.number().min(2020).max(2030).required('Year is required'),
});

const categories = [
  'Food & Dining',
  'Transportation',
  'Shopping',
  'Entertainment',
  'Bills & Utilities',
  'Healthcare',
  'Education',
  'Travel',
  'Other'
];

const months = [
  { value: 1, label: 'January' },
  { value: 2, label: 'February' },
  { value: 3, label: 'March' },
  { value: 4, label: 'April' },
  { value: 5, label: 'May' },
  { value: 6, label: 'June' },
  { value: 7, label: 'July' },
  { value: 8, label: 'August' },
  { value: 9, label: 'September' },
  { value: 10, label: 'October' },
  { value: 11, label: 'November' },
  { value: 12, label: 'December' },
];

export default function Budgets() {
  const [budgets, setBudgets] = useState([]);
  const [budgetProgress, setBudgetProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingBudget, setEditingBudget] = useState(null);
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: yupResolver(schema),
  });

  useEffect(() => {
    fetchBudgets();
    fetchBudgetProgress();
  }, [selectedMonth, selectedYear]);

  const fetchBudgets = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/budgets');
      setBudgets(response.data);
    } catch (error) {
      console.error('Error fetching budgets:', error);
      toast.error('Failed to load budgets');
    } finally {
      setLoading(false);
    }
  };

  const fetchBudgetProgress = async () => {
    try {
      const response = await axios.get(`/budgets/progress/${selectedYear}/${selectedMonth}`);
      setBudgetProgress(response.data);
    } catch (error) {
      console.error('Error fetching budget progress:', error);
    }
  };

  const onSubmit = async (data) => {
    try {
      if (editingBudget) {
        await axios.put(`/budgets/${editingBudget.id}`, data);
        toast.success('Budget updated successfully');
      } else {
        await axios.post('/budgets', data);
        toast.success('Budget created successfully');
      }
      fetchBudgets();
      fetchBudgetProgress();
      setShowModal(false);
      reset();
      setEditingBudget(null);
    } catch (error) {
      console.error('Error saving budget:', error);
      toast.error('Failed to save budget');
    }
  };

  const handleEdit = (budget) => {
    setEditingBudget(budget);
    setValue('category', budget.category);
    setValue('amount', budget.amount);
    setValue('month', budget.month);
    setValue('year', budget.year);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this budget?')) {
      try {
        await axios.delete(`/budgets/${id}`);
        toast.success('Budget deleted successfully');
        fetchBudgets();
        fetchBudgetProgress();
      } catch (error) {
        console.error('Error deleting budget:', error);
        toast.error('Failed to delete budget');
      }
    }
  };

  const getProgressColor = (progress) => {
    if (progress < 50) return 'bg-success';
    if (progress < 80) return 'bg-warning';
    return 'bg-danger';
  };

  const getProgressTextColor = (progress) => {
    if (progress < 50) return 'text-success';
    if (progress < 80) return 'text-warning';
    return 'text-danger';
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid mt-4">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="d-flex justify-content-between align-items-center mb-4"
      >
        <div>
          <h1 className="mb-0">Budgets</h1>
          <p className="text-muted">Track your spending against monthly budgets</p>
        </div>
        <div className="d-flex gap-2">
          <select
            className="form-select"
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
          >
            {months.map((month) => (
              <option key={month.value} value={month.value}>
                {month.label}
              </option>
            ))}
          </select>
          <select
            className="form-select"
            value={selectedYear}
            onChange={(e) => setSelectedYear(parseInt(e.target.value))}
          >
            {Array.from({ length: 5 }, (_, i) => new Date().getFullYear() + i).map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
          <button
            className="btn btn-primary"
            onClick={() => setShowModal(true)}
          >
            <i className="bi bi-plus-circle me-2"></i>Add Budget
          </button>
        </div>
      </motion.div>

      {/* Budget Progress Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="row mb-4"
      >
        {budgetProgress.length === 0 ? (
          <div className="col-12">
            <div className="card">
              <div className="card-body text-center py-5">
                <i className="bi bi-pie-chart fs-1 text-muted mb-3"></i>
                <h4 className="text-muted">No budgets set for this month</h4>
                <p className="text-muted">Create your first budget to start tracking your spending</p>
                <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                  Create Budget
                </button>
              </div>
            </div>
          </div>
        ) : (
          budgetProgress.map((budget, index) => (
            <motion.div
              key={budget.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
              className="col-lg-6 col-xl-4 mb-3"
            >
              <div className="card h-100">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-start mb-2">
                    <h6 className="card-title mb-0">{budget.category}</h6>
                    <div className="dropdown">
                      <button
                        className="btn btn-sm btn-outline-secondary"
                        type="button"
                        data-bs-toggle="dropdown"
                      >
                        <i className="bi bi-three-dots-vertical"></i>
                      </button>
                      <ul className="dropdown-menu">
                        <li>
                          <button
                            className="dropdown-item"
                            onClick={() => {
                              const budgetData = budgets.find(b => b.id === budget.id);
                              if (budgetData) handleEdit(budgetData);
                            }}
                          >
                            <i className="bi bi-pencil me-2"></i>Edit
                          </button>
                        </li>
                        <li>
                          <button
                            className="dropdown-item text-danger"
                            onClick={() => handleDelete(budget.id)}
                          >
                            <i className="bi bi-trash me-2"></i>Delete
                          </button>
                        </li>
                      </ul>
                    </div>
                  </div>

                  <div className="mb-3">
                    <div className="d-flex justify-content-between mb-1">
                      <small className="text-muted">Spent</small>
                      <small className={`fw-bold ${getProgressTextColor(budget.progress)}`}>
                        ${budget.spent.toLocaleString()} / ${budget.budget_amount.toLocaleString()}
                      </small>
                    </div>
                    <div className="progress" style={{ height: '8px' }}>
                      <div
                        className={`progress-bar ${getProgressColor(budget.progress)}`}
                        role="progressbar"
                        style={{ width: `${Math.min(budget.progress, 100)}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="d-flex justify-content-between align-items-center">
                    <small className={`fw-bold ${budget.is_over_budget ? 'text-danger' : 'text-success'}`}>
                      {budget.is_over_budget ? 'Over Budget' : `${(100 - budget.progress).toFixed(1)}% Left`}
                    </small>
                    <small className="text-muted">
                      ${budget.remaining.toLocaleString()} remaining
                    </small>
                  </div>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </motion.div>

      {/* Budget List */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card"
      >
        <div className="card-body">
          <h5 className="card-title">All Budgets</h5>
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Amount</th>
                  <th>Month/Year</th>
                  <th className="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                {budgets.map((budget) => (
                  <tr key={budget.id}>
                    <td>
                      <span className="badge bg-light text-dark">{budget.category}</span>
                    </td>
                    <td className="fw-bold">${budget.amount.toLocaleString()}</td>
                    <td>{months.find(m => m.value === budget.month)?.label} {budget.year}</td>
                    <td className="text-center">
                      <div className="btn-group btn-group-sm">
                        <button
                          className="btn btn-outline-primary"
                          onClick={() => handleEdit(budget)}
                          title="Edit"
                        >
                          <i className="bi bi-pencil"></i>
                        </button>
                        <button
                          className="btn btn-outline-danger"
                          onClick={() => handleDelete(budget.id)}
                          title="Delete"
                        >
                          <i className="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </motion.div>

      {/* Add/Edit Modal */}
      <AnimatePresence>
        {showModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="modal show d-block"
            style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}
          >
            <div className="modal-dialog">
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                className="modal-content"
              >
                <form onSubmit={handleSubmit(onSubmit)}>
                  <div className="modal-header">
                    <h5 className="modal-title">
                      {editingBudget ? 'Edit Budget' : 'Add Budget'}
                    </h5>
                    <button
                      type="button"
                      className="btn-close"
                      onClick={() => {
                        setShowModal(false);
                        reset();
                        setEditingBudget(null);
                      }}
                    ></button>
                  </div>
                  <div className="modal-body">
                    <div className="row g-3">
                      <div className="col-md-6">
                        <label className="form-label">Category</label>
                        <select className={`form-select ${errors.category ? 'is-invalid' : ''}`} {...register('category')}>
                          <option value="">Select category</option>
                          {categories.map((category) => (
                            <option key={category} value={category}>
                              {category}
                            </option>
                          ))}
                        </select>
                        {errors.category && <div className="invalid-feedback">{errors.category.message}</div>}
                      </div>

                      <div className="col-md-6">
                        <label className="form-label">Budget Amount</label>
                        <input
                          type="number"
                          step="0.01"
                          className={`form-control ${errors.amount ? 'is-invalid' : ''}`}
                          {...register('amount')}
                          placeholder="0.00"
                        />
                        {errors.amount && <div className="invalid-feedback">{errors.amount.message}</div>}
                      </div>

                      <div className="col-md-6">
                        <label className="form-label">Month</label>
                        <select className={`form-select ${errors.month ? 'is-invalid' : ''}`} {...register('month')}>
                          <option value="">Select month</option>
                          {months.map((month) => (
                            <option key={month.value} value={month.value}>
                              {month.label}
                            </option>
                          ))}
                        </select>
                        {errors.month && <div className="invalid-feedback">{errors.month.message}</div>}
                      </div>

                      <div className="col-md-6">
                        <label className="form-label">Year</label>
                        <select className={`form-select ${errors.year ? 'is-invalid' : ''}`} {...register('year')}>
                          <option value="">Select year</option>
                          {Array.from({ length: 5 }, (_, i) => new Date().getFullYear() + i).map((year) => (
                            <option key={year} value={year}>
                              {year}
                            </option>
                          ))}
                        </select>
                        {errors.year && <div className="invalid-feedback">{errors.year.message}</div>}
                      </div>
                    </div>
                  </div>
                  <div className="modal-footer">
                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={() => {
                        setShowModal(false);
                        reset();
                        setEditingBudget(null);
                      }}
                    >
                      Cancel
                    </button>
                    <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
                      {isSubmitting ? 'Saving...' : (editingBudget ? 'Update' : 'Add')} Budget
                    </button>
                  </div>
                </form>
              </motion.div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
