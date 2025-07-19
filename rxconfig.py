import reflex as rx

config = rx.Config(
    app_name="payroll_dashboard",
    plugins=[rx.plugins.TailwindV3Plugin()],
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
