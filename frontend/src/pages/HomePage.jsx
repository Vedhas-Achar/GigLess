import { Link } from 'react-router-dom'

export default function HomePage() {
  return (
    <section className="hero-block">
      <p className="eyebrow">University Student Freelancing Marketplace</p>
      <h1>Hire classmates. Build portfolios. Ship real work.</h1>
      <p>
        GigLess helps students offer services in programming, design, writing, and tutoring.
        Discover trusted freelancers on campus and collaborate quickly.
      </p>
      <div className="hero-actions">
        <Link to="/services" className="cta">Explore Services</Link>
        <Link to="/signup">Become a Freelancer</Link>
      </div>
    </section>
  )
}
