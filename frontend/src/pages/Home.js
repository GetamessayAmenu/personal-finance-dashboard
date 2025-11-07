import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  FaChartLine,
  FaPiggyBank,
  FaWallet,
  FaShieldAlt,
  FaMobileAlt,
  FaUsers,
  FaStar,
  FaArrowRight
} from 'react-icons/fa';

export default function Home() {
  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  };

  const stagger = {
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const features = [
    {
      icon: FaChartLine,
      title: "Track Expenses",
      description: "Monitor your spending patterns with detailed analytics and insights"
    },
    {
      icon: FaPiggyBank,
      title: "Smart Budgeting",
      description: "Set and manage budgets with intelligent recommendations"
    },
    {
      icon: FaWallet,
      title: "Financial Goals",
      description: "Achieve your financial targets with guided savings plans"
    },
    {
      icon: FaShieldAlt,
      title: "Secure & Private",
      description: "Bank-level security with complete data privacy protection"
    },
    {
      icon: FaMobileAlt,
      title: "Mobile Ready",
      description: "Access your finances anywhere with our responsive design"
    },
    {
      icon: FaUsers,
      title: "Multi-User",
      description: "Share budgets and track expenses with family members"
    }
  ];

  const stats = [
    { number: "10K+", label: "Active Users" },
    { number: "$2.5M+", label: "Tracked Expenses" },
    { number: "99.9%", label: "Uptime" },
    { number: "5★", label: "User Rating" }
  ];

  const testimonials = [
    {
      name: "Sarah Johnson",
      role: "Small Business Owner",
      content: "SmartSpend transformed how I manage my business finances. The insights are incredible!",
      rating: 5
    },
    {
      name: "Mike Chen",
      role: "Freelancer",
      content: "Finally, a budgeting app that actually helps me save money instead of just tracking it.",
      rating: 5
    },
    {
      name: "Emily Rodriguez",
      role: "Student",
      content: "As a student, this app helped me understand my spending habits and save for my goals.",
      rating: 5
    }
  ];

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-background">
          <div className="floating-element element-1"></div>
          <div className="floating-element element-2"></div>
          <div className="floating-element element-3"></div>
        </div>

        <motion.div
          className="container"
          initial="initial"
          animate="animate"
          variants={stagger}
        >
          <div className="row align-items-center min-vh-100">
            <div className="col-lg-6">
              <motion.div variants={fadeInUp}>
                <div className="hero-badge">
                  <FaStar className="star-icon" />
                  <span>Trusted by 10,000+ users</span>
                </div>
                <h1 className="hero-title">
                  Take Control of Your{' '}
                  <span className="gradient-text">Financial Future</span>
                </h1>
                <p className="hero-subtitle">
                  SmartSpend empowers you to track expenses, set budgets, and achieve your financial goals with intelligent insights and beautiful visualizations.
                </p>
                <div className="hero-actions">
                  <Link className="btn btn-primary btn-lg" to="/signup">
                    Start Free Today
                    <FaArrowRight className="ms-2" />
                  </Link>
                  <Link className="btn btn-outline-light btn-lg ms-3" to="/login">
                    Sign In
                  </Link>
                </div>
              </motion.div>
            </div>

            <div className="col-lg-6">
              <motion.div variants={fadeInUp}>
                <div className="hero-visual">
                  <div className="dashboard-preview">
                    <div className="preview-header">
                      <div className="preview-dots">
                        <span className="dot red"></span>
                        <span className="dot yellow"></span>
                        <span className="dot green"></span>
                      </div>
                    </div>
                    <div className="preview-content">
                      <div className="chart-placeholder">
                        <div className="chart-bars">
                          <div className="bar" style={{height: '60%'}}></div>
                          <div className="bar" style={{height: '80%'}}></div>
                          <div className="bar" style={{height: '40%'}}></div>
                          <div className="bar" style={{height: '90%'}}></div>
                          <div className="bar" style={{height: '70%'}}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <motion.section
        className="features-section"
        initial="initial"
        whileInView="animate"
        viewport={{ once: true }}
        variants={stagger}
      >
        <div className="container">
          <motion.div className="section-header text-center" variants={fadeInUp}>
            <h2>Everything You Need to Manage Your Money</h2>
            <p className="section-subtitle">
              Powerful features designed to help you take control of your financial life
            </p>
          </motion.div>

          <motion.div className="row g-4" variants={stagger}>
            {features.map((feature, index) => (
              <div key={index} className="col-md-6 col-lg-4">
                <motion.div
                  className="feature-card"
                  variants={fadeInUp}
                  whileHover={{ y: -5 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="feature-icon">
                    <feature.icon />
                  </div>
                  <h5 className="feature-title">{feature.title}</h5>
                  <p className="feature-description">{feature.description}</p>
                </motion.div>
              </div>
            ))}
          </motion.div>
        </div>
      </motion.section>

      {/* Stats Section */}
      <motion.section
        className="stats-section"
        initial="initial"
        whileInView="animate"
        viewport={{ once: true }}
      >
        <div className="container">
          <motion.div className="row g-4" variants={stagger}>
            {stats.map((stat, index) => (
              <div key={index} className="col-md-6 col-lg-3">
                <motion.div
                  className="stat-card"
                  variants={fadeInUp}
                  whileHover={{ scale: 1.05 }}
                >
                  <div className="stat-number">{stat.number}</div>
                  <div className="stat-label">{stat.label}</div>
                </motion.div>
              </div>
            ))}
          </motion.div>
        </div>
      </motion.section>

      {/* Testimonials Section */}
      <motion.section
        className="testimonials-section"
        initial="initial"
        whileInView="animate"
        viewport={{ once: true }}
        variants={stagger}
      >
        <div className="container">
          <motion.div className="section-header text-center" variants={fadeInUp}>
            <h2>What Our Users Say</h2>
            <p className="section-subtitle">
              Join thousands of satisfied users who have transformed their financial habits
            </p>
          </motion.div>

          <motion.div className="row g-4" variants={stagger}>
            {testimonials.map((testimonial, index) => (
              <div key={index} className="col-md-6 col-lg-4">
                <motion.div
                  className="testimonial-card"
                  variants={fadeInUp}
                  whileHover={{ y: -5 }}
                >
                  <div className="testimonial-rating">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <FaStar key={i} className="star" />
                    ))}
                  </div>
                  <p className="testimonial-content">"{testimonial.content}"</p>
                  <div className="testimonial-author">
                    <strong>{testimonial.name}</strong>
                    <span className="testimonial-role">{testimonial.role}</span>
                  </div>
                </motion.div>
              </div>
            ))}
          </motion.div>
        </div>
      </motion.section>

      {/* CTA Section */}
      <motion.section
        className="cta-section"
        initial="initial"
        whileInView="animate"
        viewport={{ once: true }}
        variants={stagger}
      >
        <div className="container">
          <motion.div className="cta-content text-center" variants={fadeInUp}>
            <h2>Ready to Take Control?</h2>
            <p className="cta-subtitle">
              Join thousands of users who are already managing their finances smarter
            </p>
            <div className="cta-actions">
              <Link className="btn btn-primary btn-lg" to="/signup">
                Get Started Free
                <FaArrowRight className="ms-2" />
              </Link>
              <Link className="btn btn-outline-primary btn-lg ms-3" to="/login">
                Sign In Instead
              </Link>
            </div>
          </motion.div>
        </div>
      </motion.section>
    </div>
  );
}