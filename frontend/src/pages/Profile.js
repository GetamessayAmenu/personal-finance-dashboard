import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import toast from 'react-hot-toast';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const profileSchema = yup.object({
  username: yup.string().min(3, 'Username must be at least 3 characters').required('Username is required'),
  email: yup.string().email('Please enter a valid email').required('Email is required'),
});

const passwordSchema = yup.object({
  currentPassword: yup.string().required('Current password is required'),
  newPassword: yup.string().min(6, 'Password must be at least 6 characters').required('New password is required'),
  confirmPassword: yup.string()
    .oneOf([yup.ref('newPassword'), null], 'Passwords must match')
    .required('Please confirm your password'),
});

const currencies = [
  { code: 'USD', symbol: '$', name: 'US Dollar' },
  { code: 'EUR', symbol: '€', name: 'Euro' },
  { code: 'GBP', symbol: '£', name: 'British Pound' },
  { code: 'JPY', symbol: '¥', name: 'Japanese Yen' },
  { code: 'CAD', symbol: 'C$', name: 'Canadian Dollar' },
  { code: 'AUD', symbol: 'A$', name: 'Australian Dollar' },
];

export default function Profile() {
  const { user, login } = useAuth();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('profile');

  const profileForm = useForm({
    resolver: yupResolver(profileSchema),
    defaultValues: {
      username: user?.username || '',
      email: user?.email || '',
    },
  });

  const passwordForm = useForm({
    resolver: yupResolver(passwordSchema),
  });

  useEffect(() => {
    if (user) {
      profileForm.reset({
        username: user.username,
        email: user.email,
      });
    }
  }, [user, profileForm]);

  const onUpdateProfile = async (data) => {
    setLoading(true);
    try {
      await axios.put('/profile', data);
      toast.success('Profile updated successfully');
      // Refresh user data
      window.location.reload();
    } catch (error) {
      console.error('Error updating profile:', error);
      toast.error('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const onChangePassword = async (data) => {
    setLoading(true);
    try {
      await axios.put('/profile/password', {
        current_password: data.currentPassword,
        new_password: data.newPassword,
      });
      toast.success('Password changed successfully');
      passwordForm.reset();
    } catch (error) {
      console.error('Error changing password:', error);
      toast.error('Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="row justify-content-center"
      >
        <div className="col-lg-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="card shadow-sm"
          >
            <div className="card-body p-4">
              <div className="text-center mb-4">
                <div className="avatar-circle mx-auto mb-3" style={{
                  width: '80px',
                  height: '80px',
                  borderRadius: '50%',
                  backgroundColor: '#007bff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '2rem',
                  color: 'white',
                  fontWeight: 'bold'
                }}>
                  {user?.username?.charAt(0).toUpperCase() || 'U'}
                </div>
                <h2 className="card-title mb-1">{user?.username || 'User'}</h2>
                <p className="text-muted">{user?.email || 'user@example.com'}</p>
              </div>

              {/* Tabs */}
              <ul className="nav nav-tabs mb-4">
                <li className="nav-item">
                  <button
                    className={`nav-link ${activeTab === 'profile' ? 'active' : ''}`}
                    onClick={() => setActiveTab('profile')}
                  >
                    <i className="bi bi-person me-2"></i>Profile
                  </button>
                </li>
                <li className="nav-item">
                  <button
                    className={`nav-link ${activeTab === 'password' ? 'active' : ''}`}
                    onClick={() => setActiveTab('password')}
                  >
                    <i className="bi bi-key me-2"></i>Password
                  </button>
                </li>
                <li className="nav-item">
                  <button
                    className={`nav-link ${activeTab === 'preferences' ? 'active' : ''}`}
                    onClick={() => setActiveTab('preferences')}
                  >
                    <i className="bi bi-gear me-2"></i>Preferences
                  </button>
                </li>
              </ul>

              {/* Profile Tab */}
              {activeTab === 'profile' && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                >
                  <h5 className="mb-3">Personal Information</h5>
                  <form onSubmit={profileForm.handleSubmit(onUpdateProfile)}>
                    <div className="mb-3">
                      <label htmlFor="username" className="form-label">
                        Username
                      </label>
                      <input
                        type="text"
                        className={`form-control ${profileForm.formState.errors.username ? 'is-invalid' : ''}`}
                        id="username"
                        {...profileForm.register('username')}
                      />
                      {profileForm.formState.errors.username && (
                        <div className="invalid-feedback">
                          {profileForm.formState.errors.username.message}
                        </div>
                      )}
                    </div>

                    <div className="mb-3">
                      <label htmlFor="email" className="form-label">
                        Email Address
                      </label>
                      <input
                        type="email"
                        className={`form-control ${profileForm.formState.errors.email ? 'is-invalid' : ''}`}
                        id="email"
                        {...profileForm.register('email')}
                      />
                      {profileForm.formState.errors.email && (
                        <div className="invalid-feedback">
                          {profileForm.formState.errors.email.message}
                        </div>
                      )}
                    </div>

                    <div className="d-grid">
                      <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading}
                      >
                        {loading ? (
                          <>
                            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                            Updating...
                          </>
                        ) : (
                          <>
                            <i className="bi bi-check-circle me-2"></i>
                            Update Profile
                          </>
                        )}
                      </button>
                    </div>
                  </form>
                </motion.div>
              )}

              {/* Password Tab */}
              {activeTab === 'password' && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                >
                  <h5 className="mb-3">Change Password</h5>
                  <form onSubmit={passwordForm.handleSubmit(onChangePassword)}>
                    <div className="mb-3">
                      <label htmlFor="currentPassword" className="form-label">
                        Current Password
                      </label>
                      <input
                        type="password"
                        className={`form-control ${passwordForm.formState.errors.currentPassword ? 'is-invalid' : ''}`}
                        id="currentPassword"
                        {...passwordForm.register('currentPassword')}
                      />
                      {passwordForm.formState.errors.currentPassword && (
                        <div className="invalid-feedback">
                          {passwordForm.formState.errors.currentPassword.message}
                        </div>
                      )}
                    </div>

                    <div className="mb-3">
                      <label htmlFor="newPassword" className="form-label">
                        New Password
                      </label>
                      <input
                        type="password"
                        className={`form-control ${passwordForm.formState.errors.newPassword ? 'is-invalid' : ''}`}
                        id="newPassword"
                        {...passwordForm.register('newPassword')}
                      />
                      {passwordForm.formState.errors.newPassword && (
                        <div className="invalid-feedback">
                          {passwordForm.formState.errors.newPassword.message}
                        </div>
                      )}
                    </div>

                    <div className="mb-3">
                      <label htmlFor="confirmPassword" className="form-label">
                        Confirm New Password
                      </label>
                      <input
                        type="password"
                        className={`form-control ${passwordForm.formState.errors.confirmPassword ? 'is-invalid' : ''}`}
                        id="confirmPassword"
                        {...passwordForm.register('confirmPassword')}
                      />
                      {passwordForm.formState.errors.confirmPassword && (
                        <div className="invalid-feedback">
                          {passwordForm.formState.errors.confirmPassword.message}
                        </div>
                      )}
                    </div>

                    <div className="d-grid">
                      <button
                        type="submit"
                        className="btn btn-warning"
                        disabled={loading}
                      >
                        {loading ? (
                          <>
                            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                            Changing...
                          </>
                        ) : (
                          <>
                            <i className="bi bi-key me-2"></i>
                            Change Password
                          </>
                        )}
                      </button>
                    </div>
                  </form>
                </motion.div>
              )}

              {/* Preferences Tab */}
              {activeTab === 'preferences' && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                >
                  <h5 className="mb-3">Preferences</h5>

                  <div className="mb-4">
                    <h6 className="mb-3">Currency</h6>
                    <div className="row g-2">
                      {currencies.map((currency) => (
                        <div key={currency.code} className="col-md-4">
                          <div className="form-check">
                            <input
                              className="form-check-input"
                              type="radio"
                              name="currency"
                              id={`currency-${currency.code}`}
                              defaultChecked={currency.code === 'USD'}
                            />
                            <label className="form-check-label" htmlFor={`currency-${currency.code}`}>
                              {currency.symbol} {currency.name}
                            </label>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="mb-4">
                    <h6 className="mb-3">Notifications</h6>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" id="budget-alerts" defaultChecked />
                      <label className="form-check-label" htmlFor="budget-alerts">
                        Budget alerts when approaching limits
                      </label>
                    </div>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" id="weekly-reports" />
                      <label className="form-check-label" htmlFor="weekly-reports">
                        Weekly spending reports
                      </label>
                    </div>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" id="monthly-summary" defaultChecked />
                      <label className="form-check-label" htmlFor="monthly-summary">
                        Monthly financial summary
                      </label>
                    </div>
                  </div>

                  <div className="mb-4">
                    <h6 className="mb-3">Display Options</h6>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" id="show-cents" defaultChecked />
                      <label className="form-check-label" htmlFor="show-cents">
                        Show cents in amounts
                      </label>
                    </div>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" id="thousand-separator" defaultChecked />
                      <label className="form-check-label" htmlFor="thousand-separator">
                        Use thousand separators (1,000)
                      </label>
                    </div>
                  </div>

                  <div className="d-grid">
                    <button className="btn btn-success">
                      <i className="bi bi-check-circle me-2"></i>
                      Save Preferences
                    </button>
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
}
