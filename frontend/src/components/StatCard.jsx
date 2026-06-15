export function StatCard({ icon: Icon, label, value }) {
  return (
    <article className="stat-card">
      <Icon size={22} />
      <div>
        <span>{label}</span>
        <strong>{value}</strong>
      </div>
    </article>
  );
}
