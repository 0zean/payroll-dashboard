import reflex as rx

config = rx.Config(
    app_name="payroll_dashboard",
    plugins=[rx.plugins.TailwindV3Plugin()],
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    frontend_port=3001,
    backend_port=8001,
    state_auto_setters=True,
)
