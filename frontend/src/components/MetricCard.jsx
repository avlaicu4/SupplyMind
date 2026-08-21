function MetricCard({ label, value, detail, tone }) {
    return (
      <article className={`metric-card ${tone}`}>
        <span>{label}</span>
        <strong>{value}</strong>
        <p>{detail}</p>
      </article>
    );
  }

  export default MetricCard;