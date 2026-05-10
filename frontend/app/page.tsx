"use client";

import { motion, useScroll, useTransform, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { useState, useRef } from "react";
import { 
  ArrowRightIcon, 
  CheckIcon, 
  SparklesIcon, 
  ShieldCheckIcon, 
  BoltIcon, 
  ChartBarSquareIcon,
  DocumentTextIcon,
  UserGroupIcon,
  RocketLaunchIcon,
  StarIcon,
  ChevronDownIcon
} from "@heroicons/react/24/outline";

const features = [
  {
    icon: ChartBarSquareIcon,
    title: "ATS Analysis",
    description: "Get instant insights on how recruiters and Applicant Tracking Systems view your resume with precision scoring."
  },
  {
    icon: SparklesIcon,
    title: "Smart Matching",
    description: "Compare your resume against job descriptions to find keyword gaps and optimization opportunities."
  },
  {
    icon: ShieldCheckIcon,
    title: "Professional Suggestions",
    description: "Receive AI-powered rewrite suggestions that make your achievements stand out to hiring managers."
  },
  {
    icon: BoltIcon,
    title: "Instant Results",
    description: "Upload, analyze, and optimize your resume in under 2 minutes with our streamlined workflow."
  }
];

const stats = [
  { value: "50K+", label: "Resumes Analyzed" },
  { value: "92%", label: "Average Match Improvement" },
  { value: "4.9/5", label: "User Satisfaction" },
  { value: "2min", label: "Average Analysis Time" }
];

const testimonials = [
  {
    name: "Sarah Chen",
    role: "Software Engineer at Google",
    quote: "ResumeAI helped me land interviews at top tech companies. The ATS scoring is incredibly accurate.",
    avatar: "SC"
  },
  {
    name: "Marcus Johnson",
    role: "Product Manager at Meta",
    quote: "The keyword matching feature transformed my resume. I went from 60% to 95% match score.",
    avatar: "MJ"
  },
  {
    name: "Emily Rodriguez",
    role: "Data Scientist at Netflix",
    quote: "Best resume optimization tool I've used. The AI suggestions are spot-on and professional.",
    avatar: "ER"
  }
];

const pricingPlans = [
  {
    name: "Starter",
    price: "Free",
    description: "Perfect for getting started",
    features: ["3 resume analyses/month", "Basic ATS scoring", "Keyword suggestions", "Email support"],
    cta: "Get Started",
    popular: false
  },
  {
    name: "Pro",
    price: "$19",
    period: "/month",
    description: "For serious job seekers",
    features: ["Unlimited analyses", "Advanced ATS scoring", "Job description matching", "Priority support", "PDF exports", "Resume rewriting"],
    cta: "Start Free Trial",
    popular: true
  },
  {
    name: "Enterprise",
    price: "Custom",
    description: "For teams and recruiters",
    features: ["Everything in Pro", "Team management", "Custom branding", "API access", "Dedicated support", "Analytics dashboard"],
    cta: "Contact Sales",
    popular: false
  }
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: [0.16, 1, 0.3, 1]
    }
  }
};

const fadeInUp = {
  hidden: { opacity: 0, y: 40 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] }
  }
};

const scaleIn = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] }
  }
};

function AnimatedBlob() {
  return (
    <motion.div
      className="absolute w-[600px] h-[600px] rounded-full opacity-30 blur-3xl"
      style={{
        background: "linear-gradient(135deg, rgba(245, 158, 11, 0.4), rgba(139, 92, 246, 0.3))"
      }}
      animate={{
        x: [0, 50, -30, 0],
        y: [0, -40, 30, 0],
        scale: [1, 1.1, 0.95, 1],
      }}
      transition={{
        duration: 15,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    />
  );
}

function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);

  if (typeof window !== 'undefined') {
    window.addEventListener('scroll', () => {
      setIsScrolled(window.scrollY > 50);
    });
  }

  return (
    <motion.nav
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      className={`fixed top-0 left-0 right-0 z-50 backdrop-blur-2xl border-b transition-all duration-500 ${
        isScrolled ? 'bg-surface-primary/90 border-border-subtle' : 'bg-transparent border-transparent'
      }`}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-20 items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-gold to-accent-goldDark flex items-center justify-center shadow-glow-sm">
                <SparklesIcon className="w-5 h-5 text-white" />
              </div>
              <div className="absolute -inset-1 rounded-xl bg-gradient-to-r from-accent-gold to-accent-violet opacity-30 blur-lg -z-10" />
            </div>
            <span className="text-xl font-bold text-white">ResumeAI</span>
          </div>
          
          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="nav-link">Features</a>
            <a href="#how-it-works" className="nav-link">How It Works</a>
            <a href="#pricing" className="nav-link">Pricing</a>
            <a href="#testimonials" className="nav-link">Testimonials</a>
          </div>
          
          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="text-sm font-medium text-gray-300 hover:text-white px-4 py-2"
            >
              Sign in
            </Link>
            <Link
              href="/signup"
              className="btn-primary text-sm px-5 py-2.5"
            >
              Get Started
              <ArrowRightIcon className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>
    </motion.nav>
  );
}

function Hero() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [0, 200]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <section ref={ref} className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      <div className="absolute inset-0">
        <AnimatedBlob />
        <div className="absolute inset-0 bg-gradient-mesh opacity-50" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,#0a0a0f_100%)]" />
      </div>

      <motion.div style={{ y, opacity }} className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="text-center max-w-5xl mx-auto"
        >
          <motion.div variants={itemVariants} className="mb-8">
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent-gold/10 border border-accent-gold/20 text-accent-gold text-sm font-medium">
              <SparklesIcon className="w-4 h-4" />
              Powered by Advanced AI
            </span>
          </motion.div>

          <motion.h1 variants={itemVariants} className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] mb-6">
            <span className="text-white">Transform Your Resume</span>
            <br />
            <span className="text-gradient-gold">Into an ATS Magnet</span>
          </motion.h1>

          <motion.p variants={itemVariants} className="text-lg md:text-xl text-gray-400 max-w-3xl mx-auto mb-10 leading-relaxed">
            Stop guessing whether your resume will pass the ATS filter. Our AI analyzes, optimizes, and helps you land more interviews at Fortune 500 companies.
          </motion.p>

          <motion.div variants={itemVariants} className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link
              href="/dashboard"
              className="btn-primary text-base px-8 py-4 group"
            >
              Start Free Analysis
              <ArrowRightIcon className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              href="#how-it-works"
              className="btn-glass text-base px-8 py-4"
            >
              See How It Works
            </Link>
          </motion.div>

          <motion.div
            variants={containerVariants}
            className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                variants={itemVariants}
                className="text-center"
              >
                <div className="text-4xl md:text-5xl font-bold text-gradient-gold mb-2">{stat.value}</div>
                <div className="text-sm text-gray-500 font-medium">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 60, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className="relative max-w-5xl mx-auto mt-20"
        >
          <div className="relative rounded-2xl bg-surface-card border border-border-subtle overflow-hidden shadow-premium">
            <div className="flex items-center gap-2 px-4 py-3 bg-surface-secondary border-b border-border-subtle">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/80" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                <div className="w-3 h-3 rounded-full bg-green-500/80" />
              </div>
              <div className="flex-1 h-7 mx-4 rounded-lg bg-surface-primary border border-border-subtle flex items-center px-3">
                <span className="text-xs text-gray-500">app.resumeai.com/dashboard</span>
              </div>
            </div>
            <div className="p-8 bg-gradient-to-b from-surface-card to-surface-secondary">
              <div className="grid md:grid-cols-3 gap-6">
                {[
                  { value: "92%", label: "ATS Score", icon: ChartBarSquareIcon, color: "gold" },
                  { value: "24", label: "Keywords Matched", icon: CheckIcon, color: "emerald" },
                  { value: "8", label: "Suggestions", icon: SparklesIcon, color: "violet" }
                ].map((item, index) => (
                  <motion.div
                    key={item.label}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.8 + index * 0.1 }}
                    className="card-premium p-6 text-center"
                  >
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-4 ${
                      item.color === 'gold' ? 'bg-accent-gold/20' :
                      item.color === 'emerald' ? 'bg-accent-emerald/20' :
                      'bg-accent-violet/20'
                    }`}>
                      <item.icon className={`w-6 h-6 ${
                        item.color === 'gold' ? 'text-accent-gold' :
                        item.color === 'emerald' ? 'text-accent-emerald' :
                        'text-accent-violet'
                      }`} />
                    </div>
                    <div className="text-4xl font-bold text-white mt-4">{item.value}</div>
                    <div className="text-sm text-gray-500 mt-1">{item.label}</div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
          
          <motion.div
            animate={{ y: [0, -10, 0] }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
            className="absolute -top-8 -right-8 w-28 h-28 bg-gradient-to-br from-accent-gold to-accent-goldDark rounded-2xl shadow-glow flex items-center justify-center"
          >
            <SparklesIcon className="w-14 h-14 text-white" />
          </motion.div>
        </motion.div>
      </motion.div>

      <motion.div
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <ChevronDownIcon className="w-6 h-6 text-gray-500" />
      </motion.div>
    </section>
  );
}

function Features() {
  return (
    <section id="features" className="py-32 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-accent-gold/5 to-transparent" />
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 relative">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={containerVariants}
          className="text-center mb-20"
        >
          <motion.span variants={itemVariants} className="badge-gold mb-4">
            Features
          </motion.span>
          <motion.h2 variants={itemVariants} className="section-title mt-4">
            Everything you need to land your dream job
          </motion.h2>
          <motion.p variants={itemVariants} className="section-subtitle max-w-2xl mx-auto">
            Our AI-powered platform provides comprehensive resume analysis and optimization tools used by over 50,000 job seekers.
          </motion.p>
        </motion.div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={containerVariants}
          className="grid md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {features.map((feature, index) => (
            <motion.div key={feature.title} variants={itemVariants}>
              <div className="card-premium p-8 h-full group">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-accent-gold/20 to-accent-gold/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                  <feature.icon className="w-7 h-7 text-accent-gold" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                <p className="text-gray-400 leading-relaxed">{feature.description}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

function HowItWorks() {
  const steps = [
    {
      icon: DocumentTextIcon,
      title: "Upload Your Resume",
      description: "Simply drag and drop your PDF resume. Our system accepts files up to 5MB."
    },
    {
      icon: BoltIcon,
      title: "AI Analysis",
      description: "Our AI scans your resume for ATS compatibility, keywords, and formatting issues."
    },
    {
      icon: SparklesIcon,
      title: "Get Insights",
      description: "Receive actionable suggestions to improve your ATS score and keyword matching."
    }
  ];

  return (
    <section id="how-it-works" className="py-32 bg-surface-secondary/50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={containerVariants}
          className="text-center mb-20"
        >
          <motion.span variants={itemVariants} className="badge-violet mb-4">
            How It Works
          </motion.span>
          <motion.h2 variants={itemVariants} className="section-title mt-4">
            Three simple steps to optimize your resume
          </motion.h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.2 }}
              className="relative"
            >
              <div className="card-premium p-8 h-full">
                <div className="absolute -top-4 -left-4 w-12 h-12 rounded-full bg-gradient-to-br from-accent-gold to-accent-goldDark flex items-center justify-center text-xl font-bold text-white shadow-glow-sm">
                  {index + 1}
                </div>
                <div className="w-16 h-16 rounded-2xl bg-accent-gold/20 flex items-center justify-center mb-6 mt-4">
                  <step.icon className="w-8 h-8 text-accent-gold" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{step.title}</h3>
                <p className="text-gray-400 leading-relaxed">{step.description}</p>
              </div>
              {index < 2 && (
                <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                  <ArrowRightIcon className="w-8 h-8 text-accent-gold/30" />
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Testimonials() {
  return (
    <section id="testimonials" className="py-32 relative overflow-hidden">
      <div className="absolute inset-0">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-accent-violet/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent-gold/10 rounded-full blur-3xl" />
      </div>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 relative">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={containerVariants}
          className="text-center mb-20"
        >
          <motion.span variants={itemVariants} className="badge-emerald mb-4">
            Testimonials
          </motion.span>
          <motion.h2 variants={itemVariants} className="section-title mt-4">
            Trusted by job seekers at top companies
          </motion.h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.15 }}
              className="card-premium p-8"
            >
              <div className="flex gap-1 mb-4">
                {[1, 2, 3, 4, 5].map((star) => (
                  <StarIcon key={star} className="w-5 h-5 text-accent-gold fill-accent-gold" />
                ))}
              </div>
              <p className="text-gray-300 leading-relaxed mb-6">"{testimonial.quote}"</p>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-accent-gold to-accent-violet flex items-center justify-center text-white font-bold">
                  {testimonial.avatar}
                </div>
                <div>
                  <div className="font-semibold text-white">{testimonial.name}</div>
                  <div className="text-sm text-gray-500">{testimonial.role}</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Pricing() {
  const [annual, setAnnual] = useState(true);

  return (
    <section id="pricing" className="py-32 bg-surface-secondary/50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={containerVariants}
          className="text-center mb-20"
        >
          <motion.span variants={itemVariants} className="badge-gold mb-4">
            Pricing
          </motion.span>
          <motion.h2 variants={itemVariants} className="section-title mt-4">
            Simple, transparent pricing
          </motion.h2>
          <motion.p variants={itemVariants} className="section-subtitle max-w-2xl mx-auto">
            Choose the plan that fits your needs. All plans include a 14-day free trial.
          </motion.p>

          <motion.div variants={itemVariants} className="flex items-center justify-center gap-4 mt-8">
            <span className={!annual ? "text-white" : "text-gray-500"}>Monthly</span>
            <button
              onClick={() => setAnnual(!annual)}
              className="relative w-14 h-8 rounded-full bg-surface-card border border-border-medium transition-colors"
            >
              <motion.div
                className="absolute top-1 w-6 h-6 rounded-full bg-accent-gold shadow-glow-sm"
                animate={{ x: annual ? 26 : 2 }}
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
              />
            </button>
            <span className={annual ? "text-white" : "text-gray-500"}>Annual <span className="text-accent-gold text-sm">(Save 20%)</span></span>
          </motion.div>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {pricingPlans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className={`relative card-premium p-8 ${plan.popular ? 'border-accent-gold/50 shadow-glow' : ''}`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <span className="badge-gold">Most Popular</span>
                </div>
              )}
              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-white mb-2">{plan.name}</h3>
                <div className="flex items-baseline justify-center gap-1">
                  <span className="text-4xl font-bold text-white">{plan.price}</span>
                  {plan.period && <span className="text-gray-500">{plan.period}</span>}
                </div>
                <p className="text-gray-500 text-sm mt-2">{plan.description}</p>
              </div>
              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-3 text-gray-300">
                    <CheckIcon className="w-5 h-5 text-accent-gold flex-shrink-0" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              <button
                className={`w-full py-3 rounded-xl font-semibold transition-all ${
                  plan.popular
                    ? 'btn-primary'
                    : 'btn-secondary'
                }`}
              >
                {plan.cta}
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

function CTA() {
  return (
    <section className="py-32 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-accent-gold/20 via-surface-primary to-accent-violet/20" />
      <div className="absolute inset-0 bg-grid-pattern opacity-5" />
      
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={containerVariants}
        className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 relative text-center"
      >
        <motion.h2 variants={fadeInUp} className="text-4xl md:text-5xl font-bold text-white mb-6">
          Ready to land your dream job?
        </motion.h2>
        <motion.p variants={fadeInUp} className="text-lg text-gray-400 mb-10 max-w-2xl mx-auto">
          Join thousands of job seekers who have transformed their resumes and accelerated their career growth.
        </motion.p>
        <motion.div variants={fadeInUp} className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/dashboard"
            className="btn-primary text-base px-8 py-4"
          >
            Get Started Free
            <ArrowRightIcon className="w-5 h-5" />
          </Link>
        </motion.div>
      </motion.div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="py-16 border-t border-border-subtle">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-4 gap-8 mb-12">
          <div className="col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-gold to-accent-goldDark flex items-center justify-center">
                <SparklesIcon className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">ResumeAI</span>
            </div>
            <p className="text-gray-500 max-w-md">
              AI-powered resume optimization to help you land your dream job at Fortune 500 companies.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-4">Product</h4>
            <ul className="space-y-2 text-gray-500">
              <li><a href="#" className="hover:text-accent-gold transition-colors">Features</a></li>
              <li><a href="#" className="hover:text-accent-gold transition-colors">Pricing</a></li>
              <li><a href="#" className="hover:text-accent-gold transition-colors">Testimonials</a></li>
              <li><a href="#" className="hover:text-accent-gold transition-colors">API</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-4">Company</h4>
            <ul className="space-y-2 text-gray-500">
              <li><a href="#" className="hover:text-accent-gold transition-colors">About</a></li>
              <li><a href="#" className="hover:text-accent-gold transition-colors">Blog</a></li>
              <li><a href="#" className="hover:text-accent-gold transition-colors">Careers</a></li>
              <li><a href="#" className="hover:text-accent-gold transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>
        <div className="divider-premium mb-8" />
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-500">
            © 2024 ResumeAI. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <a href="#" className="text-gray-500 hover:text-white transition-colors">Privacy</a>
            <a href="#" className="text-gray-500 hover:text-white transition-colors">Terms</a>
            <a href="#" className="text-gray-500 hover:text-white transition-colors">Twitter</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <Navbar />
      <Hero />
      <Features />
      <HowItWorks />
      <Testimonials />
      <Pricing />
      <CTA />
      <Footer />
    </main>
  );
}