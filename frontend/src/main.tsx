import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { api, Service, ServiceRequest, User } from "./api/client";
import "./styles.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") ?? "");
  const [user, setUser] = useState<User | null>(null);
  const [services, setServices] = useState<Service[]>([]);
  const [requests, setRequests] = useState<ServiceRequest[]>([]);
  const [view, setView] = useState("login");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function refresh(authToken = token) {
    if (!authToken) return;
    setLoading(true);
    setError("");
    try {
      const [profile, serviceList, requestList] = await Promise.all([
        api.me(authToken),
        api.services(authToken),
        api.requests(authToken),
      ]);
      setUser(profile);
      setServices(serviceList);
      setRequests(requestList);
      setView("dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load portal data");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  function saveToken(nextToken: string) {
    localStorage.setItem("token", nextToken);
    setToken(nextToken);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken("");
    setUser(null);
    setRequests([]);
    setView("login");
  }

  return (
    <main>
      <header>
        <div>
          <p className="eyebrow">Employee Access & Service Management</p>
          <h1>QA Automation Portal</h1>
        </div>
        {token && <button data-testid="logout-button" onClick={logout}>Log out</button>}
      </header>
      {error && <div role="alert" className="error">{error}</div>}
      {loading && <p data-testid="loading-state">Loading...</p>}
      {!token && view === "login" && <Login onLogin={async (next) => { saveToken(next); await refresh(next); }} onRegister={() => setView("register")} />}
      {!token && view === "register" && <Register onLogin={() => setView("login")} />}
      {token && user && (
        <section className="layout">
          <nav>
            {["dashboard", "profile", "services", "create", "requests"].map((item) => (
              <button key={item} data-testid={`nav-${item}`} onClick={() => setView(item)}>{item}</button>
            ))}
          </nav>
          {view === "dashboard" && <Dashboard user={user} requests={requests} />}
          {view === "profile" && <Profile token={token} user={user} onSaved={setUser} />}
          {view === "services" && <Services services={services} />}
          {view === "create" && <CreateRequest token={token} services={services} onCreated={() => refresh()} />}
          {view === "requests" && <Requests token={token} requests={requests} onChanged={() => refresh()} />}
        </section>
      )}
    </main>
  );
}

function Login({ onLogin, onRegister }: { onLogin: (token: string) => Promise<void>; onRegister: () => void }) {
  const [email, setEmail] = useState("qa.user@example.com");
  const [password, setPassword] = useState("Password123!");
  const [error, setError] = useState("");
  return (
    <form onSubmit={async (event) => {
      event.preventDefault();
      setError("");
      try { await onLogin((await api.login(email, password)).access_token); } catch (err) { setError(err instanceof Error ? err.message : "Invalid login"); }
    }}>
      <h2>Login</h2>
      {error && <p role="alert" className="error">{error}</p>}
      <label>Email<input data-testid="login-email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} /></label>
      <label>Password<input data-testid="login-password" required type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
      <button data-testid="login-submit">Sign in</button>
      <button type="button" onClick={onRegister}>Create account</button>
    </form>
  );
}

function Register({ onLogin }: { onLogin: () => void }) {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  return (
    <form onSubmit={async (event) => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      setError("");
      setMessage("");
      try {
        await api.register({
          email: String(data.get("email")),
          password: String(data.get("password")),
          full_name: String(data.get("full_name")),
          department: String(data.get("department")),
        });
        setMessage("Registration complete. You can log in now.");
      } catch (err) {
        setError(err instanceof Error ? err.message : "Registration failed");
      }
    }}>
      <h2>Register</h2>
      {error && <p role="alert" className="error">{error}</p>}
      {message && <p className="success">{message}</p>}
      <label>Full name<input data-testid="register-name" name="full_name" minLength={2} required /></label>
      <label>Email<input data-testid="register-email" name="email" type="email" required /></label>
      <label>Department<input name="department" defaultValue="IT" required /></label>
      <label>Password<input data-testid="register-password" name="password" type="password" minLength={8} required /></label>
      <button data-testid="register-submit">Register</button>
      <button type="button" onClick={onLogin}>Back to login</button>
    </form>
  );
}

function Dashboard({ user, requests }: { user: User; requests: ServiceRequest[] }) {
  return <section><h2>Dashboard</h2><p>Welcome, {user.full_name}.</p><p data-testid="request-status">Open requests: {requests.filter((r) => r.status === "open").length}</p></section>;
}

function Profile({ token, user, onSaved }: { token: string; user: User; onSaved: (user: User) => void }) {
  return <form onSubmit={async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    onSaved(await api.updateMe(token, { full_name: String(data.get("full_name")), department: String(data.get("department")) }));
  }}><h2>Profile</h2><label>Full name<input data-testid="profile-name" name="full_name" minLength={2} defaultValue={user.full_name} /></label><label>Department<input data-testid="profile-department" name="department" minLength={2} defaultValue={user.department} /></label><button data-testid="profile-save">Save</button></form>;
}

function Services({ services }: { services: Service[] }) {
  return <section><h2>Service Catalog</h2>{services.map((service) => <article data-testid="service-card" key={service.id}><h3>{service.name}</h3><p>{service.category}</p><p>{service.description}</p></article>)}</section>;
}

function CreateRequest({ token, services, onCreated }: { token: string; services: Service[]; onCreated: () => void }) {
  return <form onSubmit={async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    await api.createRequest(token, { service_id: Number(data.get("service_id")), title: String(data.get("title")), description: String(data.get("description")) });
    onCreated();
  }}><h2>Create Service Request</h2><label>Service<select data-testid="request-service" name="service_id">{services.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}</select></label><label>Title<input data-testid="request-title" name="title" minLength={5} required /></label><label>Description<textarea data-testid="request-description" name="description" minLength={10} required /></label><button data-testid="request-create">Submit request</button></form>;
}

function Requests({ token, requests, onChanged }: { token: string; requests: ServiceRequest[]; onChanged: () => void }) {
  const [filter, setFilter] = useState("");
  const visible = requests.filter((request) => !filter || request.status === filter);
  return <section><h2>Requests</h2><label>Status filter<select data-testid="request-filter" value={filter} onChange={(e) => setFilter(e.target.value)}><option value="">All</option><option value="open">Open</option><option value="cancelled">Cancelled</option></select></label>{visible.length === 0 && <p data-testid="empty-requests">No requests found.</p>}{visible.map((request) => <article data-testid="request-card" key={request.id}><h3>{request.title}</h3><p>{request.description}</p><p>Status: {request.status}</p><button data-testid="request-cancel" onClick={async () => { await api.cancelRequest(token, request.id); onChanged(); }}>Cancel</button></article>)}</section>;
}

createRoot(document.getElementById("root")!).render(<App />);
