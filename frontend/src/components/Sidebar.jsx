import {
    Boxes,
    Brain,
    ClipboardList,
    LayoutDashboard,
    Package,
    Truck,
  } from "lucide-react";

  const menuItems = [
    { label: "Dashboard", icon: LayoutDashboard, targetId: "dashboard", active: true },
    { label: "Products", icon: Package, targetId: "products" },
    { label: "Suppliers", icon: Truck, targetId: "suppliers" },
    { label: "Orders", icon: ClipboardList, targetId: "orders" },
    { label: "AI Assistant", icon: Brain, targetId: "ai-assistant" },
  ];

  function Sidebar() {
    function scrollToSection(targetId) {
      const element = document.getElementById(targetId);

      if (element) {
        window.history.pushState(null, "", `#${targetId}`);

        element.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    }

    return (
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Boxes size={22} />
          </div>

          <div>
            <strong>ProcureAI</strong>
            <span>Supply intelligence</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                className={item.active ? "nav-item active" : "nav-item"}
                key={item.label}
                type="button"
                onClick={() => scrollToSection(item.targetId)}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>
    );
  }

  export default Sidebar;
